# DataShield Knowledge Layer — Architecture Design
**Author**: NOVA — Research and Strategic Intelligence
**Audience**: FORGE (implementation), Ron (decision)
**Status**: Design-complete. Ready for FORGE Phase 1 sprint.
**Date**: 2026-03-26

---

## Objective

Design a semantic knowledge layer for DataShield — the automated personal data removal engine at
`C:\Users\techai\DataShield\` — using the NVIDIA Enterprise RAG Pipeline pattern. The layer must
convert the accumulated institutional knowledge scattered across YAML playbooks, PostgreSQL event
logs, and broker metadata into a queryable, generative intelligence system that (a) auto-drafts
new broker playbooks, (b) answers user questions about removal status, and (c) detects when a
broker has changed its opt-out flow before wasting full Playwright runs.

The architecture is PII-strict: no identity data, no encrypted fields, no case-linked personal
information enters the knowledge index at any point.

---

## Section 1 — Data Sources to Index

### 1.1 Source Inventory

| # | Source | What it Contains | PII Risk | Index? |
|---|--------|-----------------|----------|--------|
| 1 | `src/playbooks/brokers/*.yaml` | Opt-out selectors, URL patterns, CAPTCHA types, step sequences, success/error indicators | None | Yes — full content |
| 2 | `src/playbooks/platforms/*.yaml` | Platform-level integrations (CA DROP) | None | Yes — full content |
| 3 | `src/playbooks/registries/*.yaml` | Registry suppression flows (DMAchoice) | None | Yes — full content |
| 4 | `src/playbooks/schema.json` | Canonical schema — field definitions, enumerations | None | Yes — as reference doc |
| 5 | `brokers` table (PostgreSQL) | Domain, category, CAPTCHA type, severity, recheck cadence, health status, workflow type, dependency graph | None | Yes — export nightly |
| 6 | `events` table (PostgreSQL) | Event type, summary, error_code, error_message, detail JSONB, broker_id, timestamps | **No PII stored directly. broker_id and case_id are UUIDs. summary/error fields may contain URL fragments.** Strip `identity_id` and `case_id` before indexing. | Yes — stripped projection |
| 7 | `cases` table (aggregate view) | Per-broker confirmation rates, avg processing days, failure counts, captcha solve rates | No PII — aggregate only | Yes — materialized view |
| 8 | Legal compliance notes | State law requirements (CCPA, CDPA, CPA, etc.) | None | Yes — as structured docs |
| 9 | Email correspondence (broker responses) | Confirmation emails, rejection reasons, re-listing notices | **May contain email addresses** | Yes — with PII scrub before index |
| 10 | `kpi_snapshots` table | Confirmation rates, false match rates, CAPTCHA stats, manual intervention rates | None | Yes — nightly export |

**What is permanently excluded from the index**: `identities` table (all fields), `cases.profile_url`, `cases.screenshot_path`, `cases.matched_fields`, `cases.confirmation_code`, any decrypted PII vault output, `drop_filings`, `breach_alerts`. These are sealed at the application layer and must never cross into the RAG subsystem.

---

### 1.2 Ingestion Specifications Per Source

#### Source 1–4: Playbook YAML Files

```
Ingestion method : File watcher (watchdog) triggered on git commit or file write
                   Also: full re-ingest on schema version change
Chunk strategy   : One document per playbook file (3–6 KB each)
                   Within each doc, chunk at phase boundaries:
                     - broker metadata block → 1 chunk (fields: name, domain, category,
                       severity, captcha.type, requirements, dependencies)
                     - search phase (url + steps) → 1 chunk
                     - submit phase (method + steps + indicators) → 1 chunk
                     - status_poll block → 1 chunk (if present)
                     - kpis block → 1 chunk
                   Minimum chunk size: 150 tokens. Merge if smaller.
                   Overlap: 50 tokens between adjacent phase chunks (same playbook)
Metadata tags    : broker_name, domain, playbook_type, captcha_type, category,
                   severity, has_status_poll, version, file_path
Update frequency : On file change event. Full resync nightly at 02:00.
```

#### Source 5: Broker Table (PostgreSQL)

```
Ingestion method : Nightly SQL export → JSONL → ingest pipeline
                   Export query: SELECT id, name, domain, category, captcha,
                     captcha_config, requires_id_upload, requires_email,
                     requires_phone, recheck_days, processing_days, severity,
                     data_richness, feeds_from, feeds_to, active,
                     health_status, last_health_check, workflow_type,
                     playbook_file, playbook_type FROM brokers
Chunk strategy   : One chunk per broker row (typically 200–400 tokens as JSON)
                   Rendered as structured text, not raw JSON, for embedding quality:
                     "BeenVerified (beenverified.com) is a background_check broker
                      with severity 8 and data_richness 9. CAPTCHA: hcaptcha.
                      Recheck cadence: 45 days. Processing: 14 days.
                      Feeds from: truthfinder.com. Feeds to: neighborwho.com,
                      numberville.com. Health: [status]. Active: true."
Metadata tags    : broker_id (UUID), domain, category, captcha_type, severity,
                   health_status, active
Update frequency : Nightly. Plus immediate re-ingest when health_status changes.
```

#### Source 6: Events Table (PostgreSQL) — Stripped Projection

```
PII RULE: The event projection MUST NOT include identity_id, case_id, or any
          field that allows linking back to a specific person's removal request.

Ingestion method : Nightly batch — materialized aggregate per (broker_id, event_type,
                   error_code) for operational patterns. Not raw event rows.

Two sub-documents per broker per event type:
  A. Error pattern document:
     "Broker [name] ([domain]) error pattern: [error_code] — [error_message].
      Occurrences last 30 days: [count]. First seen: [date]. Last seen: [date].
      Context: [deduplicated summary text from events.summary]."

  B. Success pattern document (for confirmed/submitted events):
     "Broker [name] opt-out submission success pattern.
      Avg time from submit to confirmed: [X] days.
      Confirmation method: [email_verify|status_poll|auto].
      Most recent success: [date]."

Chunk strategy   : One chunk per (broker, event_category) pair.
                   Not individual events — aggregated patterns only.
Metadata tags    : broker_id, broker_name, event_type, error_code,
                   occurrence_count, date_range_start, date_range_end
Update frequency : Nightly rebuild of all aggregated pattern documents.
```

#### Source 7: Case Aggregate View

```
SQL view to create:
  CREATE MATERIALIZED VIEW ds_knowledge.broker_performance AS
  SELECT
    b.id AS broker_id,
    b.name,
    b.domain,
    b.category,
    COUNT(c.id) AS total_cases,
    AVG(EXTRACT(EPOCH FROM (c.verified_at - c.submitted_at))/86400)::numeric(5,1)
      AS avg_confirmation_days,
    SUM(CASE WHEN c.removal_confirmed THEN 1 ELSE 0 END)::float / NULLIF(COUNT(c.id),0)
      AS confirmation_rate,
    SUM(CASE WHEN c.human_review THEN 1 ELSE 0 END)::float / NULLIF(COUNT(c.id),0)
      AS human_review_rate,
    b.recheck_days,
    b.processing_days
  FROM brokers b LEFT JOIN cases c ON c.broker_id = b.id
  GROUP BY b.id, b.name, b.domain, b.category, b.recheck_days, b.processing_days;

Ingestion method : Nightly materialized view refresh → text render → ingest
Chunk strategy   : One document per broker row (same text rendering pattern as Source 5)
Update frequency : Nightly REFRESH MATERIALIZED VIEW CONCURRENTLY
```

#### Source 8: Legal Compliance Notes

```
Format          : Markdown files in new directory src/knowledge/legal/
                  One file per state + one federal overlay:
                    ccpa_california.md, cdpa_virginia.md, cpa_colorado.md,
                    ctdpa_connecticut.md, ucpa_utah.md, federal_glba.md, etc.
Chunk strategy  : Chunk at H2 section boundaries (max 512 tokens per chunk)
                  Sections: Scope, Covered Entities, Consumer Rights,
                  Opt-Out Requirements, Timelines, Enforcement
Metadata tags   : state, law_name, effective_date, covers_category[]
Update frequency: Manual — on statutory change (quarterly review)
```

#### Source 9: Email Correspondence

```
PII scrub required before indexing:
  - Strip all To:/From:/CC: headers (contain email addresses)
  - Strip any embedded PII using regex: SSN patterns, DOB patterns,
    address patterns, full name occurrences
  - Retain: broker name (infer from domain in From: header), date,
    subject (stripped of PII), body template text

Ingestion method : Email parser worker reads confirmed broker response
                   templates from a designated mailbox or stored file
                   corpus. Writes PII-stripped text to
                   src/knowledge/email_templates/{broker_domain}_{type}.txt
Chunk strategy   : One document per (broker, response_type) where
                   response_type ∈ {confirmation, rejection, re_listing_notice,
                   delay_notice, processing_notice}
Metadata tags    : broker_domain, response_type, date_received
Update frequency : As new templates are captured
```

#### Source 10: KPI Snapshots

```
Ingestion method : Nightly aggregation of kpi_snapshots into a
                   summary trend document per broker
Chunk strategy   : One document covering last 90 days of KPI trends per broker
                   "BeenVerified KPI trend (90d): confirmation_rate trended
                    from 0.72 to 0.80. Captcha solve rate: 0.91. Manual
                    intervention rate: 0.22 (above 0.25 target alert threshold)."
Update frequency : Nightly
```

---

## Section 2 — Embedding and Retrieval Architecture

### 2.1 Embedding Model Selection

**Primary choice: `nvidia/nv-embedqa-e5-v5` via NVIDIA NIM**

Rationale:
- Trained specifically for retrieval and Q&A tasks (not general-purpose)
- 4096-token context window — critical for full playbook ingestion without truncation
- 1024-dimensional output — higher fidelity than 384-dim models at acceptable storage cost
- Available as local NIM container (RTX 5090 handles it — requires ~8GB VRAM inference)
- Also available via `https://integrate.api.nvidia.com/v1/embeddings` for burst ingest

**Fallback: `nomic-ai/nomic-embed-text-v1.5` via Ollama on Spark-1**

Rationale: Already deployed on Spark-1, 8192-token context, proven in Ultra RAG. Use during
NIM downtime or if NIM latency exceeds 200ms.

**Do not use**: `text-embedding-3-small` (OpenAI) — sends DataShield operational patterns
to an external API, which violates the data isolation principle in the workspace CLAUDE.md
even though no PII is involved. The operational knowledge of which brokers fail, which
CAPTCHAs are unsolved, and which selectors work is itself a competitively sensitive asset.

### 2.2 Vector Store Selection

**Decision: pgvector in the existing DataShield PostgreSQL instance**

Do NOT use Milvus or Qdrant. Rationale:

| Factor | pgvector | Milvus | Qdrant |
|--------|----------|--------|--------|
| New infra to operate | No | Yes | Yes |
| Transactional consistency with broker data | Yes (same DB) | No | No |
| RLS isolation (proven pattern from Ultra RAG) | Yes | No | No |
| Ron's existing operational knowledge | Yes | None | None |
| Storage overhead | Low | Medium | Medium |
| HNSW at DataShield's expected scale (<50K chunks) | Perfectly adequate | Overkill | Overkill |

The DataShield knowledge base will have at most ~50,000 chunks at full scale (200 brokers ×
~10 chunks each + event patterns + legal docs). pgvector HNSW handles this in under 20ms
warm. The operational simplicity gain from staying in Postgres outweighs any marginal
retrieval quality difference at this scale.

Schema placement: new `ds_knowledge` schema within the DataShield PostgreSQL database,
isolated from the operational `public` schema by separate roles.

```sql
CREATE SCHEMA ds_knowledge;

CREATE TABLE ds_knowledge.chunks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type TEXT NOT NULL,          -- 'playbook', 'broker_meta', 'event_pattern',
                                        --  'legal', 'email_template', 'kpi_trend'
    broker_id   UUID REFERENCES brokers(id) ON DELETE SET NULL,
    broker_name TEXT,
    domain      TEXT,
    content     TEXT NOT NULL,          -- rendered text sent to embedding model
    metadata    JSONB NOT NULL DEFAULT '{}',
    embedding   vector(1024),           -- nv-embedqa-e5-v5 dimension
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    content_hash TEXT GENERATED ALWAYS AS
                  (encode(digest(content, 'sha256'), 'hex')) STORED
);

CREATE INDEX ds_knowledge_embedding_hnsw
    ON ds_knowledge.chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX ds_knowledge_source_type_idx ON ds_knowledge.chunks (source_type);
CREATE INDEX ds_knowledge_broker_idx ON ds_knowledge.chunks (broker_id);

-- BM25 full-text index (for hybrid retrieval)
ALTER TABLE ds_knowledge.chunks
    ADD COLUMN fts_vector tsvector
    GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;
CREATE INDEX ds_knowledge_fts_idx ON ds_knowledge.chunks USING GIN (fts_vector);
```

### 2.3 Chunk Strategy Summary

| Source | Chunk Size | Overlap | Strategy |
|--------|-----------|---------|----------|
| Playbook phases | 150–400 tokens | 50 tokens | Phase boundary split |
| Broker metadata | 200–400 tokens | None | One chunk per broker |
| Event patterns (aggregated) | 200–300 tokens | None | One chunk per (broker, event_type) |
| Legal notes | Up to 512 tokens | 64 tokens | H2 section boundary split |
| Email templates | 150–300 tokens | None | One chunk per (broker, response_type) |
| KPI trends | 200–300 tokens | None | One chunk per broker (90d window) |

### 2.4 Retrieval Pattern

**Hybrid retrieval: BM25 + dense cosine, RRF fusion, then cross-encoder reranking**

This is the same pattern proven in Ultra RAG. Do not use pure dense — BM25 is essential
for exact-match queries like broker domain names and error codes.

```
Query flow:
  1. User/system submits query string
  2. Parallel execution:
     a. Dense search: embed query with nv-embedqa-e5-v5, cosine similarity top-40
     b. BM25 search: PostgreSQL ts_rank_cd against fts_vector, top-40
  3. RRF fusion: score = Σ 1/(k + rank_i) with k=60, merge to top-20
  4. Cross-encoder rerank: BGE-reranker-v2-m3 on RTX 5090, pick top-5
  5. Context assembly: concatenate top-5 chunks with metadata headers
  6. Generation: Llama3.1:70b on Spark-1 (already deployed)
```

For Use Case A (playbook generation), skip step 6's standard generation path and use
the structured YAML generation prompt (see Section 3A).

For Use Case C (broker intelligence alerts), skip generation entirely — return ranked
chunks as structured signals to the alert worker.

---

## Section 3 — Three Use Cases End-to-End

### Use Case A: Playbook Generation for New Brokers

**Trigger**: `POST /api/brokers` creates a new broker record with `playbook_file: null`

**Problem**: FORGE needs to write a YAML playbook for a broker that has never been seen before.
The knowledge layer can draft a starting point in under 2 seconds rather than requiring
manual research.

**Pipeline**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ INPUT: New broker registered — name, domain, category, captcha_type │
│        (provided by user at broker creation)                         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────▼──────────────────────────┐
                    │ Query Construction                │
                    │                                  │
                    │ Dense query 1:                   │
                    │  "opt-out form workflow for      │
                    │   {category} broker with         │
                    │   {captcha_type} CAPTCHA"        │
                    │                                  │
                    │ Dense query 2:                   │
                    │  "{domain} data removal form     │
                    │   selectors steps"               │
                    │                                  │
                    │ Filter: source_type IN           │
                    │  ('playbook', 'broker_meta')     │
                    │  AND metadata->>'category'       │
                    │    = '{category}'                │
                    └──────┬──────────────────────────┘
                           │
              ┌────────────▼──────────────────┐
              │ Hybrid Retrieval (BM25 + dense)│
              │ top-5 after rerank             │
              │                               │
              │ Expected results:             │
              │  - 2–3 playbooks from same    │
              │    broker category            │
              │  - broker_meta for similar    │
              │    severity/captcha combos    │
              └────────────┬──────────────────┘
                           │
           ┌───────────────▼────────────────────────────────────┐
           │ Legal Overlay Query (parallel)                      │
           │                                                     │
           │ Dense query:                                        │
           │  "opt-out requirements {state} {data_type}"        │
           │ Filter: source_type = 'legal'                      │
           │ Returns: applicable state law chunk(s)             │
           └───────────────┬────────────────────────────────────┘
                           │
           ┌───────────────▼────────────────────────────────────┐
           │ Generation — Structured YAML Prompt                 │
           │                                                     │
           │ Model: llama3.1:70b on Spark-1                     │
           │                                                     │
           │ System prompt:                                      │
           │  "You are a DataShield playbook author. Output     │
           │   ONLY valid YAML conforming to the schema below.  │
           │   Do not add fields not in the schema.             │
           │   Use {{pii_field}} placeholders exactly as shown  │
           │   in the examples. Use multiple CSS selectors       │
           │   separated by commas for resilience."             │
           │                                                     │
           │ Context assembled:                                  │
           │  <schema.json content>                             │
           │  <3 retrieved similar playbooks>                   │
           │  <legal requirements for user's state>             │
           │  <broker metadata from db>                         │
           │                                                     │
           │ Output: Draft YAML playbook                        │
           └───────────────┬────────────────────────────────────┘
                           │
           ┌───────────────▼────────────────────────────────────┐
           │ Post-Generation Validation                          │
           │                                                     │
           │ 1. JSON Schema validate output against schema.json  │
           │ 2. Check required fields present                    │
           │ 3. Verify all selector fields are non-empty strings │
           │ 4. Verify all {{pii_field}} references are valid   │
           │    (whitelist: full_name, first_name, last_name,   │
           │     emails[0], phones[0], addresses[0],            │
           │     state_of_residence, profile_url, dob)          │
           │ 5. If validation fails → return draft with         │
           │    validation errors for human review              │
           └───────────────┬────────────────────────────────────┘
                           │
           ┌───────────────▼────────────────────────────────────┐
           │ Delivery                                            │
           │                                                     │
           │ Write to src/playbooks/brokers/{domain}.yaml       │
           │ Set broker.playbook_file in DB                     │
           │ Log event: llm_assist, detail: {draft: true,       │
           │   requires_human_validation: true}                  │
           │ Human review flag: true — playbook cannot fire     │
           │ in prod until a human approves the selectors       │
           └────────────────────────────────────────────────────┘
```

**Human review gate is mandatory**. Auto-generated selectors are starting points. CSS selectors
on live broker sites must be verified via Playwright before a real opt-out run.

---

### Use Case B: Privacy Advisor Q&A

**Trigger**: User query in the DataShield dashboard or API endpoint `POST /api/knowledge/query`

**Example queries**:
- "What happened to my removal request on Spokeo?"
- "How long does Whitepages typically take?"
- "Why did my BeenVerified submission fail?"
- "What states have the strongest opt-out rights?"

**Critical constraint**: Case-level answers (specific to an individual) must be sourced from the
operational database, not the knowledge index. The knowledge index answers policy/pattern questions
only. The API layer must route queries to the right source.

**Pipeline**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ User Query + identity_id (authenticated session)                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Query Classifier                   │
              │                                   │
              │ Rule-based (no LLM overhead):     │
              │                                   │
              │ IF query contains "my request",   │
              │    "my case", "my removal"        │
              │ → OPERATIONAL path (DB query)     │
              │                                   │
              │ IF query contains broker name     │
              │    but no "my" → HYBRID path      │
              │                                   │
              │ IF query is general ("how long",  │
              │    "what states", "typical")      │
              │ → KNOWLEDGE path (RAG only)       │
              └───────┬───────────┬───────────────┘
                      │           │
         ┌────────────▼──┐   ┌───▼─────────────────┐
         │ OPERATIONAL   │   │ KNOWLEDGE PATH       │
         │ PATH          │   │                      │
         │               │   │ Hybrid retrieval:    │
         │ DB queries:   │   │  source_type IN      │
         │  cases WHERE  │   │  ('broker_meta',     │
         │  identity_id  │   │   'event_pattern',   │
         │  = {id} AND   │   │   'legal',           │
         │  broker name  │   │   'kpi_trend',       │
         │  matches      │   │   'email_template')  │
         │               │   │                      │
         │  events WHERE │   │ Top-5 after rerank   │
         │  case_id IN   │   │                      │
         │  (above) AND  │   │ Generate answer:     │
         │  event_type   │   │  llama3.1:70b        │
         │  NOT IN       │   │  with strict prompt: │
         │  (redacted)   │   │  "Answer from        │
         │               │   │  context only. If    │
         │ Decrypt name  │   │  not in context,     │
         │ inline for    │   │  say so."            │
         │ display only  │   │                      │
         └───────┬───────┘   └───────┬─────────────┘
                 │                   │
                 └─────────┬─────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Answer Assembly                    │
              │                                   │
              │ Operational facts (if any):       │
              │  "Your Spokeo case was submitted  │
              │   on [date]. Last event: [summary]│
              │   from the audit trail."          │
              │                                   │
              │ Pattern/policy facts (if any):    │
              │  "Spokeo typically confirms in    │
              │   3 days. Confirmation rate: 90%. │
              │   Sends email verification."      │
              │                                   │
              │ Sources cited in response         │
              └────────────────────────────────────┘
```

**API endpoint specification**:

```
POST /api/knowledge/query
Body: {
  "query": "string",
  "identity_id": "uuid | null",   // null = no personal lookup
  "filters": {
    "broker_domain": "string | null",
    "source_types": ["string"] | null
  }
}

Response: {
  "answer": "string",
  "sources": [
    {"source_type": "...", "broker_name": "...", "snippet": "..."}
  ],
  "used_operational_data": boolean,
  "confidence": "high | medium | low"
}
```

---

### Use Case C: Broker Intelligence Alerts

**Trigger**: Celery rescan worker fails with a new/unexpected error pattern. Worker calls
knowledge layer to determine whether this is a known site change before escalating.

**Problem**: When Spokeo changes its opt-out form structure, the first rescan failure should
trigger a knowledge check — "has Spokeo's form changed before? What did the selector look like?
Is there a known pattern for this error?" — rather than immediately hitting human review.

**Pipeline**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ TRIGGER: Celery rescan/submit worker catches unexpected exception    │
│          OR error_code not in playbook.error_indicators             │
│          OR 3+ consecutive failures on same broker in 48h           │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Signal Extraction                  │
              │                                   │
              │ From the failed event:            │
              │  - broker_id, domain              │
              │  - error_code, error_message      │
              │  - event.detail.page_title        │
              │  - event.detail.url_at_failure    │
              │  - event.detail.selector_tried    │
              └────────────┬──────────────────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Change Detection Queries           │
              │ (NO generation — pure retrieval)  │
              │                                   │
              │ Query 1 (error similarity):        │
              │  "broker {domain} form error       │
              │   {error_code} selector failure   │
              │   {error_message_first_30_chars}" │
              │  Filter: broker_domain = {domain} │
              │  Filter: source_type =            │
              │   'event_pattern'                  │
              │                                   │
              │ Query 2 (historical baseline):    │
              │  "{domain} opt-out selectors      │
              │   submit form steps URL"          │
              │  Filter: source_type = 'playbook' │
              │  Filter: domain = {domain}        │
              │                                   │
              │ Returns scored chunks with        │
              │ similarity scores                 │
              └────────────┬──────────────────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Alert Classification               │
              │                                   │
              │ IF top chunk score > 0.88:        │
              │  → KNOWN_PATTERN — error matches  │
              │    historical pattern. Attach     │
              │    matching chunk as context.     │
              │    Auto-retry with modified       │
              │    selector from playbook history.│
              │                                   │
              │ IF top chunk score 0.65–0.88:     │
              │  → POSSIBLE_CHANGE — partial      │
              │    match. Flag for review with    │
              │    "this may be a form change."   │
              │    Attach historical playbook     │
              │    chunk for comparison.          │
              │                                   │
              │ IF top chunk score < 0.65:        │
              │  → NOVEL_FAILURE — no historical  │
              │    context. Escalate immediately. │
              │    Mark broker health_status =    │
              │    'degraded'.                    │
              └────────────┬──────────────────────┘
                           │
              ┌────────────▼──────────────────────┐
              │ Output Actions                    │
              │                                   │
              │ 1. Log event: type=system,        │
              │    summary="Intelligence alert:   │
              │    {classification}",             │
              │    detail={classification,        │
              │    top_chunk_score, retrieved}    │
              │                                   │
              │ 2. For POSSIBLE_CHANGE +          │
              │    NOVEL_FAILURE:                 │
              │    - Set case.human_review = True │
              │    - Attach retrieved chunks as   │
              │      detail.rag_context           │
              │    - Trigger Playbook Update      │
              │      Use Case A in draft mode     │
              │                                   │
              │ 3. For KNOWN_PATTERN:             │
              │    - Log only, continue retry     │
              └────────────────────────────────────┘
```

**Change detection cadence** (separate from per-failure alerts):

A scheduled task runs weekly per active broker:
1. Pull current error_pattern chunks for that broker
2. Compare error_count trend vs. 30 days prior using KPI data
3. If error rate increased > 30% week-over-week → trigger alert pipeline

---

## Section 4 — NVIDIA NeMo Retriever Integration

### 4.1 Which NIM Endpoint

**Embedding**: `nvidia/nv-embedqa-e5-v5`

```
NVIDIA API (cloud):
  POST https://integrate.api.nvidia.com/v1/embeddings
  Headers:
    Authorization: Bearer {NVIDIA_API_KEY}
    Content-Type: application/json
  Body:
    {
      "model": "nvidia/nv-embedqa-e5-v5",
      "input": ["text chunk 1", "text chunk 2", ...],
      "input_type": "passage",    // "passage" for indexing, "query" for search
      "encoding_format": "float",
      "truncate": "END"
    }
  Response:
    { "data": [{"embedding": [...1024 floats...]}, ...] }

Batch size limit: 96 passages per request (NVIDIA limit)
Rate limit (free tier): 40 RPM
Rate limit (paid): 1000 RPM
```

**Reranker**: `nvidia/nv-rerankqa-mistral-4b-v3`

```
POST https://integrate.api.nvidia.com/v1/ranking
Body:
  {
    "model": "nvidia/nv-rerankqa-mistral-4b-v3",
    "query": {"role": "user", "content": "query string"},
    "passages": [
      {"role": "user", "content": "chunk text 1"},
      ...
    ]
  }
Response:
  { "rankings": [{"index": 2, "logit": 4.21}, ...] }

Max passages per call: 40
```

### 4.2 Local NIM on RTX 5090 (Recommended for Production)

Running NIM containers locally eliminates API latency, API costs, and the risk of
operational pattern data leaving the network. RTX 5090 (32GB VRAM) handles both
the embedding NIM and reranker NIM simultaneously.

```bash
# Pull and run nv-embedqa-e5-v5 locally
docker run --gpus all --rm -it \
  -e NVIDIA_API_KEY=${NVIDIA_API_KEY} \
  -p 8001:8000 \
  nvcr.io/nim/nvidia/nv-embedqa-e5-v5:latest

# The local NIM exposes the same OpenAI-compatible API:
POST http://localhost:8001/v1/embeddings
# Same request/response format as cloud endpoint above
# No API key needed for local — auth is handled by NGC license check at startup

# Pull and run reranker locally
docker run --gpus all --rm -it \
  -e NVIDIA_API_KEY=${NVIDIA_API_KEY} \
  -p 8002:8000 \
  nvcr.io/nim/nvidia/nv-rerankqa-mistral-4b-v3:latest

POST http://localhost:8002/v1/ranking
```

**VRAM budget on RTX 5090 (32GB)**:
- nv-embedqa-e5-v5: ~4GB VRAM
- nv-rerankqa-mistral-4b-v3: ~8GB VRAM
- Remaining for RTX 5090 workloads: ~20GB

This is well within budget. Both NIMs can run simultaneously.

### 4.3 Embedding Client Module (for FORGE)

```python
# src/knowledge/embedder.py

import httpx
from typing import List
import os

NIM_BASE = os.getenv("NIM_EMBED_URL", "http://localhost:8001")  # local NIM
NIM_CLOUD = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

class NIMEmbedder:
    def __init__(self, local: bool = True):
        self.base = NIM_BASE if local else NIM_CLOUD
        self.headers = {} if local else {"Authorization": f"Bearer {NVIDIA_API_KEY}"}

    def embed_passages(self, texts: List[str]) -> List[List[float]]:
        """Embed up to 96 texts as passages (for indexing)."""
        response = httpx.post(
            f"{self.base}/v1/embeddings",
            headers=self.headers,
            json={
                "model": "nvidia/nv-embedqa-e5-v5",
                "input": texts,
                "input_type": "passage",
                "encoding_format": "float",
                "truncate": "END",
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single search query."""
        # input_type="query" uses query-tuned instruction prefix
        response = httpx.post(
            f"{self.base}/v1/embeddings",
            headers=self.headers,
            json={
                "model": "nvidia/nv-embedqa-e5-v5",
                "input": [text],
                "input_type": "query",
                "encoding_format": "float",
                "truncate": "END",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
```

---

## Section 5 — Implementation Roadmap

### Phase 1 — Weeks 1–2: Core Index and Basic Search

**Goal**: Playbook YAML files + broker metadata searchable via API. Privacy Advisor can answer
structural questions about broker workflows and CAPTCHA types.

**Tasks**:

1. Database setup (Day 1–2)
   - Add `pgvector` extension to DataShield PostgreSQL (already in migration 001 with pgcrypto —
     add `CREATE EXTENSION IF NOT EXISTS vector`)
   - Create `ds_knowledge` schema with `chunks` table + HNSW index + FTS index
   - Create `ds_knowledge_writer` role (write to ds_knowledge, read-only on brokers)
   - Create `ds_knowledge_reader` role (read ds_knowledge only — used by query API)

2. NIM setup (Day 2–3)
   - Pull nv-embedqa-e5-v5 NIM container on RTX 5090
   - Pull nv-rerankqa-mistral-4b-v3 NIM container on RTX 5090
   - Add `NIM_EMBED_URL` and `NIM_RERANK_URL` to DataShield `.env`
   - Write `src/knowledge/embedder.py` (see Section 4.3)
   - Write `src/knowledge/reranker.py` (same pattern, calls reranker NIM)

3. Ingestion pipeline (Day 3–6)
   - Write `src/knowledge/ingest/playbook_ingestor.py`
     - Reads `src/playbooks/**/*.yaml`, chunks at phase boundaries
     - Renders structured text per chunk, calls embedder, upserts to ds_knowledge.chunks
     - Uses content_hash to skip unchanged chunks (idempotent)
   - Write `src/knowledge/ingest/broker_ingestor.py`
     - Reads brokers table, renders text, embeds, upserts
   - Write `src/knowledge/ingest/legal_ingestor.py`
     - Reads `src/knowledge/legal/*.md`, chunks at H2, embeds, upserts
   - Add Celery beat task: `ingest_knowledge_sources` — runs nightly at 02:00

4. Query layer (Day 6–10)
   - Write `src/knowledge/retriever.py`
     - `hybrid_search(query, source_types, broker_domain, top_k=5)` — BM25 + dense + RRF + rerank
   - Add FastAPI router: `src/api/routers/knowledge.py`
     - `POST /api/knowledge/query` — implements query classifier + retriever + response assembly
     - `GET /api/knowledge/status` — chunk counts per source_type, last ingest timestamps

5. Seed + verify (Day 10–14)
   - Run full ingest on existing playbooks (spokeo, beenverified, whitepages)
   - Run full ingest on broker table
   - Manual test queries to verify retrieval quality
   - Verify PII exclusion: assert no identity_id appears in any chunk content

**Phase 1 deliverable**: `GET /api/knowledge/query?q=how+long+does+spokeo+take` returns a
factual answer grounded in the playbook and broker KPI data.

---

### Phase 2 — Weeks 3–4: Event Pattern RAG and Privacy Advisor Q&A

**Goal**: Event log aggregate patterns indexed. Privacy Advisor answers "why did X fail?" and
"what's the Whitepages track record?" questions with data from operational history.

**Tasks**:

1. Event pattern aggregation (Day 1–3)
   - Write SQL materialized view `ds_knowledge.broker_event_patterns`
     (stripped projection as specified in Section 1.2 Source 6)
   - Write `src/knowledge/ingest/event_pattern_ingestor.py`
   - Write `src/knowledge/ingest/kpi_trend_ingestor.py`
   - Add to nightly Celery beat task

2. Case aggregate view (Day 3–4)
   - Create materialized view `ds_knowledge.broker_performance`
   - Wire into broker_ingestor (refresh performance stats nightly alongside metadata)

3. Privacy Advisor hybrid path (Day 4–8)
   - Extend `/api/knowledge/query` to handle HYBRID path:
     - Operational DB lookup for case/event data (identity_id required, PII decrypted
       in-memory, displayed in response but never written to knowledge index)
     - Knowledge index lookup for patterns/policies
   - Implement query classifier (see Section 3, Use Case B)

4. Dashboard integration (Day 8–14)
   - Add "Ask DataShield" text input to dashboard
   - Wire to `POST /api/knowledge/query` with authenticated `identity_id`
   - Display answer with cited sources

**Phase 2 deliverable**: Dashboard Ask field correctly answers "Why did my BeenVerified
submission fail?" by combining the operational case event trail with the indexed error
pattern knowledge.

---

### Phase 3 — Month 2: Broker Intelligence Alerts and Playbook Auto-Generation

**Goal**: Proactive change detection running in the background. New broker playbook drafts
auto-generated on broker registration.

**Tasks**:

1. Alert pipeline (Week 1–2)
   - Write `src/knowledge/intelligence.py`
     - `classify_failure(broker_id, error_code, error_message, selector_tried)` → classification
     - Called from `workers/submit.py` and `workers/rescan.py` on unexpected exceptions
   - Write weekly broker health trend check Celery task
   - Log intelligence events to `events` table with `event_type='system'` and
     `detail.rag_classification`

2. Email template indexing (Week 2)
   - Write `src/knowledge/ingest/email_template_ingestor.py`
   - Write PII scrub utility: `src/knowledge/pii_scrubber.py`
     - Strips email addresses, SSN-like patterns, name/DOB occurrences
     - Keeps broker name, response type, date, body template text

3. Playbook auto-generation (Week 3–4)
   - Write `src/knowledge/playbook_generator.py`
     - Orchestrates retrieval → legal overlay → structured YAML generation
     - Validates output against `schema.json`
     - Writes draft to `src/playbooks/brokers/{domain}_draft.yaml`
   - Hook into `POST /api/brokers` endpoint
   - Add human review flag — `broker.health_status = 'draft_pending_review'`
   - Add dashboard UI: "Review auto-generated playbook" flow

4. Eval loop (Week 4)
   - Write 20 retrieval test cases (query, expected_source_type, expected_broker)
   - Track MRR@5 and NDCG@5 per source_type
   - Baseline before any embedding model or chunk strategy change

---

## Section 6 — Connection to Existing Ultra RAG

### Decision: Deploy Separate RAG Instance (Option B)

**Do not add a "datashield" collection to Ultra RAG.**

Rationale, ranked by decision weight:

**1. Data isolation is the primary driver.** Ultra RAG at `ultrarag.app` is a public-facing
endpoint. Its collections (`imds`, `personal`) are queried through a Cloudflare-tunneled public
URL. Even with RLS, sharing a PostgreSQL instance or a running RAG server between public-facing
queries and DataShield operational patterns creates an attack surface that does not need to exist.
The Ultra RAG memory in MEMORY.md explicitly notes the system was designed for IMDS (Air Force
business data) and personal documents — categories with different trust postures than private
removal workflow intelligence.

**2. The embedding model is different.** Ultra RAG currently uses `nomic-embed-text-v1.5`
(384 dimensions, via Ollama). DataShield Knowledge Layer should use `nv-embedqa-e5-v5`
(1024 dimensions, retrieval-tuned). Adding a second embedding model to Ultra RAG's ingestion
pipeline adds operational complexity to a system already running four gunicorn workers on Spark-1.
Better to keep the two systems independent.

**3. Operational coupling risk.** Ultra RAG is a research tool — Ron queries it ad hoc for IMDS
and personal knowledge. DataShield Knowledge Layer is a production system dependency — broker
alert workers and playbook generation depend on it at runtime. If Ultra RAG restarts or degrades,
DataShield's operational intelligence should not degrade with it.

**4. Schema incompatibility.** Ultra RAG uses `rag.chunks` with 384-dim vectors. DataShield
uses `ds_knowledge.chunks` with 1024-dim vectors in the same PostgreSQL instance (or the
DataShield PostgreSQL on a different port). These cannot share a vector index cleanly without
migration.

**What to reuse from Ultra RAG**: The retrieval pattern (hybrid BM25 + dense + RRF + reranker),
the RLS design (separate reader role, session-scoped collection filter), and the bridge queue
pattern (durable outbox for async writes). These are architectural patterns, not shared code —
FORGE should implement them independently in `src/knowledge/`.

**Configuration**:

```
Ultra RAG stays on:    Spark-1, port 8300, ultrarag.app
                       Collections: imds, personal
                       Embedding: nomic-embed-text-v1.5 (384d)

DataShield Knowledge:  DataShield host, ds_knowledge schema in DataShield PostgreSQL
                       Embedding: nv-embedqa-e5-v5 (1024d) via local NIM on RTX 5090
                       Exposed: /api/knowledge/* in the DataShield FastAPI app
                       No public tunnel — internal API only
```

The only point of integration between the two systems: if Ron asks Ultra RAG a question that
is better answered by DataShield Knowledge (e.g., "how long does Spokeo typically take?"),
that is a user-routing decision, not a system coupling. Both systems answer the question
independently.

---

## Architecture Diagram — Full System

```
╔══════════════════════════════════════════════════════════════════════════╗
║                     DataShield Knowledge Layer                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  KNOWLEDGE SOURCES (PII-free)          VECTOR STORE                     ║
║  ┌─────────────────────────────┐       ┌──────────────────────────────┐ ║
║  │ src/playbooks/**/*.yaml     │──────▶│ ds_knowledge.chunks          │ ║
║  │ src/knowledge/legal/*.md    │       │  - 1024-dim vectors          │ ║
║  │ src/knowledge/email_templ/  │       │  - HNSW index                │ ║
║  │ brokers table (nightly)     │       │  - GIN full-text index       │ ║
║  │ broker_event_patterns view  │       │  - metadata JSONB            │ ║
║  │ broker_performance view     │       │  - source_type filter        │ ║
║  │ kpi_snapshots (nightly)     │       └──────────────────────────────┘ ║
║  └─────────────────────────────┘                    ▲                   ║
║                    │                                │                   ║
║                    ▼                                │                   ║
║  ┌─────────────────────────────┐       ┌────────────┴─────────────────┐ ║
║  │ Ingest Pipeline (Celery)    │       │ NIM: nv-embedqa-e5-v5        │ ║
║  │  playbook_ingestor.py       │──────▶│  RTX 5090, port 8001         │ ║
║  │  broker_ingestor.py         │       │  1024-dim embeddings         │ ║
║  │  event_pattern_ingestor.py  │       └──────────────────────────────┘ ║
║  │  legal_ingestor.py          │                                        ║
║  │  email_template_ingestor.py │                                        ║
║  │  kpi_trend_ingestor.py      │                                        ║
║  └─────────────────────────────┘                                        ║
║                                                                          ║
║  QUERY LAYER                                                             ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │                      retriever.py                                 │   ║
║  │                                                                   │   ║
║  │  Query                                                            │   ║
║  │    │                                                              │   ║
║  │    ├── Dense search (embed query → cosine top-40) ────────────┐  │   ║
║  │    │                                                           │  │   ║
║  │    └── BM25 search (ts_rank_cd top-40) ──────────────────────┐│  │   ║
║  │                                                               ││  │   ║
║  │                          RRF fusion (top-20) ◀───────────────┘│  │   ║
║  │                                     │        ◀────────────────┘  │   ║
║  │                                     ▼                             │   ║
║  │                          Reranker NIM top-5                       │   ║
║  │                          nv-rerankqa-mistral-4b-v3                │   ║
║  │                          RTX 5090, port 8002                      │   ║
║  │                                     │                             │   ║
║  │                                     ▼                             │   ║
║  │                          Context Assembly                         │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
║                                        │                                 ║
║                     ┌──────────────────┼──────────────────┐             ║
║                     ▼                  ▼                  ▼             ║
║             USE CASE A          USE CASE B          USE CASE C          ║
║          Playbook Generator   Privacy Advisor    Intel Alerts            ║
║          llama3.1:70b (S1)    llama3.1:70b (S1) (no generation)        ║
║          → YAML draft         → text answer     → classification        ║
║                                                                          ║
║  SEALED ZONE (never enters knowledge index)                             ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │ identities (encrypted PII) │ cases.profile_url │ case events    │   ║
║  │ breach_alerts              │ drop_filings      │ matched_fields  │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Risks and Caveats

**Risk 1 — NIM licensing**: NVIDIA NIM requires an NGC API key and license acceptance. Free
tier has rate limits that will not support bulk ingest of 50K+ chunks in one pass. Phase 1
ingest should batch with 0.5s sleep between requests on free tier, or Ron needs to confirm
paid NIM access. Fallback: use nomic-embed-text-v1.5 via Ollama on RTX 5090 for ingest
(free, local) and switch to NIM for query-time (low volume, within free rate limits).

**Risk 2 — Event pattern PII leakage**: The event aggregation query in Section 1.2 Source 6
must be written carefully. The `events.detail` JSONB field in the current schema may contain
profile URLs or matched_fields from search results. The aggregation query must explicitly
exclude `detail` and `summary` fields that contain user-identifiable content. FORGE must
run the ingest output through a PII assertion test before Phase 2 goes live.

**Risk 3 — LLM hallucination in playbook generation**: The auto-generated YAML will hallucinate
CSS selectors for brokers it has never seen. This is expected and acceptable because the human
review gate is mandatory. The risk is if that gate is bypassed in a future automation sprint.
FORGE must enforce: `broker.health_status = 'draft_pending_review'` blocks the broker from
entering the dispatch queue until a human approves the playbook.

**Risk 4 — Ultra RAG interference**: The existing Ultra RAG system on this PC's PostgreSQL
instance uses the `rag` schema. The DataShield Knowledge Layer uses `ds_knowledge` schema
in DataShield's PostgreSQL instance. Confirm these are separate PostgreSQL instances (different
ports) or explicitly separate schemas with non-overlapping roles before Phase 1 ingest.
MEMORY.md shows Ultra RAG is at `D:\rag-ingest` (PC-local) and production is on Spark-1.
DataShield runs on localhost. These should be on different ports — verify before migration 002.

**Risk 5 — Chunk quality for event patterns**: Aggregated event patterns will be sparse until
DataShield accumulates 6+ months of operational history. Phase 2 retrieval quality for
event-pattern queries will be low initially. Set user expectation: Privacy Advisor Q&A answers
about "how long does X take" will be accurate from broker metadata (Phase 1) but answers about
"why do X requests fail" will improve over time as event patterns accumulate.

---

## Recommendation Summary

**Single ranked answer**: Build DataShield's own isolated knowledge layer in `ds_knowledge`
schema within the DataShield PostgreSQL instance. Use NIM containers on RTX 5090 for embeddings
(local, zero external API dependency). Do not couple to Ultra RAG. Execute Phase 1 immediately —
it is a 2-week FORGE sprint that produces immediate query value from existing playbooks and
broker metadata, with zero disruption to the operational system.

## Next Actions

1. **FORGE**: Confirm DataShield runs on a separate PostgreSQL port from Ultra RAG (check
   `src/api/database.py` connection string vs. `D:\rag-ingest` config). Document the port
   in DataShield `.env` before any schema migration.

2. **FORGE**: Add `CREATE EXTENSION IF NOT EXISTS vector;` to a new migration
   `src/migrations/002_knowledge_layer.sql` and create the `ds_knowledge` schema + tables.

3. **FORGE**: Pull NIM containers on RTX 5090. Verify both fit in VRAM simultaneously with
   `nvidia-smi` after startup. Target: both running, <12GB combined VRAM.

4. **FORGE**: Implement `playbook_ingestor.py` first — smallest, safest, highest immediate
   value. Run against the 3 existing playbooks (spokeo, beenverified, whitepages). Manually
   verify retrieval with 5 test queries before wiring the broker_ingestor.

5. **SENTINEL**: Review the event projection query (Section 1.2 Source 6) before Phase 2
   ingest runs. Confirm no identity_id or case-linked PII makes it into `ds_knowledge.chunks`.
   This is a mandatory security gate before event pattern indexing goes live.

6. **Ron**: Confirm whether NVIDIA API key is available for NIM cloud fallback during
   Phase 1. If not available, FORGE should configure Ollama nomic-embed-text-v1.5 as the
   primary embedder for Phase 1 and swap to NIM when licensed.
