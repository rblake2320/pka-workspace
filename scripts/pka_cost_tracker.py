#!/usr/bin/env python
"""
Aggregate session logs (logs/session_*.jsonl) into cost/usage metrics.

Writes: Owner's Inbox/reports/PKA_COST_TRACKER_REPORT.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
REPORTS_DIR = ROOT / "Owner's Inbox" / "reports"


def load_events() -> list[dict]:
    events: list[dict] = []
    for path in sorted(LOGS_DIR.glob("session_*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def compute(events: list[dict]) -> dict:
    tool_counts: Counter = Counter()
    session_counts: Counter = Counter()
    date_counts: Counter = Counter()

    for e in events:
        tool_counts[e.get("tool", "unknown")] += 1
        sid = e.get("session_id", "")[:8] or "local"
        session_counts[sid] += 1
        ts = e.get("ts", "")[:10]
        if ts:
            date_counts[ts] += 1

    return {
        "total_calls": len(events),
        "unique_sessions": len(session_counts),
        "unique_days": len(date_counts),
        "tool_breakdown": dict(tool_counts.most_common(15)),
        "daily_breakdown": dict(sorted(date_counts.items())),
        "busiest_session_calls": session_counts.most_common(1)[0][1] if session_counts else 0,
    }


def write_report(metrics: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# PKA Cost Tracker Report",
        f"- Generated: {ts}",
        f"- Total tool calls logged: {metrics['total_calls']}",
        f"- Unique sessions: {metrics['unique_sessions']}",
        f"- Days active: {metrics['unique_days']}",
        f"- Busiest session: {metrics['busiest_session_calls']} calls",
        "",
        "## Tool Call Breakdown",
    ]
    for tool, count in metrics["tool_breakdown"].items():
        lines.append(f"- {tool}: {count}")

    if metrics["daily_breakdown"]:
        lines += ["", "## Daily Activity"]
        for date, count in metrics["daily_breakdown"].items():
            lines.append(f"- {date}: {count} calls")

    out = REPORTS_DIR / "PKA_COST_TRACKER_REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    events = load_events()
    metrics = compute(events)
    write_report(metrics)

    print(
        f"# PKA Cost Tracker: {metrics['total_calls']} calls | "
        f"{metrics['unique_sessions']} sessions | "
        f"{metrics['unique_days']} days"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
