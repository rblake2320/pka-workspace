#!/usr/bin/env python
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pka_lib import MANIFEST, list_task_records


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def is_operational_task(data: dict[str, str], body: str) -> bool:
    text = " ".join(
        [
            data.get("title", ""),
            data.get("definition_of_done", ""),
            data.get("deliverable_file", ""),
            body,
        ]
    ).lower()
    excluded_terms = {
        "process",
        "hardening",
        "validation",
        "scorecard",
        "manifest",
        "session gate",
        "operating model",
        "task ledger",
        "audit script",
        "control layer",
        "test sweep",
        "reopen test",
    }
    return not any(term in text for term in excluded_terms)


def has_non_placeholder_evidence(body: str) -> bool:
    lowered = body.lower()
    if "[add evidence requirements]" in lowered:
        return False
    marker = "## Evidence Required"
    if marker not in body:
        return False
    section = body.split(marker, 1)[1]
    next_header = section.find("\n## ")
    if next_header != -1:
        section = section[:next_header]
    content = [line.strip() for line in section.splitlines() if line.strip()]
    return any(not line.startswith("[Add") for line in content)


def manifest_task_ids() -> set[str]:
    if not MANIFEST.exists():
        return set()
    ids: set[str] = set()
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| 20"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 2:
            ids.add(parts[1])
    return ids


def safe_div(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def agent_scorecard(records: list[tuple[Path, dict[str, str], str]]) -> list[dict]:
    """Compute per-agent metrics from the task ledger."""
    from collections import defaultdict

    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"completed": 0, "go": 0, "nogo_hold": 0, "rework": 0})

    for _, data, body in records:
        owner = data.get("owner", "").strip()
        if not owner:
            continue
        state = data.get("state", "")
        verdict = (data.get("verdict") or "").upper().strip()

        if state in {"delivered", "archived"}:
            stats[owner]["completed"] += 1
            if verdict == "GO":
                stats[owner]["go"] += 1
            elif verdict in {"NO-GO", "HOLD"}:
                stats[owner]["nogo_hold"] += 1
            if "reopened" in body.lower() or "escaped defect" in body.lower():
                stats[owner]["rework"] += 1

    rows = []
    for agent, s in sorted(stats.items(), key=lambda x: x[1]["completed"], reverse=True):
        completed = s["completed"]
        go = s["go"]
        rework = s["rework"]
        go_rate = f"{round(100 * safe_div(go, completed))}%" if completed else "n/a"
        rework_rate = f"{round(100 * safe_div(rework, completed))}%" if completed else "n/a"
        rows.append({
            "agent": agent,
            "completed": completed,
            "go_rate": go_rate,
            "rework_rate": rework_rate,
        })
    return rows


def main() -> int:
    records = list_task_records()
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    titles_in_manifest = manifest_task_ids()

    operational_delivered: list[tuple[dict[str, str], str]] = []
    for _, data, body in records:
        if data.get("state") not in {"delivered", "archived"}:
            continue
        if not is_operational_task(data, body):
            continue
        operational_delivered.append((data, body))

    delivered_30d = 0
    evidenced = 0
    verdict_known = 0
    verdict_held = 0
    escaped_defects = 0

    for data, body in operational_delivered:
        updated = parse_date(data.get("updated_at", ""))
        if updated and updated >= thirty_days_ago:
            delivered_30d += 1

        if data.get("task_id", "") in titles_in_manifest and has_non_placeholder_evidence(body):
            evidenced += 1

        verdict = data.get("verdict", "").upper()
        if verdict in {"GO", "HOLD", "NO-GO"}:
            verdict_known += 1
            notes = body.lower()
            if (verdict == "GO" and "escaped defect" not in notes and "reopened" not in notes) or verdict in {"HOLD", "NO-GO"}:
                verdict_held += 1

        notes = body.lower()
        if "escaped defect" in notes or "post-delivery defect" in notes or "reopened" in notes:
            escaped_defects += 1

    throughput_score = min(delivered_30d * 5, 25)
    evidence_score = round(35 * safe_div(evidenced, len(operational_delivered)))
    verdict_score = round(25 * safe_div(verdict_held, verdict_known))
    defect_score = max(0, 15 - escaped_defects * 5) if operational_delivered else 0
    score = throughput_score + evidence_score + verdict_score + defect_score

    print("PKA Scorecard")
    print(f"- Score: {score}/100")
    print(f"- Operational delivered tasks: {len(operational_delivered)}")
    print(f"- Delivered in last 30 days: {delivered_30d}")
    print(f"- Evidence coverage: {evidenced}/{len(operational_delivered)}")
    print(f"- Verdict accuracy sample: {verdict_held}/{verdict_known}")
    print(f"- Escaped defects logged: {escaped_defects}")
    print(f"- Throughput score: {throughput_score}/25")
    print(f"- Evidence score: {evidence_score}/35")
    print(f"- Verdict score: {verdict_score}/25")
    print(f"- Defect score: {defect_score}/15")

    if not operational_delivered:
        print("- Readiness: insufficient operational history")
    elif score >= 95:
        print("- Readiness: elite")
    elif score >= 85:
        print("- Readiness: strong")
    elif score >= 70:
        print("- Readiness: workable")
    else:
        print("- Readiness: not release-ready")

    # --- Agent Leaderboard ---
    agent_rows = agent_scorecard(records)
    if agent_rows:
        print("\nAgent Leaderboard")
        print(f"{'Agent':<14} {'Completed':>9} {'GO Rate':>8} {'Rework':>8}")
        print("-" * 44)
        for row in agent_rows:
            print(
                f"{row['agent']:<14} {row['completed']:>9} {row['go_rate']:>8} {row['rework_rate']:>8}"
            )
    else:
        print("\nAgent Leaderboard: no delivered tasks with assigned owners")

    return 0


if __name__ == "__main__":
    sys.exit(main())
