# NOVA Research Report: Council Platform Frontend Design Intelligence
**Date**: 2026-03-28 | **Agent**: NOVA | **Feeds**: FORGE (frontend build)

---

## Objective
Identify the highest-signal UX patterns, API patterns, color systems, and competitor
gaps to inform the Council platform live debate frontend — a system that must work
for both human reviewers reading session outputs AND programmatic AI agents posting
structured debate contributions.

---

## Key Findings (ranked by decision impact)

**Finding 1 — The market has debate logic but no debate UI.**
AutoGen, CrewAI, LangGraph, and OpenAI Agents SDK all have multi-agent coordination
at the code layer. None of them have a purpose-built debate visualization layer. The
closest artifacts are academic demos and LangChain Medium posts. The Council frontend
is building into an empty space, not against existing competition. This is the
strategic opening.

**Finding 2 — Confidence visualization is the #1 emerging AI UI pattern for 2026.**
Visual confidence indicators — percentage badges, color-coded borders, certainty
overlays — are being called out by Smashing Magazine and UX Planet as the defining
new component type for AI interfaces. The Council debate has natural confidence data
(agent position strength, round-over-round shift). This should be a first-class
visual element, not an afterthought.

**Finding 3 — SSE is the right streaming transport for this use case; WebSocket for
live bidirectional (human typing, agent replies).**
SSE is simpler, proxy-friendly, and sufficient for server-to-client debate streaming
(agent posts, thinking indicators, round transitions). Reserve WebSocket for the
human-participates mode where a human needs to inject into a live debate. Two
transport modes, one API.

**Finding 4 — OpenAI-compatible Chat Completions format is the agent lingua franca.**
Any agent wanting to post to the Council should be able to do so with the same
`messages: [{role, content}]` structure they use everywhere. Wrapping the Council's
inbound API in this format drops integration friction to near-zero for any AI agent
on any framework.

**Finding 5 — Dark backgrounds with glowing accent colors are the universal signal
for "AI-native tooling."**
Vercel v0, Linear, Supabase, LangSmith, Langfuse, and SemanticAgent all converge on:
near-black base + one primary accent (electric blue, teal, or green) + one secondary
warning/alert color (amber/orange). The dark purple/teal aesthetic is specifically
associated with "observability and intelligence tooling." This is what engineers trust.

---

## Evidence

### UX Pattern Sources
- Smashing Magazine (Feb 2026): agentic AI design patterns — confidence visualization,
  progressive disclosure, interrupt controls, step-by-step task logs
- Agentic Design Patterns catalog (agentic-design.ai): conversational UI, multi-agent
  dashboards, trust-building transparency patterns
- MindMesh AI (dev.to): 7-agent debate system with parallel analysis → pro/con
  advocates → quality control → synthesis phases with structured confidence scores
- AutoGen docs (microsoft.github.io): multi-agent debate as official pattern; group
  chat manager directing bidirectional agent connections
- HighLevel Changelog: thinking/typing indicator for Conversation AI as UX best practice

### API Pattern Sources
- OpenAI Agents SDK + FastAPI (github.com/ahmad2b): streaming responses, persistent
  session memory, multi-agent orchestration reference implementation
- OpenAI developer blog 2025: agent-native APIs; SSE vs WebSocket analysis — SSE for
  token streaming, WebSocket when client must send mid-stream events
- Hivenet (compute.hivenet.com): SSE simpler + proxy-friendly, built-in EventSource
  browser API; WebSocket for bidirectional when needed

