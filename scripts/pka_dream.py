#!/usr/bin/env python
"""
PKA Dream -- background session intelligence consolidation.

Inspired by DreamTask in Claude Code v2.1.88 (src/tasks/DreamTask/DreamTask.ts):
  orient -> gather -> consolidate -> prune

Reads session audit logs + task records + agent journals and produces
a consolidated intelligence report: activity patterns, delivery velocity,
journal health, and log retention signals.

Output: Owner's Inbox/reports/PKA_DREAM_REPORT.md
Lock:   logs/.dream (prevents concurrent runs)
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

from pka_lib import (
    LOGS_DIR,
    REPORTS_DIR,
    ROOT,
    TASKS_DIR,
    FileLock,
)

TEAM_DIR = ROOT / "Team"
DREAM_REPORT = REPORTS_DIR / "PKA_DREAM_REPORT.md"
LOCK_FILE = LOGS_DIR / ".dream"
RETENTION_DAYS = 30

AGENTS = [
    "AXIOM", "FORGE", "SENTINEL", "HELM", "NOVA",
    "VENTURE", "SPARK", "LEGAL", "SCRIBE", "GRID",
    "RADAR", "CRUCIBLE", "DEBUGGER", "WRAITH",
]


# --- Phase 1: Orient ---

def orient() -> dict:
    """Count all available data sources."""
    session_logs = sorted(LOGS_DIR.glob("session_*.jsonl"))
    task_records = [
        p for p in sorted(TASKS_DIR.glob("*.md"))
        if p.name not in {"README.md", "TASK_RECORD_TEMPLATE.md"}
    ]
    journals_with_entries = sum(
        1 for a in AGENTS
        if (TEAM_DIR / a / "journal.md").exists()
        and "### " in (TEAM_DIR / a / "journal.md").read_text(encoding="utf-8")
    )
    return {
        "session_logs": len(session_logs),
        "task_records": len(task_records),
        "journals_with_entries": journals_with_entries,
        "oldest_log": session_logs[0].name if session_logs else None,
        "newest_log": session_logs[-1].name if session_logs else None,
    }


# --- Phase 2: Gather ---

def gather() -> dict:
    """Read session logs and task records; aggregate statistics."""
    session_logs = sorted(LOGS_DIR.glob("session_*.jsonl"))

    tool_counts: Counter = Counter()
    daily_counts: Counter = Counter()

    for log_path in session_logs:
        date_match = re.search(r"session_(\d{8})", log_path.name)
        date_str = date_match.group(1) if date_match else "unknown"
        for line in log_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                tool_counts[event.get("tool", "unknown")] += 1
                daily_counts[date_str] += 1
            except json.JSONDecodeError:
                continue

    task_states: Counter = Counter()
    task_owners: Counter = Counter()
    delivered_tasks = []

    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        state = (re.search(r'^state:\s*"([^"]+)"', text, re.M) or [None, "unknown"])[1]
        owner = (re.search(r'^owner:\s*"([^"]+)"', text, re.M) or [None, "unknown"])[1]
        title = (re.search(r'^title:\s*"([^"]+)"', text, re.M) or [None, "unknown"])[1]
        task_id = (re.search(r'^task_id:\s*"([^"]+)"', text, re.M) or [None, "unknown"])[1]
        task_states[state] += 1
        task_owners[owner] += 1
        if state in {"delivered", "archived"}:
            delivered_tasks.append({"task_id": task_id, "title": title, "owner": owner})

    journal_counts: dict[str, int] = {}
    for agent in AGENTS:
        j = TEAM_DIR / agent / "journal.md"
        if j.exists():
            text = j.read_text(encoding="utf-8")
            journal_counts[agent] = len(re.findall(r"^### \d{4}-\d{2}-\d{2}", text, re.M))
        else:
            journal_counts[agent] = 0

    return {
        "total_events": sum(tool_counts.values()),
        "tool_counts": dict(tool_counts.most_common(10)),
        "daily_counts": dict(sorted(daily_counts.items())),
        "task_states": dict(task_states),
        "task_owners": dict(task_owners),
        "delivered_tasks": delivered_tasks,
        "journal_counts": journal_counts,
        "session_count": len(session_logs),
    }


# --- Phase 3: Consolidate ---

def consolidate(orient_data: dict, gather_data: dict) -> str:
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = gather_data["total_events"]

    lines = [
        "# PKA Dream Report",
        f"*Generated: {run_ts} — orient / gather / consolidate / prune*",
        "",
        "## Phase 1 -- Orient",
        f"- Session logs: {orient_data['session_logs']}",
        f"- Task records: {orient_data['task_records']}",
        f"- Agents with journal entries: {orient_data['journals_with_entries']}/14",
    ]
    if orient_data.get("oldest_log"):
        lines.append(
            f"- Log range: `{orient_data['oldest_log']}` -> `{orient_data['newest_log']}`"
        )
    lines += [
        "",
        "## Phase 2 -- Gather",
        f"- Total tool calls audited: {total:,}",
        f"- Sessions tracked: {gather_data['session_count']}",
        "",
        "### Tool call breakdown",
    ]
    for tool, count in sorted(gather_data["tool_counts"].items(), key=lambda x: -x[1]):
        pct = count / max(total, 1) * 100
        bar = "#" * max(1, int(pct / 3))
        lines.append(f"- `{tool}`: {count:,} ({pct:.1f}%) {bar}")

    if gather_data["daily_counts"]:
        lines += ["", "### Activity by day"]
        for date_str, count in sorted(gather_data["daily_counts"].items()):
            try:
                label = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError:
                label = date_str
            lines.append(f"- {label}: {count} calls")

    lines += [
        "",
        "### Task ledger",
        f"- Total: {sum(gather_data['task_states'].values())}",
    ]
    for state, count in sorted(gather_data["task_states"].items(), key=lambda x: -x[1]):
        lines.append(f"  - {state}: {count}")

    lines += ["", "### Workload by agent (tasks owned)"]
    for owner, count in sorted(gather_data["task_owners"].items(), key=lambda x: -x[1]):
        lines.append(f"- {owner}: {count}")

    lines += ["", "### Journal health"]
    for agent in AGENTS:
        count = gather_data["journal_counts"].get(agent, 0)
        flag = "" if count > 0 else "  <-- EMPTY"
        lines.append(f"- {agent}: {count} entries{flag}")

    # Consolidate key signals
    delivered_count = gather_data["task_states"].get("delivered", 0) + gather_data["task_states"].get("archived", 0)
    active_count = sum(
        v for k, v in gather_data["task_states"].items()
        if k in {"assigned", "in_progress", "under_test", "under_audit"}
    )
    empty_journals = [a for a in AGENTS if gather_data["journal_counts"].get(a, 0) == 0]

    lines += ["", "## Phase 3 -- Consolidate", ""]
    if total > 0 and gather_data["tool_counts"]:
        top_tool = max(gather_data["tool_counts"], key=gather_data["tool_counts"].get)
        lines.append(f"- Primary tool: `{top_tool}` ({gather_data['tool_counts'][top_tool]:,} calls)")
    lines.append(f"- Tasks delivered/archived: {delivered_count}")
    lines.append(f"- Tasks currently active: {active_count}")
    if empty_journals:
        lines.append(f"- Agents with empty journals: {', '.join(empty_journals)}")
    else:
        lines.append("- All agent journals have at least one entry")
    if total > 0 and gather_data["daily_counts"]:
        days = len(gather_data["daily_counts"])
        lines.append(f"- Avg tool calls/day: {total / days:.0f} ({days} active days)")
    lines.append("")

    return "\n".join(lines)


# --- Phase 4: Prune ---

def prune() -> list[str]:
    """Identify session logs older than RETENTION_DAYS."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    old_logs = []
    for log_path in sorted(LOGS_DIR.glob("session_*.jsonl")):
        m = re.search(r"session_(\d{8})", log_path.name)
        if not m:
            continue
        try:
            log_date = datetime.strptime(m.group(1), "%Y%m%d").replace(tzinfo=timezone.utc)
            if log_date < cutoff:
                old_logs.append(log_path.name)
        except ValueError:
            continue
    return old_logs


def main() -> int:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with FileLock(LOCK_FILE):
        o = orient()
        g = gather()
        report = consolidate(o, g)

        old_logs = prune()
        prune_lines = ["\n## Phase 4 -- Prune\n"]
        if old_logs:
            prune_lines.append(
                f"- {len(old_logs)} log(s) older than {RETENTION_DAYS} days (manual review/delete):"
            )
            for name in old_logs:
                prune_lines.append(f"  - `logs/{name}`")
        else:
            prune_lines.append(
                f"- All session logs within {RETENTION_DAYS}-day retention window"
            )
        prune_lines.append("")

        report += "\n".join(prune_lines)
        DREAM_REPORT.write_text(report, encoding="utf-8")

    print(
        f"PKA Dream: orient({o['task_records']} tasks, {o['session_logs']} sessions) "
        f"gather({g['total_events']:,} events) consolidate(ok) prune({len(old_logs)} old logs)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
