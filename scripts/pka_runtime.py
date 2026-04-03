#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pka_lib import (
    APPROVALS_PENDING,
    APPROVALS_RESOLVED,
    JOBS_ACTIVE,
    JOBS_ARCHIVE,
    ROOT,
    FileLock,
    ensure_runtime_dirs,
    find_task_path,
    parse_task_file,
    slugify,
    timestamp,
)


def _job_path(job_id: str) -> Path:
    active = JOBS_ACTIVE / f"{job_id}.json"
    if active.exists():
        return active
    archived = JOBS_ARCHIVE / f"{job_id}.json"
    if archived.exists():
        return archived
    raise SystemExit(f"Job not found: {job_id}")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _job_id(task_id: str) -> str:
    return f"job-{task_id.lower()}"


def _approval_id(job_id: str, approval_type: str) -> str:
    return f"approval-{slugify(job_id)}-{slugify(approval_type)}-{timestamp().replace(':', '').replace('-', '')}"


def cmd_enqueue(args: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    task_path = find_task_path(args.task_id)
    task, _ = parse_task_file(task_path)
    job_id = _job_id(args.task_id)
    path = JOBS_ACTIVE / f"{job_id}.json"
    with FileLock(JOBS_ACTIVE / ".queue"):
        if path.exists():
            raise SystemExit(f"Job already exists for task: {args.task_id}")
        payload = {
            "job_id": job_id,
            "task_id": args.task_id,
            "title": task.get("title", args.task_id),
            "status": "queued",
            "owner": args.owner or task.get("owner", ""),
            "route": task.get("route", "").split("|"),
            "current_agent": "",
            "pending_approval_id": "",
            "created_at": timestamp(),
            "updated_at": timestamp(),
            "attempts": 0,
            "resume_cursor": {
                "task_state": task.get("state", ""),
                "next_agent": args.owner or task.get("owner", ""),
            },
            "history": [
                {"ts": timestamp(), "event": "enqueued", "note": args.note or "runtime job created"}
            ],
        }
        _write_json(path, payload)
    print(f"Enqueued {path.relative_to(ROOT)}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    path = _job_path(args.job_id)
    with FileLock(path):
        payload = _load_json(path)
        if payload["status"] not in {"queued", "interrupted"}:
            raise SystemExit(f"Job {args.job_id} is not claimable from state {payload['status']}")
        payload["status"] = "running"
        payload["current_agent"] = args.agent
        payload["attempts"] = int(payload.get("attempts", 0)) + 1
        payload["updated_at"] = timestamp()
        payload["history"].append({"ts": timestamp(), "event": "claimed", "agent": args.agent, "note": args.note})
        _write_json(path, payload)
    print(f"Claimed {path.relative_to(ROOT)}")
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    path = _job_path(args.job_id)
    with FileLock(path):
        payload = _load_json(path)
        payload["updated_at"] = timestamp()
        payload["history"].append({"ts": timestamp(), "event": "heartbeat", "agent": args.agent, "note": args.note})
        _write_json(path, payload)
    print(f"Heartbeat recorded for {path.relative_to(ROOT)}")
    return 0


def cmd_interrupt(args: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    path = _job_path(args.job_id)
    with FileLock(path):
        payload = _load_json(path)
        approval_id = ""
        if args.kind == "approval":
            approval_id = _approval_id(args.job_id, args.approval_type)
            approval_path = APPROVALS_PENDING / f"{approval_id}.json"
            approval_payload = {
                "approval_id": approval_id,
                "job_id": args.job_id,
                "task_id": payload["task_id"],
                "requested_by": args.agent,
                "approval_type": args.approval_type,
                "artifact": args.artifact or "",
                "reason": args.reason,
                "status": "pending",
                "created_at": timestamp(),
                "updated_at": timestamp(),
            }
            _write_json(approval_path, approval_payload)
            payload["status"] = "waiting_approval"
            payload["pending_approval_id"] = approval_id
        else:
            payload["status"] = "interrupted"
        payload["updated_at"] = timestamp()
        payload["history"].append(
            {
                "ts": timestamp(),
                "event": "interrupt",
                "agent": args.agent,
                "kind": args.kind,
                "reason": args.reason,
                "approval_id": approval_id,
            }
        )
        _write_json(path, payload)
    print(f"Interrupted {path.relative_to(ROOT)}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    path = APPROVALS_PENDING / f"{args.approval_id}.json"
    if not path.exists():
        raise SystemExit(f"Approval not found: {args.approval_id}")
    with FileLock(path):
        approval = _load_json(path)
        job_path = _job_path(approval["job_id"])
        with FileLock(job_path):
            job = _load_json(job_path)
            job["pending_approval_id"] = ""
            job["status"] = "queued" if args.decision == "approved" else "interrupted"
            job["updated_at"] = timestamp()
            job["history"].append(
                {
                    "ts": timestamp(),
                    "event": "approval_resolved",
                    "approval_id": args.approval_id,
                    "decision": args.decision,
                    "resolver": args.resolver,
                    "note": args.note,
                }
            )
            _write_json(job_path, job)
        approval["status"] = args.decision
        approval["resolved_by"] = args.resolver
        approval["resolution_note"] = args.note
        approval["updated_at"] = timestamp()
        _write_json(path, approval)
        target = APPROVALS_RESOLVED / path.name
        path.replace(target)
    print(f"Resolved {target.relative_to(ROOT)}")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    path = _job_path(args.job_id)
    with FileLock(path):
        payload = _load_json(path)
        if payload["status"] not in {"interrupted", "queued", "waiting_approval"}:
            raise SystemExit(f"Job {args.job_id} cannot be resumed from state {payload['status']}")
        payload["status"] = "queued"
        payload["resume_cursor"]["next_agent"] = args.agent
        payload["updated_at"] = timestamp()
        payload["history"].append({"ts": timestamp(), "event": "resumed", "agent": args.agent, "note": args.note})
        _write_json(path, payload)
    print(f"Resumed {path.relative_to(ROOT)}")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    path = _job_path(args.job_id)
    with FileLock(path):
        payload = _load_json(path)
        payload["status"] = "completed"
        payload["updated_at"] = timestamp()
        payload["history"].append({"ts": timestamp(), "event": "completed", "agent": args.agent, "result": args.result})
        _write_json(path, payload)
        target = JOBS_ARCHIVE / path.name
        path.replace(target)
    print(f"Completed {target.relative_to(ROOT)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    path = _job_path(args.job_id)
    print(json.dumps(_load_json(path), indent=2))
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    files = sorted(JOBS_ACTIVE.glob("*.json"))
    if not files:
        print("No active jobs")
        return 0
    for path in files:
        payload = _load_json(path)
        print(f"{payload['job_id']}: {payload['status']} | task={payload['task_id']} | agent={payload.get('current_agent','')}")
    return 0


def cmd_list_approvals(_: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    files = sorted(APPROVALS_PENDING.glob("*.json"))
    if not files:
        print("No pending approvals")
        return 0
    for path in files:
        payload = _load_json(path)
        print(f"{payload['approval_id']}: {payload['approval_type']} | job={payload['job_id']} | requested_by={payload['requested_by']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PKA durable runtime CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    enqueue = sub.add_parser("enqueue")
    enqueue.add_argument("--task-id", required=True)
    enqueue.add_argument("--owner")
    enqueue.add_argument("--note", default="")
    enqueue.set_defaults(func=cmd_enqueue)

    claim = sub.add_parser("claim")
    claim.add_argument("--job-id", required=True)
    claim.add_argument("--agent", required=True)
    claim.add_argument("--note", default="")
    claim.set_defaults(func=cmd_claim)

    heartbeat = sub.add_parser("heartbeat")
    heartbeat.add_argument("--job-id", required=True)
    heartbeat.add_argument("--agent", required=True)
    heartbeat.add_argument("--note", required=True)
    heartbeat.set_defaults(func=cmd_heartbeat)

    interrupt = sub.add_parser("interrupt")
    interrupt.add_argument("--job-id", required=True)
    interrupt.add_argument("--agent", required=True)
    interrupt.add_argument("--kind", required=True, choices=["approval", "blocker"])
    interrupt.add_argument("--reason", required=True)
    interrupt.add_argument("--approval-type", default="manual-review")
    interrupt.add_argument("--artifact", default="")
    interrupt.set_defaults(func=cmd_interrupt)

    approve = sub.add_parser("approve")
    approve.add_argument("--approval-id", required=True)
    approve.add_argument("--resolver", required=True)
    approve.add_argument("--decision", required=True, choices=["approved", "rejected"])
    approve.add_argument("--note", default="")
    approve.set_defaults(func=cmd_approve)

    resume = sub.add_parser("resume")
    resume.add_argument("--job-id", required=True)
    resume.add_argument("--agent", required=True)
    resume.add_argument("--note", default="")
    resume.set_defaults(func=cmd_resume)

    complete = sub.add_parser("complete")
    complete.add_argument("--job-id", required=True)
    complete.add_argument("--agent", required=True)
    complete.add_argument("--result", required=True)
    complete.set_defaults(func=cmd_complete)

    status = sub.add_parser("status")
    status.add_argument("--job-id", required=True)
    status.set_defaults(func=cmd_status)

    listing = sub.add_parser("list")
    listing.set_defaults(func=cmd_list)

    approvals = sub.add_parser("list-approvals")
    approvals.set_defaults(func=cmd_list_approvals)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
