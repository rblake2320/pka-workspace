# Recovery Playbook — TASK-20260402-012

- Title: CRUCIBLE reopen test
- Current verdict: NO-GO
- Current state: under_test
- Owner: CRUCIBLE
- Route: CRUCIBLE
- Deliverable surface: not yet recorded

## Problem Summary
- Objective: test reopen command in v0.6.0
- Failure signal: task recorded with verdict `NO-GO` and requires controlled recovery.

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
