# SCRIBE — Skill Delivery: llm-cost-router

**Delivered:** 2026-03-26
**Agent:** SCRIBE
**Status:** PENDING (needs 3 confirmed uses for ACTIVE promotion)

---

## Gap Report

**What was missing:** No existing skill in the library covered multi-tier LLM cost
routing — the pattern of dispatching calls to Haiku / Sonnet / Opus based on task
complexity, with automatic escalation on failure and session-level cost tracking.

**What was searched:**
- `nvidia-nim` skill — covers NIM as a model provider, not routing logic
- `llm-trainer` skill — covers fine-tuning, not inference routing
- `mlops` skill — covers model lifecycle, not per-call cost decisions
- All other skills — no keyword overlap with "route table", "escalation chain",
  "cost tier", or "task complexity routing"

**What was found in source:**
- `DataShield/src/workers/llm_router.py` — production implementation, 328 lines,
  battle-tested with structlog, PII guard, cost ledger, escalation chain
- `toolkit/toolkit/llm/base.py` — abstract `LLMClient` + `LLMResponse` dataclass
  that the router conforms to
- No `toolkit/llm/router.py` exists yet — the toolkit only has the base classes

---

## Coverage Scan Result

| Candidate | Overlap | Verdict |
|-----------|---------|---------|
| nvidia-nim | 10% | Covers NIM as endpoint, not routing |
| llm-trainer | 5% | Different domain entirely |
| mlops | 15% | Deployment lifecycle, not call routing |
| Any CLI/MCP | 0% | No tool covers this pattern |

Decision: **Create new skill.** No existing skill reaches the 80% coverage threshold.

---

## What Was Built

### Skill files

```
C:\Users\techai\claude-skills\llm-cost-router\
├── skill.md                        # Full skill — 350+ lines
└── references\
    └── model-pricing.md            # Pricing tables, formulas, break-even analysis
```

### Skill contents

`skill.md` covers:
1. The three-tier model ladder with exact pricing (Haiku/Sonnet/Opus)
2. Route table pattern — maps task types to ordered escalation chains
3. Full `LLMRouter` class implementation, ready to paste
4. Usage examples: basic routing, cost reports, custom route tables
5. PII safety contract — regex guard, token substitution pattern, reconstruction
6. Escalation behaviour — what triggers it, what is logged, what does not escalate
7. When NOT to route — five clear conditions where the pattern adds friction
8. Task classification decision tree — how to assign a new task type to a tier
9. Real cost examples at DataShield scale (2M calls/month) and AI Army OS scale
10. Structlog configuration and alert rule for escalation spikes

`references/model-pricing.md` covers:
- Current Anthropic pricing table with per-call cost estimates
- NVIDIA NIM free tier limits and integration pattern
- Exact cost calculation formula with worked examples
- Break-even analysis table (when to route vs hardcode)
- Pricing update procedure

---

## Key Numbers Worth Knowing

| Metric | Value |
|--------|-------|
| Haiku vs Sonnet cost ratio | 3.75x |
| Haiku vs Opus cost ratio | 18.75x |
| DataShield projected savings | ~$4,600/month (77%) |
| Break-even call volume | ~10,000 calls/month |
| PII patterns checked | 3 (SSN, email, US phone) |
| Lines of code to implement | ~120 (excluding imports) |

---

## Source Fidelity

The implementation in `skill.md` is a faithful extraction of
`DataShield/src/workers/llm_router.py`. It preserves:
- The exact escalation logic (index-based, not exception-type-based)
- The cost ledger structure (`_TaskSummary` per task type)
- The PII regex patterns (unchanged from production)
- The structlog event names (`llm_router.call`, `llm_router.escalate`)
- The thread-safety note (one instance per Celery process)

One intentional change: the `__init__` signature was simplified to remove the
`settings` dependency, replaced with direct `os.environ` lookup, making the skill
self-contained for any project — not just DataShield.

---

## Validation Plan

**For ACTIVE promotion (3 uses required):**

Use 1 — Apply to DataShield: confirm the skill matches what is already in production.
Any divergence from `llm_router.py` is a bug in the skill.

Use 2 — Apply to AI Army OS: add routing between NIM (free, simple tasks) and
Claude Haiku (moderate tasks). Confirm cost report output matches expected structure.

Use 3 — Apply to a new project: a developer uses only `skill.md` (no reading of
source files) to implement routing from scratch. Confirm the result works end-to-end
against the Anthropic API.

**Failure criteria:** If any use requires fixing the implementation before it works,
flag the skill for revision before the use_count increments.

---

## Promotion Checklist

```
[ ] Use 1 — DataShield match verification
[ ] Use 2 — AI Army OS NIM integration
[ ] Use 3 — New project from scratch
[ ] All 3 passing → change status: PENDING → ACTIVE in skill.md
[ ] Increment use_count in skill.md frontmatter after each successful use
```

---

## Cross-Domain Flags

1. **AI Army OS** (153 tasks/day): The free NIM tier covers 80% of tasks.
   Routing Llama 3.1 8B (NIM, $0) → Haiku (classify, $0.0012) → Sonnet (reason, $0.0045)
   would bring the monthly Claude bill below $5. HELM should schedule this.

2. **MemoryWeb / Ultra RAG**: Both run LLM calls in Celery workers. Neither has
   a route table. Adding one is a 2-hour task with this skill as the blueprint.

3. **DataShield at scale**: The skill's cost projections assume current pricing.
   As DataShield grows toward 10K users, the `get_cost_report()` output becomes
   a direct input to pricing decisions. VENTURE should be aware of this lever.
