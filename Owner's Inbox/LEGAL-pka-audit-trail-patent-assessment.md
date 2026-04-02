# LEGAL: PKA Scored Audit Trail System — Patent Assessment

**Prepared by:** LEGAL Agent, PKA AI Team
**Date:** 2026-04-02
**Classification:** Attorney-Client Privileged Work Product — Draft for Review by Qualified Patent Counsel
**Status:** DRAFT. Not a filed document. Not legal advice.

**FILING WINDOW ALERT — READ FIRST:** The PKA audit trail system was built on 2026-04-01 (v0.2.0 adds scorecard, v0.4.0 adds PostToolUse hook) and is currently in a private repository. If the `rblake2320/verified-agent-ops` repository referenced in the CHANGELOG has any public visibility — even briefly — the 12-month AIA clock under 35 U.S.C. § 102(b)(1) has started. Determine the repository's visibility status within 48 hours. A provisional patent application should be filed within 30 days of this assessment regardless of that determination, to lock the earliest possible priority date. The cost of inaction is that a competitor reading the RADAR observation (observation 1) about this exact mechanism and filing first establishes prior art against Ron's own invention.

---

## LEGAL Verdict Up Front

**Filing Recommendation: GO (Conditional)**
**Overall Claim Strength: 6.5/10**
**Urgency: High — file provisional within 30 days**

The PKA audit trail system presents a real patent claim — not a novel-feeling engineering pattern, but a specific closed-loop mechanism that does not appear as an integrated system in any identified prior art. The conditional flag is not about novelty. It is about claim scope: the claim must be drafted narrowly enough around the specific integration mechanism to survive the Alice/Mayo software patent eligibility test and prior art rejections from the broad observability tooling ecosystem. A broad claim on "AI agent observability" fails. A narrow claim on the specific combination described below has a defensible path to grant.

This is the fourth filing in Ron's current urgent queue (NLF, DMS, BPC, and now PKA). That queue requires coordination with patent counsel to prevent any single filing from being delayed past its window by the others.

---

## Section 1: Claim Characterization

**What is the actual invention?**

The invention is a process quality control feedback loop for AI agent orchestration systems, implemented as three mechanically coupled components: (1) a PostToolUse hook that intercepts and logs every tool invocation made by an AI agent to a structured session audit log at the time of occurrence, not as a retrospective trace; (2) a normalized process readiness scoring function that reads the audit log and the task ledger and computes a dimensional score across four orthogonal metrics — throughput (recent delivery velocity), evidence coverage (ratio of delivered tasks bearing non-placeholder structured evidence), verdict accuracy (ratio of GO/NO-GO verdicts that were not subsequently contradicted by reopened tasks or escaped defects), and defect containment (escaped defect count as a penalty term) — reducing these four dimensions to a single 0–100 readiness signal; and (3) a background consolidation pipeline that, in four defined phases (orient, gather, consolidate, prune), reads the session audit logs, the task records, and the agent journals to produce a synthesized intelligence report that is intended to feed into the next session's starting context.

What makes this novel is not any individual component. It is the fact that these three components are mechanically coupled in a single automated pipeline: the tool-call hook generates the raw audit signal, the scorecard consumes the audit signal plus the task ledger to produce a normalized readiness number, and the dream consolidation consumes the same audit signal plus the task and journal state to produce a session-start intelligence packet. The three components share a common data substrate (the session_YYYYMMDD.jsonl audit logs and the YAML-frontmatter task records), and the outputs of each component are specifically designed to feed back into the AI agent's operating context in a subsequent session. No component is optional in this pipeline — removing any one of them breaks the feedback loop. This closed-loop property — from tool invocation to scored process quality to synthesized session context — is the claim.

---

## Section 2: Prior Art Analysis

### What NOVA's competitive landscape tells us

NOVA identified six platforms: CrewAI, AutoGen/MAF, LangGraph, OpenAI Agents SDK, Claude Code Agent Teams. The assessment below maps each against the specific three-component mechanism described in Section 1.

