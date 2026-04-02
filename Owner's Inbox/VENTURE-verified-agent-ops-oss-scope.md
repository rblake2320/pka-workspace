---
id: VENTURE-verified-agent-ops-oss-scope
date: 2026-04-02
author: VENTURE
status: DELIVERED
task: TASK-20260402-009
topic: verified-agent-ops — OSS v1.0 scope, 2-week sprint, success conditions
---

# verified-agent-ops — OSS v1.0 Scope

---

## 1. What Ships in OSS v1.0

The public repo is a portable process scaffold. It must work on any machine with
Claude Code and Python 3.10+ installed. No Ron-specific paths, credentials,
external services, or project knowledge. Zero external pip dependencies for the
operator layer.

### Files that ship as-is (after scrubbing, see Section 2)

**Process layer (non-negotiable — this is the product):**
- `Team/OPERATING_MODEL.md` — the task lifecycle and validation gate model
- `Team/CORE_RULES.md` — stripped of Ron-specific rules (aihangout design principles, data isolation referencing specific services)
- `Team/MESSAGE_PROTOCOL.md`
- `Team/TASK_BRIEF_TEMPLATE.md`
- `Team/tasks/` — empty directory with a README and one example sanitized task record
- `Team/[AGENT]/journal.md` x 13 — blank templates, not Ron's history
- `Team/status.md` — blank template
- `Team/handoff.md` — blank template

**Agent definitions:**
- `.claude/agents/AXIOM.md` — keep as-is; persona is generic
- `.claude/agents/NOVA.md`, `FORGE.md`, `SENTINEL.md`, `HELM.md`, `VENTURE.md`, `SPARK.md`, `LEGAL.md`, `SCRIBE.md`, `GRID.md`, `RADAR.md`, `CRUCIBLE.md`, `DEBUGGER.md`
- All 13 agent files must be reviewed before publish: strip any reference to Ron's infrastructure (Spark-1/2 IPs, ultrarag.app, specific project names, aihangout.ai platform rules)

