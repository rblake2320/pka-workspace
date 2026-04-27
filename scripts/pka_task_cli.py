#!/usr/bin/env python
"""
Minimal task ledger CLI for the PKA workspace.

Commands:
- create: create a task record
- update-state: update task state/owner/verdict/deliverable
- add-delivery: append a manifest row
- journal: write a session log entry to an agent journal
- journal-feedback: write a cross-agent feedback entry
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from pka_lib import (
    MANIFEST,
    ROOT,
    STATE_ORDER,
    TASKS_DIR,
    VALID_STATES,
    FileLock,
    find_task_path,
    next_task_id,
    parse_task_file,
    slugify,
    sync_control_files,
    today,
    write_task_file,
)
from pka_recovery_playbook import FAILED_VERDICTS, generate_for_task


def cmd_create(args: argparse.Namespace) -> int:
    route = args.route.split(",")
    route = [item.strip() for item in route if item.strip()]
    if not route:
        raise SystemExit("route must contain at least one agent")

    with FileLock(TASKS_DIR / ".task-ledger"):
        task_id = next_task_id()
        date_prefix = datetime.now(timezone.utc).strftime("%Y%m%d")
        task_suffix = task_id.lower().replace("task-", "")
        filename = f"{date_prefix}-{slugify(args.title)}-{task_suffix}.md"
        path = TASKS_DIR / filename
        data = {
            "task_id": task_id,
            "title": args.title,
            "state": args.state,
            "priority": args.priority,
            "owner": args.owner,
            "route": "|".join(route),
            "intake_file": args.intake_file or "",
            "deliverable_file": "",
            "verdict": "",
            "created_at": today(),
            "updated_at": today(),
            "definition_of_done": args.definition_of_done,
        }
        body = (
            "\n# Task Summary\n\n"
            "## Objective\n"
            f"{args.objective}\n\n"
            "## Context\n"
            f"{args.context}\n\n"
            "## Evidence Required\n"
            "- [Add evidence requirements]\n\n"
            "## Notes\n"
            "- [Add notes]\n"
        )
        write_task_file(path, data, body)
    sync_control_files()
    print(f"Created {path.relative_to(ROOT)} ({task_id})")
    return 0


def cmd_update_state(args: argparse.Namespace) -> int:
    path = find_task_path(args.task_id)
    with FileLock(path):
        data, body = parse_task_file(path)

        if args.state:
            if args.state not in VALID_STATES:
                raise SystemExit(f"invalid state: {args.state}")
            current_state = data["state"]
            if STATE_ORDER[args.state] < STATE_ORDER[current_state]:
                raise SystemExit(
                    f"refusing state regression from {current_state} to {args.state}"
                )
            data["state"] = args.state
        if args.owner:
            data["owner"] = args.owner
        if args.verdict is not None:
            data["verdict"] = args.verdict
        if args.deliverable_file is not None:
            data["deliverable_file"] = args.deliverable_file

        data["updated_at"] = today()
        write_task_file(path, data, body)

    verdict = (data.get("verdict") or "").strip()
    if verdict.upper() in FAILED_VERDICTS:
        generate_for_task(args.task_id)

    owner = data.get("owner", "")
    if data.get("state") in {"delivered", "archived"} and owner:
        journal = _journal_path(owner)
        if journal.exists():
            journal_text = journal.read_text(encoding="utf-8")
            if args.task_id not in journal_text:
                route = data.get("route", "").replace("|", ",")
                summary = data.get("title", args.task_id)
                entry = (
                    f"### {today()} — {summary}\n"
                    f"- **Task**: {args.task_id} — {summary}\n"
                    f"- **Verdict**: {data.get('verdict') or data.get('state')}\n"
                    f"- **Defects found**: none\n"
                    f"- **Learned**: Completed through the tracked PKA lifecycle with recorded evidence.\n"
                    f"- **Worked with**: {route or 'none'}"
                )
                updated = _insert_after_comment(journal_text, "## Session Log", entry)
                journal.write_text(updated, encoding="utf-8")

    sync_control_files()
    print(f"Updated {path.relative_to(ROOT)}")
    return 0


def _journal_path(agent: str) -> Path:
    agent_dir = ROOT / "Team" / agent
    if not agent_dir.is_dir():
        raise SystemExit(f"Unknown agent: {agent} (no directory at Team/{agent})")
    return agent_dir / "journal.md"


def _insert_after_comment(text: str, section_header: str, entry: str) -> str:
    """Insert entry immediately after the HTML comment block inside section_header."""
    lines = text.splitlines(keepends=True)
    in_section = False
    comment_end_idx = None

    for i, line in enumerate(lines):
        if line.strip() == section_header:
            in_section = True
            continue
        if in_section and line.strip() == "-->":
            comment_end_idx = i
            break

    if comment_end_idx is None:
        # Fallback: append under the section header if comment block not found
        for i, line in enumerate(lines):
            if line.strip() == section_header:
                lines.insert(i + 1, entry + "\n")
                return "".join(lines)
        # Section header not found — append at end
        return text + "\n" + entry + "\n"

    lines.insert(comment_end_idx + 1, "\n" + entry + "\n")
    return "".join(lines)


def cmd_journal(args: argparse.Namespace) -> int:
    journal = _journal_path(args.agent)

    # Validate task_id exists
    try:
        find_task_path(args.task_id)
    except SystemExit:
        raise SystemExit(f"Task not found: {args.task_id}")

    date_str = today()
    entry = (
        f"### {date_str} — {args.summary}\n"
        f"- **Task**: {args.task_id} — {args.summary}\n"
        f"- **Verdict**: {args.verdict}\n"
        f"- **Defects found**: {args.defects}\n"
        f"- **Learned**: {args.learned}\n"
        f"- **Worked with**: {args.worked_with}"
    )

    text = journal.read_text(encoding="utf-8")
    updated = _insert_after_comment(text, "## Session Log", entry)
    journal.write_text(updated, encoding="utf-8")
    print(f"Journal entry added to Team/{args.agent}/journal.md")
    return 0


def cmd_journal_feedback(args: argparse.Namespace) -> int:
    journal = _journal_path(args.to_agent)

    date_str = today()
    entry_line = f"- {date_str}: {args.from_agent} — {args.verdict} — \"{args.note}\""

    text = journal.read_text(encoding="utf-8")
    updated = _insert_after_comment(text, "## Feedback Received", entry_line)
    journal.write_text(updated, encoding="utf-8")
    print(f"Feedback entry added to Team/{args.to_agent}/journal.md")
    return 0


def cmd_reopen(args: argparse.Namespace) -> int:
    """Allow backward state transitions after NO-GO/HOLD/FAIL verdicts."""
    ALLOWED_REGRESSIONS = {
        ("under_audit", "in_progress"),   # SENTINEL NO-GO -> fix and retry
        ("under_test", "in_progress"),    # CRUCIBLE failure -> fix and retry
        ("delivered", "in_progress"),     # escaped defect -> rework
    }

    path = find_task_path(args.task_id)
    with FileLock(path):
        data, body = parse_task_file(path)
        current_state = data["state"]
        target_state = args.state

        if (current_state, target_state) not in ALLOWED_REGRESSIONS:
            raise SystemExit(
                f"reopen does not allow {current_state} -> {target_state}. "
                f"Allowed regressions: {', '.join(f'{a}->{b}' for a, b in ALLOWED_REGRESSIONS)}"
            )

        # Verify the task has a failure-class verdict or explicit reason
        verdict = (data.get("verdict") or "").strip().upper()
        if verdict not in FAILED_VERDICTS and not args.reason:
            raise SystemExit(
                f"reopen requires --reason when verdict is not a failure ({verdict}). "
                "Provide --reason to document why this task is being reopened."
            )

        # Log the reopen as a note in the task body
        reason_line = f"\n### Reopened {today()} — {args.reason}\n- Previous state: {current_state}\n- Verdict at reopen: {verdict or '(none)'}\n"
        data["state"] = target_state
        data["verdict"] = ""  # Clear verdict — task is active again
        data["updated_at"] = today()
        write_task_file(path, data, body + reason_line)

    sync_control_files()
    print(f"Reopened {path.relative_to(ROOT)}: {current_state} -> {target_state}")
    return 0


def cmd_add_delivery(args: argparse.Namespace) -> int:
    with FileLock(MANIFEST):
        text = MANIFEST.read_text(encoding="utf-8")
        lines = text.splitlines()
        try:
            separator_idx = lines.index("|------|------|------|------|------|------|")
        except ValueError as exc:
            raise SystemExit("Manifest table header is malformed") from exc
        insert_at = separator_idx + 1
        new_row = (
            f"| {args.date or today()} | {args.task} | {args.route} | {args.verdict} | "
            f"{args.deliverable} | {args.next_action} |"
        )
        lines.insert(insert_at, new_row)
        MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    sync_control_files()
    print("Updated Owner's Inbox/DELIVERY_MANIFEST.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PKA task ledger CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--title", required=True)
    create.add_argument("--owner", required=True)
    create.add_argument("--route", required=True, help="Comma-separated agent route")
    create.add_argument("--objective", required=True)
    create.add_argument("--context", required=True)
    create.add_argument("--definition-of-done", required=True)
    create.add_argument("--state", default="classified", choices=sorted(VALID_STATES))
    create.add_argument("--priority", default="high")
    create.add_argument("--intake-file", default="")
    create.set_defaults(func=cmd_create)

    update = sub.add_parser("update-state")
    update.add_argument("--task-id", required=True)
    update.add_argument("--state", choices=sorted(VALID_STATES))
    update.add_argument("--owner")
    update.add_argument("--verdict")
    update.add_argument("--deliverable-file")
    update.set_defaults(func=cmd_update_state)

    delivery = sub.add_parser("add-delivery")
    delivery.add_argument("--date")
    delivery.add_argument("--task", required=True)
    delivery.add_argument("--route", required=True)
    delivery.add_argument("--verdict", required=True)
    delivery.add_argument("--deliverable", required=True)
    delivery.add_argument("--next-action", required=True)
    delivery.set_defaults(func=cmd_add_delivery)

    journal = sub.add_parser("journal")
    journal.add_argument("--agent", required=True, help="Agent name (e.g. FORGE)")
    journal.add_argument("--task-id", required=True)
    journal.add_argument("--summary", required=True)
    journal.add_argument("--verdict", required=True)
    journal.add_argument("--defects", required=True)
    journal.add_argument("--learned", required=True)
    journal.add_argument("--worked-with", required=True)
    journal.set_defaults(func=cmd_journal)

    jfeedback = sub.add_parser("journal-feedback")
    jfeedback.add_argument("--from", dest="from_agent", required=True)
    jfeedback.add_argument("--to", dest="to_agent", required=True)
    jfeedback.add_argument("--verdict", required=True)
    jfeedback.add_argument("--note", required=True)
    jfeedback.set_defaults(func=cmd_journal_feedback)

    reopen = sub.add_parser("reopen", help="Reopen a task after NO-GO/HOLD/FAIL verdict")
    reopen.add_argument("--task-id", required=True)
    reopen.add_argument("--state", required=True, choices=["in_progress"],
                        help="Target state (currently only in_progress is allowed)")
    reopen.add_argument("--reason", required=True,
                        help="Required: reason for reopening (logged to audit trail)")
    reopen.set_defaults(func=cmd_reopen)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
