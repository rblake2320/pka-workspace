# Council Debate: Auto-Gap-Response Feature
**Date**: March 28, 2026 | **Participants**: 13/13 agents | **Format**: Group chat, Spark-1

---

## The Question
Should agents automatically trigger a background researcher (NOVA) + skill writer (SCRIBE) the moment they hit something unknown?

---

## Full Council Positions

| Agent | Vote | Core Argument |
|-------|------|---------------|
| **FORGE** | ✅ YES (conditional) | Feels the gap pain most — wants NOVA running parallel, but scoped query, staging buffer, pull-at-decision-gate not mid-stride interrupt |
| **VENTURE** | ✅ GO (conditional) | Compounding flywheel asset — requires confidence threshold to prevent NOVA spam on every minor uncertainty |
| **RADAR** | ✅ BUILD IT | Genuinely novel — individual self-extending agents exist, but shared-library inheritance across a specialist team is not implemented anywhere in the wild. Worth building, worth claiming |
| **NOVA** | 🔄 NO to proposal, YES to queue | Auto-spawn as reflex produces shallow research. 3 simultaneous gaps = 3 shallow dives instead of 1 deep one. Needs prioritized queue batched by AXIOM |
| **SENTINEL** | 🔄 CONDITIONAL HOLD | Auto-trigger creates unreviewed sub-chain influencing live builds with no validation gate. Agents learn to outsource gaps instead of knowing their domain. Hard gates required |
| **SPARK** | 🔄 ACCEPT (modified) | Auto-research produces the average of available sources — not sufficient for creative work. Auto-generated creative skills flagged as DRAFT, SPARK reviews before library promotion |
| **LEGAL** | 🔄 NOT A KILL (structured) | Two risks: (1) provenance/derivative works when SCRIBE encodes external sources into persistent skills, (2) removes human review buffer in regulated domains. Requires source logging, domain blocklist, SENTINEL gate |
| **HELM** | 🔄 DECLARED GAP-PAUSE | Auto-spawning corrupts the dependency graph — undeclared mid-task dependencies HELM never sequenced. Proposed model: agent signals HELM → HELM suspends task → schedules NOVA+SCRIBE as first-class items → resumes after validation |
| **SCRIBE** | ❌ NO to auto-spawn | The deliberate/pressure distinction is a load-bearing wall vs drywall — they look the same until something depends on them. Auto-filling library creates technical debt that appears to work most of the time — worst kind |
| **CRUCIBLE** | ❌ NO auto-trust | Gap-response loop only safe if mandatory validation gate between SCRIBE output and production. Auto-generating skills without smoke test = shipping untested code path. Demanded quarantine as precondition |
| **DEBUGGER** | ❌ AGENT-TRIGGERED only | Auto-spawn mid-investigation is a context-switch bomb injecting noise when signal is needed. "An interruption model dressed up as an assistance model." Agent decides when NOVA pull is relevant, not the system |
| **GRID** | ❌ FAILS AT SCALE | 20% gap rate × 343+ daily tasks = 70+ unplanned concurrent spawns. No shared gap registry = redundant spawns + conflicting skill versions. Required: rate limiting, gap fingerprint dedup, skill versioning |

---

## What The Council Rejected

The original proposal — **hair-trigger auto-spawn on any uncertainty signal** — was rejected 9 to 3 (with 4 conditional approvals that effectively require a redesign).

Key failure modes identified:
- Plan corruption (HELM)
- Context-switch noise during debugging (DEBUGGER)
- Scale collapse without dedup (GRID)
- Shallow research quality (NOVA)
- Untested skills in library (CRUCIBLE, SCRIBE)
- Legal exposure from auto-encoding external sources (LEGAL)

---

## What The Council Approved: The Revised Architecture

The underlying need is **real and novel**. The council converged on a different architecture:

### Gap Queue + HELM Scheduling Model

```
Agent hits unknown
        ↓
Agent DECLARES gap explicitly (not system-detected)
        ↓
Gap logged to shared registry (with fingerprint dedup)
        ↓
AXIOM batches + prioritizes queue
        ↓
HELM schedules NOVA as first-class plan item (not background)
        ↓
NOVA researches → feeds SCRIBE
        ↓
SCRIBE writes skill → QUARANTINE (staging, not live library)
        ↓
CRUCIBLE validates → SENTINEL approves
        ↓
Skill promoted to library (status: PENDING → 3 uses → ACTIVE)
```

### Required Controls (non-negotiable per council)
1. **Confidence threshold** — minimum severity before gap enters queue (VENTURE)
2. **Agent-declared signals** — not string-matched on language (DEBUGGER)
3. **Shared gap registry with fingerprint dedup** — no duplicate NOVA spawns (GRID)
4. **Rate limiting** on concurrent NOVA instances (GRID)
5. **Quarantine layer** — all SCRIBE outputs land in staging, never directly in live library (CRUCIBLE)
6. **CRUCIBLE smoke test + SENTINEL approval** before library promotion (CRUCIBLE, SENTINEL)
7. **Source logging** for every SCRIBE skill — provenance tracked (LEGAL)
8. **Domain blocklist** for regulated/sensitive areas requiring human review (LEGAL)
9. **Skill versioning** — no overwrite without version bump (GRID)

---

## AXIOM Recommendation

**Build the Gap Queue + HELM Scheduling model. Do not build the auto-trigger model.**

The original proposal is plan corruption. The revised model is a genuine capability upgrade.

RADAR's assessment: this pattern — **coordinated multi-agent shared-library self-improvement with structured validation gates** — does not appear to be implemented anywhere in production multi-agent frameworks (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK). It is novel IP, buildable on current infrastructure, and the quality control layer the council demands is itself the moat.

**Estimated build scope** (FORGE + SCRIBE + HELM):
- Gap registry (SQLite, gap fingerprinting, dedup) — 1 day
- Agent gap-declaration protocol (standard signal format) — half day
- HELM scheduling integration — 1 day
- SCRIBE quarantine + promotion pipeline — 1 day
- CRUCIBLE smoke test harness for skill validation — 1 day
- **Total: ~4-5 days**

---

*Full debate thread: `~/ai-business/shared/chat/20260328_14xxxx_*.md` on Spark-1*
