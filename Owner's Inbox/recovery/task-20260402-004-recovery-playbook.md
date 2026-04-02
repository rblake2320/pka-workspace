# Recovery Playbook — TASK-20260402-004

- Title: CRUCIBLE: PKA v0.5.0 Full Script Test Sweep
- Current verdict: PARTIAL PASS — 10/13, all failures cascade from process_audit defects
- Current state: delivered
- Owner: CRUCIBLE
- Route: AXIOM -> CRUCIBLE
- Deliverable surface: Owner's Inbox/CRUCIBLE-pka-v050-test-sweep.md

## Problem Summary
- Objective: Run every PKA script in scripts/ and document pass/fail for each
- Failure signal: task recorded with verdict `PARTIAL PASS — 10/13, all failures cascade from process_audit defects` and requires controlled recovery.

## Immediate Containment
- Freeze further delivery claims until the failing condition is reproduced or dismissed.
- Preserve the current artifact, logs, and task record before retrying implementation.
- Record any customer-visible or operator-visible impact in the task notes or journal.

## Rollback Steps
- Identify the last known good deliverable or commit associated with this task.
- Revert to the last verified-good state before applying any new fix attempt.
- Re-run the minimum validation needed to confirm the rollback is safe.

## Recovery Path
- Reproduce the defect or failed condition with a deterministic test if possible.
- Route the fix through DEBUGGER or FORGE depending on whether root cause is known.
- Send the task back through CRUCIBLE and SENTINEL before re-delivery.

## Evidence Required Before Re-Delivery
- Updated task record with the corrected state and verdict.
- Fresh test evidence showing the failed condition is now covered.
- Manifest update only after the final verdict is GO.

## Owner Guidance
- Do not treat the prior deliverable as final while this playbook is active.
- Ask for the reproduced failure, fix summary, and new verdict before approving next action.