**CrewAI AMP Suite:** CrewAI has per-call tracing, RBAC, and token/cost logging. This is observability tooling — it produces a trace you can look at after the fact in a dashboard. It does not compute a normalized readiness score from the trace. It does not produce a synthesized intelligence report from the trace that is intended to feed back into agent context. The AMP Suite is a monitoring product, not a process quality feedback loop. CrewAI's long-term memory system is a separate component that stores agent knowledge across sessions but is not derived from the observability trace. NOVA correctly identifies that CrewAI has no formal gate between build and ship. The absence of a GO/NO-GO verdict gate means CrewAI's trace data has no pathway into a scored quality signal. The connection between observability and process quality does not exist in CrewAI.

**AutoGen / Microsoft Agent Framework:** AutoGen 0.4 has OpenTelemetry built in and checkpointing for long workflows. The MAF enterprise audit trail was, as of NOVA's research date, still in the GA pipeline. Neither of these constitutes the PKA mechanism. OpenTelemetry produces structured traces but does not compute a normalized readiness score and does not produce a session-start intelligence consolidation. The checkpoint/resume capability is for workflow state persistence, not for process quality scoring. The key gap: AutoGen's observability tooling observes; it does not score and it does not consolidate that score back into session context.

**LangGraph:** LangGraph has immutable state versioning, full node/edge execution history per run, and deterministic replay. This is the strongest observability story of any competitor — the per-run state history is genuine. However, LangGraph's state versioning is scoped to a single run. There is no cross-session scoring function applied to the accumulated run history. There is no normalized readiness metric computed from run history. There is no dream-phase consolidation. LangSmith (a separate commercial product) provides evaluation capabilities, but evaluation of agent output quality is a different function from scoring process quality (evidence coverage, verdict accuracy, defect containment) from an audit trail. NOVA's distinction holds: LangGraph provides the best per-run audit per se; PKA provides a scored, consolidated feedback loop that operates across sessions.

**OpenAI Agents SDK:** Built-in tracing covers LLM calls, tool calls, handoffs, guardrails, and custom events. Visual DAG. Exportable traces. This is a monitoring layer. No normalized process readiness score. No session-start intelligence consolidation. No cross-session audit feedback loop. The Sessions API provides within-session continuity, not cross-session scored process quality.

**Claude Code Agent Teams:** NOVA notes explicitly: "No native audit trail; Ceros (third-party cryptographic audit layer) fills this gap; no per-task ledger." This is the most striking finding for prior art purposes. The platform against which PKA was built does not natively have an audit trail at the task level. This confirms that the specific mechanism PKA implements — attaching a PostToolUse hook to the Claude Code runtime to generate a tool-call-level session audit log and then scoring and consolidating that log into session-start context — is not present in the underlying platform itself.

### Additional prior art LEGAL identified beyond NOVA's scope

**KAIROS (referenced in PKA CHANGELOG):** The PKA CHANGELOG entry for v0.5.0 cites "KAIROS daily-log pattern" as a source. This is an acknowledgment that KAIROS influenced the design. This is a double-edged fact for patent purposes: it establishes that PKA adapted from KAIROS, which could be prior art for the logging component. However, KAIROS's daily-log pattern is a data recording mechanism. The CHANGELOG does not indicate KAIROS has a normalized readiness score function or a dream-phase consolidation. The combination remains novel even if KAIROS anticipates the logging component, because the combination claim is stronger than any individual component claim.

**LangSmith Evaluation Platform (LangChain):** LangSmith offers evaluation dashboards and trace inspection for LangGraph runs. It does not produce a normalized readiness score from an audit trail. It does not produce a session-start intelligence consolidation from that score. LangSmith is a human-facing product, not an automated feedback loop that routes back into agent context.

**MLflow / Weights and Biases (Weave):** These are ML experiment tracking tools. RADAR's filing window note correctly identifies them as the adjacent prior art. MLflow tracks model training runs. W&B Weave tracks LLM call traces. Neither computes a process readiness score against a task ledger with evidence coverage, verdict accuracy, and defect containment as dimensions. Neither produces a session-start intelligence consolidation from that score. They are in an adjacent space (ML observability) but do not overlap with the specific mechanism.

