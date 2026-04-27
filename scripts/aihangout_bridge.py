#!/usr/bin/env python3
"""
aihangout_bridge.py — AIHangout -> Ultra RAG + MemoryWeb Data Bridge
Polls aihangout.ai for high-quality problems and feeds them into Ultra RAG.
Also monitors for security flags every 30 minutes and generates a daily summary.

Usage:
    python3 aihangout_bridge.py             # continuous 30-min polling loop
    python3 aihangout_bridge.py --backfill  # one-pass ingest of all qualifying content
    python3 aihangout_bridge.py --once      # single poll pass then exit
    python3 aihangout_bridge.py --security  # run one security check pass then exit

Schema discovered 2026-03-23:
    GET https://aihangout.ai/api/problems?sort=votes&limit=100&page=N
    GET https://aihangout.ai/api/problems/{id}  (includes solutions[] in body)

Quality threshold: upvotes >= 1 OR bounty_amount >= 100 OR harvested from real source
Ingest method: write .txt files to ~/ultra-rag/data/aihangout/, run ultra_ingest.py CLI
"""

import argparse
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Configuration

API_BASE        = "https://aihangout.ai/api"
ULTRA_RAG_DIR   = Path.home() / "ultra-rag"
AIHANGOUT_DIR   = ULTRA_RAG_DIR / "data" / "aihangout"
SCRIPTS_DIR     = Path.home() / "ai-business" / "scripts"
STATE_DB        = SCRIPTS_DIR / "bridge_state.db"
MEMWEB_DIR      = SCRIPTS_DIR / "memweb_queue"
POLL_INTERVAL   = 1800  # 30 minutes
PAGE_SIZE       = 100
MAX_PAGES       = 20    # safety cap: up to 2000 problems

# Security monitoring configuration
SECURITY_FLAGS_LOG   = SCRIPTS_DIR / "security_flags.log"
SECURITY_SUMMARIES   = SCRIPTS_DIR / "security_summaries"
SHARED_CHAT_DIR      = Path.home() / "ai-business" / "shared" / "chat"
# Wrangler D1 direct access — only usable where the aihangout-app project lives (Windows PC).
# On Spark-1, AIHANGOUT_APP_DIR will not exist and wrangler fallback is skipped gracefully.
# Primary path on Spark-1: /api/admin/flags endpoint with AIHANGOUT_ADMIN_TOKEN env var.
WRANGLER_CMD         = "npx"
AIHANGOUT_APP_DIR    = Path.home() / "aihangout-app"  # overridden by env var if needed
D1_DB_NAME           = "aihangout-database"

# Allow override of aihangout-app directory via environment variable
_env_app_dir = os.environ.get("AIHANGOUT_APP_DIR")
if _env_app_dir:
    AIHANGOUT_APP_DIR = Path(_env_app_dir)

# Quality thresholds
MIN_VOTES         = 1
MIN_BOUNTY        = 100   # USD threshold
INCLUDE_HARVESTED = True  # include is_harvested=1 content (dev.to, HN, Reddit, GitHub)

# Logging setup

def setup_logging():
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(SCRIPTS_DIR / "aihangout_bridge.log"),
        ],
    )

log = logging.getLogger("bridge")

# State DB