**Operator scripts (RADAR's core 5 + full pipeline):**
- `scripts/pka_lib.py` — portable, path-based, no external deps
- `scripts/pka_session_gate.py`
- `scripts/pka_task_cli.py`
- `scripts/pka_sync.py`
- `scripts/pka_scorecard.py`
- `scripts/pka_dream.py`
- `scripts/pka_operator_run.py`
- `scripts/pka_doctor.py`
- `scripts/pka_observability.py`
- `scripts/pka_journal_compact.py`
- `scripts/pka_cost_tracker.py`
- `scripts/pka_proof_dashboard.py`
- `scripts/pka_process_audit.py`
- `scripts/pka_full_validation.py`
- `scripts/pka_resilience_test.py`
- `scripts/pka_e2e_test.py`
- `scripts/pka_post_tool_hook.py`
- `scripts/pka_message_cli.py`
- `scripts/pka_evidence_pack.py`

**Config and structure:**
- `CLAUDE.md` — REWRITTEN as generic (see Section 2)
- `CHANGELOG.md` — keep; version history establishes credibility
- `README.md` — SPARK's draft is the base; tighten the install path
- `.claude/settings.local.json` — REWRITTEN; strip Windows-specific Python path and Ron-specific MCP permissions
- `Owner's Inbox/` — directory with `owner.md` as a blank template and `DELIVERY_MANIFEST.md` as a blank template
- `Team Inbox/README.md` — generic intake instructions
- `logs/` — empty directory with `.gitkeep`
- `.gitignore` — add `logs/session_*.jsonl`, `*.lock`, `__pycache__/`

**Total file count estimate: ~60 files.** This is a scaffold, not a framework. It clones in 30 seconds and runs on first try.

---

## 2. What Stays Out

The following are PKA-specific and must not appear in the public repo:

| Item | Why it stays out |
|------|-----------------|
| `Owner's Inbox/owner.md` (Ron's version) | Personal profile. Replace with a blank template with field prompts. |
| `CLAUDE.md` (current) | Contains Ron's full project registry (50+ projects), Spark-1/2 IPs, GPU specs, PostgreSQL credentials structure, service inventory, Cloudflare tunnel URLs, and aihangout.ai platform design principles. None of this is generic. Needs a full rewrite. |
| `~/.claude/projects/.../MEMORY.md` | Not in the repo — stays out by default. |
| `.claude/settings.local.json` (current) | Hardcodes `C:/Python312/python.exe` and a full absolute path to the hook script. Must be rewritten with `python` (system default) and a relative path. MCP permissions for specific services (skills-bridge, playwright, Cloudflare bindings) must be stripped. |
| All `Owner's Inbox/` deliverables (NOVA-*, FORGE-*, etc.) | Ron's work product. Not useful to a stranger; potentially sensitive. Replace with `DELIVERY_MANIFEST.md` blank template only. |
| `Team/tasks/` existing task records | Ron's specific task history. Strip to empty directory + one example. |
| Agent journal entries (non-blank) | Ron's operational history. Ship all 13 journals as blank templates with the correct heading structure only. |
| `scripts/ai_army_chat.py`, `aihangout_*.py`, `aihangout_bridge.py` | Ron-specific integrations that live in `scripts/` but have no relationship to the process scaffold. Exclude from the repo entirely. |
| `scripts/security/`, `scripts/nvidia-blueprints/`, `scripts/ai-army-telegram-bridge/` | Same — not part of the portable scaffold. |
| `FlowBoard/` | Unrelated UI experiment. Exclude. |
| `.playwright-cli/` | Local test artifacts. Exclude via `.gitignore`. |
| `0`, `=` files | Artifact junk. Exclude. |
| `Team/hiring/` | Internal agent hiring process. Interesting but premature for v1.0 — include in v1.1 if there's community interest in customizing rosters. |
| Any reference to `192.168.12.132`, `10.0.0.2`, `ultrarag.app`, `army.ultrarag.app`, `rblake2320` in agent files | Infrastructure specifics. Find-and-remove pass required before publish. |

**The CLAUDE.md rewrite is the single most important stripping task.** The generic version should contain: owner context fields (blank), agent roster table, the two-inbox model, operating rules (already generic in CORE_RULES.md), and a pointer to `Owner's Inbox/owner.md`. Nothing project-specific.

---

## 3. Target Community

**Primary channel: Claude Code Discord and the r/ClaudeAI subreddit.**

The buyer is someone who already uses Claude Code and has started spinning up subagents with no process around them. That person lives in the Claude Code Discord. They are not on Hacker News first — HN is a second wave play after there are 200+ stars and a strong README.

**Seed post strategy (one sentence):** "I spent a month building a structured process layer for Claude Code subagents — named roles, task lifecycle, GO/NO-GO gates, persistent journals, and an audit trail — and I open-sourced the whole scaffold."

**Where specifically:**
1. Claude Code Discord — #showcase or equivalent channel. Post a short screen recording of `pka_operator_run.py` running the 9-step pipeline to completion. No blog post needed. The script output is the demo.
2. r/ClaudeAI — same post, link to GitHub
3. GitHub README — must mention "works with Claude Code" in the first sentence so it surfaces in relevant searches

Do not post to Hacker News at launch. HN rewards polish and completeness. Post there only after the first 10 outside contributors have opened issues or forks.

---

## 4. The 2-Week Sprint

### Week 1 — Extract and Publish

**Goal: public repo is live, installable, and runs clean on a fresh machine.**

| Day | Task | Owner |
|-----|------|-------|
| 1 | Audit all 13 agent files for Ron-specific content. Flag every line that needs stripping. | SENTINEL pass before FORGE touches anything |
| 1–2 | Rewrite `CLAUDE.md` as generic template. Rewrite `.claude/settings.local.json` with portable hook path. | FORGE |
| 2 | Create blank journal templates for all 13 agents (Self-Model section, Feedback Received section, last-10-entries header — no content). | FORGE |
| 2–3 | Create `Owner's Inbox/owner.md` blank template with field prompts. Create blank `DELIVERY_MANIFEST.md` template. | FORGE |
| 3 | Audit all 19 `scripts/pka_*.py` files: confirm zero hardcoded paths, confirm Python 3.10 compatibility, confirm no external pip deps beyond stdlib. | FORGE |
| 3 | Exclude non-scaffold scripts from repo: remove or `.gitignore` the `ai_army_*`, `aihangout_*`, `security/`, `nvidia-blueprints/`, `ai-army-telegram-bridge/` from the scripts directory. | FORGE |
| 4 | CRUCIBLE runs `pka_e2e_test.py` and `pka_resilience_test.py` on a clean clone in a temp directory with no Ron context. Must pass green. | CRUCIBLE |
| 4 | CRUCIBLE runs `pka_doctor.py` on the clean clone. Doctor must report healthy with no Ron-specific checks failing. | CRUCIBLE |
| 5 | SENTINEL reviews: (a) no personal data in any file, (b) no absolute paths, (c) `.gitignore` covers logs and lock files, (d) hook path is portable. GO required before publish. | SENTINEL |
| 5 | Finalize SPARK's README draft. Add a 60-second quickstart section. Add the 9-step pipeline table. Add a "make it yours" section (edit CLAUDE.md, edit owner.md). | SPARK + FORGE |
| 5 | Push to `rblake2320/verified-agent-ops` on GitHub. License: MIT. | FORGE |

### Week 2 — Seed and Listen

**Goal: first 50 stars, first outside issue or fork, first real user feedback.**

| Day | Task | Owner |
|-----|------|-------|
| 6 | Record a 90-second terminal screen capture: clone → doctor → session_gate start → create task → operator_run. No voiceover needed. | Ron or FORGE |
| 6–7 | Post to Claude Code Discord with screen capture and one-sentence framing. Post to r/ClaudeAI. | Ron |
| 7–10 | Monitor issues and discussions. Do not over-respond. Answer technical questions only. Note every pain point as a signal. | Ron (passive) |
| 8 | If any user asks "can I swap out the agents for my own?", that is the signal to start drafting the v1.1 customization guide. Do not build it yet. | RADAR monitors |
| 10 | Run `pka_scorecard.py` on the public repo as if it were a new user's workspace. Score should be 90+/100 from a fresh clone. If not, fix what failed. | CRUCIBLE |
| 10–14 | VENTURE reviews engagement data: stars, forks, issue types, questions in Discord. Write a one-page Go/No-Go memo on the paid tier. | VENTURE |

**Done at end of week 2:**
- Public repo live and linked in Claude Code Discord
- At least one outside user has cloned and either starred, forked, or opened an issue
- VENTURE has enough signal to make a paid-tier decision

---

## 5. Success Signal Before Any Paid Tier

**The threshold: 150 GitHub stars AND at least 3 outside users who report they are actively using it (issues, Discord replies, or forks with commits).**

Stars alone are not the signal. Stars are vanity. The signal is that 3 people other than Ron have integrated this into a real workflow and come back with a question, a bug, or an extension. That proves the job-to-be-done is real for people outside this specific environment.

**Secondary signal that accelerates the paid-tier decision:** Any company (not individual) opens an issue or DMs Ron asking about team deployment. One corporate inquiry equals 150 stars for decision-making purposes because it indicates willingness to pay.

**What to watch that would upgrade the timeline:**
- If a major AI newsletter (The Batch, TLDR AI, Latent Space) picks it up unprompted, accelerate paid tier planning by 30 days
- If GitHub shows >10 forks with commits within 2 weeks, the community is already building — that is a signal to publish the customization API before someone forks it into incompatibility

**What 150 stars without 3 active users means:** The framing landed but the product did not stick. The README attracted interest; the scaffold did not solve a real pain point outside Ron's context. That is the reshape signal, not the build-paid-tier signal.

---

## 6. Honest Risks

**Risk 1: The scaffold is too Ron-shaped to be useful without deep configuration.**
The current CLAUDE.md assumes a specific owner persona, a named project roster, and a defined infrastructure footprint. A new user clones it and immediately has to answer "who am I and what are my projects?" before any agent is useful. If the blank template version of CLAUDE.md is confusing rather than guiding, adoption stops at minute five. Mitigation: the "make it yours" section of the README must be prescriptive — give the user exact fill-in-the-blank instructions, not just "edit this file."

**Risk 2: Claude Code subagent behavior changes and breaks the process model.**
The entire scaffold depends on Claude Code reading `.claude/agents/` files and honoring the CLAUDE.md workspace config. Anthropic has already made one substantial change to the subagent system (the March 2026 teams update) and is actively developing the space. If agent file loading semantics change, or if Claude Code teams mode supersedes the single-agent-with-sub-agents pattern, the scaffold's core mechanic breaks. This is a platform dependency risk with no mitigation except staying close to Claude Code release notes and maintaining a compatibility table.

**Risk 3: The product is a philosophy, not a tool, and the community wants tools.**
The differentiation — formal verdicts, state-machine ledger, persistent journals — is a process discipline argument. It requires the user to trust the process and run the pipeline consistently. Developers who want automation will be disappointed: this scaffold does not make agents smarter or faster. It makes their work more auditable. That is a real value proposition for some buyers and irrelevant to most casual Claude Code users. If the Discord response is "interesting but I just prompt directly," the market is smaller than the star count will imply. Mitigation: the seed post must lead with a concrete pain point ("lost context between sessions, no record of what ran, no idea if the output was validated") not with the architecture.

---

## Recommendation: GO

Ship the OSS scaffold in 2 weeks. The extraction work is bounded (NOVA's research confirms no competitor has published this specific pattern), the distribution path is clear (Claude Code Discord is the right first channel), and the downside of not shipping is that someone else abstracts and publishes it first — the RADAR scan already flagged that frontier labs are building the same patterns internally.

The paid tier decision should not be made until the 150-star / 3-active-users threshold is hit. Building a paid tier before that threshold is commitment to a product with no validated market outside Ron's own use case.

**First move: FORGE completes the agent file audit (Day 1, Week 1). Nothing else starts until SENTINEL has confirmed zero personal data in the 13 agent files. That is the only task that can block the entire sprint.**

---

*Routes: This scope doc → FORGE to execute Week 1 build tasks. SENTINEL to run pre-publish audit (Day 5). SPARK to finalize README. VENTURE to run the post-Week-2 paid-tier assessment.*
