---
id: NOVA-agent-ops-competitive-landscape
date: 2026-04-02
author: NOVA
status: DELIVERED
topic: AI Agent Orchestration — Competitive Landscape vs PKA
---

# AI Agent Orchestration Competitive Landscape
## PKA (Verified Agent Ops) vs. CrewAI, AutoGen/MAF, LangGraph, OpenAI Agents SDK, Claude Code Teams

---

## Executive Summary

- PKA is the only platform in this comparison that couples a formal state-machine ledger, GO/NO-GO verdicts from a dedicated validation agent, and persistent cross-session agent journals as first-class, non-optional primitives — not optional plugins.
- Every competitor has observability tooling; none has a structured review gate baked into the process where a named agent must issue a verdict before work ships.
- PKA's gap is discoverability and portability: it is a private, single-tenant workspace with no SDK, no docs, and no distribution path. Every competitor has an open-source codebase or a commercial product page.

---

## Comparison Table

| Platform | Coordination model | Testing / validation | Audit trail | Agent memory (cross-session) | Verdict |
|---|---|---|---|---|---|
| **PKA (Verified Agent Ops)** | 13 named agents with fixed roles; AXIOM routes, never executes; SENTINEL gates every ship | SENTINEL issues formal GO/NO-GO verdicts; CRUCIBLE runs adversarial + security sweeps per deploy | Full YAML-front-matter ledger per task; state machine (INTAKE → ROUTING → EXECUTION → REVIEW → DELIVERED); process audit score after every session | Each agent has a persistent journal file that survives all sessions; AXIOM can read history | Strongest governance and accountability model; weakest distribution and ecosystem |
| **CrewAI** | Role-based agent crews (sequential or parallel); event-driven Flows for enterprise; manager agent for delegation | `crewai test` CLI exists; Promptfoo integration for structured evals; QA-agent pattern available but unreliable per practitioner reports | AMP Suite: per-call tracing, RBAC, token/cost logging; no structured verdict system | Hierarchical SQLite long-term memory across sessions; scoped by agent/project paths | Best ecosystem and enterprise UI; memory is real; no formal gate between build and ship |
| **AutoGen / Microsoft Agent Framework** | Group chat, sequential, concurrent, handoff, and Magentic (manager-builds-ledger) modes; AutoGen entering maintenance — MAF is successor | AutoGen Bench for benchmarking; OpenTelemetry built in; no formal QA-gate agent | MAF enterprise: compliance audit trails planned GA Q2 2026; AutoGen 0.4: message tracing + checkpointing today | Pluggable memory components; checkpoint/resume for long workflows; no native cross-session agent journal | Most technically complete coordination primitives; audit trail is enterprise-tier but still in GA pipeline |
| **LangGraph** | Graph-based cyclical workflows; supervisor + subagraph patterns; supports single, multi-agent, hierarchical; state shared between nodes | LangSmith evaluation platform (separate product); LangGraph Systems Inspector (AI-tests-AI, third-party); no built-in gate agent | Immutable state versioning; full node/edge execution history per run; deterministic replay via MCP+LangGraph; LangSmith for production monitoring | Short-term working memory within run + long-term via external DB (checkpointed); cross-session memory requires explicit wiring | Most flexible execution model; best state audit per-run; memory requires developer effort to persist cross-session |
| **OpenAI Agents SDK** (replaces Swarm) | Routines + handoffs; guardrails on input/output; tracing dashboards; Swarm is now educational-only reference | Built-in guardrails validate inputs/outputs per agent; no formal verdict system or named QA agent | Built-in tracing: LLM calls, tool calls, handoffs, guardrails, custom events; exportable traces; visual DAG; no formal ledger record per task | Sessions API for within-session continuity; long-term memory via external notes/context engineering; no native persistent agent journals | Tightest OpenAI model integration; best out-of-box guardrails; no cross-session agent identity |
| **Claude Code Agent Teams** | One lead + N teammates; each teammate has its own 1M-token context; shared task list with dependency tracking; mailbox for inter-agent messages | No built-in QA gate; no validation agent role; testing is whatever the developer instructs | No native audit trail; Ceros (third-party cryptographic audit layer) fills this gap; no per-task ledger | No persistent identity or memory across sessions; /resume does not restore teammates; session memory system exists at individual session level only | Best for parallel code execution on a single repo; worst cross-session continuity of all platforms reviewed |

---

## Where PKA Is Differentiated

**The ledger + verdict model is structurally unique.** Every other platform in this review treats observability as a monitoring concern — you can see what happened after the fact via dashboards, traces, or logs. PKA treats it as a process control concern: no task can leave EXECUTION without passing through SENTINEL's GO/NO-GO gate. The formal YAML front-matter record with a state machine means a task is either delivered or it is not — there is no ambiguous "completed with caveats" state. No competitor has this. CrewAI has QA-agent patterns but practitioners explicitly report they are unreliable; LangGraph has per-run state history but no named reviewer; AutoGen's compliance audit trail is still in the GA pipeline as of April 2026.

