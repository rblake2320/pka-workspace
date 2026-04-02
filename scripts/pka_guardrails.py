#!/usr/bin/env python
"""
pka_guardrails.py — Pre-execution guardrails for the PKA workspace.

Called by the PostToolUse hook after significant tool calls.
Detects violations and logs them to logs/guardrail_YYYYMMDD.jsonl.
Prints warnings to stderr on violations so they surface in agent output.

Three guardrails:
1. INPUT GUARDRAIL — Task agent launched without required fields (owner, route, DoD)
2. SECRET GUARDRAIL — Write/Edit contains secret patterns (API keys, passwords, tokens)
3. SCOPE GUARDRAIL — Bash command writes outside the PKA workspace

Does NOT block execution (PostToolUse fires after the fact).
Use these logs for audit and to identify agents that need coaching.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"

# --- Secret patterns ---
SECRET_PATTERNS = [
    # Generic API key patterns
    re.compile(r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}'),
    re.compile(r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}'),
    re.compile(r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'](?!.*\$\{)[^"\']{6,}["\']'),
    re.compile(r'(?i)(token|bearer)\s*[=:]\s*["\']?[A-Za-z0-9_\-\.]{20,}'),
    # AWS
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'(?i)aws.{0,20}(secret|key).{0,20}[A-Za-z0-9/+]{40}'),
    # Generic private key header
    re.compile(r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    # Anthropic / OpenAI
    re.compile(r'sk-[A-Za-z0-9_\-]{30,}'),
    re.compile(r'sk-ant-[A-Za-z0-9_\-]{30,}'),
    # Postgres connection strings with credentials
    re.compile(r'postgresql://[^:]+:[^@]{6,}@'),
]

# Patterns that are explicitly allowed (env var references, placeholders)
ALLOWLIST_PATTERNS = [
    re.compile(r'\$\{[A-Z_]+\}'),          # ${ENV_VAR}
    re.compile(r'os\.environ'),             # os.environ['KEY']
    re.compile(r'process\.env'),            # process.env.KEY
    re.compile(r'\[Add|placeholder|example|your[-_]'),  # placeholder text
    re.compile(r'%3F'),                     # URL-encoded chars in connection strings
]

# Scope: Bash write-outside-workspace patterns
BASH_WRITE_OUTSIDE_PATTERNS = [
    re.compile(r'\b(echo|printf|tee|cat\s*>|>>)\s+["\']?(?!\./|\.claude|Owner|Team|scripts|logs)(?:[A-Z]:|/(?!tmp|Users/techai/PKA))'),
]

# Required Task agent fields (checked in tool_input when tool_name is "Task")
TASK_REQUIRED_FIELDS = {"prompt"}


def _is_allowlisted(text: str, match: re.Match) -> bool:
    """Return True if the match context is an allowlisted pattern."""
    context_start = max(0, match.start() - 50)
    context_end = min(len(text), match.end() + 50)
    context = text[context_start:context_end]
    return any(p.search(context) for p in ALLOWLIST_PATTERNS)


def check_input_guardrail(tool_name: str, tool_input: dict) -> list[str]:
    """Verify Task agent launch has required structure."""
    if tool_name != "Task":
        return []
    violations = []
    prompt = str(tool_input.get("prompt", "")).strip()
    if not prompt:
        violations.append("Task launched with empty prompt — agent has no instructions")
        return violations
    # Check for the most critical missing elements in a task brief
    prompt_lower = prompt.lower()
    if len(prompt) < 50:
        violations.append(f"Task prompt is very short ({len(prompt)} chars) — may lack context")
    if "owner" not in prompt_lower and "route" not in prompt_lower and "deliver" not in prompt_lower:
        violations.append(
            "Task prompt may be missing owner/route/deliverable — agent cannot self-direct"
        )
    return violations


def check_secret_guardrail(tool_name: str, tool_input: dict) -> list[str]:
    """Scan Write/Edit content for embedded secrets."""
    if tool_name not in {"Write", "Edit", "MultiEdit"}:
        return []

    violations = []
    content_fields = []

    if tool_name == "Write":
        content_fields = [str(tool_input.get("content", ""))]
    elif tool_name == "Edit":
        content_fields = [
            str(tool_input.get("new_string", "")),
            str(tool_input.get("old_string", "")),
        ]
    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        for edit in edits:
            content_fields.append(str(edit.get("new_string", "")))

    for content in content_fields:
        if not content:
            continue
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(content):
                if not _is_allowlisted(content, match):
                    snippet = content[max(0, match.start() - 10): match.end() + 10]
                    violations.append(
                        f"Potential secret in {tool_name} content: ...{snippet[:60]}..."
                    )
    return violations


def check_scope_guardrail(tool_name: str, tool_input: dict) -> list[str]:
    """Verify Bash commands don't write outside the workspace."""
    if tool_name != "Bash":
        return []
    command = str(tool_input.get("command", ""))
    violations = []
    for pattern in BASH_WRITE_OUTSIDE_PATTERNS:
        if pattern.search(command):
            violations.append(f"Bash command may write outside workspace: {command[:100]}")
    return violations


def log_violation(tool_name: str, violations: list[str], session_id: str) -> None:
    """Append violations to the guardrail log."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    log_path = LOGS_DIR / f"guardrail_{date}.jsonl"

    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": tool_name,
        "session_id": session_id[:16] if session_id else "",
        "violations": violations,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def main() -> int:
    try:
        raw = sys.stdin.buffer.read()
        if not raw.strip():
            return 0
        data = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return 0

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    session_id = str(data.get("session_id", ""))

    violations: list[str] = []
    violations.extend(check_input_guardrail(tool_name, tool_input))
    violations.extend(check_secret_guardrail(tool_name, tool_input))
    violations.extend(check_scope_guardrail(tool_name, tool_input))

    if violations:
        log_violation(tool_name, violations, session_id)
        for v in violations:
            print(f"[GUARDRAIL WARNING] {v}", file=sys.stderr)

    return 0  # Never block — PostToolUse is informational only


if __name__ == "__main__":
    sys.exit(main())
