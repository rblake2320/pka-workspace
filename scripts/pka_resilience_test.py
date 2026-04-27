#!/usr/bin/env python
"""
Adversarial live test harness for the PKA process layer.

This script uses the real workspace and intentionally attempts to break:
- duplicate-title task creation
- state regression protections
- malformed manifest structure
- missing manifest coverage for delivered tasks
- placeholder detection in control files
- secret-pattern detection in task records
- message protocol create/archive flow

All mutations are restored before exit.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from pka_lib import acquire_validation_lock

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Team" / "tasks"
MANIFEST = ROOT / "Owner's Inbox" / "DELIVERY_MANIFEST.md"
STATUS = ROOT / "Team" / "status.md"
MESSAGES_ACTIVE = ROOT / "Team" / "messages" / "active"
MESSAGES_ARCHIVE = ROOT / "Team" / "messages" / "archive"


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


def find_task_file(task_id: str) -> Path:
    for path in TASKS_DIR.glob("*.md"):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if f'task_id: "{task_id}"' in text:
            return path
    raise RuntimeError(f"Task file not found for {task_id}")


def parse_task_id(output: str) -> str:
    start = output.find("(TASK-")
    if start == -1:
        raise RuntimeError(f"Could not parse task id from output:\n{output}")
    end = output.find(")", start)
    return output[start + 1:end]


def backup_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def restore_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> int:
    with acquire_validation_lock():
        os.environ["PKA_VALIDATION_LOCKED"] = "1"
        return _run_resilience()


def _run_resilience() -> int:
    results: list[tuple[str, bool, str]] = []
    manifest_before = backup_text(MANIFEST)
    status_before = backup_text(STATUS)
    created_tasks: list[Path] = []
    created_messages: list[Path] = []

    try:
        # 1. Duplicate-title creates must not overwrite each other.
        create_one = run(
            "scripts/pka_task_cli.py",
            "create",
            "--title",
            "Resilience Duplicate Probe",
            "--owner",
            "AXIOM",
            "--route",
            "AXIOM,FORGE",
            "--objective",
            "duplicate probe 1",
            "--context",
            "duplicate probe 1",
            "--definition-of-done",
            "duplicate probe 1",
        )
        task_id_one = parse_task_id(create_one.stdout)
        task_path_one = find_task_file(task_id_one)
        created_tasks.append(task_path_one)

        create_two = run(
            "scripts/pka_task_cli.py",
            "create",
            "--title",
            "Resilience Duplicate Probe",
            "--owner",
            "AXIOM",
            "--route",
            "AXIOM,FORGE",
            "--objective",
            "duplicate probe 2",
            "--context",
            "duplicate probe 2",
            "--definition-of-done",
            "duplicate probe 2",
        )
        task_id_two = parse_task_id(create_two.stdout)
        task_path_two = find_task_file(task_id_two)
        created_tasks.append(task_path_two)

        duplicate_ok = task_path_one != task_path_two and task_path_one.exists() and task_path_two.exists()
        results.append(("duplicate_title_protection", duplicate_ok, f"{task_path_one.name} | {task_path_two.name}"))

        # 2. Regression protection.
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id_one, "--state", "assigned", "--owner", "FORGE")
        run("scripts/pka_task_cli.py", "update-state", "--task-id", task_id_one, "--state", "in_progress", "--owner", "FORGE")
        regression = run(
            "scripts/pka_task_cli.py",
            "update-state",
            "--task-id",
            task_id_one,
            "--state",
            "classified",
            expect=1,
        )
        regression_ok = "refusing state regression" in (regression.stdout + regression.stderr)
        results.append(("state_regression_blocked", regression_ok, "classified rollback rejected"))

        # 3. Manifest corruption must be detected.
        restore_text(MANIFEST, manifest_before.replace("|------|------|------|------|------|------|", "|broken|separator|"))
        manifest_fail = run("scripts/pka_process_audit.py", expect=1)
        manifest_detection_ok = "missing the table separator" in (manifest_fail.stdout + manifest_fail.stderr)
        results.append(("manifest_corruption_detected", manifest_detection_ok, "separator corruption caught"))
        restore_text(MANIFEST, manifest_before)

        # 4. Delivered task missing manifest row must be detected.
        delivered_create = run(
            "scripts/pka_task_cli.py",
            "create",
            "--title",
            "Resilience Delivered Probe",
            "--owner",
            "AXIOM",
            "--route",
            "AXIOM,FORGE,CRUCIBLE,SENTINEL",
            "--objective",
            "delivered probe",
            "--context",
            "delivered probe",
            "--definition-of-done",
            "delivered probe",
        )
        delivered_id = parse_task_id(delivered_create.stdout)
        delivered_path = find_task_file(delivered_id)
        created_tasks.append(delivered_path)
        run(
            "scripts/pka_task_cli.py",
            "update-state",
            "--task-id",
            delivered_id,
            "--state",
            "delivered",
            "--owner",
            "AXIOM",
            "--verdict",
            "delivered",
            "--deliverable-file",
            "Owner's Inbox/test-deliverable.md",
        )
        delivered_fail = run("scripts/pka_process_audit.py", expect=1)
        delivered_detection_ok = "delivered task not found in DELIVERY_MANIFEST.md" in (delivered_fail.stdout + delivered_fail.stderr)
        results.append(("missing_manifest_row_detected", delivered_detection_ok, delivered_path.name))

        # 5. Placeholder content in status must be detected.
        restore_text(STATUS, status_before + "\n[task]\n")
        placeholder_fail = run("scripts/pka_process_audit.py", expect=1)
        placeholder_ok = "Team/status.md still contains placeholder content" in (placeholder_fail.stdout + placeholder_fail.stderr)
        results.append(("placeholder_detection", placeholder_ok, "status placeholder caught"))
        restore_text(STATUS, status_before)

        # 6. Secret pattern in task record must be detected.
        secret_task = run(
            "scripts/pka_task_cli.py",
            "create",
            "--title",
            "Resilience Secret Probe",
            "--owner",
            "AXIOM",
            "--route",
            "AXIOM,FORGE",
            "--objective",
            "secret probe",
            "--context",
            "secret probe",
            "--definition-of-done",
            "secret probe",
        )
        secret_id = parse_task_id(secret_task.stdout)
        secret_path = find_task_file(secret_id)
        created_tasks.append(secret_path)
        secret_text = backup_text(secret_path)
        restore_text(secret_path, secret_text + "\nsynthetic token ghp_123456789012345678901234567890123456\n")
        secret_fail = run("scripts/pka_process_audit.py", expect=1)
        secret_ok = "potential secret pattern detected (GitHub PAT)" in (secret_fail.stdout + secret_fail.stderr)
        results.append(("secret_scan_detection", secret_ok, secret_path.name))
        restore_text(secret_path, secret_text)

        # 7. Message protocol create/list/archive path.
        assign_result = run(
            "scripts/pka_message_cli.py",
            "assign",
            "--task-id",
            task_id_two,
            "--from-agent",
            "AXIOM",
            "--to-agent",
            "FORGE",
            "--summary",
            "resilience message flow",
            "--expected-state",
            "in_progress",
        )
        created_line = assign_result.stdout.strip().splitlines()[-1]
        message_path = Path(created_line.replace("Created ", "", 1))
        created_messages.append(message_path)
        list_result = run("scripts/pka_message_cli.py", "list")
        listed_ok = task_id_two in list_result.stdout
        archive_result = run("scripts/pka_message_cli.py", "archive", "--path", str(message_path))
        archived_path = Path(archive_result.stdout.strip().replace("Archived ", "", 1))
        archive_ok = listed_ok and archived_path.exists() and not message_path.exists()
        results.append(("message_protocol_flow", archive_ok, archived_path.name))
        if archived_path.exists():
            archived_path.unlink()

        # 8. Baseline recovery checks after all abuse.
        if delivered_path.exists():
            delivered_path.unlink()
            created_tasks = [path for path in created_tasks if path != delivered_path]
        restore_text(MANIFEST, manifest_before)
        restore_text(STATUS, status_before)
        recovery_audit = run("scripts/pka_process_audit.py")
        recovery_e2e = run("scripts/pka_e2e_test.py")
        results.append(("recovery_audit_pass", "PASS" in recovery_audit.stdout, "audit restored"))
        results.append(("recovery_e2e_pass", "PKA E2E test: PASS" in recovery_e2e.stdout, "e2e restored"))

        passed = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        score = round((passed / total) * 100) if total else 0

        print("PKA Resilience Test")
        print(f"- Score: {score}/100")
        print(f"- Passed: {passed}/{total}")
        for name, ok, detail in results:
            print(f"- {name}: {'PASS' if ok else 'FAIL'} | {detail}")
        return 0 if passed == total else 1
    finally:
        restore_text(MANIFEST, manifest_before)
        restore_text(STATUS, status_before)

        # Delete task files created in this run.
        for path in created_tasks:
            if path.exists():
                path.unlink()

        # Delete any orphaned resilience stub files left by prior runs.
        # These are identifiable by their title prefix in the frontmatter.
        _RESILIENCE_TITLE_PREFIX = "Resilience "
        for path in TASKS_DIR.glob("*.md"):
            if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            if f'title: "{_RESILIENCE_TITLE_PREFIX}' in text:
                path.unlink()

        # Delete active message files created in this run.
        for path in created_messages:
            if path.exists():
                path.unlink()

        # Delete archived messages that belong to any resilience-probe task.
        # Use title-pattern matching — never a hardcoded date.
        for path in MESSAGES_ARCHIVE.glob("*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            task_id = payload.get("task_id", "")
            summary = payload.get("summary", "")
            if "resilience" in task_id.lower() or "resilience" in summary.lower():
                path.unlink()

        run("scripts/pka_sync.py")


if __name__ == "__main__":
    sys.exit(main())