**Persistent agent journals solve a problem none of the others fully solve.** CrewAI's long-term memory is the closest analog — it persists across sessions via SQLite — but it is a shared team memory, not per-agent identity. NOVA's journal is NOVA's journal. SENTINEL's journal captures every GO/NO-GO decision SENTINEL has ever made. This means agents accumulate domain-specific judgment over time. Claude Code Teams explicitly has no cross-session agent identity. OpenAI Agents SDK requires external context engineering to approximate it. LangGraph requires developer-wired external storage. Only CrewAI has a structural equivalent, and it is scoped to crew memory rather than individual agent identity.

**The specialization model eliminates role ambiguity.** PKA's 13 named agents with fixed role boundaries — AXIOM never executes, LEGAL handles IP, CRUCIBLE handles adversarial testing — mirrors how high-stakes operations teams are actually organized. Generic agent pools (AutoGen group chat, CrewAI dynamic delegation, LangGraph supervisor patterns) allow any agent to take any task. That flexibility is powerful for general automation and creates accountability gaps in high-stakes work. When something goes wrong in PKA, the question "who was responsible for this?" has a named answer.

## Where PKA Has Gaps

**Distribution and adoption infrastructure is zero.** Every competitor has either an open-source GitHub repo, a hosted cloud product, or both. PKA is a private workspace. There is no SDK, no documentation site, no install path for a second user. If the goal is commercial product or platform, this is the first-order build requirement.

**Memory is file-based, not queryable.** Agent journals are markdown files. They are readable and persistent, but there is no semantic search, no decay/importance weighting, and no cross-agent memory graph. CrewAI's cognitive memory system — with composite scoring blending semantic similarity, recency, and importance — is architecturally ahead here. LangGraph's external-DB checkpointing and AutoGen's pluggable memory components both allow programmatic querying that markdown files do not support.

**No benchmark or comparative evaluation tooling.** AutoGen Bench, LangSmith evals, and Promptfoo integration all give competitors a way to measure agent quality over time. PKA has a process audit score (targeting 100/100), but that measures process compliance, not output quality. There is no equivalent to "run this agent against 50 test cases and report pass rate."

---

## Sources

- [CrewAI — The Leading Multi-Agent Platform](https://crewai.com/)
- [CrewAI Memory Concepts](https://docs.crewai.com/en/concepts/memory)
- [CrewAI Testing Concepts](https://docs.crewai.com/en/concepts/testing)
- [CrewAI OSS 1.0 GA Announcement](https://www.crewai.com/blog/crewai-oss-1-0---we-are-going-ga)
- [CrewAI Cognitive Memory Blog](https://blog.crewai.com/how-we-built-cognitive-memory-for-agentic-systems/)
- [Microsoft Agent Framework Introduction — Azure Blog](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)
- [AutoGen v0.4 Reimagining — Microsoft Research](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)
- [AutoGen to Microsoft Agent Framework Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
- [AutoGen Studio: No-Code Developer Tool — Microsoft Research](https://www.microsoft.com/en-us/research/publication/autogen-studio-a-no-code-developer-tool-for-building-and-debugging-multi-agent-systems/)
- [LangGraph — LangChain](https://www.langchain.com/langgraph)
- [LangGraph Overview Docs](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Systems Inspector — Medium](https://medium.com/@nirdiamant21/langgraph-systems-inspector-an-ai-agent-for-testing-and-verifying-langgraph-agents-a8d1c2400d60)
- [LangSmith Evaluation Platform](https://www.langchain.com/langsmith/evaluation)
- [OpenAI Agents SDK — Official Docs](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK Sessions](https://openai.github.io/openai-agents-python/sessions/)
- [OpenAI New Tools for Building Agents](https://openai.com/index/new-tools-for-building-agents/)
- [OpenAI Swarm — GitHub (archived reference)](https://github.com/openai/swarm)
- [Claude Code Agent Teams — Official Docs](https://code.claude.com/docs/en/agent-teams)
- [Claude Code Agent Teams — March 2026 Update](https://blog.imseankim.com/claude-code-team-mode-multi-agent-orchestration-march-2026/)
- [Claude Code Session Memory](https://claudefa.st/blog/guide/mechanics/session-memory)
- [AI Agent Memory Comparative Analysis (LangGraph, CrewAI, AutoGen)](https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp)
- [Top 9 AI Agent Frameworks — Shakudo, March 2026](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)
- [Best Multi-Agent Frameworks 2026 — GuruSup](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