**DreamTask in Claude Code v2.1.88 (referenced in pka_dream.py source code):** This is the most significant prior art risk item in the entire assessment. The `pka_dream.py` docstring explicitly states: "Inspired by DreamTask in Claude Code v2.1.88 (src/tasks/DreamTask/DreamTask.ts): orient -> gather -> consolidate -> prune." The RADAR report also references the "Anthropic Claude Code source leak (v2.1.88, DreamTask pattern)" as confirming these patterns are in active internal development at frontier labs.

This creates two related legal issues that must be addressed before filing:

First, if DreamTask in Claude Code v2.1.88 is available to the public — even through a source leak — it constitutes prior art for the orient/gather/consolidate/prune pipeline structure. The four-phase structure itself is not novel if DreamTask is prior art. The claim must be drafted to focus on the specific combination of inputs (session audit logs + task ledger + agent journals) and the specific outputs (session-start intelligence report + normalized readiness score + audit trail) rather than on the four-phase pipeline structure, which is attributable to DreamTask.

Second, if the PKA codebase contains code derived from a source leak of proprietary Anthropic code, there is a potential copyright infringement issue that is independent of the patent question. If `pka_dream.py` incorporated significant amounts of DreamTask code rather than merely being inspired by its architecture, that raises copyright exposure. Ron needs to assess whether the inspiration was architectural (safe) or textual/structural (potentially infringing). This is a separate legal question from patentability. LEGAL recommends Ron review this with qualified counsel before filing or publishing the PKA codebase. The claim in the docstring that the four-phase pipeline was "inspired by" DreamTask is the right framing if the code is independently written; it is a liability if the code is derived. Clarify this before filing.

**Anthropic's own Claude Code platform:** Anthropic is developing agent orchestration capabilities internally (per RADAR's note about DreamTask). If Anthropic ships a comparable closed-loop scored audit system in Claude Code before Ron files a provisional, it constitutes prior art that may block the claim even if it postdates Ron's conception. Filing quickly limits this risk. Ron cannot control Anthropic's release schedule; he can control his filing date.

### What specifically is NOT in any identified prior art

Across all platforms reviewed, no system has been identified that mechanically couples all three of these components in a single automated pipeline:

- A tool-invocation-level audit hook that fires in real time during agent operation (not as a retrospective trace or log)
- A normalized multi-dimensional process readiness score computed from that audit trail against a structured task ledger with explicit evidence, verdict, and defect dimensions
- A background intelligence consolidation that reads the same audit trail and task state to produce a session-start context document through a defined four-phase pipeline

The combination is the claim. The components individually have prior art. The coupling mechanism has no prior art in any platform surveyed.

---

## Section 3: Filing Recommendation

**Recommendation: GO (Conditional)**

The conditions are:

**Condition 1 — DreamTask copyright clarification:** Before filing or publishing, Ron must determine whether `pka_dream.py` is architecturally inspired by DreamTask (safe for filing) or textually/structurally derived from proprietary Anthropic code (requires counsel review before filing). This does not prevent filing a provisional, but it affects how the dream consolidation component is described in the specification. If the code is independently written and merely follows the same four-phase pattern, the filing proceeds normally. If it is derived, the claim must be scoped to avoid the derived elements and the copyright question must be resolved separately.

**Condition 2 — Repository visibility audit:** The CHANGELOG entry for v0.4.0 states "Repo separated to `rblake2320/verified-agent-ops` (origin fixed from council.git)." This means the code exists in a named GitHub repository. Determine within 48 hours whether `rblake2320/verified-agent-ops` is or has ever been public. A public repository is an enabling disclosure that starts the 12-month AIA clock under 35 U.S.C. § 102(b)(1). If it has been public, determine the earliest date it was made public. That date is the start of the filing window, and the provisional must be filed before the 12-month anniversary of that date.

**If both conditions are met (code is independent, repo is private or has never been public):** The filing window is fully open. File provisional within 30 days. Priority date will be the filing date.

**Claim scope recommendation:** File on the specific combination described in Section 1 — the three-component closed feedback loop — not on any individual component. The individual components (audit logging, process scoring, background consolidation) are each too close to existing prior art to survive as independent claims. The combination, with the specific inputs, outputs, and coupling mechanism described, is the defensible claim.

