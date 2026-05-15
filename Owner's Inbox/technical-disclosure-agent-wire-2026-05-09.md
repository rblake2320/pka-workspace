# Technical Disclosure — Agent Wire Layer
## Policy-as-Code Enforcement for Multi-Agent Systems

**Date of disclosure:** 2026-05-09
**Author:** Ron Blake (rblake2320)
**Primary commit:** `991fbfee7f166206f038bd8274adac807a5b2b8b` (2026-05-09 18:46:00 -0500)
**Repository:** agent-wire (local, PKA workspace)
**Foundation:** selfconnect-enterprise `48ffb80f2b41756588a0523efbd8010428f2badc` (2026-05-09)
**Status:** Working system, live proof run, 18/18 checks passed

---

## What This Is

A policy-as-code enforcement layer for multi-agent AI systems on Windows. Every action an AI agent attempts passes through a deny-by-default policy evaluator before execution. The decision — allow or deny — is logged to a cryptographically signed, hash-chained ledger. The system operates independently of any AI model's reasoning or output.

The distinguishing claim: **enforcement is structural, not instructional.** An agent cannot perform a denied action regardless of what any model outputs, because the check occurs in Python code before any action executes.

---

## What This Is Not

**Not prompt-based safety.** System prompts, CLAUDE.md rules, and "don't do X" instructions are defense-in-depth. They work until they don't — confused model, bad context window, jailbreak, session that doesn't read the rules. Agent-wire moves the enforcement boundary out of the prompt layer entirely.

**Not a certified MLS system.** No Common Criteria evaluation, no DIACAP, no FedRAMP. The enforcement properties are software-level, proved by tests and live demonstration.

**Not coupled to any specific AI provider.** The dispatch check is Python code that runs before any model call. The model never sees a denied action — it is intercepted before reaching execution.

---

## System Architecture (Non-Obvious Design Decisions)

### 1. Deny-by-Default Vocabulary

Actions are not blocked by blacklist — they are permitted by whitelist only. An agent's `allowed_actions` list is explicit and minimal. Any action not in the list is denied with a specific reason string, regardless of how reasonable the action might appear. The vocabulary (`execute_shell`, `deploy`, `research`, etc.) is finite and enumerated.

**Why this matters:** A blacklist approach fails open when an attacker finds a string not on the list. A vocabulary-constrained whitelist fails closed — unknown actions are denied by definition.

The Haiku/BlueStacks scenario (AI agent proposing to kill the host application) is structurally impossible under this design: `kill_process`, `uninstall_app`, `execute_shell` have no slot in the permitted vocabulary for any agent. The deny happens before any model reasoning runs.

### 2. Cryptographic Ledger With Kill Switch Compatibility

Every dispatch decision — allow or deny — is written to a JSONL ledger. Each entry is signed with ed25519 (DPAPI-backed private key) and hashes the previous entry. The chain is tamper-evident: modifying any entry invalidates all subsequent entries.

**The non-obvious property:** The kill switch (`WIRE_ENABLED=false`) bypasses the policy enforcer but does not write to the ledger. When the wire is re-enabled, the next decision resumes the chain from where it left off. The kill switch and the audit trail are compatible — the safety valve does not corrupt the accountability mechanism.

**Proved at commit `991fbfe`:** Chain valid with 4 entries spanning allow + deny + revoked + cross-role decisions. Chain integrity verified via `AgentLedger.verify()` after roundtrip through kill switch disable/re-enable.

### 3. Classification Tiers as a Data-Sensitivity Gate

Agents are not just action-gated — they are data-gated. An agent with `max_classification=CUI` is denied at the policy layer when the dispatch context carries `classification=SECRET`. This is enforced by the same Bell-LaPadula lattice comparator used in SelfConnect Enterprise (`rank(label) <= rank(ceiling)`).

**Why this is non-obvious:** Most agent authorization systems gate on what an agent can *do*, not on what *data* it can touch. A confused SPARK agent (content role, CUI ceiling) cannot be prompted into processing SECRET-classified material even if the model believes it should. The classification check is independent of the action check.

