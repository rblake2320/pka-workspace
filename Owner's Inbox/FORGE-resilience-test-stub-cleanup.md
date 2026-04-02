# FORGE: Resilience Test Stub Cleanup

**Task**: TASK-20260402-008
**Date**: 2026-04-02
**Agent**: FORGE
**Verdict**: PASS -- both resilience test and process audit exit 0

---

## What Was Changed

### File: `scripts/pka_resilience_test.py`

The `finally` block (lines 271-310) was rewritten to handle three cleanup concerns:

**Bug 1: Orphan stubs from prior runs were never cleaned up.**
The original `finally` block only deleted files tracked in the `created_tasks` list, which is built during the current run. If a previous run crashed mid-cleanup, or if the test was run before the cleanup code existed, orphan stub files would persist in `Team/tasks/` forever. Two such orphans (`20260402-resilience-duplicate-probe-20260402-001.md` and `20260402-resilience-duplicate-probe-20260402-002.md`) were found in the ledger from a prior run.

**Fix**: After deleting `created_tasks`, the `finally` block now scans all files in `TASKS_DIR` and deletes any whose frontmatter title starts with `"Resilience "`. This catches orphans from any prior run regardless of date or task ID sequence.

**Bug 2: Hardcoded date in archive message cleanup.**
Line 285 of the original code checked `payload.get("task_id", "").startswith("TASK-20260401-")` -- a hardcoded date that would never match tasks created on 2026-04-02 or any future date. This meant archived messages from resilience probes were never cleaned up after 2026-04-01.

**Fix**: The archive cleanup now uses case-insensitive string matching on both `task_id` and `summary` fields for the word "resilience", which is date-independent and matches any resilience probe message from any run.

### File: `Owner's Inbox/DELIVERY_MANIFEST.md`

Three pre-existing ledger gaps were fixed (not caused by the resilience test, but exposed by it):

1. **TASK-20260402-009** (VENTURE) -- delivered with deliverable file present, but missing manifest row. Added via `pka_task_cli.py add-delivery`.
2. **TASK-20260402-010** (HELM) -- same pattern. Added via CLI.
3. **TASK-20260402-011** (LEGAL) -- same pattern. Added via CLI.
4. **Stale stub rows** for TASK-20260402-001 and 002 (archived-stub verdicts) were removed since those files no longer exist.
5. **Duplicate HELM row** (two different entries for TASK-20260402-010 from different sessions) was deduplicated.

---

## Actual Output

### Resilience Test (exit 0)
```
PKA Resilience Test
- Score: 100/100
- Passed: 9/9
- duplicate_title_protection: PASS | 20260402-resilience-duplicate-probe-20260402-012.md | 20260402-resilience-duplicate-probe-20260402-013.md
- state_regression_blocked: PASS | classified rollback rejected
- manifest_corruption_detected: PASS | separator corruption caught
- missing_manifest_row_detected: PASS | 20260402-resilience-delivered-probe-20260402-014.md
- placeholder_detection: PASS | status placeholder caught
- secret_scan_detection: PASS | 20260402-resilience-secret-probe-20260402-015.md
- message_protocol_flow: PASS | 20260402-174841-task_assignment-task-20260402-013.json
- recovery_audit_pass: PASS | audit restored
- recovery_e2e_pass: PASS | e2e restored
```

### Process Audit (exit 0)
```
PKA process audit: PASS
```

### Post-Run Stub Count
```
Resilience stub files remaining: 0
  (none -- cleanup working correctly)
```

---

## Edge Cases Handled

1. **Mid-run exception safety**: The entire cleanup is inside `try/finally`, so even if a test probe throws an unhandled exception, cleanup still executes. This was already in place and remains intact.

2. **Orphans from prior runs**: The title-based sweep (`title: "Resilience "` prefix match) catches stubs regardless of when they were created or what task ID sequence they used. The sentinel prefix is specific enough to never match real tasks (e.g., task 008 "FORGE: Fix pka_resilience_test.py stub self-cleanup" is correctly ignored).

3. **Date independence**: The archive message cleanup uses content matching ("resilience" in task_id or summary) instead of a hardcoded date prefix, so it works across date boundaries.

4. **Safe deletion**: Files are checked with `path.exists()` before `unlink()`. The orphan sweep wraps `read_text()` in a try/except to handle encoding errors or concurrent deletion.

5. **Manifest restoration**: The `finally` block restores the manifest to its pre-test snapshot (`manifest_before`), which means any manifest rows added by test probes (e.g., the delivered probe) are also rolled back. This was already correct in the original code.

---

## What Was NOT Changed

- The test probes themselves (all 9) are unchanged.
- The `pka_process_audit.py` script is unchanged.
- The `pka_lib.py` shared library is unchanged.
- The `pka_e2e_test.py` script is unchanged.
- The overall try/finally structure of `main()` is preserved.
