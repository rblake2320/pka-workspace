# Claude Code Source Leak — Full Intelligence Brief
**Date**: 2026-03-31 | **Assembled by**: NOVA (5 parallel research agents)
**Classification**: Breaking / Confirmed / Permanent

---

## Executive Summary

Anthropic accidentally shipped the **entire Claude Code TypeScript source** (512,000 lines, 1,900 files) in npm package `@anthropic-ai/claude-code` v2.1.88 via a 59.8 MB source map file. Discovered 4:23 AM ET. **It is permanent** — 41,500+ forks, 8,100 DMCA takedowns, clean-room rewrites already shipping. Anthropic confirmed it. No customer data exposed. This is the tool you are using right now.

---

## The Leak: What Happened

| Item | Detail |
|------|--------|
| Package | `@anthropic-ai/claude-code` v2.1.88 |
| File leaked | `cli.js.map` — 59.8 MB source map |
| Contents | 512,000 lines TypeScript, 1,900 files |
| Root cause | Bun bundler generates `.map` files by default — team forgot to disable |
| Discovered | 4:23 AM ET, @Fried_rice (Chaofan Shou) on X |
| X post views | 16 million |
| GitHub forks | 41,500+ within hours |
| GitHub stars | 30,000 (claimed fastest ever) |
| DMCA takedowns | ~8,100 issued by Anthropic |
| Status | **Permanent** — mirrors, rewrites, decentralized hosting |
| Anthropic statement | *"Release packaging issue caused by human error, not a security breach. No customer data or credentials exposed."* |
| Context | Second Anthropic leak in 5 days (Mythos model docs leaked March 26) |

---

## Community Engagement (live as of report time)

| Thread | Score | Comments |
|--------|-------|----------|
| HN: "Claude Code's source code has been leaked via a map file" (treexs) | **1,880 pts** | 920 |
| HN: "The Claude Code Source Leak: fake tools, frustration regexes, undercover mode" (alex000kim) | **708 pts** | 293 |
| HN: "Claude Code full source code leaked on NPM" (dheerajmp — buildable copy) | 47 pts | 3 |
| r/ClaudeAI | Active | — |
| r/LocalLLaMA | Active (focus: hidden features, local model integration) | — |
| HuggingFace discussion | Active | — |

---

## What Was Inside: Hidden Features (44 Feature Flags Total)

### KAIROS
- Always-on background daemon
- GitHub webhook integration
- Nightly `/dream` memory distillation cycle
- Scheduled context refresh
- Effectively: Claude Code is always watching your repos, even when you're not running it

### Undercover Mode (`undercover.ts`)
- Strips "Generated with Claude Code" attribution from commits to public repos
- Strips Anthropic internal codenames from output
- **Exact code note**: *"There is NO force-OFF. This guards against model codename leaks."*
- Implication: you can't turn it off even if you wanted to

### Buddy
- Tamagotchi-style AI companion with 18 species, rarity tiers, and stats
- Apparently in active development

### ULTRAPLAN
- Unreleased enhanced planning mode (beyond what /plan currently does)

### Additional Unreleased Features
- Voice command mode (dedicated CLI)
- Actual Playwright browser control (not just web fetch — full interaction)
- Background agents with sleep/self-resume (persistent across sessions)
- Persistent cross-session memory
- Multi-agent swarm orchestration

---

## Anti-Competitive / Anti-Distillation Mechanisms

These are the most legally interesting findings:

| Mechanism | How It Works |
|-----------|--------------|
| **Fake tool injection** | Injects fake/poison tools into API requests to corrupt competitor training data scraped from Claude conversations |
| **Cryptographic summarization** | Server-side text summaries carry cryptographic signatures — verifiable that summaries came from Anthropic servers |
| **CCH Attestation** | A Zig native module scans HTTP bodies for the string `cch=f232f`. When found, **corrupts conversation content**, breaks prompt caching, forces "10-20x more tokens" consumed. Effectively a silent anti-scraping tax. |

---

## Internal Model Codenames Exposed

| Codename | Maps To |
|----------|---------|
| **Capybara** | Claude 4.6 variant |
| **Fennec** | Opus 4.6 |
| **Numbat** | Unknown (referenced in source) |

