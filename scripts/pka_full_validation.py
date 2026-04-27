#!/usr/bin/env python
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pka_lib import LOGS_DIR, REPORTS_DIR, acquire_validation_lock

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = LOGS_DIR / "pka_validation_history.jsonl"
LATEST_REPORT = REPORTS_DIR / "PKA_LATEST_VALIDATION_REPORT.md"


def run(*args: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    with acquire_validation_lock():
        os.environ["PKA_VALIDATION_LOCKED"] = "1"
        return _run_suite()


def _run_suite() -> int:
    checks: list[tuple[str, bool, str]] = []

    ok, output = run("scripts/pka_process_audit.py")
    checks.append(("baseline_audit", ok, output))

    ok, output = run("scripts/pka_session_gate.py", "start")
    checks.append(("session_start", ok, output))

    for idx in range(1, 4):
        ok, output = run("scripts/pka_e2e_test.py")
        checks.append((f"e2e_run_{idx}", ok, output))

    ok, output = run("scripts/pka_resilience_test.py")
    checks.append(("resilience_suite", ok, output))

    ok, output = run("scripts/pka_process_audit.py")
    checks.append(("post_resilience_audit", ok, output))

    ok, output = run("scripts/pka_session_gate.py", "end")
    checks.append(("session_end", ok, output))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    history_entry = {
        "timestamp": timestamp,
        "score": score,
        "passed": passed,
        "total": total,
        "checks": [
            {
                "name": name,
                "ok": ok,
                "summary": output.splitlines()[0] if output else "",
            }
            for name, ok, output in checks
        ],
    }
    with HISTORY_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(history_entry) + "\n")

    report_lines = [
        "# PKA Latest Validation Report",
        "",
        f"- Timestamp: {timestamp}",
        f"- Score: {score}/100",
        f"- Passed: {passed}/{total}",
        "",
        "## Checks",
    ]
    for name, ok, output in checks:
        summary = output.splitlines()[0] if output else ""
        report_lines.append(f"- {name}: {'PASS' if ok else 'FAIL'} | {summary}")
    LATEST_REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("PKA Full Validation")
    print(f"- Score: {score}/100")
    print(f"- Passed: {passed}/{total}")
    for name, ok, output in checks:
        summary = output.splitlines()[0] if output else ""
        print(f"- {name}: {'PASS' if ok else 'FAIL'} | {summary}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
