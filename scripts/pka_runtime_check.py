#!/usr/bin/env python
from __future__ import annotations

import json
import sys

from pka_lib import APPROVALS_PENDING, JOBS_ACTIVE, ensure_runtime_dirs

VALID_JOB_STATES = {"queued", "running", "waiting_approval", "interrupted", "completed"}


def main() -> int:
    ensure_runtime_dirs()
    issues: list[str] = []
    jobs = sorted(JOBS_ACTIVE.glob("*.json"))
    approvals = sorted(APPROVALS_PENDING.glob("*.json"))

    for path in jobs:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"{path.name}: invalid json ({exc})")
            continue
        if payload.get("status") not in VALID_JOB_STATES:
            issues.append(f"{path.name}: invalid status {payload.get('status')}")
        if not payload.get("task_id"):
            issues.append(f"{path.name}: missing task_id")
        if payload.get("status") == "waiting_approval" and not payload.get("pending_approval_id"):
            issues.append(f"{path.name}: waiting_approval without pending_approval_id")

    for path in approvals:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"{path.name}: invalid json ({exc})")
            continue
        job_id = payload.get("job_id", "")
        if job_id and not (JOBS_ACTIVE / f"{job_id}.json").exists():
            issues.append(f"{path.name}: linked job missing ({job_id})")

    if issues:
        print("PKA Runtime Check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PKA Runtime Check: PASS")
    print(f"- Active jobs: {len(jobs)}")
    print(f"- Pending approvals: {len(approvals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
