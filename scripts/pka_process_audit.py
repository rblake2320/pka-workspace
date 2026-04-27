#!/usr/bin/env python
"""
Lightweight process audit for the PKA workspace.

Purpose:
- validate the task ledger
- catch stale placeholder control files
- verify delivered tasks are represented in the manifest
- scan shared process files for high-confidence secret patterns
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM_DIR = ROOT / "Team"
TASKS_DIR = TEAM_DIR / "tasks"
OWNER_INBOX = ROOT / "Owner's Inbox"
MANIFEST = OWNER_INBOX / "DELIVERY_MANIFEST.md"
STATUS = TEAM_DIR / "status.md"
HANDOFF = TEAM_DIR / "handoff.md"
RUNTIME_JOBS = TEAM_DIR / "runtime" / "jobs" / "active"
RUNTIME_APPROVALS = TEAM_DIR / "runtime" / "approvals" / "pending"

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

REQUIRED_FRONTMATTER = {
    "task_id",
    "title",
    "state",
    "owner",
    "route",
    "created_at",
    "updated_at",
    "definition_of_done",
}

PLACEHOLDER_MARKERS = {
    "[not yet populated]",
    "[timestamp]",
    "[task]",
    "[agent]",
    "[Highest-priority next action]",
}

SECRET_PATTERNS = [
    ("AWS Access Token", re.compile(r"\b(?:AKIA|ASIA|A3T[A-Z0-9]|ABIA|ACCA)[A-Z2-7]{16}\b")),
    ("GitHub PAT", re.compile(r"\bghp_[0-9A-Za-z]{36}\b")),
    ("GitHub Fine-Grained PAT", re.compile(r"\bgithub_pat_\w{82}\b")),
    ("Anthropic API Key", re.compile(r"\bsk-ant-(?:api|admin)[0-9A-Za-z_-]{20,}\b")),
    ("OpenAI API Key", re.compile(r"\bsk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}\b")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    ("Private Key Block", re.compile(r"-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY(?: BLOCK)?-----", re.I)),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("invalid frontmatter block")

    block = parts[1]
    data: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key:
            existing = data.setdefault(current_list_key, [])
            if isinstance(existing, list):
                existing.append(line[4:].strip().strip('"'))
            continue
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            data[key] = []
            current_list_key = key
            continue

        data[key] = parse_scalar(value)
        current_list_key = None

    return data


def has_placeholders(text: str) -> bool:
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def scan_for_secrets(paths: list[Path]) -> list[str]:
    findings: list[str] = []
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(
                    f"{path.relative_to(ROOT)}: potential secret pattern detected ({label})"
                )
    return findings


def audit_task_records() -> list[str]:
    issues: list[str] = []
    manifest_text = read_text(MANIFEST) if MANIFEST.exists() else ""

    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue

        try:
            data = parse_frontmatter(path)
        except ValueError as exc:
            issues.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        missing = sorted(key for key in REQUIRED_FRONTMATTER if key not in data)
        if missing:
            issues.append(
                f"{path.relative_to(ROOT)}: missing frontmatter fields: {', '.join(missing)}"
            )
            continue

        state = str(data.get("state", "")).strip()
        if state not in VALID_STATES:
            issues.append(f"{path.relative_to(ROOT)}: invalid state '{state}'")

        route = data.get("route")
        if not isinstance(route, list) or not route:
            issues.append(f"{path.relative_to(ROOT)}: route must be a non-empty list")

        title = str(data.get("title", "")).strip()
        task_id = str(data.get("task_id", "")).strip()
        verdict = str(data.get("verdict", "")).strip()
        deliverable_file = str(data.get("deliverable_file", "")).strip()

        if verdict == "delivered" and state not in {"delivered", "archived"}:
            issues.append(
                f"{path.relative_to(ROOT)}: verdict is delivered but state is '{state}'"
            )

        if state in {"delivered", "archived"}:
            if not deliverable_file:
                issues.append(
                    f"{path.relative_to(ROOT)}: state '{state}' requires deliverable_file"
                )
            if task_id not in manifest_text and title not in manifest_text:
                issues.append(
                    f"{path.relative_to(ROOT)}: delivered task not found in DELIVERY_MANIFEST.md"
                )

    return issues


def audit_control_files() -> list[str]:
    issues: list[str] = []

    for control_file in (STATUS, HANDOFF, MANIFEST):
        if not control_file.exists():
            issues.append(f"Missing required control file: {control_file.relative_to(ROOT)}")

    if STATUS.exists() and has_placeholders(read_text(STATUS)):
        issues.append("Team/status.md still contains placeholder content")

    if HANDOFF.exists() and has_placeholders(read_text(HANDOFF)):
        issues.append("Team/handoff.md still contains placeholder content")

    if MANIFEST.exists():
        lines = read_text(MANIFEST).splitlines()
        if "| Date | Task | Route | Verdict | Deliverable | Next Action |" not in lines:
            issues.append("Owner's Inbox/DELIVERY_MANIFEST.md is missing the table header")
        if "|------|------|------|------|------|------|" not in lines:
            issues.append("Owner's Inbox/DELIVERY_MANIFEST.md is missing the table separator")
        if lines and len(lines) > 1:
            separator_idx = None
            for idx, line in enumerate(lines):
                if line == "|------|------|------|------|------|------|":
                    separator_idx = idx
                    break
            if separator_idx is not None:
                for prelude_line in lines[:separator_idx]:
                    if prelude_line.startswith("| ") and "Date" not in prelude_line:
                        issues.append(
                            "Owner's Inbox/DELIVERY_MANIFEST.md has delivery rows outside the table body"
                        )
                        break

    return issues


def audit_journals() -> list[str]:
    issues: list[str] = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        try:
            data = parse_frontmatter(path)
        except ValueError:
            continue  # already caught in audit_task_records
        state = str(data.get("state", "")).strip()
        if state != "delivered":
            continue
        task_id = str(data.get("task_id", "")).strip()
        owner = str(data.get("owner", "")).strip()
        if not owner or not task_id:
            continue
        journal_path = ROOT / "Team" / owner / "journal.md"
        if not journal_path.exists():
            issues.append(f"Team/{owner}/journal.md: file missing (owner of {task_id})")
            continue
        journal_text = read_text(journal_path)
        if task_id not in journal_text:
            issues.append(
                f"Team/{owner}/journal.md: no entry for delivered task {task_id}"
            )
    return issues


def audit_runtime_state() -> list[str]:
    issues: list[str] = []
    for path in sorted(RUNTIME_JOBS.glob("*.json")):
        try:
            payload = json.loads(read_text(path))
        except Exception as exc:
            issues.append(f"{path.relative_to(ROOT)}: invalid runtime job json ({exc})")
            continue
        if not payload.get("task_id"):
            issues.append(f"{path.relative_to(ROOT)}: runtime job missing task_id")
        if payload.get("status") == "waiting_approval" and not payload.get("pending_approval_id"):
            issues.append(f"{path.relative_to(ROOT)}: waiting_approval without pending_approval_id")
    for path in sorted(RUNTIME_APPROVALS.glob("*.json")):
        try:
            payload = json.loads(read_text(path))
        except Exception as exc:
            issues.append(f"{path.relative_to(ROOT)}: invalid approval json ({exc})")
            continue
        job_id = payload.get("job_id", "")
        if job_id and not (RUNTIME_JOBS / f"{job_id}.json").exists():
            issues.append(f"{path.relative_to(ROOT)}: linked runtime job missing ({job_id})")
    return issues


def audit_evidence_bundles() -> list[str]:
    """Validate all JSON evidence bundles in governance/evidence/."""
    issues: list[str] = []
    evidence_dir = ROOT / "governance" / "evidence"
    if not evidence_dir.exists():
        return issues  # no bundles yet is not an error

    BUNDLE_EVIDENCE_CLASSES = {"tool_receipt", "live_observation", "source_attribution", "inference", "ungrounded"}

    for path in sorted(evidence_dir.glob("*.json")):
        try:
            bundle = json.loads(read_text(path))
        except Exception as exc:
            issues.append(f"governance/evidence/{path.name}: invalid JSON ({exc})")
            continue

        for field in ("bundle_id", "task_id", "agent_id", "verdict", "created_at", "items"):
            if field not in bundle:
                issues.append(f"governance/evidence/{path.name}: missing field '{field}'")

        items = bundle.get("items", [])
        if not isinstance(items, list):
            issues.append(f"governance/evidence/{path.name}: 'items' must be a list")
            continue

        for idx, item in enumerate(items):
            cls = item.get("class", "")
            if cls not in BUNDLE_EVIDENCE_CLASSES:
                issues.append(f"governance/evidence/{path.name}: item[{idx}] invalid class '{cls}'")
            for req in ("claim", "evidence", "timestamp"):
                if not item.get(req):
                    issues.append(f"governance/evidence/{path.name}: item[{idx}] missing '{req}'")

        verdict = bundle.get("verdict", "").upper()
        if verdict == "GO":
            has_hard = any(i.get("class") in ("tool_receipt", "live_observation") for i in items)
            if not has_hard:
                issues.append(f"governance/evidence/{path.name}: GO verdict with no tool_receipt/live_observation")

    return issues


def audit_handoff_json() -> list[str]:
    """Validate structured handoff JSON if present."""
    issues: list[str] = []
    handoff_json = TEAM_DIR / "handoff.json"
    if not handoff_json.exists():
        return issues  # not yet generated is not an error

    try:
        data = json.loads(read_text(handoff_json))
    except Exception as exc:
        issues.append(f"Team/handoff.json: invalid JSON ({exc})")
        return issues

    for field in ("session_id", "timestamp", "tasks_active", "tasks_delivered"):
        if field not in data:
            issues.append(f"Team/handoff.json: missing field '{field}'")

    return issues


def main() -> int:
    issues: list[str] = []

    if not TASKS_DIR.exists():
        issues.append("Team/tasks directory is missing")

    issues.extend(audit_control_files())
    issues.extend(audit_task_records())
    issues.extend(audit_journals())
    issues.extend(audit_runtime_state())
    issues.extend(audit_evidence_bundles())
    issues.extend(audit_handoff_json())

    secret_paths = [STATUS, HANDOFF, MANIFEST]
    if TASKS_DIR.exists():
        secret_paths.extend(path for path in TASKS_DIR.glob("*.md"))
    issues.extend(scan_for_secrets(secret_paths))

    if issues:
        print("PKA process audit: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PKA process audit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
