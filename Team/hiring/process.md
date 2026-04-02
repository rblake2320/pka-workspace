# Agent Hiring Pipeline

## How It Works
Ron identifies a gap in team capability. AXIOM routes the hire request
to HELM. HELM creates the new agent file. AXIOM updates the roster.
New agent is active in the next session.

## Step 1 — Identify the Gap
Ron drops a hire request in `Team Inbox/` using this format:

```
HIRE REQUEST
Role needed: [what this agent does]
Trigger: [when should AXIOM route to this agent]
Key outputs: [what this agent delivers]
Named: [name if Ron has one, else AXIOM proposes]
```

## Step 2 — AXIOM Validates the Request
Before HELM creates the agent, AXIOM checks:
- [ ] Does this role overlap with an existing agent?
- [ ] Is the trigger clause specific enough to route correctly?
- [ ] Does Ron's owner.md context justify this hire?

If overlaps found: AXIOM proposes merging into an existing agent instead.
If gap is real: AXIOM routes to HELM with a green light.

## Step 3 — HELM Creates the Agent File
HELM writes `.claude/agents/[NAME].md` using the template below.
HELM also:
- Creates `Team/[NAME]/readme.md` (working directory)
- Adds the agent to `Team/roster.md`
- Delivers a hire summary to `Owner's Inbox/`

## Step 4 — AXIOM Updates CLAUDE.md
AXIOM moves the new agent from "Bench" to "Active Agent Roster" in
`CLAUDE.md`.

## Step 5 — Confirmation to Ron
HELM delivers a one-page hire summary to `Owner's Inbox/` confirming:
- Agent name and mission
- What triggers routing to this agent
- What outputs to expect
- First suggested task to run

---

## Agent File Template

Copy this to `.claude/agents/[NAME].md`:

```markdown
---
name: [NAME]
description: [One sentence — what this agent does and when AXIOM should
activate it. Be specific about triggers so routing is precise.]
model: claude-opus-4-6
---

# [NAME] — [Role Title]

## Mission
[2-3 sentences. What problem does this agent solve? What is the cost of
not having it? What makes it different from existing agents?]

## Laws
- [Non-negotiable rule 1]
- [Non-negotiable rule 2]
- [Non-negotiable rule 3]
- Nothing generic. Nothing bloated. Nothing untested presented as done.
- Only correct, useful, and outcome-driving.

## Every Deliverable — Required Structure
1. **[Section 1]** — [what goes here]
2. **[Section 2]** — [what goes here]
3. **[Section 3]** — [what goes here]
4. **[Section 4]** — [what goes here]
5. **[Section 5]** — [what goes here]

Output format: Answer → Reasoning → Risks → Action. Always in that order.

## Handoff Rules
- Receives work from: [which agents hand off to this one]
- Delivers to: [Owner's Inbox / which agents receive this agent's output]
- Flags to AXIOM when: [escalation conditions]

## What [NAME] Never Does
- [Hard constraint 1]
- [Hard constraint 2]
- [Hard constraint 3]
```

---

## Bench Agents (pre-approved, not yet hired)

*(empty — all pre-scoped agents have been hired as of 2026-03-23)*

To add a new bench candidate, follow Steps 1–2 above and leave the agent
in Bench status until Ron approves the hire.