---

## Code Quality Issues (Community Findings)

These surfaced in the HN threads and are relevant to your reliance on Claude Code:

| Finding | Detail |
|---------|--------|
| **Zero automated tests** | 0 tests across 64,464 lines of production code |
| **Sentiment via regex** | Frustration detection: `/\b(wtf\|shit\|fuck)\b/i` — not LLM, literally a regex |
| **Silent model downgrade** | After 3 consecutive 529 errors → silently switches Opus to Sonnet with **no user notification** |
| **Failure rate** | 16.3% API failure rate across 3,539 requests over 6 days (internal telemetry) |
| **Orphaned tool calls** | 5.4% of tool calls dropped/orphaned silently |
| **Monster function** | Single function: 3,167 lines, 486 branch points, 12 nesting levels |

The silent Opus→Sonnet downgrade is the most operationally relevant — if you're hitting 529s during heavy Spark work, you may have been getting Sonnet responses while paying for/expecting Opus.

---

## Separate Concurrent Threat: Axios npm RAT

Unrelated to the Claude Code leak but happened same day — worth knowing:

| Item | Detail |
|------|--------|
| Package | `axios` npm (or malicious fork) |
| Versions | 1.14.1, 0.30.4 |
| Window | 00:21–03:29 UTC March 31 (brief, caught fast) |
| Origin | North Korean supply chain attack |
| Marker | `plain-crypto-js` in `package-lock.json` |
| Risk to you | **Only if you ran `npm install` between 00:21–03:29 UTC today** |

**Action**: Run this check on any system that ran npm install today:
```bash
grep -r "plain-crypto-js" package-lock.json node_modules/.package-lock.json 2>/dev/null
```

Your Spark systems and Windows PC — if you didn't run npm install in that 3-hour window, you're clean.

---

## Clean-Room Rewrites Already Shipping

- **claw-code** by Sigrid Jin — Python clean-room rewrite, shipped before sunrise
- Copyright law allows clean-room rewrites if no original code is copied, just behavior replicated from public knowledge
- DMCA takedowns cannot touch these

---

## Key Resources

| Resource | URL |
|----------|-----|
| HN Primary Thread | https://news.ycombinator.com/item?id=47584540 |
| HN Deep-Dive Thread | https://news.ycombinator.com/item?id=47586778 |
| Original discovery (X) | https://x.com/Fried_rice/status/2038894956459290963 |
| Best technical analysis | https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/ |
| Curated insights index | https://github.com/nblintao/awesome-claude-code-postleak-insights |
| Decrypt coverage | https://decrypt.co/362917/anthropic-accidentally-leaked-claude-code-source-internet-keeping-forever |
| The Register | https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/ |
| CyberNews | https://cybernews.com/security/anthropic-claude-code-source-leak/ |

---

## What This Means for You (Operational Impact)

1. **Silent Opus→Sonnet downgrade**: If you've been getting weird/weaker Claude Code responses during heavy API periods, now you know why. You were getting Sonnet silently.

2. **KAIROS**: The always-on daemon is presumably not in your current CLI build — it's an unreleased feature. No action needed.

3. **Undercover Mode**: If you use Claude Code to commit to public repos, it may be stripping attribution. Unclear if enabled by default in released builds.

4. **CCH Attestation / `cch=f232f`**: If any of your systems (especially AI Army OS, Ultra RAG, aihangout.ai) are proxying Claude API calls through custom middleware, check that you're not accidentally injecting or stripping headers in a way that triggers this. Symptoms: unexpectedly high token counts.

5. **Anti-distillation fake tools**: If you're scraping Claude conversations to build training data for your own models (NLF pipeline, etc.) — the fake tools may be in there. Worth filtering for tool responses that don't match actual tool schemas.

6. **Axios RAT**: Run the grep above on any system that did npm install today.

---

## Confidence Level

**High** — confirmed by Anthropic official statement, 5 independent sources across HN/Reddit/news media, original X discovery post with 16M views. Uncertainty exists only on exact numbers (forks, stars, view counts) — all from secondary reporting. Core technical facts (source map, features exposed, CCH attestation, code quality stats) come from direct source analysis by independent researchers.
