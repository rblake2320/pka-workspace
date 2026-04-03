# SENTINEL Pre-Implementation Checklist
# Version: 1.0 | Created: 2026-04-02 | Source: v0.7.0 skeptic review retrospective

## Purpose

Run this checklist against any plan before it goes to execution. The goal is not to block
good plans — it is to find the gaps that well-written plans routinely hide. The plan already
did the inventing. This checklist finds where the plan could hurt you.

Any agent can run this review. SENTINEL runs it by default on all plans flagged CRITICAL
or higher. FORGE and HELM should self-apply it before marking a plan ready.

---

## The 4-Question Filter

Apply these four questions to every destructive, irreversible, or assumption-dependent step:

| # | Question | What it catches |
|---|----------|----------------|
| 1 | **Worst case:** What breaks if this step fails or the assumption is wrong? | Blast radius |
| 2 | **Scope:** Does the command/change affect only what's intended? Are adjacent systems protected? | Scope creep |
| 3 | **Recoverability:** Is there a snapshot/backup/rollback before every irreversible operation? | Unrecoverable state |
| 4 | **Wording vs. implementation:** Does the plan promise something the code doesn't enforce? | False confidence |

---

## Section 1: Destructive Operations

- [ ] Every `git rm`, `git reset`, `DROP TABLE`, `rm -rf`, force-push, or equivalent has a **preflight snapshot** immediately before it
- [ ] The snapshot is **timestamped** and the restoration procedure is documented or self-evident
- [ ] Destructive commands include **explicit path arguments** — never broad globs or repo root when a subdirectory is the actual target
- [ ] Adjacent systems (other repos, services, databases) that share the target directory or namespace are **explicitly excluded by name**
- [ ] If a snapshot is skipped (low-risk judgment call), the reasoning is documented in the plan

**Principle: Reversible over irreversible. Create a checkpoint before every overwrite.**

---

## Section 2: Scope Containment

- [ ] The narrowest possible path/scope is used for every operation — if you only mean `"PKA testing/"`, the command says `"PKA testing/"`, not `.`
- [ ] The plan names every adjacent system that could be affected and confirms it won't be
- [ ] Side effects on shared state (indexes, registry, database schemas) are identified and isolated
- [ ] If the plan says "this only affects X," there is a verification step that confirms X is the only thing affected after execution

**Principle: Exact scope over broad scope. The path must be as narrow as the intent.**

---

## Section 3: Timeouts, Thresholds, and Limits

- [ ] Every timeout, budget, or threshold is **calibrated to observed runtime** — not to a round number that "sounds reasonable"
- [ ] If a process already runs beyond the proposed timeout under normal operation, the timeout will not be used as-is
- [ ] Stale-lock and session-expiry logic handles the case where the owning process is still alive but slow (not just dead)
- [ ] Budget overruns degrade gracefully — they skip or warn, they do not crash or corrupt
- [ ] New performance-sensitive operations have a circuit breaker: if they run long, they exit cleanly and the system continues

**Principle: Observable behavior over assumptions. Calibrate to measured reality.**

---

## Section 4: Generated Files and Exit Codes

- [ ] Every file described as "generated, not committed" appears explicitly in `.gitignore`
- [ ] The `.gitignore` entry includes a comment explaining why the file is generated (prevents future confusion)
- [ ] Warning-only outputs **exit with code 0** — non-zero exits are reserved for blocking failures
- [ ] The plan does not say "don't commit X" without a corresponding `.gitignore` enforcement
- [ ] If a file's source-of-truth status is ambiguous (generated vs. edited by hand), the plan resolves the ambiguity

**Principle: Declarations without enforcement create drift. If it's generated, gitignore it.**

---

## Section 5: Metrics and Computed Outputs

- [ ] Every metric, score, rate, or percentage includes a **sample-size qualifier** in its definition
- [ ] There is a defined minimum sample threshold below which the metric is suppressed or labeled "low sample"
- [ ] Low-sample outputs show **raw counts only** — no percentages, no trends, no "GO/NO-GO" that would appear precise
- [ ] The threshold is documented in the code, not just in the plan
- [ ] The plan does not present a 1-task "trend" or a 1-task "rate" as meaningful signal

**Principle: Statistically honest over impressive. Small samples get qualifiers, not fake precision.**

---

## Section 6: Portability and Hardcoded Values

- [ ] No paths, folder names, or environment values are hardcoded where a computed equivalent is available
- [ ] Portability checks validate **relationships** (workspace root == git root) not **literals** (git root == "PKA testing")
- [ ] If the repo is renamed or cloned to a different path, all checks still pass without modification
- [ ] Environment-specific values (ports, hosts, paths) are injected from configuration, not baked into logic

**Principle: Validate relationships, not literals. Portable systems survive renaming and migration.**

---

## Section 7: Final Acceptance Gate

Before marking the plan READY FOR EXECUTION, confirm all five core principles are satisfied:

- [ ] **Reversible:** No irreversible operation without a documented checkpoint
- [ ] **Scoped:** Destructive commands target the narrowest possible path
- [ ] **Calibrated:** Timeouts and thresholds reflect observed runtime, not intuition
- [ ] **Enforced:** Generated files are gitignored; warning outputs exit 0
- [ ] **Honest:** Metrics are qualified by sample size when below meaningful threshold

If any box is unchecked, the plan returns to the authoring agent with specific gap descriptions.
"Probably fine" is not an acceptable answer. Either fix it or document why it doesn't apply.

---

## How to File a Finding

When a gap is found, document it in this format:

```
Finding: [short label]
Step affected: [plan section/step number]
Original wording: [exact quote from plan]
Gap: [what could go wrong and why]
Principle violated: [which of the 5 principles]
Recommended fix: [specific change to the plan or implementation]
```

This format was established from the v0.7.0 review. See `Owner's Inbox/REVIEW-METHODOLOGY-LEARNING-v070.md`
for the full retrospective with all 7 findings documented end-to-end.

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-02 | Initial version — derived from v0.7.0 skeptic review retrospective |
