# RADAR: PKA v0.1–0.5 Opportunity Scan
*Agent: RADAR | Date: 2026-04-02 | Scan scope: v0.1.0 – v0.5.0*

---

## Observation 1: The Scored Audit Trail Is the Patent Claim

**Signal strength: HIGH**

PKA has assembled something that does not exist as a coherent, patentable
system elsewhere: a stateful AI task lifecycle engine that couples a
structured evidence ledger (task records with required evidence fields),
a continuous audit trail generated via PostToolUse hooks at the tool-call
level, a self-scoring process readiness function (pka_scorecard.py), and a
background intelligence consolidation pass (pka_dream.py) that produces a
synthesized signal from sessions, task history, and agent journal health in
four defined phases. None of these capabilities is novel in isolation. Their
combination — specifically the closed-loop feedback from tool-call audit to
scored readiness to background consolidation — is not something a search of
the prior art space (CrewAI, AutoGen, LangGraph, KAIROS) will surface as an
integrated system.

The patent claim window is open right now and it is narrow. CrewAI and
AutoGen both added "memory" and "observability" features in 2025. None of
them has a scored readiness metric derived from an audit trail that also
informs a dream-phase synthesis. The specific mechanism to protect is: an AI
agent orchestration system that (a) logs every tool invocation to a session
audit log, (b) scores agent throughput, evidence coverage, verdict accuracy,
and escaped defect rate against a normalized 100-point scale, and (c)
periodically consolidates that signal into a structured intelligence report
that feeds back into session start context. The combination of (a)+(b)+(c)
in a single automated pipeline is the claim.

Filing window risk: if any major platform (LangSmith, Weights and Biases
Weave, or Anthropic themselves) ships a comparable closed-loop scored audit
system before a provisional is filed, prior art is established and the
window closes. The Anthropic Claude Code source leak (v2.1.88, DreamTask
pattern) that PKA adapted confirms these patterns are in active internal
development at frontier labs. The filing window is 6-12 months at most.

**Recommended action:** Route to LEGAL immediately for provisional patent
assessment on the specific mechanism: tool-call-level audit trail + scored
readiness function + background intelligence consolidation as an integrated
AI orchestration feedback loop.

---

## Observation 2: PKA Is a Sellable Product, but the Wrong Framing Will Kill It

**Signal strength: MEDIUM**

PKA as currently built is not a product. It is Ron's personal operating
system for AI work. But the gap it fills is real and commercially
underserved: enterprises deploying AI agents through tools like AutoGen,
CrewAI, or custom Claude Code setups have no lightweight process control
layer — no inbox routing, no evidence-gated delivery, no scored audit, no
session continuity without engineering overhead. The market for "AI agent
governance and observability" is nascent and currently occupied by vendors
targeting data science pipelines (MLflow, W&B) rather than orchestration
workflows.

The sellable version of PKA is not "AI agent orchestration" — that market
is crowded with better-funded competitors. The sellable version is
"AI operations process control for teams already using Claude Code or
similar agentic tools." The SKU is: a Git-hosted workspace scaffold (not a
SaaS, not a platform) that any operator drops into their repo and gets
session gates, task ledger, delivery manifest, scored audit, and dream
synthesis on day one. The price point is either $0 open-source (builds
distribution and credibility for paid support/consulting) or $499/year for
a team license of an enhanced version with a web dashboard. The buyer is the
AI engineering lead at a company of 10-100 people deploying Claude Code
agents without a process framework.

The risk in productizing is that PKA's competitive advantage is depth of
integration with Ron's specific environment. Genericized, the differentiation
shrinks. The correct path is to extract the 5 portable scripts
(pka_operator_run.py, pka_scorecard.py, pka_dream.py, pka_session_gate.py,
pka_task_cli.py), clean them of environment-specific assumptions, and publish
as an open-source scaffold under a permissive license. This creates prior art
on the pattern and builds inbound interest before any SaaS decision is made.

**Recommended action:** Direct VENTURE to scope a 2-week open-source scaffold
extraction — strip Ron-specific environment assumptions from the 5 portable
scripts, write a generic OPERATING_MODEL.md, publish to GitHub under the
verified-agent-ops repo already created, and seed 2-3 AI engineering
communities with a post. Evaluate interest before investing in a paid tier.

---

## Observation 3: Council and AgentForge Need PKA's Infrastructure Right Now

**Signal strength: HIGH**

Of Ron's 50+ projects, two have an immediate, high-leverage integration case
that requires no new engineering — only a config extension.

Council (C:\Users\techai\council\, port 8601) is a multi-agent debate
platform with 128 tests and 319 agent memories. Its test suite and agent
memory are exactly the artifacts PKA's scorecard and dream synthesis were
designed to track. Council tasks currently have no lifecycle ledger, no
delivery evidence requirements, and no scored audit trail. Defects found in
the Council CRUCIBLE sweep (TASK-20260402-004) are being tracked in one-off
markdown files rather than the task ledger. This means Council's operational
history is invisible to PKA's readiness scoring, and Council's CRUCIBLE
results are not flowing into any continuous quality signal. The integration
cost is zero: add Council as a tracked project in PKA's task ledger, point
pka_dream.py at Council's test logs, and Council's delivery history becomes
part of the scored audit. Council's agent count (13 specialists mirroring
PKA's roster) makes it the most natural first integration target.

AgentForge (D:\agentvault, port 8400, Phase 1 complete with 34/34 tests)
is the second target. AgentForge is Ron's agent marketplace — the system that
creates, registers, and manages agents. It has an existing passing test suite
but no continuous session audit, no scored readiness metric, and no delivery
manifest. This is precisely the gap PKA closes. More importantly, AgentForge
is the infrastructure layer under which PKA's agent roster itself could be
managed at scale. Integrating PKA's task ledger with AgentForge's agent
registry creates a traceable chain from "agent is hired" to "agent has a
delivery record" to "agent's readiness score affects routing decisions."
That chain does not exist anywhere in the ecosystem today, and it is the
foundation of the patent claim in Observation 1 applied at scale.

**Recommended action:** HELM should add Council and AgentForge as tracked
integration targets in the PKA task ledger this week, then FORGE should
extend pka_dream.py to accept a configurable project list and scan their
test logs and delivery artifacts in the Gather phase. Estimated effort: one
focused session.

---

## The Question Nobody Asked

Why is PKA tracking agent journal health (journals with entries / 13) but
not tracking agent contribution quality — which agents produced deliverables
that required FORGE rework, which agents produced GO verdicts that later
surfaced escaped defects, and which agent pairings generated the highest
throughput with the lowest defect rate?

The current scorecard measures the system. It does not measure the agents
inside it. An agent-level performance model fed by the existing audit trail
would allow routing decisions to be evidence-based rather than rule-based.
AXIOM currently routes by task type. With agent performance data, AXIOM could
route by demonstrated track record. That is the capability that separates PKA
from every competitor and it is one scoring extension away from the data
already being collected.

This is not a backlog item. It is the next version of the patent claim.

---

*Routes: Observation 1 → LEGAL | Observation 2 → VENTURE | Observation 3 → HELM*
*Filing urgency on Observation 1: within 30 days*
