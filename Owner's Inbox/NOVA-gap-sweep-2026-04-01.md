# NOVA Gap Sweep — April 1, 2026
# Security, Supply Chain, and AI DevOps Intelligence

**Objective:** Identify gaps in the PKA ecosystem that have opened in the last 90 days —
specifically: supply chain threats, Ollama/Vite/Cloudflare/npm/Python package vulnerabilities,
AI agent monitoring standards, and CI/CD best practices we are not yet meeting.

**Classification:** Internal — do not share externally.
**Delivered:** C:\Users\techai\PKA testing\Owner's Inbox\NOVA-gap-sweep-2026-04-01.md

---

## Key Findings — Ranked by Decision Impact

### FINDING 1 — CRITICAL: LiteLLM PyPI Package Was Backdoored (March 24, 2026)
**Risk: IMMEDIATE credential exposure if litellm 1.82.7 or 1.82.8 was installed anywhere**

The threat group TeamPCP backdoored LiteLLM versions 1.82.7 and 1.82.8 on PyPI on March 24, 2026.
The attack vector was a compromised Trivy GitHub Action in LiteLLM's own CI/CD pipeline.
The malicious payload installed a `.pth` file (`litellm_init.pth`) that executes automatically on
every Python process startup, exfiltrating: SSH keys, AWS/GCP/Azure credentials, Kubernetes secrets,
database passwords, CI/CD tokens, `.env` file contents, and cryptocurrency wallet data.

The LiteLLM library is commonly used as an AI router/proxy layer — a category of tool that exists in
the AI Army stack and in any project using multi-model routing (including the AI Router Platform, AI Army OS,
and any endpoint calling Ollama or NIM APIs through a Python abstraction layer).

**Action required:** Check every Spark-1, Spark-2, and Windows PC Python environment for LiteLLM.
Treat any environment where 1.82.7 or 1.82.8 was installed as a full credential compromise event.

Safe versions: 1.82.6 and below (confirmed clean) or 1.82.9+ (post-Mandiant audit).

