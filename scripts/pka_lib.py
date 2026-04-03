#!/usr/bin/env python
from __future__ import annotations

import contextlib
import ctypes
import ctypes.wintypes
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEAM_DIR = ROOT / "Team"
TASKS_DIR = TEAM_DIR / "tasks"
STATUS = TEAM_DIR / "status.md"
HANDOFF = TEAM_DIR / "handoff.md"
MANIFEST = ROOT / "Owner's Inbox" / "DELIVERY_MANIFEST.md"
MESSAGES_ACTIVE = TEAM_DIR / "messages" / "active"
MESSAGES_ARCHIVE = TEAM_DIR / "messages" / "archive"
LOGS_DIR = ROOT / "logs"
REPORTS_DIR = ROOT / "Owner's Inbox" / "reports"
RUNTIME_DIR = TEAM_DIR / "runtime"
JOBS_ACTIVE = RUNTIME_DIR / "jobs" / "active"
JOBS_ARCHIVE = RUNTIME_DIR / "jobs" / "archive"
APPROVALS_PENDING = RUNTIME_DIR / "approvals" / "pending"
APPROVALS_RESOLVED = RUNTIME_DIR / "approvals" / "resolved"

VALID_STATES = {
    "new",
    "classified",
    "assigned",
    "in_progress",
    "under_test",
    "under_audit",
    "delivered",
    "archived",
}