**What NOT to claim:** Do not claim the four-phase pipeline structure (orient/gather/consolidate/prune) as an independent claim. DreamTask is prior art for the structure. Do not claim "AI agent observability" broadly — the entire observability ecosystem is prior art. Do not claim the scorecard dimensions individually — throughput measurement, defect counting, and verdict tracking each have prior art in software quality metrics literature. Claim the combination.

---

## Section 4: Filing Window

**RADAR's 6–12 month estimate is partially correct and partially optimistic.**

The outer bound of 6–12 months is accurate if the current risk factors do not materialize. But there are three specific events that close the window earlier:

**Risk Event 1 — Anthropic ships a comparable system in Claude Code:** Claude Code is under active development. The DreamTask reference in PKA's own codebase confirms Anthropic has this pattern internally. If Anthropic ships a PostToolUse hook framework with scoring and consolidation as built-in Claude Code features, it becomes prior art against the PKA claim. Timeline: unpredictable, but given the v2.1.88 reference, this could be weeks to months, not a year. This is the highest-probability window-closing event.

**Risk Event 2 — LangSmith or W&B ships a closed-loop scoring system:** If LangSmith adds a normalized readiness score function that feeds back into agent session context — which is a natural product evolution from their existing evaluation platform — the combination claim weakens substantially. Timeline: 6–12 months is a reasonable estimate for this risk.

**Risk Event 3 — The `rblake2320/verified-agent-ops` repository was or becomes public:** If this repository is or has been public, the 12-month AIA clock is running. The window is not 6–12 months from now — it is 12 months minus the time since the earliest public exposure. This risk closes the window immediately upon its materialization if undetected.

**Accurate filing window:** The window is open right now and closes upon the earliest of: the first public disclosure of PKA (whether by Ron or by Anthropic shipping the equivalent), or 12 months from any prior enabling disclosure. Given Risk Event 1, LEGAL revises the effective filing window from RADAR's "6–12 months" to **30–90 days** for a prudent filing strategy. The difference is that RADAR set the outer bound on a general market timeline. The DreamTask prior art risk compresses that bound to 30–90 days.

---

## Section 5: Provisional Application Draft Outline

**Application Title:** System and Method for Continuous Process Quality Feedback in AI Agent Orchestration Systems

### Background of the Invention

The background section should establish: (1) the growth of multi-agent AI orchestration systems, (2) the lack of structured process quality monitoring in existing platforms, (3) the specific problem of AI agent quality drift between sessions — the absence of a mechanism that computes how well an AI agent's process is performing and feeds that signal back into subsequent sessions, (4) the limitations of existing observability tools (they produce traces that require human inspection; they do not produce a scored quality signal; they do not feed back into agent context automatically), and (5) the prior art gap: existing systems observe agent behavior but do not close the loop from observation to scored quality to session context.

The DreamTask reference should be cited as inspiration for the consolidation pipeline structure, with explicit acknowledgment that the novel contribution is the combination with the audit hook and the process readiness score applied to a task ledger with evidence, verdict, and defect dimensions.

### Summary of the Invention

A computer-implemented system and method for continuous process quality feedback in an AI agent orchestration system, comprising: an audit data collection layer that captures structured records of tool invocations made by one or more AI agents during session execution; a process readiness scoring module that computes a normalized quality score from the audit records and a task state ledger using multiple orthogonal quality dimensions; and a background intelligence consolidation module that periodically synthesizes the audit records, task state, and agent journal data into a structured report intended for injection into subsequent agent session contexts; wherein the three components are coupled through a shared structured audit data substrate such that tool invocation data flows automatically from the collection layer through the scoring module and into the consolidation module without human intervention.

### Detailed Description

The detailed description should cover:

- The PostToolUse hook mechanism: how it intercepts tool calls in real time, what fields it captures (timestamp, tool name, session ID, summarized input, summarized result), and how it writes to a date-partitioned JSONL audit log
- The audit log schema: the specific structure of the session_YYYYMMDD.jsonl records as the shared data substrate
- The task ledger schema: the YAML frontmatter fields (task_id, state, owner, verdict, definition_of_done, deliverable_file) and the state machine transitions (new → classified → assigned → in_progress → under_test → under_audit → delivered → archived)
- The process readiness scoring function: the four dimensions (throughput score capped at 25/100, evidence coverage score weighted at 35/100, verdict accuracy score weighted at 25/100, defect containment score weighted at 15/100), the normalization formulas for each, the labeled readiness tiers (elite, strong, workable, not release-ready), and the rationale for the dimension weights
- The background consolidation pipeline: the four phases and their specific functions — orient (enumerate and count available data sources), gather (aggregate statistics across session logs, task records, and agent journals), consolidate (synthesize into a structured intelligence report with activity patterns, delivery velocity, journal health, and log retention signals), and prune (identify session logs older than the retention window for review or deletion)
- The coupling mechanism: how the same session_YYYYMMDD.jsonl data and task records are consumed by both the scoring module and the consolidation module, creating a shared data substrate
- The session context feedback path: how the consolidated intelligence report is made available at the start of the next agent session (via placement in the Owner's Inbox/reports directory, which the session gate reads)
- The lock file mechanism: the .dream lock file that prevents concurrent consolidation runs

### Claims Sketch (3–5 Independent Claims)

**Independent Claim 1 (System):**

A computer-implemented system for process quality feedback in an AI agent orchestration system, the system comprising: a hook component configured to intercept tool invocations made by at least one AI agent during a session and write structured records of each invocation to a persistent session audit log in real time during session execution; a process readiness scoring component configured to read the session audit log and a structured task ledger and compute a normalized process quality score based on at least: a delivery throughput metric derived from task records with a delivered state updated within a defined time window; an evidence coverage metric derived from the ratio of delivered task records containing structured non-placeholder evidence fields to total delivered task records; a verdict accuracy metric derived from the ratio of GO/NO-GO verdicts associated with delivered task records that were not subsequently contradicted by escaped defect records; and a defect containment metric derived from the count of task records containing escaped defect indicators; and a consolidation component configured to read the session audit log, the task ledger, and one or more agent journal files and produce a structured intelligence report summarizing activity patterns, task delivery state, and agent journal health, wherein the intelligence report is written to a location accessible to the AI agent at the start of a subsequent session.

**Independent Claim 2 (Method):**

A computer-implemented method for providing process quality feedback in an AI agent orchestration system, the method comprising: intercepting, via a hook registered with an AI agent execution environment, tool invocations made by the AI agent and writing a structured record of each tool invocation to a session audit log; reading the session audit log and a task state ledger to compute a normalized process readiness score using a weighted combination of a delivery throughput dimension, an evidence coverage dimension, a verdict accuracy dimension, and a defect containment dimension; executing a background consolidation pipeline comprising: an orient phase that enumerates available session audit logs, task records, and agent journals; a gather phase that aggregates tool call statistics, task state distributions, and agent journal entry counts from the enumerated data sources; a consolidate phase that produces a structured intelligence report from the aggregated statistics; and a prune phase that identifies session audit logs outside a defined retention window; and writing the structured intelligence report to a location configured to be read by the AI agent at session initialization.

**Independent Claim 3 (The Session Continuity Feedback Loop):**

A computer-implemented system for continuous process quality monitoring across sessions of an AI agent orchestration system, comprising: a persistent audit data substrate comprising at least one session log file containing structured records of tool invocations made by at least one AI agent, wherein each record includes a timestamp, a tool identifier, a session identifier, and a summarized input and result for the invocation; a process readiness scoring component coupled to the persistent audit data substrate and to a task state ledger, the scoring component configured to produce a normalized score on a defined scale based on quality dimensions derived from both the audit data substrate and the task state ledger; and a background consolidation component coupled to the persistent audit data substrate and to one or more agent journal files, the consolidation component configured to execute without human initiation and produce a session context document from the audit data and journal state, wherein the session context document is made available to the AI agent orchestration system before the initiation of a subsequent agent session; wherein the scoring component and the consolidation component share the same persistent audit data substrate such that tool invocation data is captured once and consumed by both components.

**Dependent Claim 4 (on Claim 1 or 3 — the specific scoring formula):**

The system of Claim 1, wherein computing the normalized process quality score comprises: assigning a throughput score equal to a product of a count of task records updated to a delivered state within a thirty-day window and a first scalar constant, bounded by a first maximum value; assigning an evidence coverage score equal to a product of a second scalar constant and the ratio of delivered task records containing non-placeholder evidence sections to total delivered task records; assigning a verdict accuracy score equal to a product of a third scalar constant and the ratio of task records bearing a verdict indicator and not containing escaped defect language to total task records bearing a verdict indicator; assigning a defect containment score equal to a fourth maximum value reduced by a penalty per task record containing escaped defect language; and computing the normalized process quality score as the sum of the throughput score, the evidence coverage score, the verdict accuracy score, and the defect containment score.

**Dependent Claim 5 (on Claim 1 or 3 — the lock-protected background execution):**

The system of Claim 1, wherein the consolidation component is further configured to acquire an exclusive file-system lock before executing the consolidation pipeline and release the lock upon completion, such that concurrent executions of the consolidation pipeline are prevented.

### Abstract

A system and method for continuous process quality feedback in AI agent orchestration environments. A PostToolUse hook intercepts tool invocations made by AI agents in real time and writes structured records to a date-partitioned session audit log. A process readiness scoring component reads the session audit log and a structured task ledger to compute a normalized quality score across delivery throughput, evidence coverage, verdict accuracy, and defect containment dimensions. A background consolidation component reads the same audit log, task ledger, and agent journal files to produce a structured session context document through orient, gather, consolidate, and prune phases. The three components share a common persistent audit data substrate, creating a closed feedback loop from tool invocation to scored process quality to synthesized session context available at subsequent session initialization.

---

## Section 6: Action Items (Ordered by Priority)

**Action 1 — Within 48 hours:** Audit the visibility of the `rblake2320/verified-agent-ops` GitHub repository. Log in to GitHub and check: (a) is the repository currently public or private; (b) has it ever been public (check GitHub settings history, any prior commits, and any web indexing by searching Google for "site:github.com rblake2320 verified-agent-ops"); (c) has any other PKA-related repository ever been public with code containing the scorecard, hook, or dream consolidation logic. Report the earliest enabling disclosure date to patent counsel. This is the single most important factual determination before filing.

**Action 2 — Within 48 hours:** Assess the DreamTask copyright question. Review `pka_dream.py` and compare it to the DreamTask source (if accessible) to determine whether the four-phase pipeline is independently implemented or textually derived from the Anthropic codebase. If the implementation is independent (same architecture, different code), document that fact. If there is any substantial similarity in code structure beyond the four phase names, consult qualified counsel on both the copyright question and how to characterize the invention in the patent specification to avoid claims that read on derived code.

**Action 3 — Within 30 days:** Engage a qualified patent prosecution attorney with AI systems and software patent experience. Brief them on: (a) the three-component combination claim described in this document; (b) the DreamTask prior art risk and the copyright clarification from Action 2; (c) the repository disclosure status from Action 1; (d) the existence of three other pending urgent filings (NLF, DMS, BPC) so counsel can coordinate priority dates and manage the queue. File a provisional patent application covering the full system as described in the Section 5 outline.

**Action 4 — Within 30 days, concurrent with Action 3:** Do not make the `rblake2320/verified-agent-ops` repository public and do not write or publish any blog post, technical writeup, forum post, or social media post describing the PKA scored audit trail mechanism until the provisional is filed. A single enabling public disclosure before the provisional is filed irrevocably starts the AIA clock and eliminates European Patent Convention protection (EPC has no inventor grace period). RADAR's Observation 2 recommends open-sourcing the scaffold for distribution purposes — this must wait until after the provisional is filed.

**Action 5 — Within 60 days of provisional filing:** Commission a targeted prior art search on the specific combination claim against: LangSmith (LangChain), Weights and Biases Weave, MLflow, and any Anthropic patent applications filed in 2025–2026 covering agent orchestration observability. The search should focus specifically on whether any prior art document or application discloses the combination of a real-time tool-call hook, a normalized multi-dimensional process quality score derived from that hook's output against a task ledger, and a background consolidation pipeline that feeds back into session context. Budget $1,500–$2,500 for a professional search. Results determine whether the independent claims in the non-provisional should be adjusted before filing.

**Action 6 — Coordinate with the NLF/DMS/BPC queue:** As noted in the BPC assessment (LEGAL-bpc-patent-assessment.md), Ron has three other urgent provisional filings already identified. Patent counsel should be briefed on all four simultaneously. The PKA claim is independent of the NLF, DMS, and BPC claims — there is no overlap in subject matter — but managing four provisional filings in a 30-day window requires coordinated attorney engagement. Confirm with counsel that the PKA provisional can be included in the same engagement window as the other three.

---

## Risk Summary

| Risk | Level | Rationale |
|------|-------|-----------|
| DreamTask prior art on four-phase consolidation | High | Explicitly cited in source code. Claim must not rely on the phase structure as the novel element. |
| Alice/Mayo software patent eligibility | Medium-High | AI system software claims face Alice scrutiny. Mitigation: anchor every claim element to a concrete data structure or file-system operation, not abstract quality concepts. |
| Repository public disclosure | Medium-High | A GitHub repository exists. Visibility status is unknown. If public, the clock is running and the window may be narrowed. Determine immediately. |
| Anthropic ships equivalent before filing | Medium-High | DreamTask pattern is in active internal development at Anthropic. Filing before this materializes is the only mitigation. |
| Broad observability ecosystem (LangSmith, W&B, MLflow) | Medium | Adjacent prior art. Mitigated by claiming the specific combination, not observability broadly. |
| Copyright exposure on pka_dream.py | Medium | Requires factual determination before filing. If the code is independently written, this risk is Low. |
| RADAR open-sourcing recommendation (Observation 2) | Low if sequenced correctly | If the scaffold is open-sourced before the provisional is filed, it becomes a prior art disclosure. The open-source release must follow the provisional filing, not precede it. |

---

## What This Patent Is Worth If Granted

A granted patent on the specific three-component closed-loop mechanism has licensing value in the enterprise AI operations market. The addressable licensees are: vendors building agent orchestration platforms (CrewAI, LangChain, Microsoft MAF) who would read on the claim if they ship a comparable integrated system; enterprise AI governance tooling vendors (companies building compliance and audit layers for AI agent deployments, which is an emerging market segment); and developer tooling vendors (GitHub, JetBrains, Atlassian) building AI coding assistant governance tools for enterprise customers.

Conservative licensing value estimate for a granted US patent: $200,000–$2,000,000 NPV over patent life, assuming the enterprise AI governance tooling market reaches scale by 2028–2030 and a 0.25%–1.0% royalty rate on implementations that read on the specific combination claim. This estimate is rough. A qualified IP valuation firm would be required for any licensing negotiation or investor-facing representation. The value is meaningful but secondary to the defensive value: a granted patent prevents competitors from freely implementing the same closed-loop mechanism and claiming it as their own.

---

*Note on the patent queue: LEGAL has now identified four urgent provisional filings in Ron's portfolio (NLF — project_nlf_system.md, DMS — project_dms.md, BPC — LEGAL-bpc-patent-assessment.md, and this PKA claim). All four are in the 30-day urgent filing window per their respective assessments. This is a resource constraint, not a legal constraint — the filings are independent and non-conflicting. But attempting to engage patent counsel on four simultaneous provisional applications without advance notice creates execution risk. Brief counsel on all four in one call, confirm capacity, and establish a parallel-track filing schedule before the 30-day window closes on any one of them.*

---

*LEGAL does not practice law. This document identifies issues, assesses risk levels, and recommends engagement of qualified legal counsel. Engage a registered USPTO patent practitioner before any filing action. Do not publicly disclose the PKA scored audit trail mechanism, the verified-agent-ops repository, or any code or documentation enabling a person skilled in the art to practice this invention before a provisional application is filed.*

*LEGAL — IP Strategy, Patents and Legal Risk*
*PKA AI Team — 2026-04-02*