Sources:
- [Datadog Security Labs — TeamPCP Campaign Analysis](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/)
- [Snyk — How a Poisoned Security Scanner Backdoored LiteLLM](https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm/)
- [BleepingComputer — LiteLLM Backdoor Credential Stealer](https://www.bleepingcomputer.com/news/security/popular-litellm-pypi-package-compromised-in-teampcp-supply-chain-attack/)
- [The Register — Telnyx also hit in same campaign](https://www.theregister.com/2026/03/30/telnyx_pypi_supply_chain_attack_litellm/)

---

### FINDING 2 — CRITICAL: Axios npm Package Backdoored — Cross-Platform RAT Delivered (March 31, 2026)
**Risk: Any npm install run on March 31 may have executed a RAT dropper**

Yesterday (March 31, 2026), a North Korean threat actor (UNC1069, attributed by Google Threat Intel)
compromised the npm credentials of axios's lead maintainer and published two poisoned releases:

- `axios@1.14.1` — MALICIOUS
- `axios@0.30.4` — MALICIOUS
- Safe versions: `axios@1.14.0` or `axios@0.30.3`

The injected dependency (`plain-crypto-js@4.2.1`) runs a postinstall script that drops a cross-platform RAT:
- **Windows**: PowerShell RAT with Registry Run key persistence
- **macOS**: C++ binary at `/Library/Caches/com.apple.act.mond`, 60-second beacon
- **Linux**: Python RAT at `/tmp/ld.py`

All variants support arbitrary command execution, file enumeration, payload delivery, and self-termination.
C2 endpoint: `packages.npm.org/product0-2` — block egress to `sfrclak[.]com`.

Axios is in 80% of cloud environments. Any project with a `node_modules/` that ran `npm install`
on March 31 is suspect: this covers aihangout-app, council frontend, AgentForge, and any other
Node-based frontend that had a recent dependency update.

Sources:
- [The Hacker News — Axios Supply Chain Attack](https://thehackernews.com/2026/03/axios-supply-chain-attack-pushes-cross.html)
- [SANS Institute — Axios npm Supply Chain Compromise](https://www.sans.org/blog/axios-npm-supply-chain-compromise-malicious-packages-remote-access-trojan)
- [Snyk — Axios Compromised](https://snyk.io/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/)
- [Huntress — Supply Chain Compromise](https://www.huntress.com/blog/supply-chain-compromise-axios-npm-package)
- [Wiz — Axios npm Compromised](https://www.wiz.io/blog/axios-npm-compromised-in-supply-chain-attack)

---

### FINDING 3 — HIGH: Ollama Has Three Unpatched CVEs — 175,000 Servers Exposed Globally

Three distinct Ollama vulnerabilities are confirmed active:

**CVE-2025-63389 — Authentication Bypass (Critical)**
Affects Ollama v0.12.3 and below. API endpoints require no authentication, enabling remote model
management operations. Our Cloudflare tunnel exposes `ollama.ultrarag.app` → Spark-1:11434.
This is the precise attack surface this CVE targets.

**CVE-2025-51471 — Cross-Domain Token Exposure**
Ollama 0.6.7 — manipulated WWW-Authenticate realm in `/api/pull` allows token theft.

**Out-of-Bounds Write — Arbitrary Code Execution (pre-0.7.0)**
Model file parsing vulnerability in mllama model handling. Fixed in 0.7.0 by rewriting
the vulnerable C++ code in Go. Any Ollama instance running models with mllama architecture
(multimodal models like LLaVA variants) on a version below 0.7.0 is exploitable.

Current state: Ollama is running on Spark-1 (port 11434, 46 models) and Spark-2 (port 11434, 7 models),
accessible via `ollama.ultrarag.app`. Ollama version on each Spark is unknown from this session.
Must verify both are on 0.7.0+ and 0.12.4+.

Sources:
- [CSO Online — Ollama Patches Critical Vulnerability](https://www.csoonline.com/article/2503268/ollama-patches-critical-vulnerability-in-open-source-ai-framework.html)
- [NVD — CVE-2025-63389](https://nvd.nist.gov/vuln/detail/CVE-2025-63389)
- [Oligo Security — More Models, More ProbLLMs](https://www.oligo.security/blog/more-models-more-probllms)
- [Security Boulevard — Exposed Ollama Servers](https://securityboulevard.com/2026/03/exposed-ollama-servers-security-risks-of-publicly-accessible-llm-infrastructure/)
- [Wiz — CVE-2025-51471](https://www.wiz.io/vulnerability-database/cve/cve-2025-51471)

---

### FINDING 4 — HIGH: Vite Has Three Active Arbitrary File Read CVEs

Three Vite vulnerabilities are actively tracked. The aihangout-app and council frontend both use Vite.
These CVEs affect the dev server — not necessarily production builds — but if any Vite dev server
is exposed on a non-localhost interface (even temporarily), these are exploitable:

**CVE-2025-30208** — Append `?import&raw??` to bypass @fs path restrictions. Read any file on the server.
Fixed in: Vite 6.2.3, 6.1.2, 6.0.12, 5.4.15, 4.5.10.

**CVE-2025-32395** — '#' character in HTTP request-target bypasses security checks on Node/Bun.
Fixed in: Vite 6.2.6, 6.1.5, 6.0.15, 5.4.18, 4.5.13.

**CVE-2025-46565** — Slash-dot bypass leaks secret files from dev server.
Active, patch status: check current Vite version.

**React Server Components (GHSA-fmh4-wr37-44fp)** — @vitejs/plugin-rsc with react-server-dom-webpack
versions prior to 19.0.1/19.1.2/19.2.1 enables unauthenticated RCE via deserialization.

Action: Verify Vite version in all frontend package.json files. Update to patched versions.

Sources:
- [Snyk — Vite Vulnerabilities](https://security.snyk.io/package/npm/vite)
- [SentinelOne — CVE-2025-30208](https://www.sentinelone.com/vulnerability-database/cve-2025-30208/)
- [Security Boulevard — CVE-2025-31486](https://securityboulevard.com/2025/04/vite-arbitrary-file-read-vulnerability-cve-2025-31486/)
- [CVE News — CVE-2025-46565](https://www.cve.news/cve-2025-46565/)
- [GitHub Advisory — GHSA-fmh4-wr37-44fp](https://github.com/vitejs/vite-plugin-react/security/advisories/GHSA-fmh4-wr37-44fp)

---

### FINDING 5 — HIGH: TeamPCP Cascading Campaign Is Still Active
**Telnyx also hit March 27; pattern is broadening**

The TeamPCP supply chain campaign did not stop at LiteLLM. Timeline:
- March 19: Trivy (security scanner) GitHub Action compromised
- March 24: LiteLLM PyPI poisoned (using stolen Trivy CI credentials)
- March 27: Telnyx PyPI (versions 4.87.1, 4.87.2) backdoored
- March 30: CanisterWorm npm campaign ran in parallel
- March 31: Axios npm backdoored (UNC1069 — possibly related actor)

This is an accelerating campaign specifically targeting AI-layer dependencies: LLM routers, HTTP clients,
and security tooling. Any Python package installed from PyPI in March 2026 without hash pinning is suspect.
The pattern: compromise the CI/CD pipeline of a trusted tool first, then use those credentials downstream.

The AI Army ecosystem uses pip installs across multiple Spark environments without lock files or hash pinning.
That is the systemic gap this campaign is designed to exploit.

Sources:
- [ReversingLabs — TeamPCP Cascading Attack](https://www.reversinglabs.com/blog/teampcp-supply-chain-attack-spreads)
- [Trend Micro — TeamPCP Telnyx Attack](https://www.trendmicro.com/en_us/research/26/c/teampcp-telnyx-attack-marks-a-shift-in-tactics.html)
- [Kaspersky — Trivy and LiteLLM Supply Chain](https://www.kaspersky.com/blog/critical-supply-chain-attack-trivy-litellm-checkmarx-teampcp/55510/)
- [Arctic Wolf — TeamPCP Full Campaign](https://arcticwolf.com/resources/blog/teampcp-supply-chain-attack-campaign-targets-trivy-checkmarx-kics-and-litellm-potential-downstream-impact-to-additional-projects/)

---

### FINDING 6 — MEDIUM: No AI-Specific Monitoring — Silent Hallucinations Are Invisible

This is the gap elite companies close that small teams uniformly miss.

Traditional monitoring (uptime, latency, HTTP 200) does not detect the failure modes specific to AI agents:
hallucination (confident wrong answers), output drift (quality degrades as prompts or models change),
skipped reasoning steps, and tool selection errors. These all return HTTP 200 with normal latency.

The 2026 standard from OpenTelemetry's GenAI Semantic Conventions defines specific attributes for tracing:
agent tasks, actions, tool calls, memory reads, and team coordination — none of which are logged in the
current AI Army OS setup. The current monitoring on Hermes is process-level (4h poll) with zero
output quality signals.

Elite teams are running eval-in-CI: automated golden test suites that run on every agent config change,
scoring outputs for faithfulness, relevance, and hallucination rate before promoting to production.
The PKA scorecard gap (throughput: 4/5 operational tasks) and the Hermes watchdog gap (not reboot-tested)
are symptoms of the same underlying issue: behavior is monitored at the process level, not the output level.

Sources:
- [UptimeRobot — AI Agent Monitoring Best Practices 2026](https://uptimerobot.com/knowledge-hub/monitoring/ai-agent-monitoring-best-practices-tools-and-metrics/)
- [ThousandEyes — Monitoring AI Agents for Production Reliability](https://www.thousandeyes.com/blog/monitoring-ai-agents-production-reliability)
- [Braintrust — Best AI Agent Observability Tools 2026](https://www.braintrust.dev/articles/best-ai-agent-observability-tools-2026)
- [OpenTelemetry — GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Galileo — LLM Drift Monitoring Platforms](https://galileo.ai/blog/best-llm-output-drift-monitoring-platforms)
- [dasroot.net — Measuring Hallucination Rates in Production](https://dasroot.net/posts/2026/03/measuring-hallucination-rates-production-ai/)

---

### FINDING 7 — MEDIUM: No Dependency Pinning or Hash Verification Across the Stack

The standard gap that enabled all three supply chain attacks above is lack of hash pinning.
LiteLLM, Axios, and Telnyx were all installed from PyPI/npm without cryptographic hash verification.
`pip install litellm` without a lock file with `--hash` flags will silently pull a poisoned version
if the malicious window is open at install time.

Current state of the ecosystem:
- Python environments on Spark-1 and Spark-2 install via bare `pip install`
- No `requirements.txt` hash pinning (`--hash=sha256:...`)
- No `pip-audit` or `safety` scanning in any known CI path
- npm projects do not use `npm ci` (which enforces lockfile) in any automated build

The fix is not complex but must be systematic: `pip-audit` run monthly, lockfiles committed for all
production environments, and `npm ci` enforced over `npm install` in any automated context.

Sources:
- [Harness.io — AI Deployment CI/CD Best Practices 2026](https://www.harness.io/blog/ai-deployment-in-production-orchestrate-llms-rag-agents)
- [AWS Prescriptive Guidance — CI/CD for Agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/cicd-and-automation.html)

---

### FINDING 8 — LOW: Cloudflare Pages Cache — No Active Security Vulnerability, But Process Gap Exists

No new security CVEs were found for Cloudflare Pages in the last 90 days.
The existing known issue (stale .map files on the aihangout CDN) is an operational gap, not a security one.

Cloudflare's own documentation confirms: stale assets after deployment require a manual "Purge Everything"
via Caching > Configuration in the dashboard, or via the Cache Purge API. This is not automated in the
current deploy flow for aihangout-app.

The risk is low (stale source maps do not create security exposure; they create debugging confusion
and may serve outdated JS to users). Fix is trivial: add `curl` cache purge call to deploy script.

Sources:
- [Cloudflare Docs — Serving Pages](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- [Cloudflare Changelog — Cache Response Rules (March 24, 2026)](https://developers.cloudflare.com/changelog/post/2026-03-24-cache-response-rules/)

---

## Evidence Summary

| Finding | Source Confidence | Window | Severity |
|---------|------------------|--------|----------|
| LiteLLM supply chain | Multiple tier-1 sources (Datadog, Snyk, BleepingComputer, Kaspersky) | Active | CRITICAL |
| Axios supply chain | Multiple tier-1 sources (Hacker News, SANS, Snyk, Wiz, Huntress) | Active (yesterday) | CRITICAL |
| Ollama CVEs | NVD + CSO + Oligo + Wiz | Active | HIGH |
| Vite CVEs | Snyk + SentinelOne + GitHub Advisory | Active | HIGH |
| TeamPCP campaign | ReversingLabs + Trend Micro + Arctic Wolf | Active, expanding | HIGH |
| AI monitoring gap | UptimeRobot + ThousandEyes + OpenTelemetry spec | Structural | MEDIUM |
| Dependency pinning | Industry standard gap, confirmed by attack pattern | Structural | MEDIUM |
| Cloudflare cache | Cloudflare docs only — no CVE found | Operational | LOW |

---

## Risks — Where This Analysis Could Be Wrong

1. **LiteLLM presence unknown**: This analysis assumes LiteLLM may be in the stack based on the
   AI Router Platform and multi-model routing. If it was never installed, Finding 1 is moot.
   Verification takes 30 seconds: `pip show litellm` on each Spark.

2. **Ollama version unknown**: The exact Ollama versions on Spark-1 and Spark-2 are not known
   from this session. If both are already on 0.7.0+ and 0.12.4+, Findings 3's CVEs are patched.

3. **Axios install timing**: The attack window was approximately 2-3 hours on March 31. If no
   `npm install` ran during that window, exposure is zero. If any CI/CD or dev server ran
   `npm install` on March 31, exposure is possible.

4. **Vite dev server exposure**: These CVEs only apply when the dev server is running and accessible.
   If Vite dev servers are strictly localhost-only, the file read vulnerabilities require local access.

5. **Source confidence on Ollama exposed servers stat**: The "175,000 exposed" figure comes from
   a single scanner report (Security Boulevard). The general risk is confirmed; the scale may vary.

---

## Recommendation

Single ranked answer: **Address the supply chain exposure first. It happened yesterday and last week.**

The CVEs and monitoring gaps are important but structural — they can be scheduled. The supply chain
attacks are active events where credential windows may already be open. The order of operations:

1. **Today**: Run `pip show litellm` on Spark-1 and Spark-2. If version is 1.82.7 or 1.82.8 — full
   incident response: rotate all SSH keys, AWS keys, API keys, database passwords, and .env contents.
2. **Today**: Audit all npm `node_modules/` on Windows PC for axios@1.14.1 or @0.30.4. Block egress
   to `sfrclak[.]com` at the router level immediately.
3. **This week**: Verify Ollama versions on both Sparks. Update to 0.7.0+ and 0.12.4+.
   Consider taking `ollama.ultrarag.app` offline until CVE-2025-63389 is patched.
4. **This week**: Audit Vite versions in all frontend projects. Pin to patched versions.
5. **This month**: Implement `pip-audit` and `npm audit` as periodic checks.
   Move to hash-pinned `requirements.txt` for all Spark production environments.
6. **This month**: Add one output-quality check to Hermes (e.g., eval golden set of 10 queries,
   score for response quality on restart). This closes both the watchdog reboot-test gap and
   the hallucination monitoring gap in one instrument.

---

## Next Actions

| Action | Owner | Deadline | Effort |
|--------|-------|----------|--------|
| `pip show litellm` on Spark-1 + Spark-2 | Ron or HELM | Today | 2 min |
| Audit npm `node_modules/` for poisoned axios | FORGE | Today | 15 min |
| Block `sfrclak[.]com` egress at router | Ron | Today | 5 min |
| Check Ollama version on both Sparks | HELM | This week | 5 min |
| Disable `ollama.ultrarag.app` if Ollama < 0.12.4 | Ron | This week | 5 min |
| Audit Vite versions in all frontend package.json | FORGE | This week | 30 min |
| Add `pip-audit` to Spark maintenance scripts | FORGE | This month | 2 hrs |
| Add eval golden set to Hermes watchdog | FORGE | This month | 4 hrs |
| Add Cloudflare cache purge to aihangout deploy script | FORGE | This month | 1 hr |

---

*NOVA — Research and Strategic Intelligence*
*Sweep date: 2026-04-01*
*Next sweep recommended: 2026-05-01 (or immediately after any major dependency install)*
