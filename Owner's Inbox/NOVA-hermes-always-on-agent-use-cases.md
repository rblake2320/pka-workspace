# NOVA: Always-On AI Agent Use Cases for Hermes
**Date**: 2026-03-31
**Prepared for**: Ron
**Context**: Hermes running 24/7 on Spark-1 (GB10, 120GB RAM, RTX 5090 equivalent), SSH to Spark-1/2, local LLMs (no cloud cost), Telegram delivery

---

## Objective
Rank the highest-value, most-impressive, actually-deployed use cases for an always-on AI agent with Telegram interface, terminal/SSH access, and local LLMs — filtered specifically for Ron's stack.

---

## Key Findings

The signal across GitHub, arXiv, homelab communities, and AI agent forums points to one clear truth: **the biggest leverage gap is between people running reactive chatbots and people running proactive autonomous agents on a cron schedule with persistent memory.** Ron's setup (120GB RAM, local 70B models, SSH to multiple machines, no cloud cost) puts him in the top 0.1% of homelab operators. Most impressive use cases below require exactly that kind of infrastructure.

The 5 highest-ROI categories are:
1. Overnight autonomous software engineering (SWE-agent class)
2. Financial market intelligence synthesis (TradingAgents/FinRobot class)
3. Competitive and research intelligence monitoring (deep research agents)
4. Security scanning and self-audit of own infrastructure
5. Cross-machine system health intelligence with proactive remediation

---

## Ranked Use Cases

### 1. Overnight Software Engineering Agent
**What it does**: Give Hermes a list of open GitHub issues or TODO items across your repos before you go to sleep. It runs SWE-agent or mini-SWE-agent (100-line scaffold) against them using your local LLM, creates branches, writes fixes, and sends you a Telegram summary with diffs by morning.

**Why it's high-value**: mini-SWE-agent scores >74% on SWE-bench Verified with Claude. OpenHands CodeAct 2.1 resolves 53% of real GitHub issues without human intervention. With your 70B model on Spark-1, real-world issue resolution overnight is not hypothetical — it's deployed. You have 40+ active projects with open issues.

**Complexity**: Medium — SWE-agent has local LLM support via Ollama backend. Wire output to Telegram.

**Fits Ron's setup**: Direct fit. SSH to Spark-1/2, git repos already there, Ollama running 46 models. Schedule via cron, morning Telegram report.

