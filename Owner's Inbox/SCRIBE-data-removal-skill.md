# SCRIBE Deliverable — data-removal-automation Skill

**Delivered by:** SCRIBE
**Date:** 2026-03-26
**Status:** PENDING (requires 3 confirmed uses before promotion to ACTIVE)

---

## Gap Report

**Domain:** Automated personal data removal — data broker opt-out
automation using Playwright, Celery, FastAPI, and PostgreSQL.

**What was searched:** Full coverage scan across all 30 existing skills,
Docker MCP catalog, installed CLIs, pip packages, and the self-learning
knowledge base.

**What was found:** No existing skill covers this domain above 43%
relevance. The closest partial match was `ai-data-privacy-compliance`
(43%) which covers privacy risk identification but has zero automation
patterns, no Celery/Playwright content, and no broker-specific
knowledge. The gap is real and wide.

---

## Coverage Scan Result

| Source | Best Match | Relevance | Gap |
|--------|-----------|-----------|-----|
| Existing skills | ai-data-privacy-compliance | 43% | Missing all automation patterns |
| MCP catalog | (unavailable — Docker offline) | — | — |
| Installed CLIs | python, pip, docker | 0% domain match | None cover data removal |
| pip packages | — | — | No data-removal library exists |
| KB entries | 0 | — | No prior learning on this domain |

**Decision: CREATE new skill.** Nothing covered the domain at 80%+.

---

## Decision Rationale

The DataShield project at `C:\Users\techai\DataShield\src` is a
complete, production-grade reference implementation. Reading the actual
source files — not guessing from docs — gave the skill real, tested
patterns for every section. This is not a generic "how to scrape"
skill; it is a specific architecture for a legally sensitive,
privacy-first automation domain that recurs whenever privacy tools
are built.

A bridge skill was rejected because no existing CLI, MCP, or SDK covers
data broker automation at any level of completeness.

---

## Skill Artifacts Created

### Primary Skill
`C:\Users\techai\claude-skills\data-removal-automation\skill.md`

**15 sections covering:**
1. Core architecture (FastAPI → Celery Beat → Workers → BrowserEngine → Playbook → PIIVault)
2. PIIVault — AES-256-GCM per-field encryption with full Python implementation
3. Playbook YAML schema — complete with step actions and PII placeholder reference
4. Database schema — ORM models for Identity, Broker, Case, Event, DropFiling, etc.
5. Celery configuration — 4 queues, rate limiting, Beat schedule
6. BrowserEngine — anti-detection setup, search flow, submission flow, method dispatch table
7. Case state machine — all states and transitions
8. Guardrail layer — 5 BLOCK rules, 3 WARN rules, decorator pattern
9. LLM router — route table, cost tracking, PII anonymisation contract
10. NeMo OCR integration — 3 use cases, graceful degradation
11. Broker dependency graph — cascade pattern and handle_cascade() implementation
12. Legal compliance — California DELETE Act, CCPA, GDPR, evidence logging
13. Complete search worker example — full pattern including retry logic
14. Extension points — CAPTCHA solving, email verification, GPC signal
15. Validation plan and quick reference commands

### Reference File
`C:\Users\techai\claude-skills\data-removal-automation\references\broker-patterns.md`

**Contents:**
- Opt-out method taxonomy (form / email / api / california_drop / manual / status_poll)
- Broker category map (people search, aggregators, background check, marketing lists)
- 9 documented anti-patterns with detection and mitigation for each
- Severity scoring guide (1-10 scale with examples)
- Data richness scoring guide (1-10 scale)
- Known broker dependency chains (Intelius → Spokeo → PeopleFinders, etc.)
- Playbook authoring checklist (13-item pre-commit verification)

---

## Source Files Read

All patterns are grounded in real DataShield source code:

| File | What it contributed |
|------|---------------------|
| `src/api/pii_vault.py` | Full PIIVault implementation |
| `src/workers/orchestrator.py` | dispatch_pending, schedule_rescans, handle_cascade |
| `src/workers/guardrails.py` | All 5 BLOCK rules, 3 WARN rules, @guardrail decorator |
| `src/workers/llm_router.py` | Route table, LLMResponse, cost tracking, _assert_no_raw_pii |
| `src/browser/engine.py` | execute_search, execute_form_submission, anti-detection, OCR integration |
| `src/workers/search.py` | Full search worker pattern including LLM re-scoring |
| `src/workers/celery_app.py` | Queue routing, Beat schedule, rate limit config |
| `src/api/models.py` | Full ORM schema — all 8 tables |
| `src/playbooks/brokers/spokeo.yaml` | Reference playbook with real selectors |

---

## Risks and Limitations

1. **CAPTCHA solving is not wired.** The `_solve_captcha()` method in
   BrowserEngine has the integration point but the actual 2captcha/
   anticaptcha API call is not implemented. The skill documents exactly
   where to wire it. Any system built from this skill needs to complete
   this step before production use.

2. **Playbook selectors drift.** Broker sites change their HTML
   frequently. Selectors in the Spokeo playbook were current at time
   of authoring. Production use requires a health-check loop and
   selector maintenance workflow.

3. **Per-identity salt not implemented.** PIIVault uses a fixed salt
   (`b"dra-pii-vault-v1"`). The skill notes this and flags per-identity
   salts as the v2 upgrade. For a multi-tenant system, per-identity
   salts are required to prevent cross-identity key oracle attacks.

4. **Email verification loop.** Brokers that require email confirmation
   (Spokeo, Whitepages) have the `needs_email_verify` flag set but the
   inbox polling and link-clicking logic is not implemented in
   DataShield. The skill documents the extension point.

---

## Validation Criteria for ACTIVE Promotion

Track use_count in the skill frontmatter. After 3 confirmed real-world
applications where all of the following are verified:

- PIIVault used — no plaintext PII in database confirmed
- At least one playbook YAML executed against a live broker
- Guardrail layer active — no PII field names in task results
- LLM router used with anonymised prompts only
- Evidence screenshots logged per submission
- Case state machine completing full cycles without stuck states
