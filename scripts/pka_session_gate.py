#!/usr/bin/env python
"""
Session gate for the PKA workspace.

Modes:
- start: verify core session-start files exist, surface non-terminal tasks,
         write Team/tasks/RESUME.json for machine-readable resumption
- end:   run the process audit, write RESUME.json for next session
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pka_lib import APPROVALS_PENDING, JOBS_ACTIVE, MESSAGES_ACTIVE, TASKS_DIR, ensure_runtime_dirs, parse_task_file, timestamp


ROOT = Path(__file__).resolve().parent.parent
TEAM_INBOX = ROOT / "Team Inbox"
OWNER_PROFILE = ROOT / "Owner's Inbox" / "owner.md"
HANDOFF = ROOT / "Team" / "handoff.md"
STATUS = ROOT / "Team" / "status.md"
AUDIT = ROOT / "scripts" / "pka_process_audit.py"
RESUME_PATH = TASKS_DIR / "RESUME.json"

NON_TERMINAL = {"new", "classified", "assigned", "in_progress", "under_test", "under_audit"}
# Lower number = higher priority in work queue
_STATE_PRIORITY = {
    "in_progress": 0,
    "under_test": 1,
    "under_audit": 1,
    "assigned": 2,
    "classified": 3,
    "new": 4,
}
STALE_HOURS = 48
INBOX_STALE_HOURS = 24  # Items older than this are flagged UNPROCESSED

# Classify Team Inbox items by extension
_INBOX_TYPES = {
    ".html": "artifact",
    ".htm": "artifact",
    ".md": "brief",
    ".txt": "brief",
    ".pdf": "document",
    ".png": "asset",
    ".jpg": "asset",
    ".jpeg": "asset",
    ".gif": "asset",
    ".json": "data",
    ".csv": "data",
    ".py": "code",
    ".ts": "code",
    ".js": "code",
}


def _classify_inbox_item(path: Path) -> str:
    return _INBOX_TYPES.get(path.suffix.lower(), "file")


def _scan_inbox_items() -> list[dict]:
    """Return enriched metadata for all non-processed Team Inbox items."""
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=INBOX_STALE_HOURS)
    items = []
    for path in sorted(TEAM_INBOX.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if "processed" in rel.parts or path.name == "README.md":
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            age_h = (now - mtime).total_seconds() / 3600
            unprocessed = mtime < threshold
        except Exception:
            age_h = 0.0
            unprocessed = False
        items.append({
            "path": str(rel),
            "type": _classify_inbox_item(path),
            "age_hours": round(age_h, 1),
            "unprocessed": unprocessed,
        })
    return items


def _scan_non_terminal_tasks() -> list[dict]:
    """Return frontmatter dicts for all non-terminal task records.

    Wraps each parse call in try/except — corrupt files are skipped with a
    warning rather than crashing the entire scan.
    """
    results = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        try:
            data, _ = parse_task_file(path)
        except Exception as exc:
            print(f"  [WARN] Could not parse {path.name}: {exc}")
            continue
        if data.get("state", "") in NON_TERMINAL:
            results.append(data)
    return results


def _build_resume(tasks: list[dict]) -> dict:
    """Build a machine-readable resumption manifest from non-terminal tasks."""
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=STALE_HOURS)

    queue = []
    for t in tasks:
        state = t.get("state", "")
        updated_str = t.get("updated_at", "")
        stale = False
        if updated_str:
            try:
                updated = datetime.strptime(updated_str[:10], "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                stale = updated < threshold
            except ValueError:
                pass
        queue.append(
            {
                "task_id": t.get("task_id", "?"),
                "title": t.get("title", "?"),
                "state": state,
                "owner": t.get("owner", "?"),
                "updated_at": updated_str,
                "stale": stale,
                "priority": _STATE_PRIORITY.get(state, 99),
            }
        )

    # Ranked: in_progress first, then by priority, stale tasks surfaced first within each tier
    queue.sort(key=lambda x: (x["priority"], not x["stale"], x["updated_at"]))

    active_messages: list[str] = []
    if MESSAGES_ACTIVE.exists():
        for p in sorted(MESSAGES_ACTIVE.glob("*.json")):
            active_messages.append(str(p.relative_to(ROOT)))

    ensure_runtime_dirs()
    active_jobs: list[dict] = []
    for p in sorted(JOBS_ACTIVE.glob("*.json")):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
            active_jobs.append(
                {
                    "job_id": payload.get("job_id", p.stem),
                    "task_id": payload.get("task_id", ""),
                    "status": payload.get("status", ""),
                    "current_agent": payload.get("current_agent", ""),
                    "pending_approval_id": payload.get("pending_approval_id", ""),
                }
            )
        except Exception:
            continue

    pending_approvals: list[dict] = []
    for p in sorted(APPROVALS_PENDING.glob("*.json")):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
            pending_approvals.append(
                {
                    "approval_id": payload.get("approval_id", p.stem),
                    "job_id": payload.get("job_id", ""),
                    "approval_type": payload.get("approval_type", ""),
                    "requested_by": payload.get("requested_by", ""),
                }
            )
        except Exception:
            continue

    inbox_items = _scan_inbox_items()

    return {
        "generated_at": timestamp(),
        "non_terminal_count": len(queue),
        "active_messages": active_messages,
        "active_jobs": active_jobs,
        "pending_approvals": pending_approvals,
        "work_queue": queue,
        "inbox_items": inbox_items,
        "inbox_unprocessed_count": sum(1 for i in inbox_items if i["unprocessed"]),
    }


def _write_resume(resume: dict) -> None:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    RESUME_PATH.write_text(json.dumps(resume, indent=2), encoding="utf-8")


def cmd_start(_: argparse.Namespace) -> int:
    required = [TEAM_INBOX, OWNER_PROFILE, HANDOFF, STATUS]
    missing = [path.relative_to(ROOT) for path in required if not path.exists()]
    if missing:
        print("PKA session start: FAIL")
        for item in missing:
            print(f"- Missing required path: {item}")
        return 1

    # Scan non-terminal tasks and build resumption manifest
    tasks = _scan_non_terminal_tasks()
    resume = _build_resume(tasks)
    _write_resume(resume)

    inbox_items = resume["inbox_items"]
    unprocessed = [i for i in inbox_items if i["unprocessed"]]

    print("PKA session start: PASS")
    print(f"- Team Inbox items: {len(inbox_items)}")
    if unprocessed:
        print(f"  [WARN] *** {len(unprocessed)} UNPROCESSED item(s) in Team Inbox (>{INBOX_STALE_HOURS}h old) — AXIOM must route before proceeding ***")
    for item in inbox_items[:20]:
        flag = " [UNPROCESSED]" if item["unprocessed"] else ""
        print(f"  - [{item['type']}] {item['path']} (age: {item['age_hours']}h){flag}")

    print(f"- Active messages: {len(resume['active_messages'])}")
    for m in resume["active_messages"][:5]:
        print(f"  - {m}")
    print(f"- Active jobs: {len(resume['active_jobs'])}")
    for job in resume["active_jobs"][:10]:
        approval_flag = f" approval={job['pending_approval_id']}" if job["pending_approval_id"] else ""
        print(f"  - {job['job_id']} | task={job['task_id']} | status={job['status']} | agent={job['current_agent']}{approval_flag}")
    print(f"- Pending approvals: {len(resume['pending_approvals'])}")
    for approval in resume["pending_approvals"][:10]:
        print(f"  - {approval['approval_id']} | job={approval['job_id']} | type={approval['approval_type']} | requested_by={approval['requested_by']}")

    queue = resume["work_queue"]
    stale_count = sum(1 for t in queue if t["stale"])
    print(f"- Non-terminal tasks: {resume['non_terminal_count']}")
    if stale_count:
        print(f"  [WARN] {stale_count} task(s) stale (>{STALE_HOURS}h since last update)")
    for task in queue[:15]:
        stale_flag = " [STALE]" if task["stale"] else ""
        print(
            f"  - [{task['state']}] {task['task_id']} | "
            f"owner={task['owner']}{stale_flag}"
        )

    print("- Required reads: Owner's Inbox/owner.md, Team/handoff.md, Team/status.md")
    print(f"- RESUME.json written: {RESUME_PATH.relative_to(ROOT)}")
    return 0


def cmd_end(_: argparse.Namespace) -> int:
    result = subprocess.run([sys.executable, str(AUDIT)], cwd=ROOT)

    # Write RESUME.json at session end so the next start has a baseline even if
    # the session crashes before an explicit end command is issued.
    tasks = _scan_non_terminal_tasks()
    resume = _build_resume(tasks)
    _write_resume(resume)
    print(f"- RESUME.json written: {RESUME_PATH.relative_to(ROOT)}")

    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PKA session gate")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.set_defaults(func=cmd_start)

    end = sub.add_parser("end")
    end.set_defaults(func=cmd_end)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