**Source**: [SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent) | [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | [OpenHands](https://openhands.dev/)

---

### 2. Nightly Financial Intelligence Briefing
**What it does**: Hermes runs TradingAgents multi-agent framework overnight (Ollama backend, configured with llm_provider: "ollama"). Specialized sub-agents — fundamental analyst, sentiment analyst, technical analyst, bear/bull debate agents — each ingest market data for a watchlist. A synthesis agent writes an equity brief. Delivered to Telegram at 7AM.

**Why it's high-value**: TradingAgents framework (arXiv 2412.20138) shows that multi-agent debate significantly outperforms single-agent analysis in backtests. FinRobot generates professional equity research reports from local models. This runs at $0 marginal cost with your GB10 cluster vs. Bloomberg terminal pricing.

**Complexity**: Complex — but TradingAgents supports Ollama natively. Requires data feed (yfinance is free, good enough for personal use).

**Fits Ron's setup**: Strong fit. GB10 handles 70B for overnight batch. No cloud cost. Telegram delivery trivial via existing Hermes setup.

**Source**: [TradingAgents](https://github.com/TauricResearch/TradingAgents) | [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | [AlphaAgents arXiv](https://arxiv.org/html/2508.11152v1)

---

### 3. Deep Research Digest on arXiv + Competitive Landscape
**What it does**: Hermes monitors arXiv categories (cs.AI, cs.CL, cs.LG, q-fin.TR) nightly via RSS. New papers are fetched, abstracts embedded, clustered by relevance to Ron's patent portfolio and active projects. A local LLM writes a 1-page synthesized brief: "What dropped last night that matters to you." Delivered to Telegram every morning.

**Why it's high-value**: arXiv publishes 200-400 AI papers per day. Manual triage is impossible. This is the gap between staying ahead and getting blindsided by prior art or a competitor. The brief can include: patent risk flags, technique extraction for NLF/DMS, competitive moves on aihangout.ai verticals.

**Complexity**: Medium — RSS + embedding + local LLM summarization. No exotic dependencies.

**Fits Ron's setup**: Perfect fit. Ultra RAG already does embedding + semantic search. Wrap with a cron job and Telegram push. Legal-relevant findings auto-tag for LEGAL agent review.

**Source**: [Deep Research Survey arXiv](https://arxiv.org/abs/2508.12752) | [Awesome AI Agent Papers GitHub](https://github.com/VoltAgent/awesome-ai-agent-papers)

---

### 4. Autonomous Penetration Testing of Own Infrastructure (PentAGI)
**What it does**: PentAGI is a fully autonomous multi-agent security scanner that orchestrates 20+ tools (Nmap, Metasploit, sqlmap, etc.) against a defined target scope. You point it at your own servers (Spark-1, council :8601, aihangout.ai staging, DataShield endpoints). It runs overnight, stores all findings in PostgreSQL with pgvector, and delivers a structured vulnerability report to Telegram.

**Why it's high-value**: You have 15+ live services across Spark-1/2, VPS, and Windows PC. CRUCIBLE does manual test runs. PentAGI runs continuously and finds what humans miss on late-night deploys. This is the difference between "we think it's secure" and "it was probed at 3AM and here's what was exposed."

**Complexity**: Complex — Docker-based deployment, scope definition required, needs isolated network targeting to avoid hitting prod unintentionally.

**Fits Ron's setup**: Strong fit. PostgreSQL + pgvector already running on Spark-1. Docker already running. Telegram webhook trivial. Run against staging/dev targets first.

**Source**: [PentAGI GitHub](https://github.com/vxcontrol/pentagi) | [PentAGI site](https://pentagi.com/)

---

### 5. Proactive Cross-Machine System Health Intelligence
**What it does**: Hermes runs a scheduled health intelligence loop every 15 minutes. It SSH-tunnels into Spark-1 and Spark-2, collects: service status, disk usage trends, GPU utilization, RAM pressure, failed jobs, error log spikes, S3 backup confirmation, Ollama queue depth. A local LLM interprets the data (not just thresholds — actual interpretation). Only messages Ron when something is anomalous, wrong, or trending toward a failure.

**Why it's high-value**: You currently rely on manual checks and crash watchers. The system now has 15+ services across 3 machines. An LLM reading logs can catch "NCCL timeout errors are increasing — distributed training will fail in ~2 hours" before the process crashes. The homelab community calls this the single highest-leverage always-on agent task.

**Complexity**: Simple to medium — mostly SSH + log parsing. The LLM reasoning layer on top is the novel part.

**Fits Ron's setup**: Perfect fit. Hermes already has SSH access. Spark-1 already runs the AI Army OS heartbeat system. This extends it with intelligence rather than just pinging.

**Source**: [Homelab AI Stack DEV Community](https://dev.to/signal-weekly/the-homelab-ai-stack-in-2026-what-self-hosters-are-actually-running-2d58) | [Homelab Automation BSWEN](https://docs.bswen.com/blog/2026-03-27-homelab-automation-ai-agent/)

---

### 6. Autonomous Competitive Intelligence Monitor (Competitor + Patent Tracking)
**What it does**: Hermes monitors a defined target set of competitor sites, product pages, GitHub repos, and patent databases (USPTO, Google Patents). When something changes — new feature launch, new patent filing, pricing change, new blog post — the LLM classifies the signal, writes a 2-sentence impact statement for Ron's business, and Telegrams only the high-signal hits.

**Why it's high-value**: You have DataShield, aihangout.ai, AgentForge, Pay2KnowMe, and 3+ patent patent portfolios in active competitive markets. Manual monitoring is impossible. Browse AI and similar tools do this commercially at $200+/month; you can run it at $0 with your stack.

**Complexity**: Medium — web scraping + diff detection + LLM classification. Playwright already in your stack (LUCIE).

**Fits Ron's setup**: Strong fit. Playwright installed, local LLMs available, Telegram output already wired. Patent monitoring could feed directly into LEGAL agent review queue.

**Source**: [Browse AI](https://www.browse.ai/) | [ScrapeGraphAI](https://scrapegraphai.com/)

---

### 7. Nightly Full-Codebase Audit + Tech Debt Report
**What it does**: Hermes runs a static analysis + LLM review pass across a rotating set of your repos overnight. Tools: ruff/pylint/eslint for syntax, but more importantly, a local LLM reads changed files from the last 7 days and flags: security anti-patterns, hardcoded credentials (pattern match first, then LLM confirm), dead code, inconsistent error handling, missing test coverage on new functions. Telegram report with ranked issues.

**Why it's high-value**: You have 40+ projects and ship fast. CRUCIBLE catches functional bugs in testing but tech debt accumulates silently. A nightly audit on your most active repos (aihangout-app, council, DataShield, AgentForge) costs you nothing and catches the issues before they become incidents.

**Complexity**: Medium — git diff + static analysis is trivial; LLM-layer review requires good prompting but no exotic tooling.

**Fits Ron's setup**: Perfect fit. All code is accessible via SSH from Hermes. Schedule as cron, rotate repos weekly.

**Source**: [How to Run Claude Code as Autonomous Agent](https://dev.to/boucle2026/how-to-run-claude-code-as-an-autonomous-agent-with-a-cron-job-hec) | [Hermes Agent NousResearch](https://github.com/NousResearch/hermes-agent)

---

### 8. Automated Memory Ingestion + Knowledge Base Freshness
**What it does**: Hermes watches for new documents landing in designated drop folders (on Windows PC or Spark-1). When something new appears — a PDF, a chat export, a markdown note, a code file — it automatically runs embedding + ingest into Ultra RAG, tags it with project context, and confirms via Telegram. Also runs a nightly "stale knowledge" scan: memories older than 90 days that haven't been accessed are flagged for pruning or refresh.

**Why it's high-value**: MemoryWeb has 4,002 memories but the last ingestion was 2026-03-02. The `mw_post_session.py` hook isn't firing (noted in MEMORY.md). This is a known gap causing your own AI agents to work from stale context. Automating this closes a real bottleneck in your personal productivity stack.

**Complexity**: Simple — file watch + existing Ultra RAG ingest pipeline. The new part is the LLM-powered staleness classifier.

**Fits Ron's setup**: Perfect fit. Ultra RAG ingest script already exists at Spark-1. This just adds the watch loop and Telegram confirmation.

**Source**: [Knowledge Agent Template Vercel](https://github.com/vercel-labs/knowledge-agent-template) | [Ultra RAG project memory](../memory/project_ultra_rag.md)

---

### 9. Job Application Agent (or Lead Generation Agent)
**What it does**: Hermes monitors federal contracting opportunities (SAM.gov), government IT contract awards, and relevant job boards on a schedule. For GovCon/Acq-Copilot targets: it finds new solicitations matching a defined profile (keywords, NAICS codes, dollar thresholds), writes a first-pass qualification summary ("Why Ron wins or loses this bid"), and Telegrams the hot ones. One developer built this to apply to jobs while he slept — the same pattern applies to contract hunting.

**Why it's high-value**: Federal contracting opportunities have short response windows. Missing a SAM.gov posting because you weren't monitoring it is a direct revenue miss. Your GovCon Platform already has SAM.gov integration — Hermes becomes the 24/7 watch dog.

**Complexity**: Medium — SAM.gov API is public, well-documented. LLM scoring of opportunity fit is the value-add layer.

**Fits Ron's setup**: Strong fit. GovCon Platform on Spark-1. Acq-Copilot knowledge already trained. This extends your existing infrastructure as an always-on bidding intelligence layer.

**Source**: [AI Agent That Applies to Jobs While You Sleep - DEV Community](https://dev.to/nathanhamlett/i-built-an-ai-agent-that-applies-to-jobs-while-i-sleep-43og)

---

### 10. Self-Improving Skills Library (Hermes Native Feature)
**What it does**: NousResearch Hermes Agent natively creates new skills after completing complex tasks. When Hermes solves a novel problem (e.g., a new type of API integration, a new parsing pattern, a new deployment procedure), it writes that as a reusable skill, stores it locally, and optionally publishes to agentskills.io. Over time, the agent gets measurably faster and more capable at your specific workflows.

**Why it's high-value**: This is the difference between an agent that plateaus and one that compounds. After 30 days of active use, a skill-creating agent completes recurring tasks 3-5x faster because it has memorized the exact shell commands, API patterns, and preferences for your environment. This is the "flywheel" for personal AI productivity.

**Complexity**: Simple — this is a built-in Hermes Agent feature, not a custom build.

**Fits Ron's setup**: Perfect fit. Ron already runs NousResearch Hermes on Spark-1 (`~/hermes-agent/`). Activating skill auto-creation just requires enabling the feature.

**Source**: [Hermes Agent NousResearch](https://hermes-agent.nousresearch.com/) | [Hermes Agent Messaging Gateway](https://www.mintlify.com/NousResearch/hermes-agent/user-guide/messaging)

---

### 11. Live-SWE-Agent: Self-Evolving Code Scaffold
**What it does**: Live-SWE-agent is not just a code fixer — it autonomously evolves its own scaffold while solving problems. It starts with a minimal bash tool and writes its own extensions as it discovers gaps. Running this locally on your repos means you get an agent that becomes specifically adapted to your codebases over time. Achieves 79.2% on SWE-bench Verified with Claude Opus 4.5.

**Why it's high-value**: Current state-of-the-art for autonomous software engineering. The self-evolution aspect means it's not a static tool — it improves itself during the work session. For Ron's 40+ repos, this is a force multiplier.

**Complexity**: Complex — requires careful sandboxing so self-modification doesn't escape the target scope.

**Fits Ron's setup**: Strong fit with sandboxing. Docker isolation on Spark-1 is the right container for this.

**Source**: [Live-SWE-agent arXiv](https://arxiv.org/html/2511.13646v3) | [Live-SWE-agent GitHub](https://github.com/OpenAutoCoder/live-swe-agent)

---

### 12. Automated Meeting/Audio Transcription + Action Item Extraction
**What it does**: Hermes watches a folder for new audio/video files (Zoom recordings, voice memos, phone call recordings). Whisper transcribes, a local LLM extracts action items, decisions, open questions, and project tags. Output goes into the appropriate project memory file in Ultra RAG and a Telegram summary with extracted TODOs is sent immediately.

**Why it's high-value**: Knowledge that lives in unprocessed recordings is dead knowledge. This turns every recorded conversation into a structured memory entry with zero manual effort. The n8n homelab community calls this one of the most practical always-on agent workflows — "a folder watcher, Whisper, and Ollama" is 80% of the build.

**Complexity**: Simple to medium — Whisper is already available on your stack. The LLM action-item extraction prompt is the only novel component.

**Fits Ron's setup**: Strong fit. Whisper available locally, Ultra RAG ingest already works, Telegram output trivial.

**Source**: [n8n Ollama Workflows](https://blog.n8n.io/local-llm/) | [Homelab AI Stack 2026](https://dev.to/signal-weekly/the-homelab-ai-stack-in-2026-what-self-hosters-are-actually-running-2d58)

---

### 13. Autonomous PR Review Bot for Your Own Repos
**What it does**: Hermes watches GitHub webhooks (or polls via API) for new PRs across your repos. When a PR opens, it automatically: checks out the branch, runs the test suite, has the local LLM review the diff for bugs/style/security issues, and posts a structured code review comment. You see a Telegram notification: "PR #47 in council — 2 issues flagged, tests pass."

**Why it's high-value**: You are a solo operator across 40+ projects. Getting a code review before you merge is often skipped because there's no second reviewer. This provides a consistent, zero-cost second opinion on every merge.

**Complexity**: Medium — GitHub webhooks + local git + LLM diff review. OpenCode and Hermes both have documented patterns for this.

**Fits Ron's setup**: Strong fit. All repos accessible via SSH. GitHub API is free-tier capable for personal use.

**Source**: [OpenCode Architecture](https://sesamedisk.com/opencode-ai-coding-agent-architecture/) | [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)

---

### 14. Ouroboros Pattern: Self-Modifying Agent with Sandboxed Evolution
**What it does**: An agent that is given permission to rewrite its own code within a sandboxed container. Inspired by the Ouroboros-max project (born Feb 16, 2026, evolved through 30+ self-directed cycles in 24 hours with zero human intervention). The agent monitors its own failure modes, identifies bottlenecks, writes patches, tests them in isolation, and promotes successful ones to production.

**Why it's high-value**: This is the bleeding edge. No one has fully solved safe self-modification, but sandboxed versions are running now. Ron's AI Army OS already has autonomous task execution; adding a self-improvement loop to a non-critical service (e.g., the AI Army dashboard) would generate real evidence for Patent #9 (NLF Teacher-Student) and demonstrate a live version of the flywheel.

**Complexity**: Complex — requires strict Docker sandbox, rollback mechanism, and approval gate before promotion.

**Fits Ron's setup**: Fits with caution. Run only in Docker on Spark-2 (isolated). Never pointed at production. This is also patent evidence material.

**Source**: [Ouroboros-max GitHub](https://github.com/AntonAndrusenko/ouroboros-max)

---

### 15. Autonomous Data Freshness Agent for aihangout.ai
**What it does**: Hermes monitors aihangout.ai platform health metrics overnight: new user registrations, post volume trends, API error rates, content moderation queue depth, Telegram bot response times. When a metric drops outside normal range, it doesn't just alert — it diagnoses: checks logs, identifies the relevant service, attempts a known fix (restart, cache clear, config reload), and only escalates to Ron if it can't resolve automatically.

**Why it's high-value**: aihangout.ai is live post-launch. Night-time user activity happens. An issue at 2AM that doesn't get fixed until 8AM is 6 hours of degraded experience for real users. Auto-remediation of the 80% of issues that are simple (service crash, Redis OOM, hung process) means Ron's platform self-heals while he sleeps.

**Complexity**: Medium — monitoring is simple; the auto-remediation playbook is the work. Start with 5 known failure modes, build from there.

**Fits Ron's setup**: Perfect fit. Hermes already has SSH to Spark-1/VPS. aihangout.ai services are documented. This is the most direct platform-protection use case.

**Source**: [Hermes Agent — Autonomous Tasks](https://hermes-agent.nousresearch.com/) | [Homelab AI Automation](https://docs.bswen.com/blog/2026-03-27-homelab-automation-ai-agent/)

---

### 16. Quantitative Portfolio Optimization Agent (Overnight Batch)
**What it does**: Hermes runs the NVIDIA Quantitative Portfolio Optimization blueprint (already cloned to Spark-1 `~/ai-business/quantitative-portfolio-optimization/`) on a weekly schedule. Feeds it updated price data, runs multi-factor optimization, generates a rebalancing recommendation, and sends a structured Telegram brief: "Current allocation vs. optimal, 3 moves to make, risk explanation."

**Why it's high-value**: This blueprint exists in your repo and hasn't been operationalized. It uses your local GPU. The gap between "cloned a repo" and "woke up to an investment brief every Sunday morning" is about 4 hours of wiring work.

**Complexity**: Medium — blueprint is already cloned; needs data feed wiring and Telegram output.

**Fits Ron's setup**: Perfect fit. Spark-1 has the blueprint. Just needs data ingest and output routing to Telegram.

**Source**: [NVIDIA Blueprints on Spark-1] (internal — already cloned) | [AlphaAgents arXiv](https://arxiv.org/html/2508.11152v1)

---

### 17. Telegram-Triggered Computer Use Agent
**What it does**: Ron sends a Telegram message: "Download the latest EEOC compliance report, extract the key numbers, add them to the DataShield pitch deck." Hermes receives the message, uses a browser automation agent (Playwright — already in LUCIE stack) to navigate to the EEOC site, downloads the PDF, OCR-extracts the data (DataShield already has NVIDIA OCR), generates the slides, and confirms completion via Telegram. End-to-end: human sends one message, receives a finished artifact.

**Why it's high-value**: This is the OpenClaw pattern that got 250,000 GitHub stars. The viral demos were: "I texted it, it booked my flight." The same pattern applied to business tasks (research → doc → artifact) is 10x more valuable than consumer demos. Ron has all the components.

**Complexity**: Complex — multi-step with state, browser automation, OCR, document generation. But all components are deployed.

**Fits Ron's setup**: Strong fit. Playwright in LUCIE, OCR in DataShield, Telegram wired via Hermes. Requires workflow orchestration glue.

**Source**: [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) | [OpenClaw Use Cases 2026](https://skywork.ai/skypage/en/openclaw-ai-agents-automation/2036708876028346368)

---

### 18. Nightly LoRA Adapter Evaluation + Model Drift Detection
**What it does**: You have 53 LoRA adapters trained. Hermes runs a lightweight eval suite overnight against each active adapter using a fixed test set. It compares today's scores against the baseline. If a model shows degradation (e.g., MK Seller Copilot answers are shorter, less specific, or the eval score drops >5%), Hermes flags it immediately via Telegram with: which adapter, which eval category degraded, and the recommended action (retrain, rollback, or investigate).

**Why it's high-value**: Model drift is real and sneaky. Models in production (MK Seller Copilot :8767, CarSales, TravelAgent) can degrade without obvious crashes. Catching this weekly rather than when a user complains is the professional way to run a model portfolio.

**Complexity**: Medium — eval suite already partially exists (carsales_hammer_suite.py, various test files in repo). Hermes just runs them on a schedule and interprets the output.

**Fits Ron's setup**: Perfect fit. All adapters, evals, and Ollama instances are local. Schedule: nightly eval, weekly full suite.

**Source**: Internal — Ron's eval scripts already exist in Spark-1 home directory.

---

### 19. Autonomous Patent Prior Art Monitor
**What it does**: Hermes monitors Google Patents and USPTO for new filings in your patent space: autonomous AI coordination systems, neural compression (DMS), teacher-student learning (NLF), AI router platforms. When a new patent publishes or a patent application enters your claim space, it: (a) downloads the full text, (b) has the local LLM compare claims against your provisional applications, (c) classifies as "no conflict," "monitor," or "URGENT — consult attorney," and (d) Telegrams Ron immediately on "URGENT" findings.

**Why it's high-value**: You have 40+ patents in various stages, including provisionals on NLF (Patent #9), DMS (#10), NLF+DMS integration (#11), and AI Router (#P-001-003). Prior art published after your provisional filing date doesn't hurt you, but prior art you miss before filing does. This is a legal risk monitoring system running at $0.

**Complexity**: Medium — Google Patents has an unofficial API; USPTO has an official one. LLM claim comparison is the intelligence layer.

**Fits Ron's setup**: Strong fit. Feeds directly into LEGAL agent's queue. Flag outputs go to `Owner's Inbox/` for LEGAL review.

**Source**: [LEGAL patent provisionals memory](../memory/patent_portfolio.md)

---

### 20. Automated Daily Standup: AI Army Status Digest
**What it does**: Every morning at 8AM, Hermes polls all AI Army components (AI Army OS :8500, AI Army Hub :8765, all Spark-1/2 services, S3 backup status, Cloudflare tunnel health, MemoryWeb freshness, Ultra RAG collection stats). It writes a 10-line executive brief: what ran overnight, what succeeded, what failed, what needs attention today. Delivered to Telegram before Ron opens his laptop.

**Why it's high-value**: You have 15+ active services across 3 machines. Currently there is no unified morning brief. You find out about overnight failures reactively. This closes that gap with a single always-on process that takes 30 minutes to set up.

**Complexity**: Simple — this is pure polling + LLM synthesis. No complex dependencies.

**Fits Ron's setup**: Perfect fit. All APIs and endpoints are known. This is the entry point — build this first before the more complex automations above.

**Source**: [Morning Briefing AI Agent](https://blog.fundmore.ai/i-built-an-ai-agent-that-briefs-me-every-morning-heres-what-changed) | [AI Army OS memory](../memory/project_ai_army_os.md)

---

## Evidence Summary

| Source | Type | Strength |
|--------|------|----------|
| SWE-agent (NeurIPS 2024, 53% SWE-bench) | Research + deployed open source | Strong |
| OpenHands CodeAct 2.1 (53% SWE-bench) | Research + deployed open source | Strong |
| mini-SWE-agent (74% SWE-bench verified) | Deployed open source | Strong |
| TradingAgents (arXiv 2412.20138) | Research with Ollama backend | Strong |
| PentAGI (12,500+ GitHub stars, production deployments) | Community-validated | Strong |
| Hermes Agent / NousResearch (production, active development) | Deployed | Strong |
| Ouroboros-max (early, 30+ self-directed cycles reported) | Early stage | Moderate |
| Live-SWE-agent (arXiv 2511.13646, 79.2% SWE-bench) | Research, not yet widely deployed | Moderate |
| Homelab AI Stack DEV Community reports | Community anecdote | Moderate |

---

## Risks

1. **Local LLM quality gap**: Some of these (SWE-agent, TradingAgents) were benchmarked on Claude/GPT-4. Your 70B model (llama3.1:70b) will perform lower. The tasks still work — expect 60-70% of the benchmark ceiling, not 100%.

2. **Overnight jobs consuming GPU memory**: If multiple overnight jobs queue simultaneously (code audit + fin analysis + SWE-agent), GPU contention on Spark-1 is real. Need job scheduling with mutex locks.

3. **PentAGI scope creep**: Must be pointed at isolated/staging targets only. A misconfigured scope that hits production or external targets is a security and legal incident.

4. **Self-modifying agent (Ouroboros pattern)**: This is the highest risk item. Sandboxing must be air-tight. Do not deploy without Docker isolation + rollback mechanism.

5. **Patent monitor false positives**: LLM claim comparison is not a lawyer. "No conflict" from the LLM is not legal clearance. Use as a triage layer, not a final determination.

---

## Recommendation

**Start with #20 (Daily Standup Digest) and #5 (Cross-Machine Health Intelligence).** Both are simple, deliver immediate value, and prove the pattern. Once these are running, add #3 (arXiv digest) and #8 (memory ingestion automation) — both close known gaps in your current stack. Then graduate to #1 (overnight SWE-agent) and #2 (financial briefing).

Priority order for first 30 days:
1. Daily standup digest (#20) — 30-minute build, immediate payoff
2. Cross-machine health intelligence (#5) — closes the "crash at 3AM" gap
3. arXiv + competitive digest (#3) — positions you on research and patent landscape
4. Memory ingestion automation (#8) — fixes the known MemoryWeb staleness problem
5. Overnight code issue fixer (#1) — the highest-leverage coding productivity tool

Hold #14 (self-modifying agent) and #11 (Live-SWE-agent) until the simpler ones are stable. Those require careful sandboxing and are not for the first iteration.

---

## Next Actions

1. HELM: Schedule build sprint for items 20, 5, 3, 8 in that sequence
2. FORGE: Build the daily standup digest as first deliverable — polling script + LLM synthesis + Telegram push
3. LEGAL: Items #19 (patent monitor) and #6 (competitive intelligence) should be reviewed for any data access or IP capture legal exposure before deployment
4. SENTINEL: Before going live with PentAGI (#4), get a scope approval review to ensure no external targets or production systems are in the blast radius
5. Ron: Confirm watchlist for financial briefing (#2) — which tickers/sectors matter most

---

*Sources:*
- [SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent)
- [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent)
- [OpenHands](https://openhands.dev/)
- [Live-SWE-agent arXiv](https://arxiv.org/html/2511.13646v3)
- [TradingAgents](https://github.com/TauricResearch/TradingAgents)
- [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot)
- [AlphaAgents arXiv](https://arxiv.org/html/2508.11152v1)
- [PentAGI](https://github.com/vxcontrol/pentagi)
- [Hermes Agent NousResearch](https://github.com/NousResearch/hermes-agent)
- [Ouroboros-max](https://github.com/AntonAndrusenko/ouroboros-max)
- [Homelab AI Stack 2026](https://dev.to/signal-weekly/the-homelab-ai-stack-in-2026-what-self-hosters-are-actually-running-2d58)
- [Deep Research Survey arXiv](https://arxiv.org/abs/2508.12752)
- [Homelab Automation BSWEN](https://docs.bswen.com/blog/2026-03-27-homelab-automation-ai-agent/)
- [Morning Briefing Agent](https://blog.fundmore.ai/i-built-an-ai-agent-that-briefs-me-every-morning-heres-what-changed)
- [n8n Ollama Local LLM](https://blog.n8n.io/local-llm/)
- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [Awesome AI Agent Papers](https://github.com/VoltAgent/awesome-ai-agent-papers)
