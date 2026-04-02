#!/usr/bin/env python
"""
pka_memory_sync.py — Backfill existing PKA journal entries into MemoryWeb.

MemoryWeb MCP is the semantic memory backend for PKA agents. This script reads
all agent journals and POSTs each session log entry to MemoryWeb via its HTTP API.

Usage:
    python scripts/pka_memory_sync.py [--dry-run] [--agent AGENT]

Options:
    --dry-run     Print what would be synced without posting to MemoryWeb
    --agent       Sync only the specified agent (e.g. FORGE, NOVA)

MemoryWeb API: http://localhost:8100 (or memoryweb.ultrarag.app via tunnel)
Authentication: None required on localhost; JWT required on tunnel endpoint.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM_DIR = ROOT / "Team"

# All known agents with journals
AGENTS = [
    "AXIOM", "NOVA", "FORGE", "SENTINEL", "CRUCIBLE",
    "HELM", "DEBUGGER", "GRID", "RADAR", "SCRIBE",
    "SPARK", "VENTURE", "LEGAL",
]

# MemoryWeb API base URL (localhost preferred; falls back to tunnel)
MEMORYWEB_LOCAL = "http://localhost:8100"
MEMORYWEB_TUNNEL = "https://memoryweb.ultrarag.app"

# Entry pattern: ### YYYY-MM-DD — summary
ENTRY_PATTERN = re.compile(
    r"^### (\d{4}-\d{2}-\d{2}) — (.+?)$",
    re.MULTILINE,
)
FIELD_PATTERN = re.compile(r"^- \*\*(.+?)\*\*: (.+)$", re.MULTILINE)


def parse_journal_entries(journal_path: Path) -> list[dict[str, str]]:
    """Parse session log entries from a journal markdown file."""
    if not journal_path.exists():
        return []

    text = journal_path.read_text(encoding="utf-8")

    # Only parse the Session Log section
    session_log_match = re.search(r"^## Session Log\b", text, re.MULTILINE)
    if not session_log_match:
        return []
    session_text = text[session_log_match.end():]

    # Stop at next ## section
    next_section = re.search(r"^## \w", session_text, re.MULTILINE)
    if next_section:
        session_text = session_text[: next_section.start()]

    entries = []
    for match in ENTRY_PATTERN.finditer(session_text):
        date_str = match.group(1)
        summary = match.group(2).strip()

        # Extract fields from lines after the header until next entry
        start = match.end()
        end_match = ENTRY_PATTERN.search(session_text, start)
        entry_text = session_text[start: end_match.start() if end_match else len(session_text)]

        fields: dict[str, str] = {}
        for field_match in FIELD_PATTERN.finditer(entry_text):
            fields[field_match.group(1).lower()] = field_match.group(2).strip()

        if summary and "none yet" not in summary.lower():
            entries.append({
                "date": date_str,
                "summary": summary,
                "task": fields.get("task", ""),
                "verdict": fields.get("verdict", ""),
                "learned": fields.get("learned", ""),
                "worked_with": fields.get("worked with", ""),
            })

    return entries


def post_to_memoryweb(api_base: str, agent: str, entry: dict[str, str]) -> bool:
    """POST a journal entry to the MemoryWeb API. Returns True on success."""
    tags = [agent, "journal-sync"]
    verdict = entry.get("verdict", "").strip()
    if verdict:
        tags.append(f"verdict:{verdict.lower().replace(' ', '-')[:20]}")

    payload = {
        "title": f"[{agent}] {entry['summary']}",
        "content": (
            f"Agent: {agent}\n"
            f"Date: {entry['date']}\n"
            f"Task: {entry['task']}\n"
            f"Verdict: {verdict}\n"
            f"Learned: {entry.get('learned', '')}\n"
            f"Worked with: {entry.get('worked_with', '')}"
        ),
        "tags": tags,
        "metadata": {
            "source": "pka_memory_sync",
            "agent": agent,
            "date": entry["date"],
            "synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    }

    data = json.dumps(payload).encode("utf-8")
    url = f"{api_base}/api/memories"

    try:
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 201)
    except urllib.error.URLError:
        return False
    except Exception:
        return False


def detect_api_base() -> str | None:
    """Check if MemoryWeb is reachable locally; fall back to tunnel."""
    for base in (MEMORYWEB_LOCAL, MEMORYWEB_TUNNEL):
        try:
            req = urllib.request.Request(f"{base}/api/health", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return base
        except Exception:
            continue
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync PKA journal entries to MemoryWeb")
    parser.add_argument("--dry-run", action="store_true", help="Print without posting")
    parser.add_argument("--agent", help="Sync only this agent (e.g. FORGE)")
    args = parser.parse_args()

    agents_to_sync = [args.agent.upper()] if args.agent else AGENTS

    # Verify agents exist
    for agent in agents_to_sync:
        if agent not in AGENTS:
            print(f"Unknown agent: {agent}. Valid: {', '.join(AGENTS)}", file=sys.stderr)
            return 1

    if not args.dry_run:
        api_base = detect_api_base()
        if not api_base:
            print(
                "MemoryWeb not reachable at localhost:8100 or memoryweb.ultrarag.app.\n"
                "Start MemoryWeb (Spark-2 port 8100) or check Cloudflare tunnel.",
                file=sys.stderr,
            )
            return 1
        print(f"MemoryWeb detected at: {api_base}")
    else:
        api_base = MEMORYWEB_LOCAL
        print("DRY RUN — no data will be posted")

    total_synced = 0
    total_skipped = 0

    for agent in agents_to_sync:
        journal_path = TEAM_DIR / agent / "journal.md"
        entries = parse_journal_entries(journal_path)

        if not entries:
            print(f"  {agent}: no journal entries found")
            continue

        print(f"  {agent}: {len(entries)} entries found")

        for entry in entries:
            if args.dry_run:
                print(f"    [DRY] {entry['date']} — {entry['summary'][:60]}")
                total_synced += 1
                continue

            ok = post_to_memoryweb(api_base, agent, entry)
            if ok:
                print(f"    [OK] {entry['date']} — {entry['summary'][:60]}")
                total_synced += 1
            else:
                print(f"    [SKIP] {entry['date']} — {entry['summary'][:60]} (post failed)")
                total_skipped += 1

    print(f"\nSync complete: {total_synced} posted, {total_skipped} failed")
    return 0 if total_skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