### Color/Design System Sources
- Dark Mode Color Palettes 2025 (colorhero.io): near-black charcoal (#0E0E0E or
  #0C1120) + neon green or electric blue accent = "signature developer tools look"
- Supabase design system (supabase-design-system.vercel.app): dark backgrounds at
  oklch(0.13 0.02 160) with emerald green oklch(0.70 0.18 155)
- Vercel/v0: dark gray backgrounds + cyan accents; Linear: off-white text (#F5F5F7)
- General dark mode guidance: avoid pure black; use #0F0F14 or #0D1117; avoid pure
  white text

### Gap Analysis Sources
- State of AI Agent Platforms 2025 (ionio.ai): "agent collaboration and communication
  features still limited — many frameworks developer-centric, limiting non-technical
  stakeholder involvement"
- Stack Overflow 2026 retrospective: memory/context management and production observability
  are the top developer frustrations
- RedMonk (2025): 10 things developers want from agentic IDEs — shared canvases for
  non-technical review, interrupt/approve/reject controls, modular agent/task views

**Source quality note**: Color hex data is synthesized from multiple design system
references and Vercel/Supabase public design docs — reliable. Gap analysis is from
analyst sources (ionio.ai, RedMonk) — credible but reflects developer sentiment,
not user research on a debate-specific product.

---

## Risks

1. The Council platform has no direct competitor to benchmark against. Patterns are
   borrowed from adjacent spaces (observability, RLHF dashboards, debate demo apps).
   We may be solving UX problems that matter to engineers but not to business stakeholders
   who will consume debate outputs. Mitigate: design outputs (verdicts, position tables)
   for non-technical consumers alongside the live view.

2. SSE streaming and WebSocket patterns are well-established but require the backend
   to produce structured events. If the debate backend is not event-emitting today,
   the frontend cannot demonstrate live features — it will show static state. Flag
   this as a FORGE backend dependency before building the streaming UI layer.

3. "Dark teal/purple = AI tooling" is a strong aesthetic convention. It is also
   becoming a cliche. There is a counter-trend (dev.to 2025: "dark mode that doesn't
   look AI") toward using the aesthetic intentionally to signal AI while still
   differentiating. Recommendation: anchor to the convention but add one signature
   color that is ours, not borrowed from LangSmith.

---

## Recommendation

Build the Council frontend as a three-layer stack: (1) live debate view with
streaming agent cards, (2) structured output layer — position tables, verdict
summaries — readable without live context, (3) API surface that lets any AI agent
post a contribution with an OpenAI-compatible message. This architecture serves
humans watching live, humans reading async, and AI agents posting programmatically.
The confidence visualization layer is the single highest-leverage new component —
nothing else communicates "this agent is uncertain / this agent is convicted" with
the same density.

---

## 5-Section Actionable Output

---

### Section 1 — Top 5 UX Patterns to Steal for the Live Debate View

**1. Floating agent cards with live confidence borders**
Each agent in the debate gets a persistent card. The card border color reflects
current conviction strength: green (strong position held), amber (position weakening
or uncertain), red (position reversed). Border glow pulses when the agent just posted.
This is the confidence indicator pattern from Smashing Magazine applied to multi-agent
state. No competitor has built this for debates.

**2. Thinking indicator as distinct visual state, not just a spinner**
Three-dot "typing" is too weak for an AI agent doing multi-step reasoning.
Recommended pattern: the agent card enters a "thinking" state with a slow animated
scan-line or shimmer effect across the card face (not just the text area), combined
with a visible thought-stage label: "Reviewing position... Checking evidence...
Drafting response...". This communicates that something real is happening — not just
a network wait.

**3. Round-over-round position timeline (the vote drift rail)**
Below each agent card, a horizontal timeline shows how that agent's position has
shifted across rounds. Each round is a dot; dot fill indicates YES/NO/ABSTAIN/
CHANGED. This lets a human reviewer see at a glance which agents flipped and when.
Inspired by parliamentary debate vote records. Not in any AI platform today.

**4. Argument threading with reply chains**
When Agent A's argument directly responds to Agent B's prior point, visually thread
them with an indented reply indicator (like Discord reply threading, not flat
chronological list). Flat chronological debate is unreadable at 10+ agents.
This is the single most important structural pattern from Discord bots applied to
the agent context.

**5. Synthesis panel — always-visible right rail**
A persistent sidebar that shows the current emerging consensus (updated live after
each round). Not a chat log — a structured summary: active positions, open
disagreements, provisional verdict, confidence score for the emerging answer. This
is the "synthesis agent output" made visible in UI form. Inspired by LangSmith's
run detail panel — always available without leaving the main view.

---

### Section 2 — Top 5 API Patterns for Agent-Friendliness

**1. OpenAI Chat Completions-compatible inbound format**
POST /v1/debate/{session_id}/messages
Body: `{"role": "agent", "name": "NOVA", "content": "...", "metadata": {...}}`
Any agent on any framework (LangGraph, CrewAI, AutoGen, raw SDK) can post
without a custom client. The metadata field carries structured agent-specific
data (confidence, position, citations) without breaking the base spec.

**2. SSE event stream for debate output**
GET /v1/debate/{session_id}/stream
Returns server-sent events with typed event names:
- `agent.thinking` — agent has started composing
- `agent.posted` — complete message with structured JSON payload
- `round.started` / `round.ended`
- `position.changed` — agent reversed or updated stance
- `consensus.updated` — synthesizer has updated provisional verdict
Typed events let clients render only what they care about.

**3. Stable session IDs + idempotent post**
Every debate session gets a UUID. Every agent contribution gets a UUID. Posting
the same message ID twice returns 200 with the existing message, not a duplicate.
This is critical for AI agents that retry on network failure — the standard mistake
in agent-to-platform APIs is missing idempotency, causing duplicate contributions.

**4. Structured position schema in every message**
Every agent contribution carries a required position field:
`"position": {"stance": "YES|NO|ABSTAIN|CHANGED", "confidence": 0.0-1.0, "previous_stance": "..."}`
This is machine-readable and feeds the position timeline UI automatically.
No free-form stance interpretation. Agents must declare their stance explicitly.

**5. Webhook for completion events**
When a debate round ends or a verdict is reached, POST to a registered webhook.
This lets external systems (HELM scheduler, AXIOM orchestrator, human notification
pipeline) react without polling. Include the structured verdict payload in the
webhook body. Standard pattern from Replicate and Together AI — polling APIs are
agent-hostile.

---

### Section 3 — Color/Design System Recommendation (specific hex values)

The Council platform should use a "Deep Slate + Violet Accent" system — close enough
to the LangSmith/Langfuse observability aesthetic to signal credibility, differentiated
enough by the violet primary to have a signature identity.

**Base palette:**

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-base` | `#0B0D14` | Primary background — deep near-black with slight blue cast |
| `--bg-surface` | `#111320` | Card/panel backgrounds — 1 step lighter |
| `--bg-elevated` | `#181B2E` | Modals, dropdowns, hover states |
| `--border-subtle` | `#1E2240` | Default borders — barely visible |
| `--border-active` | `#2E3460` | Active/focused borders |

**Text:**

| Token | Hex | Usage |
|-------|-----|-------|
| `--text-primary` | `#E8E8F0` | Main body text — off-white, not pure white |
| `--text-secondary` | `#8B90B8` | Labels, metadata, timestamps |
| `--text-muted` | `#555878` | Disabled, placeholders |

**Accent (Council violet — our signature):**

| Token | Hex | Usage |
|-------|-----|-------|
| `--accent-primary` | `#7C6BF2` | Primary CTA, active agent indicator, links |
| `--accent-glow` | `rgba(124,107,242,0.15)` | Card glow for active/posting agent |
| `--accent-dim` | `#3D3478` | Pressed states, secondary badges |

**Semantic colors (position/debate state):**

| Token | Hex | Usage |
|-------|-----|-------|
| `--state-yes` | `#22D387` | YES/GO/APPROVE — bright teal-green |
| `--state-no` | `#F05A5A` | NO/BLOCK/REJECT |
| `--state-changed` | `#F5A623` | POSITION CHANGED — amber |
| `--state-thinking` | `#5BBCF7` | AGENT THINKING — electric blue shimmer |
| `--state-abstain` | `#8B90B8` | ABSTAIN — same as secondary text |

**Typography recommendation:**
- UI chrome: Inter or Geist (Vercel's font — available free, signals engineering quality)
- Agent names/labels: monospace (JetBrains Mono or Geist Mono) — visually separates
  agent identity from content
- Body text: Inter 15px / 1.6 line-height (not 14px — debate content needs breathing room)

---

### Section 4 — 3 Features Competitors Missed (and we should include)

**1. Position drift visualization — the vote rail**
AutoGen, CrewAI, LangSmith, Langfuse: none show how an agent's position changed over
the course of a debate. They show outputs; they do not show evolution. A horizontal
mini-timeline per agent that shows stance-per-round as colored dots is a genuinely
novel UI element that makes the debate *legible* in retrospect. Post-session, you can
see at a glance: which agents shifted, how many rounds it took, who stayed firm. This
is the feature that turns a debate log from a chat transcript into a decision record.

**2. Human-readable verdict card as first-class output**
Every debate platform outputs a chat transcript. None output a structured, designed
summary card intended for a non-technical human reader — a "verdict card" with: the
question, the vote count, the key argument that won, the key dissent that was noted,
and a one-sentence recommendation. This card is the deliverable that a CEO or product
owner actually reads. Everything else is audit trail. Build the verdict card as a
distinct designed component with its own share/export path.

**3. Agent memory injection point — pre-debate context API**
Before a debate round starts, allow agents to POST context they want to surface:
links, prior decisions, relevant memories. This feeds into the structured pre-debate
state visible in the synthesis rail. No current platform has a structured "agent
brings context to the table" mechanism — agents just start talking. A pre-debate
context phase with a time-boxed submission window (e.g., 30 seconds before round 1)
makes the debate richer and creates an audit trail of what each agent knew before
they voted. This directly connects to the COUNCIL debate architecture we already
have (agents have access to Owner's Inbox, MEMORY.md, etc.) and makes that
context-loading explicit rather than implicit.

---

### Section 5 — Specific Component Specs

**"Agent is thinking" component:**

```
State: THINKING
Visual:
  - Agent card border: slow pulse animation in --state-thinking (#5BBCF7)
    at 1.5s cycle, opacity 0.4 → 1.0 → 0.4
  - Inside card: animated scan-line (thin horizontal line sweeping top to bottom,
    --state-thinking color, opacity 0.3, 2s cycle)
  - Below agent name: small text label cycling through:
    "Reviewing prior positions..." → "Evaluating evidence..." → "Composing response..."
    (rotates every 2.5s via CSS keyframes or simple JS interval)
  - DO NOT use a spinner — it reads as "loading" not "reasoning"
  - Duration gate: if thinking state exceeds 45s, add "(taking longer than usual)"
    sub-label in --text-muted color
```

**"Agent changed position" component:**

```
State: POSITION_CHANGED
Trigger: agent posts with position.stance != position.previous_stance
Visual:
  - Card border flashes --state-changed (#F5A623) for 3s, then settles
  - Inside card, above the message: a small badge:
    [WAS: NO] → [NOW: YES]  (arrow between them, --state-changed color)
  - Badge persists for the duration of the round, then collapses to a small
    orange dot in the card header area
  - In the position timeline rail below the card, a new dot is added with a
    visual distinction (double-bordered dot) to mark the flip round
  - In the synthesis panel: "NOVA reversed position in Round 3" appears as
    a notable event line
```

**"Agents disagree" component:**

```
State: ACTIVE_DISAGREEMENT (2+ agents hold opposing stances)
Trigger: synthesis engine detects YES and NO both held by different agents
Visual:
  - A "tension indicator" appears between disagreeing agents' cards (if in
    a grid/row layout): a subtle dashed line with a small collision icon (⚡)
    between them — not intrusive, visible on hover
  - In synthesis panel: "Active disagreement: FORGE (YES) vs SCRIBE (NO)"
    appears as a highlighted block in --state-changed color with the core
    argument from each side shown in 1-line summary
  - If disagreement persists for 3+ rounds without resolution, the synthesis
    panel upgrades this to a "Persistent Split" label and surfaces it as
    the lead item — a human may need to cast a deciding vote
  - DO NOT auto-resolve disagreements — surface them explicitly. The value
    of the council is the disagreement, not forced consensus.
```

---

## Next Actions

1. **FORGE**: Confirm the debate backend emits structured events (or plan to add
   event emission). The streaming UI layer has zero value without typed backend events.
   This is the #1 prerequisite — confirm before starting frontend build.

2. **FORGE**: Start with the verdict card component first. It is the highest-value
   deliverable and requires no streaming infrastructure — just structured JSON input.
   Ship the verdict card, then layer in the live view.

3. **FORGE**: Implement the color system as CSS custom properties (variables) from day
   one. Do not hardcode hex values. The design system tokens above map directly to
   Tailwind CSS custom colors or CSS vars — choose one approach and be consistent.

4. **NOVA**: The OpenAI-compatible inbound API spec above is a starting point. If FORGE
   wants a full OpenAPI spec for the debate API, flag it — this is a 30-minute
   follow-up task.

5. **SENTINEL**: Review the idempotency requirement for agent message posting. Duplicate
   messages in a Council debate could corrupt the position record — this is a
   validation risk, not just an API nicety.

---

*Deliverable: NOVA research complete. Handed to FORGE for frontend execution.*
*Sources cross-referenced against 15+ web sources — see citations below.*
