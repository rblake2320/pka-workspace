#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys

from pka_lib import archive_message, create_message_file, read_text, timestamp


def cmd_assign(args: argparse.Namespace) -> int:
    payload = {
        "type": "task_assignment",
        "timestamp": timestamp(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id,
        "summary": args.summary,
        "expected_state": args.expected_state,
    }
    path = create_message_file(payload, args.task_id)
    print(f"Created {path}")
    return 0


def cmd_blocker(args: argparse.Namespace) -> int:
    payload = {
        "type": "blocker",
        "timestamp": timestamp(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id,
        "severity": args.severity,
        "reason": args.reason,
        "requested_action": args.requested_action,
    }
    path = create_message_file(payload, args.task_id)
    print(f"Created {path}")
    return 0


def cmd_approval(args: argparse.Namespace) -> int:
    payload = {
        "type": "approval_request",
        "timestamp": timestamp(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id,
        "approval_type": args.approval_type,
        "artifact": args.artifact,
    }
    path = create_message_file(payload, args.task_id)
    print(f"Created {path}")
    return 0


def cmd_approval_response(args: argparse.Namespace) -> int:
    payload = {
        "type": "approval_response",
        "timestamp": timestamp(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id,
        "approval_id": args.approval_id,
        "decision": args.decision,
        "note": args.note,
    }
    path = create_message_file(payload, args.task_id)
    print(f"Created {path}")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    payload = {
        "type": "completion_notice",
        "timestamp": timestamp(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id,
        "artifact": args.artifact,
        "next_owner": args.next_owner,
        "next_state": args.next_state,
    }
    path = create_message_file(payload, args.task_id)
    print(f"Created {path}")
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    from pathlib import Path

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"Message not found: {path}")
    target = archive_message(path)
    print(f"Archived {target}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    from pka_lib import MESSAGES_ACTIVE

    files = sorted(MESSAGES_ACTIVE.glob("*.json"))
    if not files:
        print("No active messages")
        return 0
    for path in files:
        try:
            payload = json.loads(read_text(path))
            print(f"{path.name}: {payload.get('type')} {payload.get('task_id','')}")
        except json.JSONDecodeError:
            print(f"{path.name}: invalid json")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PKA message protocol CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    assign = sub.add_parser("assign")
    assign.add_argument("--task-id", required=True)
    assign.add_argument("--from-agent", required=True)
    assign.add_argument("--to-agent", required=True)
    assign.add_argument("--summary", required=True)
    assign.add_argument("--expected-state", required=True)
    assign.set_defaults(func=cmd_assign)

    blocker = sub.add_parser("blocker")
    blocker.add_argument("--task-id", required=True)
    blocker.add_argument("--from-agent", required=True)
    blocker.add_argument("--to-agent", required=True)
    blocker.add_argument("--severity", required=True, choices=["critical", "high", "medium", "low"])
    blocker.add_argument("--reason", required=True)
    blocker.add_argument("--requested-action", required=True)
    blocker.set_defaults(func=cmd_blocker)

    approval = sub.add_parser("approval")
    approval.add_argument("--task-id", required=True)
    approval.add_argument("--from-agent", required=True)
    approval.add_argument("--to-agent", required=True)
    approval.add_argument("--approval-type", required=True)
    approval.add_argument("--artifact", required=True)
    approval.set_defaults(func=cmd_approval)

    approval_response = sub.add_parser("approval-response")
    approval_response.add_argument("--task-id", required=True)
    approval_response.add_argument("--approval-id", required=True)
    approval_response.add_argument("--from-agent", required=True)
    approval_response.add_argument("--to-agent", required=True)
    approval_response.add_argument("--decision", required=True, choices=["approved", "rejected"])
    approval_response.add_argument("--note", default="")
    approval_response.set_defaults(func=cmd_approval_response)

    complete = sub.add_parser("complete")
    complete.add_argument("--task-id", required=True)
    complete.add_argument("--from-agent", required=True)
    complete.add_argument("--to-agent", required=True)
    complete.add_argument("--artifact", required=True)
    complete.add_argument("--next-owner", required=True)
    complete.add_argument("--next-state", required=True)
    complete.set_defaults(func=cmd_complete)

    archive = sub.add_parser("archive")
    archive.add_argument("--path", required=True)
    archive.set_defaults(func=cmd_archive)

    listing = sub.add_parser("list")
    listing.set_defaults(func=cmd_list)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