### 4. Runtime Dispatch Decoupled From Model Reasoning

The dispatch check occurs at the layer that calls the agent, not inside the agent. An orchestrator (AXIOM) calls `dispatcher.dispatch("FORGE", "build")` before invoking FORGE. If the check denies, FORGE never receives the task. The model running inside FORGE never sees a denied dispatch — it simply isn't invoked.

**Why this is non-obvious:** Prompt-based guardrails work inside the model's context window. They can be reasoned around, ignored, or overridden by sufficiently adversarial prompting. Wire-layer enforcement operates outside the model's context window — the model has no access to it and cannot influence it.

### 5. Identity Binding Without Central Authority

Each agent has a stable `WIRE-{NAME}-{ID}` identifier. The wire system itself holds a machine-bound ed25519 identity provisioned via Windows DPAPI. Identity is not self-declared by the agent — it is assigned by the roster at dispatch time. An agent cannot claim a different identity to acquire different permissions.

---

## Live Proof — `991fbfe` (2026-05-09 18:46:00 -0500)

The script `live_integration_test.py` runs against real infrastructure (real DPAPI identity, real ledger on disk) and proves:

| Check | Result |
|-------|--------|
| NOVA/research → allow, ledger written | PASS |
| Ledger entry decision=allow | PASS |
| FORGE/execute_shell → deny (Haiku scenario) | PASS |
| FORGE/research → deny (cross-role) | PASS |
| HAIKU-AGENT-UNTRUSTED → deny (unregistered) | PASS |
| Revoked FORGE/build → deny | PASS |
| 4-entry chain valid after allow+deny+revoked dispatches | PASS |
| Kill switch: unknown agent allowed (bypass) | PASS |
| Kill switch: enforcement restored (re-enable) | PASS |

**18/18 checks passed.** Run date: 2026-05-09. Reproducible from the commit.

---

## Relationship to SelfConnect Enterprise

Agent-wire imports from `selfconnect-enterprise` as a dependency. Zero files in selfconnect-enterprise were modified to build agent-wire. The `v1.0.0-docs` tag on selfconnect-enterprise (`48ffb80`) is unchanged.

SelfConnect Enterprise provides: `PolicyEnforcer`, `PolicyBundle`, `AgentLedger`, `AgentIdentity`, `LabelEnvelope`, `Classification`.

Agent-wire provides: the agent roster (13 agents with explicit policies), the `Dispatcher` class that bridges orchestration to enforcement, and the live runtime integration.

The layered structure is intentional and maintained: enforcement primitives in enterprise, orchestration binding in wire, agent execution in Claude Code subagents. Each layer is independently testable and independently deployable.

---

## Prior Art Assessment (at time of disclosure)

As of 2026-05-09, no publicly known system combines:
- Deny-by-default vocabulary enforcement at the orchestration layer (not the model layer)
- Cryptographic hash-chain audit ledger for AI agent dispatch decisions
- Classification-tier data-sensitivity gating (Bell-LaPadula) applied to agent dispatch
- Kill switch that bypasses enforcement without corrupting the audit chain
- Windows-native machine-bound identity for agent dispatch signing

Individual components exist (prompt guardrails, output filters, API-level rate limiting). The combination as a cohesive enforcement substrate at the dispatch layer — operating outside the model's context window — is the novel claim.

---

## Repositories and Artifacts

| Artifact | Location | Commit |
|----------|----------|--------|
| agent-wire source | `C:\Users\techai\PKA testing\agent-wire\` | `991fbfe` |
| selfconnect-enterprise | `C:\Users\techai\PKA testing\selfconnect-enterprise\` | `48ffb80` (tag: v1.0.0-docs) |
| Live proof script | `agent-wire/live_integration_test.py` | included in `991fbfe` |
| pka-workspace (parent) | `C:\Users\techai\PKA testing\` | submodule pointers current |

---

*This document was prepared on 2026-05-09 as a private technical disclosure contemporaneous with the working system demonstration at commit `991fbfe`. It has not been reviewed by patent counsel. It is not a patent application.*
