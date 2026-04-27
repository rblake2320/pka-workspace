#!/usr/bin/env python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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
    steps = [
        ("doctor", ("scripts/pka_doctor.py",)),
        ("machine_health", ("scripts/pka_machine_health.py",)),
        ("sync", ("scripts/pka_sync.py",)),
        ("entitlements", ("scripts/pka_entitlement_check.py",)),
        ("runtime", ("scripts/pka_runtime_check.py",)),
        ("full_validation", ("scripts/pka_full_validation.py",)),
        ("scorecard", ("scripts/pka_scorecard.py",)),
        ("telemetry", ("scripts/pka_telemetry.py",)),
        ("observability", ("scripts/pka_observability.py",)),
        ("journal_compact", ("scripts/pka_journal_compact.py",)),
        ("cost_tracker", ("scripts/pka_cost_tracker.py",)),
        ("dream", ("scripts/pka_dream.py",)),
        ("proof_dashboard", ("scripts/pka_proof_dashboard.py",)),
    ]

    print("PKA Operator Run")
    failures = 0
    for name, command in steps:
        ok, output = run(*command)
        if not ok:
            failures += 1
        summary = output.splitlines()[0] if output else ""
        print(f"- {name}: {'PASS' if ok else 'FAIL'} | {summary}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