STATE_ORDER = {
    "new": 0,
    "classified": 1,
    "assigned": 2,
    "in_progress": 3,
    "under_test": 4,
    "under_audit": 5,
    "delivered": 6,
    "archived": 7,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today() -> str:
    return utc_now().strftime("%Y-%m-%d")


def timestamp() -> str:
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FileLock:
    """Cross-process file lock with stale-lock detection.

    When a lock is created, writes ``{pid}:{unix_timestamp}`` into the lock
    file so that a competing process can detect and break stale locks.

    Stale detection (either condition):
    - Lock age > STALE_SECONDS (300 s / 5 minutes)
    - PID recorded in lock file is no longer alive (Windows-safe check via
      ctypes.windll.kernel32.OpenProcess — NOT os.kill which is unsafe on
      Windows and can terminate processes)

    Stale breaks are logged to ``logs/guardrail_YYYYMMDD.jsonl``.
    """

    STALE_SECONDS: int = 300  # 5 minutes

    def __init__(self, target: Path, retries: int = 50, delay: float = 0.1):
        self.lock_path = target.with_suffix(target.suffix + ".lock")
        self.retries = retries
        self.delay = delay
        self.fd: int | None = None

    # ── PID liveness ──────────────────────────────────────────────────────

    @staticmethod
    def _is_pid_alive(pid: int) -> bool:
        """Return True if the PID is alive on Windows using OpenProcess."""
        try:
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, pid
            )
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return False
        except Exception:
            # If ctypes check fails for any reason, assume alive (safe default)
            return True

    # ── Stale detection ───────────────────────────────────────────────────

    def _check_stale(self) -> bool:
        """Break the lock if it is stale.  Returns True if lock was broken."""
        try:
            content = self.lock_path.read_text(encoding="utf-8").strip()
            parts = content.split(":", 1)
            if len(parts) != 2:
                return False
            pid = int(parts[0])
            ts = float(parts[1])
            age = time.time() - ts
            pid_dead = not self._is_pid_alive(pid)
            if age > self.STALE_SECONDS or pid_dead:
                self._log_stale_break(pid, age, pid_dead)
                try:
                    self.lock_path.unlink()
                except FileNotFoundError:
                    pass
                return True
        except Exception:
            pass
        return False

    def _log_stale_break(self, pid: int, age: float, pid_dead: bool) -> None:
        try:
            log_dir = ROOT / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"guardrail_{utc_now().strftime('%Y%m%d')}.jsonl"
            entry = json.dumps(
                {
                    "ts": timestamp(),
                    "tool": "FileLock",
                    "session_id": "system",
                    "violations": [
                        f"Stale lock broken: {self.lock_path.name} | "
                        f"pid={pid} | age={age:.0f}s | pid_dead={pid_dead}"
                    ],
                }
            )
            with open(str(log_path), "a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
        except Exception:
            pass

    # ── Context manager ───────────────────────────────────────────────────

    def __enter__(self) -> "FileLock":
        for _ in range(self.retries):
            try:
                self.fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                # Record pid:timestamp for stale detection by competing processes
                os.write(self.fd, f"{os.getpid()}:{time.time()}".encode())
                return self
            except FileExistsError:
                if self._check_stale():
                    # Stale lock was broken — retry immediately on next iteration
                    continue
                time.sleep(self.delay)
        raise SystemExit(f"Could not acquire lock: {self.lock_path}")

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass


VALIDATION_LOCK = LOGS_DIR / ".pka-validation"


def acquire_validation_lock(timeout_s: int = 600) -> "FileLock | contextlib.AbstractContextManager[None]":
    """Suite-level lock preventing concurrent validation runs.

    If PKA_VALIDATION_LOCKED=1 is set (a parent process holds the lock),
    returns a no-op context manager to avoid deadlock in nested subprocess calls.
    Timeout defaults to 600s (10 min) to exceed the longest known validation run.
    """
    if os.environ.get("PKA_VALIDATION_LOCKED") == "1":
        return contextlib.nullcontext()
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    # 0.5s delay × (timeout_s * 2) retries ≈ timeout_s seconds of waiting
    retries = max(1, timeout_s * 2)
    return FileLock(VALIDATION_LOCK, retries=retries, delay=0.5)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def next_task_id() -> str:
    prefix = utc_now().strftime("TASK-%Y%m%d-")
    existing = []
    for path in TASKS_DIR.glob("*.md"):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        text = read_text(path)
        match = re.search(r'^task_id:\s*"(' + re.escape(prefix) + r'(\d{3}))"$', text, re.M)
        if match:
            existing.append(int(match.group(2)))
    return f"{prefix}{(max(existing) + 1 if existing else 1):03d}"


def parse_task_file(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} has invalid frontmatter")
    block = parts[1]
    body = parts[2]
    data: dict[str, str] = {}
    current_key: str | None = None
    route_items: list[str] = []

    for raw_line in block.splitlines():
        if raw_line.startswith("  - ") and current_key == "route":
            route_items.append(raw_line[4:].strip().strip('"'))
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        current_key = key if value == "" else None
        if key == "route":
            route_items = []
            continue
        data[key] = value

    data["route"] = "|".join(route_items)
    return data, body


def write_task_file(path: Path, data: dict[str, str], body: str) -> None:
    route_lines = "\n".join(f'  - "{item}"' for item in data["route"].split("|") if item)
    content = (
        "---\n"
        f'task_id: "{data["task_id"]}"\n'
        f'title: "{data["title"]}"\n'
        f'state: "{data["state"]}"\n'
        f'priority: "{data["priority"]}"\n'
        f'owner: "{data["owner"]}"\n'
        "route:\n"
        f"{route_lines}\n"
        f'intake_file: "{data["intake_file"]}"\n'
        f'deliverable_file: "{data["deliverable_file"]}"\n'
        f'verdict: "{data["verdict"]}"\n'
        f'created_at: "{data["created_at"]}"\n'
        f'updated_at: "{data["updated_at"]}"\n'
        f'definition_of_done: "{data["definition_of_done"]}"\n'
        "blockers: []\n"
        "---\n"
        f"{body}"
    )
    path.write_text(content, encoding="utf-8")


def find_task_path(task_id: str) -> Path:
    for path in TASKS_DIR.glob("*.md"):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        if f'task_id: "{task_id}"' in read_text(path):
            return path
    raise SystemExit(f"Task not found: {task_id}")


def list_task_records() -> list[tuple[Path, dict[str, str], str]]:
    records = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        data, body = parse_task_file(path)
        records.append((path, data, body))
    return records


def latest_relevant_tasks(limit: int = 5) -> list[dict[str, str]]:
    records = []
    for path, data, _ in list_task_records():
        record = dict(data)
        record["_path"] = str(path.relative_to(ROOT))
        records.append(record)
    records.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return records[:limit]


def sync_control_files() -> None:
    tasks = latest_relevant_tasks(10)
    active = [
        t for t in tasks
        if t.get("state") not in {"delivered", "archived"}
    ]
    delivered = [
        t for t in tasks
        if t.get("state") in {"delivered", "archived"} or t.get("verdict") == "delivered"
    ]

    last_updated = today()

    active_rows = []
    if active:
        for task in active[:5]:
            active_rows.append(
                f'| {task.get("owner","—")} | {task.get("state","—")} | {task.get("title","—")} | '
                f'{task.get("updated_at","—")} | {"none"} |'
            )
    else:
        active_rows.append("| — | — | No active routed work | — | — |")

    pending_rows = []
    if active:
        for task in active[:5]:
            pending_rows.append(
                f'| {task.get("title","—")} | {task.get("owner","—")} | {task.get("state","—")} | {task.get("_path","—")} |'
            )
    else:
        pending_rows.append("| — | — | — | — |")

    delivered_titles = ", ".join(f'`{t.get("title","")}`' for t in delivered[:3]) if delivered else "none"
    pending_titles = ", ".join(f'`{t.get("title","")}`' for t in active[:3]) if active else "none"
    key_decision = "Use the task ledger and real tests as the source of truth"

    status_text = "\n".join(
        [
            "# Team Status Board",
            "*Updated by AXIOM at session start/end. Updated by agents during task execution.*",
            f"*Last updated: {last_updated}*",
            "",
            "## Active Work",
            "| Agent | Status | Current Task | Started | Blocked By |",
            "|-------|--------|-------------|---------|------------|",
            *active_rows,
            "",
            "## Last Session Summary",
            f"- **Date**: {last_updated}",
            f"- **Tasks completed**: {len(delivered)}",
            f"- **Deliverables to Owner's Inbox**: {delivered_titles}",
            f"- **Pending/blocked**: {pending_titles}",
            f"- **Key decisions made**: {key_decision}",
            "",
            "## Pending Work (cross-session)",
            "| Task | Assigned To | Status | Notes |",
            "|------|------------|--------|-------|",
            *pending_rows,
            "",
            "## Session-Start Checklist",
            "- [ ] `Team Inbox/` reviewed",
            "- [ ] `Owner's Inbox/owner.md` reviewed",
            "- [ ] `Team/handoff.md` reviewed",
            "- [ ] `Team/status.md` reviewed",
            "- [ ] New work classified",
            "- [ ] Highest-priority route confirmed",
            "",
        ]
    )

    accomplished = []
    if delivered:
        for task in delivered[:5]:
            accomplished.append(
                f'- {task.get("title","—")} | Route: {task.get("route","").replace("|"," -> ")} | '
                f'Result: {task.get("verdict") or task.get("state","—")} | Output: `{task.get("deliverable_file") or task.get("_path","—")}`'
            )
    else:
        accomplished.append("- No delivered work recorded")

    pending = []
    if active:
        for task in active[:5]:
            pending.append(
                f'- {task.get("title","—")} | Current state: {task.get("state","—")} | Owner: {task.get("owner","—")} | Blocker: none'
            )
    else:
        pending.append("- No active consequential tasks")

    next_actions = [
        "- Review active tasks in `Team/tasks/`",
        "- Update `Owner's Inbox/DELIVERY_MANIFEST.md` for any new deliverable",
        "- Run `python scripts/pka_process_audit.py` before closeout",
    ]

    handoff_text = "\n".join(
        [
            "# Session Handoff",
            "*Written by AXIOM at session end. Read by AXIOM at next session start.*",
            "*This file is OVERWRITTEN each session — only the most recent handoff matters.*",
            "",
            "## Last Session",
            f"- **Date**: {last_updated}",
            "- **Duration**: Rolling session state",
            "- **Ron's focus**: High-rigor AI operating process",
            "- **Session outcome**: clean progress",
            "",
            "## What Was Accomplished",
            *accomplished,
            "",
            "## What Is Pending",
            *pending,
            "",
            "## What Needs Attention Next",
            *next_actions,
            "",
            "## Agent Notes",
            "- AXIOM: Treat `Team/OPERATING_MODEL.md` as canonical",
            "- FORGE: Keep consequential work in the task ledger",
            "- SENTINEL/CRUCIBLE: green claims require real tests",
            "",
            "## Spark-1 Status at Session End",
            "- Not updated by local auto-sync",
            "",
            "## Session-End Checklist",
            "- [ ] `Team Inbox/` reviewed and relevant items classified",
            "- [ ] `Team/status.md` updated to match reality",
            "- [ ] `Owner's Inbox/DELIVERY_MANIFEST.md` updated",
            "- [ ] Deliverables placed in `Owner's Inbox/`",
            "- [ ] Relevant agent journals updated",
            "- [ ] Temp artifacts cleaned up or moved out of workspace root",
            "",
        ]
    )

    STATUS.write_text(status_text, encoding="utf-8")
    HANDOFF.write_text(handoff_text, encoding="utf-8")


def create_message_file(payload: dict[str, object], short_name: str) -> Path:
    MESSAGES_ACTIVE.mkdir(parents=True, exist_ok=True)
    MESSAGES_ARCHIVE.mkdir(parents=True, exist_ok=True)
    file_name = f"{utc_now().strftime('%Y%m%d-%H%M%S')}-{payload['type']}-{slugify(short_name)}.json"
    path = MESSAGES_ACTIVE / file_name
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def archive_message(path: Path) -> Path:
    MESSAGES_ARCHIVE.mkdir(parents=True, exist_ok=True)
    target = MESSAGES_ARCHIVE / path.name
    path.replace(target)
    return target


def ensure_runtime_dirs() -> None:
    for path in (RUNTIME_DIR, JOBS_ACTIVE, JOBS_ARCHIVE, APPROVALS_PENDING, APPROVALS_RESOLVED):
        path.mkdir(parents=True, exist_ok=True)
