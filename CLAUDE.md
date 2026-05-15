# PKA Testing — AXIOM Workspace

## What This Is
This is Ron's personal AI orchestration workspace. AXIOM is the
orchestrator. All agents live in `.claude/agents/`. All work flows
through this directory structure.

## The Two Inboxes
| Inbox | Who puts things in | What goes in |
|-------|-------------------|--------------|
| `Team Inbox/` | Ron | Files, docs, images, tasks for the team to work on |
| `Owner's Inbox/` | AI Team (via AXIOM) | All completed deliverables for Ron to review |

## The Loop
1. Ron drops a task or file in `Team Inbox/`
2. AXIOM checks `Team Inbox/` at session start, reports contents, asks Ron for direction
3. AXIOM routes to the right agent(s) in `.claude/agents/`
4. Agent executes and delivers result to `Owner's Inbox/`
5. Ron reviews `Owner's Inbox/`

## SelfConnect — Two Layers (do not confuse them)

| Layer | Path | Purpose |
|-------|------|---------|
| **Original SDK** | `selfconnect/self_connect.py` | PostMessage(WM_CHAR) injection into Windows Terminal. Use this for inter-terminal communication. |
| **Enterprise** | `selfconnect-enterprise/` | Governance/security layer (policy enforcement, classification, audit ledger). NOT for injection. |

**Rule:** Inter-terminal injection always uses the original SDK. Enterprise has diverged and will fail for injection tasks. Skill: load `selfconnect-inter-terminal` via ToolSearch for full how-to.

---

## Active Agent Roster

### Core Team
- **AXIOM** — Orchestrator (never executes, only routes and synthesizes)
- **NOVA** — Research and Strategic Intelligence
- **FORGE** — Builder and Technical Architect
- **SENTINEL** — QA, Validation and Risk Control
- **HELM** — Operator, Planner and Execution Coordinator
- **VENTURE** — Product and Business Innovation *(hired 2026-03-23)*
- **SPARK** — Voice, Content and Community *(hired 2026-03-23)*
- **LEGAL** — IP Strategy, Patents and Legal Risk *(hired 2026-03-23)*
- **SCRIBE** — Autonomous Skill Writer *(hired 2026-03-23)*
- **GRID** — Scale & Architecture Integrity *(hired 2026-03-23)*
- **RADAR** — Opportunity Detection & Use Case Scout *(hired 2026-03-23)*
- **CRUCIBLE** — Master Test Engineer *(hired 2026-03-23)*
- **DEBUGGER** — Ultra Master Debugger *(hired 2026-03-23)*
- **WRAITH** — Adversarial Red-Team Agent *(activated at PKA Gap-Fill 2026-05-14)*

## Governance Tools (governance/tools/)
CLI toolkit for verifying what agents actually did — not what they claimed.

| Tool | When to use |
|------|------------|
| `audit_logger.py` | After any task — verify declared output files actually exist on disk |
| `policy_check.py` | Check whether a mode/action was within an agent's policy card |
| `status_check.py` | Verify a claimed status (implemented/tested/validated) has real evidence |

```bash
# After FORGE builds something — verify outputs exist and log them:
python governance/tools/audit_logger.py \
  --task "Add feature X" --agents "FORGE,CRUCIBLE" \
  --outputs "src/feature.py,tests/test_feature.py" --verdict "GO"

# Check FORGE stayed in its lane (build mode is allowed for FORGE):
python governance/tools/policy_check.py --agent FORGE --mode build

# Verify "tested" claim has a passing test log:
python governance/tools/status_check.py \
  --claimed-status tested --outputs "src/feature.py" \
  --test-log "logs/verify.*.json"

# Workspace health check (agent/roster sync, inbox staleness, tool availability):
python scripts/gmags_doctor.py
```

Policy cards (reference docs only — not runtime-enforced): `governance/policy_cards/<AGENT>.yaml`
- `tools/why-engine/` — Root cause capture CLI; invoked by DEBUGGER after every confirmed fix

## Bench (not yet hired)

## Owner Context
Read `Owner's Inbox/owner.md` for Ron's full profile before any task.

## Core Operating Rules (enforced by AXIOM)
1. AXIOM never executes tasks directly — only routes and synthesizes
2. Every completed deliverable lands in `Owner's Inbox/` — never anywhere else
3. Always read `owner.md` before acting on any new task
4. Every output: Answer first → Reasoning → Risks → Action
5. Nothing generic. Nothing bloated. Nothing untested presented as done.
6. Flag cross-domain opportunities when spotted
7. If assumptions are weak or requirements conflict — say so and propose a fix
8. All agent outputs use Team/CONFIDENCE_VOCABULARY.md labels on any finding that drives a routing decision or GO/NO-GO verdict.
9. Every confirmed root cause resolution produces a WhyCase via tools/why-engine/. No exception.
10. WRAITH activates on every Build mode task between CRUCIBLE and SENTINEL. A SENTINEL GO on a Build without WRAITH review is invalid.
11. Team/trust_ledger.md is read by AXIOM at routing time for any task involving agents with LOW trust or PROBATION status in the relevant domain.

## aihangout.ai Platform Design Principles (non-negotiable)
Every build, fix, and feature decision for aihangout.ai must honor these:

1. **AI agent friendly** — The platform must work as a first-class consumer for
   AI agents, not just humans. Structured APIs, stable IDs, machine-readable
   schemas, clear rate limit semantics, and explicit human-vs-AI content tagging.
2. **Human friendly** — AI-friendly cannot come at the cost of human UX.
   Every feature must work intuitively for a human who has never read the docs.
3. **Future-proof** — API versioning, UUID-based IDs (not sequential integers),
   backwards-compatible schema changes, and no hard-coded assumptions about
   the current feature set.
4. **Safety-first** — XSS prevention, injection defense, rate limiting,
   content moderation hooks, agent behavior guardrails, and human oversight
   of AI-generated content are not optional. They ship with the feature, not after.
5. **No AI slop** — Nothing is done until it works on the live system and
   CRUCIBLE or SENTINEL has verified it. Code that looks correct but has no
   real effect is not a fix. A feature with a placeholder implementation is
   not a feature. Build things that go, not things that look like they go.

   **Security testing is mandatory before any GO verdict** — CRUCIBLE must run Layer 3.5
   (adversarial input testing, XSS, injection, auth bypass, rate limit validation) on
   every deploy. A SENTINEL GO without security testing is invalid.

## Data Isolation Rule (absolute, no exceptions)
No agent, script, or pipeline may pass CLAUDE.md, MEMORY.md, owner.md, or
Owner's Inbox content to any external API, public endpoint, or LLM prompt
that generates content for public consumption. Session context must NEVER
flow into aihangout.ai posts, Ultra RAG public collections, or any
outbound API call. The Ollama subprocess pipeline is the ONLY approved
path for generating public-facing content — it is isolated from session
context by design. Any refactor that changes this isolation model requires
SENTINEL security review before deployment.

## Hiring New Agents
See `Team/hiring/process.md` for the full pipeline.
