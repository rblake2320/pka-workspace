#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pka_lib import (
    HANDOFF,
    LOGS_DIR,
    MANIFEST,
    REPORTS_DIR,
    ROOT,
    STATUS,
    TASKS_DIR,
    parse_task_file,
)

REQUIRED_PATHS = [
    ROOT / "Team Inbox",
    ROOT / "Owner's Inbox" / "owner.md",
    ROOT / "Team" / "OPERATING_MODEL.md",
    ROOT / "Team" / "AGENT_TOOL_ENTITLEMENTS.json",
    ROOT / "scripts" / "pka_runtime.py",
    ROOT / "scripts" / "pka_runtime_check.py",
    TASKS_DIR,
    MANIFEST,
    STATUS,
    HANDOFF,
]

HISTORY_FILE = LOGS_DIR / "pka_validation_history.jsonl"
LATEST_REPORT = REPORTS_DIR / "PKA_LATEST_VALIDATION_REPORT.md"
OBS_REPORT = REPORTS_DIR / "PKA_OBSERVABILITY_REPORT.md"


def check_paths() -> list[str]:
    issues: list[str] = []
    for path in REQUIRED_PATHS:
        if not path.exists():
            issues.append(f"Missing required path: {path.relative_to(ROOT)}")
    return issues


def check_python() -> list[str]:
    issues: list[str] = []
    if sys.version_info < (3, 11):
        issues.append(f"Python too old: {sys.version.split()[0]}")
    return issues


def check_git_boundary() -> list[str]:
    issues: list[str] = []
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        issues.append("Git root could not be determined")
        return issues
    git_root = Path(result.stdout.strip())
    if git_root != ROOT:
        issues.append(f"Workspace is nested inside parent git root: {git_root}")
    return issues


def check_validation_history() -> list[str]:
    issues: list[str] = []
    if not HISTORY_FILE.exists():
        issues.append("Validation history missing: logs/pka_validation_history.jsonl")
        return issues
    lines = [line for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        issues.append("Validation history file is empty")
        return issues
    latest = json.loads(lines[-1])
    if int(latest.get("score", 0)) < 100:
        issues.append(f"Latest validation score below 100: {latest.get('score', 0)}")
    return issues


def check_reports() -> list[str]:
    issues: list[str] = []
    for path in (LATEST_REPORT, OBS_REPORT):
        if not path.exists():
            issues.append(f"Missing report: {path.relative_to(ROOT)}")
    return issues


def check_chat_key() -> list[str]:
    issues: list[str] = []
    key_paths = [
        Path.home() / ".ssh" / "ai_army_codex",
        Path.home() / ".ssh" / "ai_army",
    ]
    if not any(path.exists() for path in key_paths):
        issues.append(f"Missing AI Army SSH key: {key_paths[0]} or {key_paths[1]}")
    return issues


def check_memory_size() -> list[str]:
    """Check MEMORY.md is within the 200-line / 25 KB dual cap (from Claude Code source)."""
    issues: list[str] = []
    memory_path = (
        Path.home()
        / ".claude"
        / "projects"
        / "C--Users-techai"
        / "memory"
        / "MEMORY.md"
    )
    if not memory_path.exists():
        return issues
    text = memory_path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    byte_count = len(text.encode("utf-8"))
    if line_count > 200:
        issues.append(f"MEMORY.md is {line_count} lines (cap: 200) — truncation risk")
    if byte_count > 25_000:
        issues.append(f"MEMORY.md is {byte_count:,} bytes (cap: 25,000) — truncation risk")
    return issues


def check_hooks() -> list[str]:
    issues: list[str] = []
    settings_path = ROOT / ".claude" / "settings.local.json"
    if not settings_path.exists():
        issues.append("No .claude/settings.local.json — hooks cannot be configured")
        return issues
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        if not data.get("hooks"):
            issues.append("hooks key absent from .claude/settings.local.json")
        else:
            post = data["hooks"].get("PostToolUse", [])
            if not post:
                issues.append("PostToolUse hook not configured")
    except (json.JSONDecodeError, Exception) as exc:
        issues.append(f"Could not parse settings.local.json: {exc}")
    return issues


def check_stale_tasks() -> list[str]:
    """Warn about non-terminal tasks whose updated_at is older than 48 hours."""
    issues: list[str] = []
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=48)
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        try:
            data, _ = parse_task_file(path)
        except Exception:
            continue
        state = data.get("state", "")
        if state in {"delivered", "archived"}:
            continue
        updated_str = data.get("updated_at", "")
        if not updated_str:
            continue
        try:
            updated = datetime.strptime(updated_str[:10], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        if updated < threshold:
            age_h = (now - updated).total_seconds() / 3600
            issues.append(
                f"Stale task: {data.get('task_id','?')} | "
                f"owner={data.get('owner','?')} | state={state} | "
                f"{age_h:.0f}h since last update"
            )
    return issues


def check_health_surfaces() -> list[str]:
    issues: list[str] = []
    for path in (
        ROOT / "scripts" / "pka_machine_health.py",
        ROOT / "scripts" / "pka_entitlement_check.py",
        ROOT / "scripts" / "pka_recovery_playbook.py",
        ROOT / "scripts" / "pka_runtime.py",
        ROOT / "scripts" / "pka_runtime_check.py",
    ):
        if not path.exists():
            issues.append(f"Missing readiness control: {path.relative_to(ROOT)}")
    return issues


def main() -> int:
    checks = [
        ("python", check_python()),
        ("paths", check_paths()),
        ("git_boundary", check_git_boundary()),
        ("validation_history", check_validation_history()),
        ("reports", check_reports()),
        ("chat_key", check_chat_key()),
        ("hooks_configured", check_hooks()),
        ("memory_size", check_memory_size()),
        ("readiness_controls", check_health_surfaces()),
        ("stale_tasks", check_stale_tasks()),
    ]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_issues = sum(len(issues) for _, issues in checks)

    print("PKA Doctor")
    print(f"- Timestamp: {timestamp}")
    for name, issues in checks:
        if issues:
            print(f"- {name}: WARN")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"- {name}: PASS")

    if total_issues == 0:
        print("- Overall: healthy")
        return 0

    print(f"- Overall: warnings present ({total_issues})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
