#!/usr/bin/env python
"""
PostToolUse hook — two responsibilities:
1. Append every significant tool call to logs/session_YYYYMMDD.jsonl (audit trail)
2. Run pka_guardrails.py checks to detect secret leaks, out-of-scope writes,
   and malformed Task launches (violations logged to logs/guardrail_YYYYMMDD.jsonl)

Receives JSON on stdin from Claude Code:
  {
    "session_id": "...",
    "hook_event_name": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {...},
    "tool_response": {...}
  }

Always exits 0 — PostToolUse cannot block execution, only observe.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
SCRIPTS_DIR = ROOT / "scripts"

# Lazy-import guardrails to avoid breaking the hook if the file is missing
def _run_guardrails(data: dict) -> None:
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from pka_guardrails import (
            check_input_guardrail,
            check_scope_guardrail,
            check_secret_guardrail,
            log_violation,
        )
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
    except Exception:
        pass  # Never break the hook


def _summarize_input(inp: dict) -> str:
    if not inp:
        return ""
    for key in ("command", "file_path", "pattern", "query", "url", "path", "old_string"):
        if key in inp:
            val = str(inp[key])
            return val[:200] if len(val) > 200 else val
    return str(inp)[:200]


def _summarize_result(resp: object) -> str:
    if isinstance(resp, str):
        return resp[:120]
    if isinstance(resp, dict):
        for key in ("output", "content", "result", "error", "stdout", "stderr"):
            if key in resp:
                val = str(resp[key])
                return val[:120]
        return str(resp)[:120]
    return ""


def main() -> int:
    try:
        raw = sys.stdin.buffer.read()
        if not raw.strip():
            return 0
        data = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return 0

    # 1. Audit log
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        date = datetime.now(timezone.utc).strftime("%Y%m%d")
        log_path = LOGS_DIR / f"session_{date}.jsonl"

        record = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tool": data.get("tool_name", "unknown"),
            "session_id": str(data.get("session_id", ""))[:16],
            "input": _summarize_input(data.get("tool_input") or {}),
            "result": _summarize_result(data.get("tool_response")),
        }

        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass  # Never fail — hook must not interrupt agent ops

    # 2. Guardrails (runs after audit log — never blocks)
    _run_guardrails(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
