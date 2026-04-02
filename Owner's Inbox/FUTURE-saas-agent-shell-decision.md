# Future TODO: SaaS-Ready Agent Orchestration Shell

**Captured**: 2026-03-27
**Status**: NOT building now — reference note for when the time comes

---

## Decision

Ron's personal stack (PKA workspace, MemoryWeb, Ultra RAG, AI Army OS, etc.) stays as-is. It works. Don't refactor it, don't extract from it, don't try to make it generic.

When the time comes, build a clean SaaS shell from the ground up — informed by everything learned from the personal stack, but not derived from it.

---

## Key Principles

- **Personal stack = personal.** It will keep growing with new integrations. That's fine.
- **SaaS shell = separate repo, clean slate.** No MemoryWeb, no Ultra RAG, no personal infra baked in.
- **DataShield = open source candidate.** Push to GitHub as a free standalone tool so anyone can remove their sold personal info. Not tied to the orchestration shell.
- **Other agent groups will be built too** — each as their own clean product, not forks of the personal stack.
- The personal stack is the R&D lab. The SaaS products are what ships from the lessons learned.

---

## What the SaaS Shell Needs (capture now, build later)

- Agent definition format (like `.claude/agents/` but no personal references)
- Inbox routing system (Team Inbox / Owner's Inbox pattern — proven to work)
- Plugin architecture for integrations (RAG, memory, LLM providers are all plugins, not core)
- Agent hiring/onboarding pipeline
- Config-driven, no hardcoded paths/IPs/keys
- Works without NVIDIA hardware, Spark cluster, or any of Ron's specific infra

---

## Zero Trust Architecture (non-negotiable for SaaS)

- **No implicit trust between agents, nodes, or integrations** — every request proves identity
- **WireGuard mesh networking** (Tailscale or equivalent) for inter-node communication
- **Agent identity verification** — each agent has cryptographic identity, not just a name
- **Plugin sandboxing** — integrations (RAG, memory, LLM providers) run in isolated contexts with scoped permissions
- **Mutual TLS** for all service-to-service calls
- **No shared secrets** — per-agent, per-integration credential scoping
- **NVIDIA BlueField DPU support** — optional for enterprise customers on NVIDIA infra (hardware-level zero trust)
- **Audit trail on every cross-boundary call** — who called what, when, with what permissions

---

**Status: NOT building now** — reference note for when the time comes
