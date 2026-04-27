# Review Methodology Learning — v0.7.0 Skeptic Review Retrospective
# Prepared for: Ron | Date: 2026-04-02 | Author: SENTINEL via AXIOM

---

## What This Document Is

The SENTINEL skeptic review of the v0.7.0 plan raised 7 issues. All 7 were absorbed into
the plan before implementation. This document captures **how the review worked**, **why it
caught what it caught**, and **how to make it repeatable**.

This is a process-learning document, not a code document. The goal is to turn a one-time
review into a team capability.

---

## How the Review Worked — The 4-Question Filter

The skeptic review applied a consistent filter to every gap in the plan. It is not clever.
It is mechanical and relentless.

| # | Question | What it catches |
|---|----------|----------------|
| 1 | What's the worst case if the assumption is wrong? | Blast radius |
| 2 | What can it break if executed as written? | Scope creep |
| 3 | What proof or safeguard is missing? | Recoverability |
| 4 | Is the wording tighter than the implementation? | False confidence |

The plan already did the inventing. The review's job was to find where the plan could hurt you.
Every finding came from applying one of these four questions to a specific step.

---

## The 7 Findings — Full Chain

### Finding 1: Parent-repo cleanup too broad

**Original plan said:** `git rm -r --cached` from `C:\Users\techai\` — implied it would clean "parent repo"

**Skeptic caught:** Council files are also tracked in the parent repo. A broad `git rm` could
mutate council's index too. Council has its own healthy `.git` — touching it from the parent
is not our problem.

**Question applied:** *What can it break if executed as written?*

**Principle: Exact scope over broad scope.** When a destructive command accepts a path argument,
the path must be as narrow as possible.

**Resolution:** Step 9 was rewritten to explicitly target only `"PKA testing/"`. Council was
excluded by name. The commit message and REPO_ALIGNMENT.md both document the scope.
Verification: `git ls-files "council/"` still returns 6 tracked files — untouched.

---

### Finding 2: No preflight snapshot before force-push

**Original plan said:** Force-push to pka-workspace (required because no common ancestor)

**Skeptic caught:** `--force` without a just-before snapshot is trusting memory. If the remote
had unexpected content, it's gone forever.

**Question applied:** *What proof or safeguard is missing?*

**Principle: Reversible changes over irreversible ones.** Before any overwrite, create a
checkpoint you can restore from without asking anyone.

**Resolution:** Step 7 added: `git ls-remote origin` to log refs, then `git clone --bare`
to create `pka-workspace-backup.git`. The backup exists at
`C:\Users\techai\pka-workspace-backup.git`, timestamped 1 minute before the force-push.

---

### Finding 3: Telemetry needs runtime budget

**Original plan said:** Add telemetry as operator step 7 (all sections run sequentially)

**Skeptic caught:** The operator pipeline already takes significant time. If telemetry grows
expensive (more JSONL files, more tasks), it could slow the entire pipeline with no degradation
path.

**Question applied:** *What's the worst case if the assumption is wrong?*

**Principle: Runtime trust over feature count.** A feature that makes the system slower without
a circuit breaker is a liability, not an improvement.

**Resolution:** `SECTION_BUDGET_S = 3.0` — each of the 8 sections is individually timed.
If any section exceeds 3s, its output is replaced with `[TIMING] Skipped | took Xs, budget is 3.0s`.
The section header is preserved so you know what was skipped. Exit code stays 0 regardless.

---

### Finding 4: 120s stale lock too aggressive

**Original plan said:** Break stale locks after 120 seconds

**Skeptic caught:** `pka_full_validation.py` already runs well beyond 100 seconds. If the same
FileLock is used broadly, 120s would break valid locks during legitimate long-running work.
"Don't convert recovery into corruption."

**Question applied:** *Is the wording tighter than the implementation?*

**Principle: Observable behavior over assumptions.** The timeout must be calibrated to what
actually runs under the lock, not to what sounds reasonable in the abstract.

**Resolution:** `STALE_SECONDS = 300` (5 minutes). Additionally, a PID liveness check was added
using `ctypes.windll.kernel32.OpenProcess` — if the owning process is dead, the lock is broken
immediately regardless of age. The check is dual-condition (age OR dead PID) rather than
age-only.

---

### Finding 5: RESUME.json needs .gitignore entry

**Original plan said:** "generated, not committed" — but didn't enforce that anywhere

**Skeptic caught:** If a generated file isn't gitignored, it creates false diffs, repo noise,
and ambiguous truth sources. Saying "don't commit it" is a policy; gitignoring it is enforcement.

**Question applied:** *Is the wording tighter than the implementation?*

**Principle: Declarations without enforcement create drift.** If you say a file is generated,
the tooling must treat it that way. Otherwise the next `git add .` commits it.

**Resolution:** `.gitignore` explicitly lists `Team/tasks/RESUME.json` with a comment:
"Machine-generated session resumption manifest — rebuilt on every start/end."

---

### Finding 6: Agent Velocity overstates signal on small data

**Original plan said:** Compute median time-to-delivery and GO-rate trends per agent

**Skeptic caught:** Most agents have 1-2 completed tasks. Computing a "GO rate" from 1 task
(100% or 0%) creates fake certainty. The number looks precise but is statistically meaningless.

**Question applied:** *What's the worst case if the assumption is wrong?*

**Principle: Statistically honest outputs over impressive-looking outputs.** A metric with a
weak sample should say so, not hide behind a precise-looking percentage.

**Resolution:** `MIN_TASKS_PER_AGENT = 5`. Below that threshold, the output shows only raw
counts with "(low sample | trend needs 5+ completed)". GO rate is suppressed entirely.
Above the threshold, the full metric is shown.

---

### Finding 7: Doctor git check should be portable

**Original plan said:** Verify git root is `PKA testing/`

**Skeptic caught:** Hardcoding a folder name works locally but breaks if the workspace is
cloned elsewhere or renamed. The invariant should be "workspace root equals git root,"
not "git root equals this specific path."

**Question applied:** *What can it break if executed as written?*

**Principle: Validate relationships, not literals.** Portable systems check that two things
are the same, not that one thing equals a hardcoded value.

**Resolution:** `check_git_boundary()` compares `git rev-parse --show-toplevel` against
`ROOT`, where `ROOT = Path(__file__).resolve().parent.parent`. No hardcoded path strings
anywhere. Works on any machine.

---

## The 5 Underlying Principles

All 7 findings trace back to 5 principles. These are the skeptic's actual operating criteria.
They are defensive, not inventive.

| # | Principle | What it guards against |
|---|-----------|----------------------|
| 1 | **Reversible over irreversible** | Unrecoverable state after a mistake |
| 2 | **Exact scope over broad scope** | Collateral damage to adjacent systems |
| 3 | **Observable behavior over assumptions** | Timeouts calibrated to intuition, not reality |
| 4 | **Declarations with enforcement** | Policies that say one thing, tooling that does another |
| 5 | **Statistically honest over impressive** | Fake precision from small samples |

These are not novel. The reason they catch real problems is that they are applied systematically
to every step, not just to steps that look risky. Finding 7 (hardcoded path) does not look risky.
Finding 5 (gitignore) does not look risky. The filter catches them because it asks the same
questions regardless of how safe a step appears.

---

## What Makes This Repeatable

### The mechanism

The skeptic review is not a personality — it is a procedure. Any agent can run it by applying
the 4-question filter to every plan step. The filter does not require domain expertise. It
requires willingness to imagine the plan failing and ask: what breaks?

### The timing

The review runs **after** the plan is written, **before** execution begins. This is the only
window where findings are cheap. A finding at plan-review time costs a sentence. The same
finding at execution time costs rollback, debugging, or data loss.

### The output format

Every finding is documented as:
- Original wording (exact quote from plan)
- Gap (what could go wrong and why)
- Principle violated (which of the 5)
- Recommended fix (specific change)

This format prevents vague findings that generate debate instead of action.

### The standard

The checklist is at `Team/SENTINEL/pre-implementation-checklist.md`. It encodes the 4-question
filter and the 5 principles into checkable items. Run it against any plan before marking
READY FOR EXECUTION.

---

## Self-Test: Would This Checklist Have Caught All 7?

| Finding | Checklist section | Would it catch it? |
|---------|------------------|-------------------|
| 1: Broad git rm | Section 2 (Scope Containment) | Yes — "narrowest possible path" item |
| 2: No backup before force-push | Section 1 (Destructive Operations) | Yes — "preflight snapshot" item |
| 3: No telemetry budget | Section 3 (Timeouts/Thresholds) | Yes — "circuit breaker" item |
| 4: 120s lock too short | Section 3 (Timeouts/Thresholds) | Yes — "calibrated to observed runtime" item |
| 5: RESUME.json not gitignored | Section 4 (Generated Files) | Yes — "gitignore enforcement" item |
| 6: Agent velocity fake precision | Section 5 (Metrics) | Yes — "minimum sample threshold" item |
| 7: Hardcoded path | Section 6 (Portability) | Yes — "validate relationships not literals" item |

**Result: 7/7.** The checklist would have caught all findings from the v0.7.0 review
if applied prospectively. This confirms the checklist is a faithful encoding of the review
methodology, not a post-hoc rationalization.

---

## What This Changes for the Team

1. **SENTINEL** runs the checklist against every plan rated CRITICAL or higher before approval
2. **FORGE and HELM** self-apply the checklist before marking any plan READY
3. **Findings are filed** in the standard format — vague objections without a specific recommended fix are not accepted
4. **The threshold for "probably fine" is zero** — if a step can't pass the 4-question filter, it either gets a fix or the reasoning is documented

The goal is not to slow down execution. The goal is to make findings cheap. A finding at
plan stage costs one conversation turn. A finding at rollback stage costs hours.

---

*Retrospective complete. Checklist at `Team/SENTINEL/pre-implementation-checklist.md`.*
