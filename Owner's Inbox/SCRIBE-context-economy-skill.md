# SCRIBE Delivery — context-economy Skill

**Agent**: SCRIBE — Autonomous Skill Writer
**Date**: 2026-03-26
**Status**: DELIVERED — skill at PENDING, requires 3 successful uses to promote to ACTIVE

---

## Gap Report

**Domain**: Session hygiene, token budget management, context window discipline
**Gap**: No existing skill in the library covers how to prevent token waste from
bloated CLAUDE.md files, bulk skill loading, agent output flooding the main
conversation, or inline credential exposure.

**Searched**:
- All 34 skills in `C:\Users\techai\claude-skills\` — zero at 80%+ relevance
- Docker MCP catalog — unavailable (Docker not running)
- Installed CLIs — none applicable
- Self-learning KB — no entries in this domain

**Closest partial matches (none above 50%)**:
- `soul-keeper` — 50% relevance; covers session state but not token hygiene
- `cli-first-check` — 33% relevance; covers tool selection but not context load discipline
- `audit-trace-bridge` — 33% relevance; covers logging but not context budgeting

---

## Coverage Scan Result

No existing skill, CLI, MCP, or package covers this domain at the 80% threshold.

---

## Decision

**CREATE new skill from scratch.**

Reasoning: This is a recurring operational problem — CLAUDE.md has grown to
200+ lines with completed work logs, inline API keys visible in session context,
and agent outputs pasting into the main conversation. None of the 34 existing
skills address the mechanics of context budgeting. A bridge to an existing tool
is not applicable because the problem is behavioral (load discipline) not tooling.

---

## Skill Artifact

### Files Created

| File | Purpose |
|---|---|
| `C:\Users\techai\claude-skills\context-economy\skill.md` | Main skill — 10 sections covering all hygiene areas |
| `C:\Users\techai\claude-skills\context-economy\references\trim-checklist.md` | Printable start/end checklist + trim procedure |

### Skill Coverage (10 sections)

1. **Token Budget Problem** — table of waste sources with approximate token costs
2. **CLAUDE.md Hygiene Protocol** — what belongs, what does not, trim procedure
   with exact commands and archive path
3. **Skills Loading Protocol** — correct vs wrong load patterns, session budget of ≤3
4. **Agent Output Discipline** — file-first rule, in-conversation summary template,
   200-line threshold
5. **Credential Hygiene** — storage locations table, exposure response procedure
6. **Context Window Checkpoints** — milestone-to-action table
7. **Task-Type Load Guide** — what to load vs skip per task type (8 task types)
8. **Red Flags** — immediate-action triggers with exact responses
9. **Session Start Checklist** — 6-item quick check
10. **Session End Checklist** — 5-item close check

---

## Immediate Impact on Current System

The CLAUDE.md in `C:\Users\techai\CLAUDE.md` is currently far above the 100-line
threshold. Based on session context, it contains:

- Multiple "TODAY'S WORK COMPLETED" logs from August 2025 (6+ months stale)
- An OpenAI API key inline (`sk-proj-4wbTuBPRnjDp...`)
- Full architecture documentation for UltraSecure Email and UltraChat (completed projects)
- Redundant skill tables that duplicate what skills-bridge already serves

**Recommended immediate actions** (in order):

1. Archive current CLAUDE.md to `~/.claude-history/CLAUDE_archive_2026-03-26.md`
2. Remove all "TODAY'S WORK COMPLETED" sections from Aug/Dec 2025
3. Remove the inline OpenAI key — rotate it (it has been in session context)
4. Remove UltraSecure Email and UltraChat architecture sections (move to project docs)
5. Verify CLAUDE.md is under 100 lines

This is flagged as a security action, not just hygiene: the exposed key has been
in session context and should be treated as compromised.

---

## Validation Plan

This skill reaches ACTIVE status after 3 confirmed successful uses:

| Use | Criteria |
|---|---|
| Use 1 | CLAUDE.md trim performed: before > 100 lines, after < 100 lines, no credentials remaining |
| Use 2 | Skills loaded on-demand during a session (not bulk-loaded); ≤3 skills used |
| Use 3 | Agent output routed to Owner's Inbox file instead of pasted into conversation |

Track uses by incrementing `use_count` in `skill.md` frontmatter.

---

## Risks

- **Adoption risk**: This skill only works if the session discipline is actually applied.
  Consider adding a session-start hook that checks CLAUDE.md line count automatically.
- **Archive drift**: `.claude-history/` archives will grow over time and eventually need
  their own cleanup policy. Recommend quarterly purge of archives older than 90 days.
- **Key already exposed**: The OpenAI key visible in the current CLAUDE.md session context
  (`sk-proj-4wbTuBPRnjDp...`) should be rotated regardless of whether this skill is adopted.

---

SCRIBE out.
