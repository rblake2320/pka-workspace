#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pka_lib import ROOT, find_task_path, parse_task_file

RECOVERY_DIR = ROOT / "Owner's Inbox" / "recovery"
FAILED_VERDICTS = {"HOLD", "NO-GO", "PARTIAL PASS", "FAIL"}


def _objective_from_body(body: str) -> str:
    marker = "## Objective"
    if marker not in body:
        return "Objective not parsed from task body"
    tail = body.split(marker, 1)[1].strip()
    if not tail:
        return "Objective not parsed from task body"
    return tail.splitlines()[0].strip() or "Objective not parsed from task body"


def generate_for_task(task_id: str) -> Path:
    path = find_task_path(task_id)
    data, body = parse_task_file(path)
    RECOVERY_DIR.mkdir(parents=True, exist_ok=True)

    verdict = (data.get("verdict") or data.get("state") or "unknown").strip()
    title = data.get("title", task_id)
    route = data.get("route", "").replace("|", " -> ") or "unassigned"
    objective = _objective_from_body(body)
    deliverable = data.get("deliverable_file") or "not yet recorded"
    owner = data.get("owner", "unknown")
    filename = f"{task_id.lower()}-recovery-playbook.md"
    target = RECOVERY_DIR / filename

    lines = [
        f"# Recovery Playbook — {task_id}",
        "",
        f"- Title: {title}",
        f"- Current verdict: {verdict}",
        f"- Current state: {data.get('state', 'unknown')}",
        f"- Owner: {owner}",
        f"- Route: {route}",
        f"- Deliverable surface: {deliverable}",
        "",
        "## Problem Summary",
        f"- Objective: {objective}",
        f"- Failure signal: task recorded with verdict `{verdict}` and requires controlled recovery.",
        "",
        "## Immediate Containment",
        "- Freeze further delivery claims until the failing condition is reproduced or dismissed.",
        "- Preserve the current artifact, logs, and task record before retrying implementation.",
        "- Record any customer-visible or operator-visible impact in the task notes or journal.",
        "",
        "## Rollback Steps",
        "- Identify the last known good deliverable or commit associated with this task.",
        "- Revert to the last verified-good state before applying any new fix attempt.",
        "- Re-run the minimum validation needed to confirm the rollback is safe.",
        "",
        "## Recovery Path",
        "- Reproduce the defect or failed condition with a deterministic test if possible.",
        "- Route the fix through DEBUGGER or FORGE depending on whether root cause is known.",
        "- Send the task back through CRUCIBLE and SENTINEL before re-delivery.",
        "",
        "## Evidence Required Before Re-Delivery",
        "- Updated task record with the corrected state and verdict.",
        "- Fresh test evidence showing the failed condition is now covered.",
        "- Manifest update only after the final verdict is GO.",
        "",
        "## Owner Guidance",
        "- Do not treat the prior deliverable as final while this playbook is active.",
        "- Ask for the reproduced failure, fix summary, and new verdict before approving next action.",
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a recovery playbook for a failed task")
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args()
    target = generate_for_task(args.task_id)
    print(f"Generated {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
