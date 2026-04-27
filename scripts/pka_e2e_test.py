#!/usr/bin/env python
"""
Real end-to-end integration test for the PKA process layer.

This test uses the actual workspace files and actual CLI scripts.
It creates a real temporary task record, advances it through the lifecycle,
checks that state regression is blocked, writes a real manifest entry,
runs the real audit/session gate, and restores any temporary changes.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pka_lib import acquire_validation_lock

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Team" / "tasks"
MANIFEST = ROOT / "Owner's Inbox" / "DELIVERY_MANIFEST.md"


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != expect:
        raise RuntimeError(
            f"Command failed: {' '.join(args)}\n"
            f"Expected exit code {expect}, got {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def current_date_strings() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y%m%d"), now.strftime("%Y-%m-%d")


def find_task_file(task_id: str) -> Path:
    for path in TASKS_DIR.glob("*.md"):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if f'task_id: "{task_id}"' in text:
            return path
    raise RuntimeError(f"Could not find task file for {task_id}")


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise RuntimeError(message)


def main() -> int:
    date_prefix, iso_date = current_date_strings()
    title = "Real E2E Validation Task"
    objective = "Validate the full PKA process using the real workspace and scripts"
    context = "Live integration test for ledger, manifest, session gates, and audit"
    dod = "Task is created, advanced, delivered, logged, audited, and regression is blocked"

    with acquire_validation_lock():
        return _run_test(date_prefix, iso_date, title, objective, context, dod)


def _run_test(
    date_prefix: str,
    iso_date: str,
    title: str,
    objective: str,
    context: str,
    dod: str,
) -> int:
    manifest_before = MANIFEST.read_text(encoding="utf-8")
    task_path: Path | None = None
    task_id: str | None = None

    try:
        create_result = run(
            "scripts/pka_task_cli.py",
            "create",
            "--title",
            title,
            "--owner",
            "AXIOM",
            "--route",
            "AXIOM,FORGE,CRUCIBLE,SENTINEL",
            "--objective",
            objective,
            "--context",
            context,
            "--definition-of-done",
            dod,
            "--intake-file",
            "Team Inbox/real-e2e-validation.md",
        )
        match = re.search(r"\((TASK-\d{8}-\d{3})\)", create_result.stdout)
        if not match:
            raise RuntimeError(f"Could not parse task id from create output:\n{create_result.stdout}")
        task_id = match.group(1)
        task_path = find_task_file(task_id)

        run("scripts/pka_session_gate.py", "start")
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id, "--state", "assigned", "--owner", "FORGE")
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id, "--state", "in_progress", "--owner", "FORGE")
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id, "--state", "under_test", "--owner", "CRUCIBLE")
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id, "--state", "under_audit", "--owner", "SENTINEL")

        regression = run(
            "scripts/pka_task_cli.py",
            "update-state",
            "--task-id",
            task_id,
            "--state",
            "in_progress",
            expect=1,
        )
        assert_contains(
            regression.stderr or regression.stdout,
            "refusing state regression",
            "Regression protection did not trigger as expected",
        )

        deliverable = "Team/tasks real e2e task record and process scripts"
        run(
            "scripts/pka_task_cli.py",
            "update-state",
            "--task-id",
            task_id,
            "--state",
            "delivered",
            "--owner",
            "AXIOM",
            "--verdict",
            "delivered",
            "--deliverable-file",
            "Team/tasks/; scripts/pka_process_audit.py; scripts/pka_task_cli.py; scripts/pka_session_gate.py",
        )
        run(
            "scripts/pka_task_cli.py",
            "add-delivery",
            "--date",
            iso_date,
            "--task",
            title,
            "--route",
            "AXIOM -> FORGE -> CRUCIBLE -> SENTINEL -> AXIOM",
            "--verdict",
            "delivered",
            "--deliverable",
            deliverable,
            "--next-action",
            "Treat this as the reference E2E validation result",
        )

        task_text = task_path.read_text(encoding="utf-8")
        assert_contains(task_text, 'state: "delivered"', "Task did not reach delivered state")
        assert_contains(task_text, 'verdict: "delivered"', "Task verdict was not persisted")

        manifest_text = MANIFEST.read_text(encoding="utf-8")
        assert_contains(
            manifest_text,
            f"| {iso_date} | {title} | AXIOM -> FORGE -> CRUCIBLE -> SENTINEL -> AXIOM | delivered | {deliverable} | Treat this as the reference E2E validation result |",
            "Manifest row was not written correctly",
        )

        run("scripts/pka_process_audit.py")
        run("scripts/pka_session_gate.py", "end")

        print("PKA E2E test: PASS")
        print(f"- Task created and delivered: {task_id}")
        print("- State regression protection verified")
        print("- Manifest write verified")
        print("- Audit and session gate passed")
        return 0
    finally:
        MANIFEST.write_text(manifest_before, encoding="utf-8")
        if task_path and task_path.exists():
            task_path.unlink()


if __name__ == "__main__":
    sys.exit(main())