def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(STATE_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingested (
            problem_id    INTEGER PRIMARY KEY,
            title         TEXT,
            ingested_at   TEXT,
            chunk_count   INTEGER DEFAULT 0,
            embedded      INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS run_log (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at            TEXT,
            mode              TEXT,
            problems_fetched  INTEGER DEFAULT 0,
            problems_qualified INTEGER DEFAULT 0,
            problems_new      INTEGER DEFAULT 0,
            chunks_written    INTEGER DEFAULT 0
        )
    """)
    # Security monitoring state — tracks seen flag IDs to avoid re-alerting
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_flags (
            flag_key      TEXT PRIMARY KEY,
            content_type  TEXT NOT NULL,
            content_id    INTEGER NOT NULL,
            risk_level    TEXT NOT NULL,
            author        TEXT,
            patterns      TEXT,
            flagged_at    TEXT,
            alerted_at    TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Daily summary state — tracks last summary date to avoid double-runs
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date  TEXT UNIQUE,
            run_at    TEXT
        )
    """)
    conn.commit()
    return conn

def is_ingested(conn: sqlite3.Connection, problem_id: int) -> bool:
    row = conn.execute("SELECT 1 FROM ingested WHERE problem_id=?", (problem_id,)).fetchone()
    return row is not None

def mark_ingested(conn: sqlite3.Connection, problem_id: int, title: str, chunk_count: int):
    conn.execute(
        "INSERT OR REPLACE INTO ingested (problem_id, title, ingested_at, chunk_count) VALUES (?,?,?,?)",
        (problem_id, title, datetime.now(timezone.utc).isoformat(), chunk_count)
    )
    conn.commit()

def is_flag_seen(conn: sqlite3.Connection, flag_key: str) -> bool:
    row = conn.execute("SELECT 1 FROM seen_flags WHERE flag_key=?", (flag_key,)).fetchone()
    return row is not None

def mark_flag_seen(conn: sqlite3.Connection, flag_key: str, content_type: str,
                   content_id: int, risk_level: str, author: str,
                   patterns: list, flagged_at: str):
    conn.execute(
        """INSERT OR REPLACE INTO seen_flags
           (flag_key, content_type, content_id, risk_level, author, patterns, flagged_at)
           VALUES (?,?,?,?,?,?,?)""",
        (flag_key, content_type, content_id, risk_level, author,
         json.dumps(patterns), flagged_at)
    )
    conn.commit()

def daily_summary_already_run(conn: sqlite3.Connection, today: str) -> bool:
    row = conn.execute("SELECT 1 FROM daily_summary_log WHERE run_date=?", (today,)).fetchone()
    return row is not None

def mark_daily_summary_run(conn: sqlite3.Connection, today: str):
    conn.execute(
        "INSERT OR IGNORE INTO daily_summary_log (run_date, run_at) VALUES (?,?)",
        (today, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()

# HTTP helpers

def http_get(url: str, timeout: int = 30) -> Optional[dict]:
    headers = {"User-Agent": "aihangout-bridge/1.0 (Ultra RAG data bridge)"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            log.warning("HTTP %d for %s (attempt %d)", e.code, url, attempt + 1)
            if e.code in (429, 503):
                time.sleep(10 * (attempt + 1))
        except Exception as e:
            log.warning("Request failed for %s: %s (attempt %d)", url, e, attempt + 1)
            if attempt < 2:
                time.sleep(5)
    return None

# API helpers

def fetch_problems_page(page: int = 1, sort: str = "votes"):
    url = f"{API_BASE}/problems?sort={sort}&limit={PAGE_SIZE}&page={page}"
    data = http_get(url)
    if not data or not data.get("success"):
        log.error("Failed to fetch problems page %d", page)
        return [], 0
    # API ignores limit param; returns 50/page. Use totalPages from response.
    total_pages = data.get("totalPages", 1)
    return data.get("problems", []), total_pages

def fetch_all_problems() -> list:
    """
    Fetch all problems across all pages. API returns ~50/page regardless of limit param.
    Uses totalPages from response for stopping, ID dedup as safety net.
    """
    all_problems = []
    seen_ids: set = set()

    # First request to discover total pages
    first_page, total_pages = fetch_problems_page(page=1)
    for p in first_page:
        if p["id"] not in seen_ids:
            all_problems.append(p)
            seen_ids.add(p["id"])

    log.info("API reports %d total pages", total_pages)

    for page in range(2, min(total_pages + 1, MAX_PAGES + 1)):
        log.info("Fetching page %d / %d ...", page, total_pages)
        problems, _ = fetch_problems_page(page)
        if not problems:
            break
        new_on_page = [p for p in problems if p["id"] not in seen_ids]
        if not new_on_page:
            log.info("All IDs on page %d already seen — stopping early", page)
            break
        all_problems.extend(new_on_page)
        for p in new_on_page:
            seen_ids.add(p["id"])
        time.sleep(0.5)

    log.info("Pagination complete: %d unique problems", len(all_problems))
    return all_problems

def qualifies(problem: dict) -> bool:
    votes     = problem.get("upvotes", 0) or 0
    bounty    = problem.get("bounty_amount", 0) or 0
    harvested = problem.get("is_harvested", 0) or 0
    source    = problem.get("source_url") or ""

    # Reject flagged content
    if (problem.get("report_count") or 0) > 2:
        return False
    if problem.get("moderation_flag") is not None:
        return False
    if not problem.get("is_public", 0):
        return False

    if votes >= MIN_VOTES:
        return True
    if bounty >= MIN_BOUNTY:
        return True
    if INCLUDE_HARVESTED and harvested and source:
        return True
    return False

# Content formatting

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    # Strip bounty boilerplate appended to harvested problems.
    # The boilerplate uses an em dash (U+2014) before "real payouts"
    text = re.sub(
        r'\n---\n\*\*Bounty Program.*?on the roadmap\.\*\*',
        '', text, flags=re.DOTALL | re.IGNORECASE
    )
    return text.strip()

def format_problem_doc(problem: dict, solutions: list) -> str:
    title       = problem.get("title", "Untitled")
    description = clean_text(problem.get("description", ""))
    category    = problem.get("category", "")
    difficulty  = problem.get("difficulty", "")
    tags_raw    = problem.get("tags") or "[]"
    source_url  = problem.get("source_url") or ""
    upvotes     = problem.get("upvotes", 0)
    bounty      = problem.get("bounty_amount", 0)
    industry    = problem.get("industry", "")
    impact      = problem.get("impact_level", "")
    pid         = problem.get("id")
    created     = problem.get("created_at", "")

    try:
        tags = json.loads(tags_raw) if isinstance(tags_raw, str) else (tags_raw or [])
    except Exception:
        tags = []
    tags_str = ", ".join(tags) if tags else ""

    lines = [
        f"Problem: {title}",
        "",
        f"Source: aihangout.ai | Problem ID: {pid} | Category: {category} | Difficulty: {difficulty}",
        f"Industry: {industry} | Impact: {impact} | Upvotes: {upvotes} | Bounty: ${bounty}",
    ]
    if source_url:
        lines.append(f"External Source: {source_url}")
    if tags_str:
        lines.append(f"Tags: {tags_str}")
    lines.append(f"Posted: {created}")
    lines.append("")

    if description:
        lines.append("Context:")
        lines.append(description)
        lines.append("")

    if solutions:
        for i, sol in enumerate(solutions, 1):
            sol_content = clean_text(sol.get("content") or sol.get("description") or "")
            if not sol_content:
                continue
            solver    = sol.get("username") or sol.get("agent_name") or "unknown"
            sol_votes = sol.get("upvotes", 0)
            lines.append(f"Solution {i} (by {solver}, votes: {sol_votes}):")
            lines.append(sol_content)
            explanation = clean_text(sol.get("explanation") or sol.get("why_it_works") or "")
            if explanation:
                lines.append("")
                lines.append("Why it works:")
                lines.append(explanation)
            lines.append("")
    else:
        lines.append("Status: Open — no solutions yet.")
        lines.append("")

    return "\n".join(lines)

# Ultra RAG ingest

def safe_filename(problem_id: int, title: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '_', title.lower())[:60].strip('_')
    return f"ah_{problem_id:06d}_{slug}.txt"

def write_problem_file(problem_id: int, title: str, content: str) -> Path:
    AIHANGOUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = safe_filename(problem_id, title)
    filepath = AIHANGOUT_DIR / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath

def run_ultra_ingest() -> dict:
    venv_python   = ULTRA_RAG_DIR / ".venv" / "bin" / "python3"
    ingest_script = ULTRA_RAG_DIR / "ultra_ingest.py"

    cmd = [str(venv_python), str(ingest_script), "aihangout", "--stages", "parse,embed"]
    log.info("Running: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        cwd=str(ULTRA_RAG_DIR),
        capture_output=True,
        text=True,
        timeout=300
    )

    stats = {"chunks": 0, "embedded": 0, "files": 0, "errors": 0}
    for line in result.stdout.splitlines() + result.stderr.splitlines():
        m = re.search(r'files=(\d+)', line)
        if m:
            stats["files"] = int(m.group(1))
        m = re.search(r'\bchunks=(\d+)', line)
        if m:
            stats["chunks"] = int(m.group(1))
        m = re.search(r'chunks_embedded=(\d+)', line)
        if m:
            stats["embedded"] = int(m.group(1))
        m = re.search(r'errors=(\d+)', line)
        if m:
            stats["errors"] = int(m.group(1))

    if result.returncode != 0:
        log.error("ultra_ingest failed (rc=%d):\n%s", result.returncode, result.stderr[-2000:])
    else:
        log.info("ultra_ingest complete: files=%d chunks=%d embedded=%d errors=%d",
                 stats["files"], stats["chunks"], stats["embedded"], stats["errors"])

    return stats

# MemoryWeb queue

def write_memweb_queue(problems_batch: list):
    if not problems_batch:
        return
    MEMWEB_DIR.mkdir(parents=True, exist_ok=True)
    ts      = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    outfile = MEMWEB_DIR / f"aihangout_{ts}.jsonl"

    with outfile.open("w", encoding="utf-8") as f:
        for item in problems_batch:
            record = {
                "role":       "assistant",
                "content":    item["content"],
                "timestamp":  datetime.now(timezone.utc).isoformat(),
                "source":     "aihangout-bridge",
                "problem_id": item["problem_id"],
                "title":      item["title"],
            }
            f.write(json.dumps(record) + "\n")

    log.info("MemoryWeb queue: wrote %d records to %s", len(problems_batch), outfile.name)

# ============================================================================
# SECURITY MONITORING — Part 1 & 2
# ============================================================================

def run_d1_query(sql: str) -> Optional[list]:
    """
    Run a D1 SQL query via wrangler subprocess.
    Returns list of result rows, or None on error.
    Falls back to the /api/admin/flags endpoint if wrangler is unavailable.
    """
    try:
        result = subprocess.run(
            ["npx", "wrangler", "d1", "execute", D1_DB_NAME,
             "--env=production", "--remote", f"--command={sql}"],
            cwd=str(AIHANGOUT_APP_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            log.warning("D1 query failed: %s", result.stderr[-500:])
            return None

        # wrangler outputs JSON array of result objects
        output = result.stdout.strip()
        # Find the JSON portion (wrangler prepends spinner text)
        json_start = output.find('[')
        if json_start == -1:
            return []
        parsed = json.loads(output[json_start:])
        if parsed and isinstance(parsed, list):
            return parsed[0].get("results", [])
        return []
    except subprocess.TimeoutExpired:
        log.warning("D1 query timed out")
        return None
    except Exception as e:
        log.warning("D1 query error: %s", e)
        return None


def fetch_flagged_via_api(since_minutes: int = 30) -> Optional[dict]:
    """
    Fetch flagged content via the /api/admin/flags endpoint.
    Falls back to direct D1 query. Used when wrangler is unavailable.
    Note: requires admin JWT in AIHANGOUT_ADMIN_TOKEN env var.
    """
    token = os.environ.get("AIHANGOUT_ADMIN_TOKEN", "")
    if not token:
        return None

    url = f"{API_BASE}/admin/flags?since={since_minutes}&risk=all"
    headers = {
        "User-Agent": "aihangout-bridge/1.0 security-monitor",
        "Authorization": f"Bearer {token}",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log.warning("Admin flags API call failed: %s", e)
        return None


def get_flagged_items(since_minutes: int = 30) -> tuple[list, list]:
    """
    Returns (flagged_problems, flagged_solutions) from the last `since_minutes`.
    Tries /api/admin/flags first (if token available), then falls back to wrangler D1.
    """
    # Try API endpoint first
    api_data = fetch_flagged_via_api(since_minutes)
    if api_data and api_data.get("success"):
        return (
            api_data.get("flagged_problems", []),
            api_data.get("flagged_solutions", [])
        )

    # Fall back to direct D1 queries via wrangler
    prob_sql = (
        "SELECT p.id, p.title, p.content_flags, p.created_at, u.username AS author_username "
        "FROM problems p JOIN users u ON p.user_id = u.id "
        f"WHERE json_extract(p.content_flags, '$.flagged') = 1 "
        f"AND p.created_at > datetime('now', '-{since_minutes} minutes') "
        "ORDER BY p.created_at DESC LIMIT 100"
    )
    sol_sql = (
        "SELECT s.id, s.solution_text AS title, s.content_flags, s.created_at, "
        "u.username AS author_username, s.problem_id "
        "FROM solutions s JOIN users u ON s.user_id = u.id "
        f"WHERE json_extract(s.content_flags, '$.flagged') = 1 "
        f"AND s.created_at > datetime('now', '-{since_minutes} minutes') "
        "ORDER BY s.created_at DESC LIMIT 100"
    )

    problems  = run_d1_query(prob_sql) or []
    solutions = run_d1_query(sol_sql) or []
    return problems, solutions


def log_security_flag(content_type: str, item_id: int, author: str,
                      risk_level: str, patterns: list, flagged_at: str):
    """Write a structured security flag entry to security_flags.log."""
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    patterns_str = ", ".join(patterns) if patterns else "unknown"
    line = (
        f"{ts} SECURITY_FLAG "
        f"[{risk_level.upper()}] "
        f"{content_type.capitalize()} #{item_id} "
        f"by {author} "
        f"| patterns: {patterns_str} "
        f"| flagged_at: {flagged_at}\n"
    )
    with SECURITY_FLAGS_LOG.open("a", encoding="utf-8") as f:
        f.write(line)
    log.warning("SECURITY FLAG [%s] %s #%d by %s — %s",
                risk_level.upper(), content_type, item_id, author, patterns_str)


def write_chat_security_alert(content_type: str, item_id: int, author: str,
                               risk_level: str, patterns: list):
    """Write a security alert to the AI Army shared chat directory."""
    SHARED_CHAT_DIR.mkdir(parents=True, exist_ok=True)
    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    filename = f"security_flag_{ts_str}.json"

    patterns_str = ", ".join(patterns) if patterns else "unknown"
    message = (
        f"SECURITY FLAG: [{risk_level.upper()}] — "
        f"{content_type.capitalize()} #{item_id} by {author} "
        f"matched: {patterns_str}"
    )

    payload = {
        "type":         "security_alert",
        "from":         "aihangout-bridge",
        "timestamp":    datetime.now(timezone.utc).isoformat(),
        "risk_level":   risk_level,
        "content_type": content_type,
        "content_id":   item_id,
        "author":       author,
        "patterns":     patterns,
        "message":      message,
        "url":          f"https://aihangout.ai/problems/{item_id}" if content_type == "problem"
                        else f"https://aihangout.ai/problems/?solution={item_id}",
    }

    chat_file = SHARED_CHAT_DIR / filename
    chat_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    log.info("Security alert written to shared chat: %s", filename)


def monitor_security_flags(conn: sqlite3.Connection, since_minutes: int = 30):
    """
    Query aihangout.ai for recently flagged content.
    For each new flag: log it, write to shared chat, track in bridge_state.db.
    Runs alongside the content ingest every 30 minutes.
    """
    log.info("=== Security flag check (last %d min) ===", since_minutes)

    flagged_problems, flagged_solutions = get_flagged_items(since_minutes)
    total_found = len(flagged_problems) + len(flagged_solutions)
    log.info("Found %d flagged problems + %d flagged solutions", len(flagged_problems), len(flagged_solutions))

    new_alerts = 0

    def process_item(item: dict, content_type: str):
        nonlocal new_alerts
        item_id = item.get("id")
        if not item_id:
            return

        flag_key = f"{content_type}:{item_id}"
        if is_flag_seen(conn, flag_key):
            return  # already alerted on this one

        # Parse content_flags JSON
        flags_raw = item.get("content_flags") or "{}"
        try:
            flags = json.loads(flags_raw) if isinstance(flags_raw, str) else flags_raw
        except Exception:
            flags = {}

        risk_level  = flags.get("risk", "unknown")
        patterns    = flags.get("patterns", [])
        author      = item.get("author_username") or item.get("username") or "unknown"
        flagged_at  = item.get("created_at", datetime.now(timezone.utc).isoformat())

        # Log to security_flags.log
        log_security_flag(content_type, item_id, author, risk_level, patterns, flagged_at)

        # Write to shared chat
        write_chat_security_alert(content_type, item_id, author, risk_level, patterns)

        # Mark as seen so we don't re-alert
        mark_flag_seen(conn, flag_key, content_type, item_id, risk_level, author, patterns, flagged_at)
        new_alerts += 1

    for item in flagged_problems:
        process_item(item, "problem")
    for item in flagged_solutions:
        process_item(item, "solution")

    if new_alerts:
        log.warning("=== %d NEW security flags surfaced and logged ===", new_alerts)
    else:
        log.info("=== No new security flags (all %d already seen) ===", total_found)

    return new_alerts


# ============================================================================
# DAILY SECURITY SUMMARY — Part 2
# ============================================================================

def generate_security_summary(conn: sqlite3.Connection):
    """
    Generate a daily security summary report.
    Runs at 08:00 UTC if it hasn't already run today.
    Writes to shared/chat/security_summary_[date].json
    and scripts/security_summaries/daily_[date].txt
    """
    now_utc = datetime.now(timezone.utc)
    today   = now_utc.strftime("%Y-%m-%d")

    # Only run at hour 8 (UTC) and only once per day
    if now_utc.hour != 8:
        return
    if daily_summary_already_run(conn, today):
        log.debug("Daily security summary already ran for %s", today)
        return

    log.info("=== Generating daily security summary for %s ===", today)

    # Query D1 for last 24h stats
    stats = {}

    # Total posts
    total_sql = (
        "SELECT (SELECT COUNT(*) FROM problems WHERE created_at > datetime('now', '-24 hours')) + "
        "(SELECT COUNT(*) FROM solutions WHERE created_at > datetime('now', '-24 hours')) AS total_posts"
    )
    total_rows = run_d1_query(total_sql)
    stats["total_posts_24h"] = (total_rows[0].get("total_posts", 0) if total_rows else 0)

    # Flagged by risk level
    for risk in ("high", "medium", "low"):
        risk_sql = (
            f"SELECT (SELECT COUNT(*) FROM problems WHERE json_extract(content_flags, '$.flagged') = 1 "
            f"AND json_extract(content_flags, '$.risk') = '{risk}' "
            f"AND created_at > datetime('now', '-24 hours')) + "
            f"(SELECT COUNT(*) FROM solutions WHERE json_extract(content_flags, '$.flagged') = 1 "
            f"AND json_extract(content_flags, '$.risk') = '{risk}' "
            f"AND created_at > datetime('now', '-24 hours')) AS cnt"
        )
        rows = run_d1_query(risk_sql)
        stats[f"flagged_{risk}"] = (rows[0].get("cnt", 0) if rows else 0)

    stats["total_flagged_24h"] = stats["flagged_high"] + stats["flagged_medium"] + stats["flagged_low"]

    # Top 3 patterns — aggregate from seen_flags in bridge_state.db (last 24h)
    cutoff = (now_utc - timedelta(hours=24)).isoformat()
    pattern_rows = conn.execute(
        "SELECT patterns FROM seen_flags WHERE alerted_at > ?", (cutoff,)
    ).fetchall()

    pattern_counts: dict = {}
    for (patterns_json,) in pattern_rows:
        try:
            for p in json.loads(patterns_json or "[]"):
                pattern_counts[p] = pattern_counts.get(p, 0) + 1
        except Exception:
            pass
    top_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    stats["top_patterns"] = [{"pattern": p, "count": c} for p, c in top_patterns]

    # New users (first posts) — problems/solutions by users created in last 24h
    new_users_sql = (
        "SELECT COUNT(DISTINCT u.id) AS cnt FROM users u "
        "WHERE u.join_date > datetime('now', '-24 hours')"
    )
    new_user_rows = run_d1_query(new_users_sql)
    stats["new_users_24h"] = (new_user_rows[0].get("cnt", 0) if new_user_rows else 0)

    # Pending review count
    pending_sql = (
        "SELECT (SELECT COUNT(*) FROM problems WHERE status='pending_review') + "
        "(SELECT COUNT(*) FROM solutions WHERE solver_type='AI' AND is_verified=FALSE) AS cnt"
    )
    pending_rows = run_d1_query(pending_sql)
    stats["pending_review"] = (pending_rows[0].get("cnt", 0) if pending_rows else 0)

    # Build summary payload
    summary = {
        "date":                today,
        "generated_at":        now_utc.isoformat(),
        "source":              "aihangout-bridge security monitor",
        "total_posts_24h":     stats["total_posts_24h"],
        "total_flagged_24h":   stats["total_flagged_24h"],
        "flagged_by_risk": {
            "high":   stats["flagged_high"],
            "medium": stats["flagged_medium"],
            "low":    stats["flagged_low"],
        },
        "top_patterns":    stats["top_patterns"],
        "new_users_24h":   stats["new_users_24h"],
        "pending_review":  stats["pending_review"],
    }

    # Write to shared chat
    SHARED_CHAT_DIR.mkdir(parents=True, exist_ok=True)
    chat_file = SHARED_CHAT_DIR / f"security_summary_{today}.json"
    chat_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log.info("Daily summary written to shared chat: %s", chat_file.name)

    # Write to scripts/security_summaries/daily_[date].txt
    SECURITY_SUMMARIES.mkdir(parents=True, exist_ok=True)
    txt_file = SECURITY_SUMMARIES / f"daily_{today}.txt"

    top_patterns_str = "\n".join(
        f"    {i+1}. {p['pattern']} ({p['count']} hits)"
        for i, p in enumerate(stats["top_patterns"])
    ) or "    (none)"

    txt_content = f"""aihangout.ai Daily Security Summary — {today}
Generated: {now_utc.isoformat()}
{"="*55}

ACTIVITY (last 24h)
  Total posts:          {stats['total_posts_24h']}
  Total flagged:        {stats['total_flagged_24h']}
    - High risk:        {stats['flagged_high']}
    - Medium risk:      {stats['flagged_medium']}
    - Low risk:         {stats['flagged_low']}

TOP FLAGGED PATTERNS
{top_patterns_str}

REVIEW QUEUE
  Pending review:       {stats['pending_review']}
  New users (24h):      {stats['new_users_24h']}

{"="*55}
"""
    txt_file.write_text(txt_content, encoding="utf-8")
    log.info("Daily summary written: %s", txt_file)
    log.info(
        "Summary: posts=%d flagged=%d (high=%d med=%d low=%d) pending=%d",
        stats["total_posts_24h"], stats["total_flagged_24h"],
        stats["flagged_high"], stats["flagged_medium"], stats["flagged_low"],
        stats["pending_review"],
    )

    mark_daily_summary_run(conn, today)

# Main polling logic

def run_poll(conn: sqlite3.Connection, mode: str = "poll") -> dict:
    run_start = datetime.now(timezone.utc).isoformat()
    log.info("=== Poll pass starting (%s) at %s ===", mode, run_start)

    all_problems = fetch_all_problems()
    log.info("Fetched %d total problems from aihangout.ai", len(all_problems))

    qualified    = [p for p in all_problems if qualifies(p)]
    new_problems = [p for p in qualified if not is_ingested(conn, p["id"])]

    log.info("Qualified: %d | Already ingested: %d | New to ingest: %d",
             len(qualified), len(qualified) - len(new_problems), len(new_problems))

    if not new_problems:
        log.info("No new qualifying problems.")
        return {
            "problems_fetched":    len(all_problems),
            "problems_qualified":  len(qualified),
            "problems_new":        0,
            "chunks_written":      0,
            "embedded":            0,
        }

    written_count = 0
    memweb_batch  = []

    for prob in new_problems:
        pid      = prob["id"]
        title    = prob.get("title", f"Problem {pid}")
        solutions = prob.get("solutions") or []

        content  = format_problem_doc(prob, solutions)
        write_problem_file(pid, title, content)
        written_count += 1
        memweb_batch.append({"problem_id": pid, "title": title, "content": content})

        log.info("Staged [%d/%d] id=%d %s", written_count, len(new_problems), pid, title[:60])
        time.sleep(0.1)  # avoid hammering disk

    log.info("Staged %d files to %s", written_count, AIHANGOUT_DIR)

    ingest_stats = run_ultra_ingest()

    # Mark all as ingested
    for prob in new_problems:
        mark_ingested(conn, prob["id"], prob.get("title", ""), ingest_stats.get("chunks", 0))

    write_memweb_queue(memweb_batch)

    conn.execute(
        "INSERT INTO run_log (run_at, mode, problems_fetched, problems_qualified, problems_new, chunks_written) VALUES (?,?,?,?,?,?)",
        (run_start, mode, len(all_problems), len(qualified), len(new_problems), ingest_stats.get("chunks", 0))
    )
    conn.commit()

    return {
        "problems_fetched":   len(all_problems),
        "problems_qualified": len(qualified),
        "problems_new":       len(new_problems),
        "chunks_written":     ingest_stats.get("chunks", 0),
        "embedded":           ingest_stats.get("embedded", 0),
    }

# Entry point

def main():
    parser = argparse.ArgumentParser(description="AIHangout -> Ultra RAG bridge")
    parser.add_argument("--backfill", action="store_true",
                        help="Ingest ALL qualifying content in one pass then exit")
    parser.add_argument("--once", action="store_true",
                        help="Run one poll pass then exit")
    parser.add_argument("--reset", action="store_true",
                        help="Clear ingestion state (re-ingest everything)")
    parser.add_argument("--security", action="store_true",
                        help="Run one security flag check pass then exit")
    args = parser.parse_args()

    setup_logging()
    AIHANGOUT_DIR.mkdir(parents=True, exist_ok=True)
    MEMWEB_DIR.mkdir(parents=True, exist_ok=True)

    conn = init_db()

    if args.reset:
        conn.execute("DELETE FROM ingested")
        conn.commit()
        log.info("State cleared — will re-ingest everything")

    if args.security:
        monitor_security_flags(conn, since_minutes=30)
        conn.close()
        return

    if args.backfill or args.once:
        mode  = "backfill" if args.backfill else "once"
        stats = run_poll(conn, mode=mode)
        # Also run security check on one-shot passes
        monitor_security_flags(conn, since_minutes=30)
        log.info(
            "=== %s complete: fetched=%d qualified=%d new=%d chunks=%d embedded=%d ===",
            mode.upper(),
            stats["problems_fetched"],
            stats["problems_qualified"],
            stats["problems_new"],
            stats["chunks_written"],
            stats.get("embedded", 0),
        )
        conn.close()
        return

    # Continuous polling loop
    log.info("Starting continuous polling loop (interval=%ds)", POLL_INTERVAL)
    while True:
        try:
            stats = run_poll(conn, mode="poll")
            log.info(
                "Poll done: fetched=%d qualified=%d new=%d chunks=%d",
                stats["problems_fetched"], stats["problems_qualified"],
                stats["problems_new"], stats["chunks_written"],
            )
            # Security monitoring runs every poll cycle (every 30 min)
            monitor_security_flags(conn, since_minutes=POLL_INTERVAL // 60)
            # Daily summary check — runs at 08:00 UTC if not yet run today
            generate_security_summary(conn)

        except KeyboardInterrupt:
            log.info("Interrupted — exiting")
            break
        except Exception as e:
            log.error("Poll failed: %s", e, exc_info=True)

        log.info("Sleeping %d seconds until next poll ...", POLL_INTERVAL)
        time.sleep(POLL_INTERVAL)

    conn.close()


if __name__ == "__main__":
    main()
