#!/usr/bin/env python
"""
PKA Quality Trend Tracker — per-agent verdict trends over time.

Reads: logs/pka_quality_tracker.jsonl (written by pka_lib.record_verdict)
Writes: reports/PKA_QUALITY_TRENDS.md

Usage:
    python scripts/pka_quality_tracker.py          # generate trend report
    python scripts/pka_quality_tracker.py --json    # output raw JSON to stdout
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from pka_lib import LOGS_DIR, REPORTS_DIR, ROOT

QUALITY_LOG = LOGS_DIR / "pka_quality_tracker.jsonl"
REPORT_PATH = REPORTS_DIR / "PKA_QUALITY_TRENDS.md"


def load_records() -> list[dict]:
    if not QUALITY_LOG.exists():
        return []
    records = []
    for line in QUALITY_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


KNOWN_TOPOLOGIES = {"linear", "debate", "tree_search", "parallel_audit", "simulation", "red_team"}


def compute_trends(records: list[dict], window_days: int = 30) -> dict:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=window_days)

    agent_stats: dict[str, dict] = defaultdict(lambda: {
        "total": 0, "go": 0, "nogo": 0, "hold": 0,
        "defects": 0, "error_categories": defaultdict(int),
    })

    topology_stats: dict[str, dict] = defaultdict(lambda: {
        "total": 0, "go": 0, "nogo": 0, "hold": 0, "defects": 0,
    })

    overall = {"total": 0, "go": 0, "nogo": 0, "hold": 0, "defects": 0}

    for rec in records:
        ts_str = rec.get("ts", "")
        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue

        if ts < cutoff:
            continue

        agent = rec.get("agent_id", "unknown")
        verdict = rec.get("verdict", "").upper()
        defects = rec.get("defect_count", 0)
        error_cat = rec.get("error_category", "")
        topology = rec.get("topology", "linear")

        agent_stats[agent]["total"] += 1
        topology_stats[topology]["total"] += 1
        overall["total"] += 1

        if verdict == "GO":
            agent_stats[agent]["go"] += 1
            topology_stats[topology]["go"] += 1
            overall["go"] += 1
        elif verdict == "NO-GO":
            agent_stats[agent]["nogo"] += 1
            topology_stats[topology]["nogo"] += 1
            overall["nogo"] += 1
        elif verdict == "HOLD":
            agent_stats[agent]["hold"] += 1
            topology_stats[topology]["hold"] += 1
            overall["hold"] += 1

        agent_stats[agent]["defects"] += defects
        topology_stats[topology]["defects"] += defects
        overall["defects"] += defects

        if error_cat:
            agent_stats[agent]["error_categories"][error_cat] += 1

    # Compute rates
    results = {
        "window_days": window_days,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "overall": {
            **overall,
            "go_rate": round(100 * overall["go"] / overall["total"], 1) if overall["total"] else 0,
        },
        "agents": {},
        "topologies": {},
    }

    for agent, stats in sorted(agent_stats.items()):
        total = stats["total"]
        results["agents"][agent] = {
            "total": total,
            "go": stats["go"],
            "nogo": stats["nogo"],
            "hold": stats["hold"],
            "go_rate": round(100 * stats["go"] / total, 1) if total else 0,
            "defects": stats["defects"],
            "top_error_categories": dict(
                sorted(stats["error_categories"].items(), key=lambda x: x[1], reverse=True)[:5]
            ),
        }

    for topology, stats in sorted(topology_stats.items()):
        total = stats["total"]
        results["topologies"][topology] = {
            "total": total,
            "go": stats["go"],
            "nogo": stats["nogo"],
            "hold": stats["hold"],
            "go_rate": round(100 * stats["go"] / total, 1) if total else 0,
            "defects": stats["defects"],
        }

    return results


def generate_report(trends: dict) -> str:
    lines = [
        "# PKA Quality Trends",
        f"*Generated: {trends['generated_at']} | Window: {trends['window_days']} days*",
        "",
    ]

    ov = trends["overall"]
    lines.extend([
        "## Overall",
        f"- Total verdicts: {ov['total']}",
        f"- GO rate: {ov['go_rate']}%",
        f"- GO: {ov['go']} | NO-GO: {ov['nogo']} | HOLD: {ov['hold']}",
        f"- Total defects: {ov['defects']}",
        "",
    ])

    agents = trends.get("agents", {})
    if agents:
        lines.extend([
            "## Per-Agent Trends",
            f"| {'Agent':<14} | {'Total':>5} | {'GO':>3} | {'NO-GO':>5} | {'HOLD':>4} | {'GO Rate':>7} | {'Defects':>7} |",
            f"|{'-'*16}|{'-'*7}|{'-'*5}|{'-'*7}|{'-'*6}|{'-'*9}|{'-'*9}|",
        ])
        for agent, stats in agents.items():
            lines.append(
                f"| {agent:<14} | {stats['total']:>5} | {stats['go']:>3} | "
                f"{stats['nogo']:>5} | {stats['hold']:>4} | "
                f"{stats['go_rate']:>6.1f}% | {stats['defects']:>7} |"
            )
        lines.append("")

        # Flag agents with regression (GO rate < 70% with 3+ verdicts)
        regressions = [
            (a, s) for a, s in agents.items()
            if s["total"] >= 3 and s["go_rate"] < 70.0
        ]
        if regressions:
            lines.extend(["## Regression Alerts"])
            for agent, stats in regressions:
                top_errors = ", ".join(
                    f"{cat} ({count})" for cat, count in stats["top_error_categories"].items()
                ) or "uncategorized"
                lines.append(
                    f"- **{agent}**: GO rate {stats['go_rate']}% "
                    f"({stats['total']} verdicts) — top errors: {top_errors}"
                )
            lines.append("")

    topologies = trends.get("topologies", {})
    if topologies:
        lines.extend([
            "## Topology Correlation",
            f"| {'Topology':<16} | {'Total':>5} | {'GO':>3} | {'NO-GO':>5} | {'HOLD':>4} | {'GO Rate':>7} | {'Defects':>7} |",
            f"|{'-'*18}|{'-'*7}|{'-'*5}|{'-'*7}|{'-'*6}|{'-'*9}|{'-'*9}|",
        ])
        for topo, stats in topologies.items():
            lines.append(
                f"| {topo:<16} | {stats['total']:>5} | {stats['go']:>3} | "
                f"{stats['nogo']:>5} | {stats['hold']:>4} | "
                f"{stats['go_rate']:>6.1f}% | {stats['defects']:>7} |"
            )
        lines.append("")

        # Flag topologies with low GO rates (3+ verdicts, <70%)
        weak_topologies = [
            (t, s) for t, s in topologies.items()
            if s["total"] >= 3 and s["go_rate"] < 70.0
        ]
        if weak_topologies:
            lines.extend(["## Topology Alerts"])
            for topo, stats in weak_topologies:
                lines.append(
                    f"- **{topo}**: GO rate {stats['go_rate']}% over {stats['total']} tasks — "
                    f"consider whether this topology is being used in appropriate contexts"
                )
            lines.append("")

    if not agents:
        lines.extend([
            "## No Data",
            "No verdict records found in the tracking window.",
            "Verdicts are recorded via `pka_lib.record_verdict()` — ",
            "SENTINEL should call this after every GO/NO-GO/HOLD decision.",
            "",
        ])

    return "\n".join(lines)


def main() -> int:
    records = load_records()
    trends = compute_trends(records)

    if "--json" in sys.argv:
        print(json.dumps(trends, indent=2))
        return 0

    report = generate_report(trends)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    # Summary to stdout
    ov = trends["overall"]
    print(f"PKA Quality Tracker: {ov['total']} verdicts in last 30 days")
    print(f"- Overall GO rate: {ov['go_rate']}%")
    print(f"- Defects: {ov['defects']}")
    agents = trends.get("agents", {})
    regressions = [a for a, s in agents.items() if s["total"] >= 3 and s["go_rate"] < 70.0]
    if regressions:
        print(f"- REGRESSION ALERT: {', '.join(regressions)}")
    print(f"- Report: {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
