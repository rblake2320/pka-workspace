# SCRIBE Deliverable — background-researcher Skill

**From**: SCRIBE — Autonomous Skill Writer
**To**: Owner's Inbox
**Date**: 2026-03-26
**Status**: PENDING (requires 3 successful uses to promote to ACTIVE)

---

## What Was Created

Two files installed at `C:\Users\techai\claude-skills\background-researcher\`:

| File | Purpose |
|------|---------|
| `skill.md` | The full skill — trigger logic, 5 agent templates, execution pattern, output standards |
| `references/research-domains.md` | Catalog of Ron's 8 active domains with search terms, competitors, regulators, signal sources |

---

## Gap Report

**What was missing**: No existing skill covered the pattern of spinning
up parallel research agents at session start, running them in background
without blocking conversation, and delivering signal-first intel to
Owner's Inbox.

**What was searched**: 6 skills matched at low relevance (33-50%).
The closest, `multi-agent-orchestration`, covers agent design patterns
but contains nothing on research agent templates, domain catalogs,
auto-trigger logic, or Owner's Inbox delivery protocols.

**Decision**: CREATE new skill. No existing skill covered the domain at
80%+ threshold. No CLI, MCP, or SDK covers this pattern either.

---

## What the Skill Does

When triggered (explicitly or automatically), the skill guides Claude to:

1. Read `owner.md` and session context to identify active domains
2. Select the right research agent templates (up to 5)
3. Launch all agents in a single message, all in background
4. Continue the main conversation immediately
5. Surface results at the next natural pause — or interrupt if a
   🔴 Act Now signal is found

---

## The 5 Agent Templates

| # | Template | When to Use |
|---|----------|-------------|
| 1 | AI/ML Weekly Sweep | Every session (if not run in last 48 hours) |
| 2 | Competitive Intelligence | When primary project is in active build/launch phase |
| 3 | Technology Landscape | Before committing to building a capability |
| 4 | Regulatory/Compliance Scan | For GovTech, privacy, fintech, defense domains |
| 5 | Cross-Project Opportunity | Once per session — portfolio-level pattern detection |

---

## How to Use It

### Invoke explicitly:
Say any of these trigger phrases in any session:
- "Run a research sweep"
- "What's new in [domain]?"
- "Intel sweep before we start"
- "Background researcher"
- "Stay current on [topic]"

### Auto-triggers (no command needed):
Claude will launch automatically when:
- Session starts with 3+ active projects in context
- A new domain is introduced Ron hasn't researched recently
- Ron says "deploy," "launch," or "ship" for a project with no
  recent competitive intel
- Ron is about to build something — pre-build tool scan fires first

### What comes back:
Reports land in `C:\Users\techai\PKA testing\Owner's Inbox\` named:
- `NOVA-aiml-weekly-sweep-YYYYMMDD.md`
- `NOVA-competitive-[project]-YYYYMMDD.md`
- `NOVA-tech-landscape-[capability]-YYYYMMDD.md`
- `NOVA-regulatory-[domain]-YYYYMMDD.md`
- `NOVA-cross-project-opportunity-YYYYMMDD.md`

Every report uses the 🔴/🟡/🟢 signal format. Act Now items surface
first. Sources cited for every finding.

---

## The 8 Domains Cataloged

`references/research-domains.md` covers these domains with full detail
(search terms, competitors, regulators, signal sources):

1. AI Agents & Multi-Agent Systems
2. RAG / Search / Knowledge Systems
3. Privacy Tech & Zero-Knowledge Systems
4. GovTech / Defense / IMDS
5. Browser Automation & Test Engineering
6. LLM Training & Fine-Tuning
7. AI Community & Social Platforms
8. Infrastructure & MLOps

---

## Promotion Criteria

Skill is currently PENDING. Promote to ACTIVE after 3 uses where:

- Agents launched in parallel without blocking conversation
- At least one report landed in Owner's Inbox correctly formatted
- Output followed 🔴/🟡/🟢 signal-first format
- Ron acted on or acknowledged a finding

To promote: update `status: PENDING` to `status: ACTIVE` in skill.md
frontmatter and increment `use_count`.

---

## Risks

- **Context budget**: 5 agents per sweep is the hard cap. Each agent
  uses context. More than 5 in parallel risks degraded output quality
  or timeouts.
- **Weak web sources**: NOVA is instructed to flag thin data explicitly.
  If a finding has a weak source, the report will say so in Research
  Gaps — trust the flag.
- **Data isolation**: The skill explicitly prohibits passing CLAUDE.md,
  MEMORY.md, or owner.md into external API calls. Research agents query
  public web sources only. Session context never flows out.
- **Staleness**: The 48-hour re-sweep block prevents redundant agent
  launches but means a fast-moving domain could have a 48-hour gap.
  Override by saying "fresh sweep on [domain]."

---

## What SCRIBE Did Not Build

- No MCP integration (researched — no existing MCP covers parallel
  research agent coordination with Owner's Inbox delivery)
- No automation script — this skill operates through Claude's native
  Agent tool pattern, no external tooling required
- No scheduler — auto-trigger is session-start logic, not cron-based.
  A persistent scheduler would require a separate infrastructure skill.
