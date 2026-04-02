# NOVA: NVIDIA Blueprints — "Smarter With Every Action"
**Strategic Analysis | SENTINEL-Corrected**
**Date**: 2026-03-27 | **Status**: Final (post-audit)

---

## 1. What Ron Asked

> "We have all these agents and what are we building if not something that gets bigger and smarter with every action?"

That question is about **flywheel mechanics**. A flywheel doesn't just accumulate data — it converts activity into capability, which drives more activity, which drives more capability. The three NVIDIA blueprints in the DGX Spark playbook (Multi-Agent Chatbot, Video Search & Summarization, Data Flywheel) each address a different layer of that loop.

The core tension in the current ecosystem: **data is accumulating but nothing is learning from it.** The agents produce structured outputs. The NLF consumer captures corrections. The Spark cluster has 240GB of unified inference memory sitting idle overnight. The loop is almost closed — but "almost" means it isn't spinning.

---

## 2. The Five Learning Loops — Honest Status

| Loop | What It Does | Status | Evidence Source |
|------|-------------|--------|----------------|
| **Memory** | Session → MemoryWeb → injected into next session | **PARTIAL** | Per memory docs — works for Ron's sessions; broken at scale for Spark-1 agents (ingest path not wired) |
| **Retrieval** | Query → Ultra RAG → UCB re-rank → better answers | **PARTIAL** | Per memory docs — IMDS corpus only (4,015 chunks); no aihangout.ai bridge; community content not indexed |
| **Model Improvement** | Activity data → fine-tune → cheaper/smarter model | **NOT WORKING** | Per memory docs — data captured via workload_id tagging; zero fine-tune cycles ever run; Data Flywheel deployed on Spark-2 but idle |
| **Correction** | Craig corrects → NLF captures → training data | **CAPTURED, NOT APPLIED** | Per memory docs — NLF consumer in dry-run; data exists, no training pipeline consuming it |
| **Community** | aihangout.ai activity → Ultra RAG → enriched answers | **NOT CONNECTED** | Per memory docs — platform live, content accumulating, no bridge to retrieval layer |

**Verdict**: Of five loops, zero are fully closed. The ecosystem is accumulating without compounding. Every day of inaction on Loop 3 (Data Flywheel) is a day of lost training signal that cannot be recovered.

---

## 3. What Each NVIDIA Blueprint Actually Does

### Blueprint A: Multi-Agent Chatbot
**(SENTINEL-verified)**

**Architecture confirmed:**
- LangGraph state machine: `START → generate → should_continue → (action → generate) | END`
- 3-iteration cap on tool-calling loops (`max_iterations = 3`)
- **4 MCP servers** (confirmed exact file listing):
  - `rag.py` — document retrieval
  - `code_generation.py` — DeepSeek-Coder-6.7B on llama.cpp (confirmed)
  - `image_understanding.py` — Qwen**2**-VL-7B via TensorRT-LLM (Docker deploys Qwen2, not 2.5; the MCP code references 2.5 — upstream repo discrepancy)
  - `weather_test.py` — mock/demo only, hardcoded fake responses
- Primary model: gpt-oss-120b (default in config.py)
- Routing: function-calling for tool selection, BUT hardcoded string matching determines which models support tools (checks for "gpt-oss-20b" and "gpt-oss-120b" by name) — hybrid, not pure dynamic routing
- Storage: PostgreSQL with 3 tables (conversations, chat_metadata, images), multi-tier cache, TTLs (300s default, 3600s images)
- Embedding: Qwen3-Embedding-4B-Q8_0 (confirmed)
- Vector DB: Milvus — standard CPU deployment, 1000-char chunks, 200 overlap (GPU acceleration claim is **false** for this deployment)

**What it does NOT do:** No feedback loop, no preference learning, no retraining. The system persists conversations but does not improve from them. This is confirmed by design — it's a reference implementation, not a production learning system.

**Key pattern worth adopting:** MCP-as-agent-interface enables composable tool dispatch. Any new capability (VSS, BehaviorShield, CivicMind sensors) can be exposed as an MCP server and plugged into the supervisor without touching the core agent logic.

---

### Blueprint B: Video Search and Summarization (VSS)
**(SENTINEL-verified, partial — some details unconfirmable from public repo)**

**Architecture confirmed:**
- 4-layer stack: NIM models → Kafka stream processing → Elasticsearch metadata → agent layer
- NIM models in use: Cosmos-Reason2-8B (VLM), Nemotron-Nano-9B-v2 (LM) — confirmed
- Message bus: Kafka (Confluent Platform 8.1.1), **19 topics** (confirmed exact count)
- Metadata: Elasticsearch 9.3.0, port 9200
- Agent orchestration: LangGraph + NVIDIA AIQ Toolkit (confirmed via source code)
- **19 registered agent tools** (confirmed from `register.py` — NOT 28; the 28 figure is raw filesystem items including subdirectories and helpers)
- Tool names from actual registry: `attribute_search`, `incidents`, `embed_search`, and 16 others — these are the real names, not the previously claimed list
- **5 reference workflows confirmed:**
  1. Q&A and Report Generation
  2. Alert Verification
  3. Real-Time Alerts
  4. Video Search
  5. Long Video Summarization
- Supported on DGX Spark with DGX OS 7.4.0 (confirmed)

**MCP server note:** A MCP server is mentioned in the project but port 9901 and the previously cited tool names (`get_incident`, `get_sensor_ids`, etc.) **could not be confirmed** from any accessible file in the public repo. Do not rely on those specifics.

**Why it matters for the ecosystem:**
- BehaviorShield (mAP 93.3% trained) has no query interface — VSS provides exactly that pattern
- CivicMind's municipal surveillance use case maps directly to the 4-layer VSS architecture
- The Kafka event stream architecture handles the scale that Spark-1's current polling approach cannot
- Natural fit: plug BehaviorShield detection outputs into Kafka topics → VSS agent layer provides Q&A on incidents

**Hardware note:** VSS requires substantial NIM hosting. Assess GPU/licensing requirements from the DGX OS 7.4.0 playbook before committing — Spark-1 at 95% disk capacity (204GB free, confirmed this session) is not ready for another full stack deployment without cleanup first.

---

### Blueprint C: Data Flywheel
**(SENTINEL-verified | Already deployed on Spark-2)**

**Status:** Deployed and confirmed via `docker inspect` this session — `nvidia-data-flywheel` compose config present on Spark-2. **This is the missing piece that closes Loop 3.**

**Architecture confirmed:**
- **9 logical pipeline stages** (documented in `docs/08-workflow-orchestration.md`):
  1. `initialize_workflow`
  2. `create_datasets`
  3. `wait_for_llm_as_judge`
  4. `spin_up_nim`
  5. `run_base_eval`
  6. `run_icl_eval`
  7. `start_customization`
  8. `run_customization_eval`
  9. `finalize_flywheel_run`
- **13 total Celery tasks** (includes orchestration/cleanup: `run_generic_eval`, `shutdown_deployment`, `run_nim_workflow_dag`, `delete_job_resources`)
- Fine-tuning: NeMo Customizer, LoRA (epochs=2, batch=16, lr=0.0001, adapter_dim=32)
- Evaluation: NeMo Evaluator as LLM-as-judge
- **4 confirmed evaluation metrics:**
  1. `similarity` — integer 1-10, LLM-judged
  2. `function_name` — float 0-1, programmatic
  3. `function_name_and_args_accuracy` — float 0-1, programmatic
  4. `tool_calling_correctness` — integer 0 or 1, LLM-judged
- ICL: `semantic_similarity` or `uniform_distribution` selection, 1-3 examples/prompt, max 32,768 token context
- Workload isolation: `workload_id` tags each distinct LLM call type — this is how it knows which call patterns to optimize

**Pipeline autonomy (corrected framing):**
The evaluation pipeline **runs fully automatically** — no human approval gates exist in the DAG. What requires human review is the final promotion of a fine-tuned model to replace the production model. The broader claim "does NOT auto-deploy" is true but incomplete — the entire pipeline up to that point runs without human intervention.

**The 98.6% cost reduction:**
Confirmed from the README. HR chatbot benchmark: fine-tuned Llama-3.2-1B matched ~98% accuracy of Llama-3.1-70B baseline on tool-calling. **This figure is workload-specific** — it reflects a narrow, well-defined tool-calling task. Do not generalize to all inference workloads.

**GPU requirements (internal repo inconsistency noted):**
- README: 6x H100/A100 for local LLM judge, 2x for remote judge
- `config.yaml`: 4 GPUs for judge
- The repo contradicts itself. The 2-GPU minimum for remote judge is confirmed. The local judge figure should be validated before planning hardware.

---

## 4. How They Connect — The Integration Architecture

The flywheel closes when all five loops feed each other:

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE COMPLETE LOOP                          │
│                                                                 │
│  Agent acts                                                     │
│      │                                                          │
│      ▼                                                          │
│  LLM call logged with workload_id ──────► Elasticsearch         │
│      │                                        │                 │
│      ▼                                        ▼                 │
│  Craig corrects ──► NLF captures ──► Training data pool        │
│      │                                        │                 │
│      ▼                                        ▼                 │
│  MemoryWeb ingests session ◄── Data Flywheel reads logs         │
│      │                             │                            │
│      ▼                             ▼                            │
│  Next session smarter ◄── LLM-as-judge A/B eval                │
│                             │                                   │
│                             ▼                                   │
│                     Human reviews ──► promotes smaller model    │
│                             │                                   │
│                             ▼                                   │
│                     Freed VRAM ──► more concurrent tasks        │
│                             │                                   │
│                             ▼                                   │
│                     More data ──► flywheel spins faster ──►─┐  │
│                                                              │  │
│  ◄───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**The VSS layer adds video modality:**
```
BehaviorShield detects event
    │
    ▼
Kafka topic (mdx-behavior or mdx-alerts)
    │
    ▼
VSS agent layer (19 tools, LangGraph + NAT)
    │
    ▼
Q&A / Alert Verification / Video Search workflows
    │
    ▼
Structured incident data → Elasticsearch → Data Flywheel reads it
```

**The MCP composability pattern:**
```
Any new capability (BehaviorShield, CivicMind, Ultra RAG, NLF)
    │
    ▼
Exposed as MCP server (following multi-agent chatbot pattern)
    │
    ▼
Plugged into supervisor without touching core agent logic
    │
    ▼
Immediately available to all agents via tool dispatch
```

---

## 5. Priority Order (When Sparks Are Free)

**Ranked by flywheel impact, not complexity:**

### Priority 1: Run First Data Flywheel Cycle
**Closes: Loop 3 (model improvement)**
- Already deployed on Spark-2 — this is activation, not installation
- Pick one workload with sufficient data (AI Army OS tool calls are the obvious candidate — 153+ tasks/day generates structured logs)
- Tag existing LLM calls with `workload_id` if not already done
- Run one full cycle: base eval → ICL eval → LoRA fine-tune → comparison
- Even a failed cycle produces calibration data. A successful cycle frees VRAM and proves the loop works.
- **Prerequisite**: Spark-2 has 2.4TB free and 121GB RAM (confirmed this session) — capacity is not the blocker

### Priority 2: Activate NLF Consumer
**Closes: Loop 4 (correction → training data)**
- Consumer is in dry-run — data is captured but not flowing into training
- Activation path: connect NLF output to Data Flywheel dataset creation step
- This means corrections Craig makes today become training examples for next month's model
- Low lift, high leverage — the data collection is already working

### Priority 3: Fix shared_chat MemoryWeb Ingest at Scale
**Closes: Loop 1 for agents (not just Ron's sessions)**
- Per documentation: Spark-1 agents don't have the ingest path wired
- Fix: wire `mw_post_session.py` equivalent for agent sessions on Spark-1
- Without this, agent learning is one-directional — they consume Ron's memories but don't contribute their own

### Priority 4: Evaluate VSS Hardware/Licensing Requirements
**Enables: Loop 5 (video modality) + BehaviorShield + CivicMind**
- Do not deploy — assess only
- Read the DGX OS 7.4.0 playbook sections on VSS hardware requirements
- Check if Spark-1 disk (currently 95% full, 204GB free) can be cleared enough to host VSS
- Licensing: NVIDIA NIM microservices for Cosmos-Reason2-8B and Nemotron-Nano-9B — confirm NGC entitlement covers these
- Decision point: deploy full VSS stack on Spark-2 (2.4TB free) or wait for dedicated hardware

### Priority 5: Multi-Agent Chatbot Pattern Adoption
**Impact: Composability — lower urgency**
- The chatbot itself is a reference demo (weather mock tool confirms this)
- The valuable pattern: MCP-as-agent-interface for composable tool dispatch
- Adoption means: wrap BehaviorShield, NLF, and Ultra RAG query as MCP servers
- Each becomes a first-class citizen in any supervisor agent without custom integration work
- No deployment required — this is a refactor pattern, applies when touching those services

---

## 6. Flywheel Scorecard

**Current state per documentation (not live-verified this session):**

| Spoke | Score | Max | Notes |
|-------|-------|-----|-------|
| Data collection | 5 | 6 | Logs flowing; workload_id tagging partial |
| Data → Model | 4 | 6 | Flywheel deployed, no cycles run |
| Models → Responses | 2 | 4 | Base models only, no fine-tuned variants in production |
| Memory (session) | 4 | 6 | Works for Ron; broken for agents at scale |
| Retrieval quality | 6 | 8 | IMDS good; no community content bridge |
| Correction loop | 4 | 6 | NLF capturing; consumer inactive |
| Multi-modal | 2 | 4 | BehaviorShield trained but no query interface |
| Community signal | 2 | 4 | Platform live; no indexing pipeline |
| **TOTAL** | **29** | **38** | **76%** |

**First fine-tune cycle impact estimate:** +6 points (data→model + models→responses closes to near-max). Scorecard would move to 35/38 (92%) with Priorities 1-3 complete.

**Weakest spokes requiring action:**
1. `data → model` (4/6) — closed by Priority 1
2. `models → responses` (2/4) — closed by Priority 1
3. `community signal` (2/4) — requires aihangout→Ultra RAG bridge (not in current priorities, but noted)
4. `multi-modal` (2/4) — closed by VSS deployment (Priority 4+)

---

## 7. What's Verified vs What's Documented

**Critical distinction: some claims below are SSH-confirmed facts from this session. Others are sourced from memory files and have not been live-verified.**

### SSH-Confirmed This Session
| Fact | Evidence |
|------|---------|
| Data Flywheel deployed on Spark-2 | `docker inspect` showed nvidia-data-flywheel compose config |
| vllm-head on Spark-1, vllm-worker on Spark-2 | `docker ps` confirmed both containers running |
| 3 GGUF model files on Spark-1 (~70GB total) | `ls -lh` showed files present |
| Spark-1 disk: 95% full, 204GB free | `df -h` |
| Spark-2 disk: 33% used, 2.4TB free | `df -h` |
| Spark-2 RAM: 89/121GB in use | `free -h` |
| LangGraph state machine in multi-agent chatbot | SENTINEL repo inspection of `backend/agent.py` |
| 4 MCP servers (exact filenames) | SENTINEL repo inspection of `backend/tools/mcp_servers/` |
| 19 registered VSS agent tools | SENTINEL repo inspection of `agent/src/vss_agents/tools/register.py` |
| Data Flywheel: 9 logical stages, 13 Celery tasks | SENTINEL repo inspection of source + docs |
| 4 evaluation metrics (exact names) | SENTINEL repo inspection of `docs/06-evaluation-types-and-metrics.md` |
| Qwen2-VL-7B (not 2.5) in Docker | SENTINEL repo inspection of `docker-compose-models.yml` |
| Milvus is CPU, not GPU-accelerated | SENTINEL repo inspection — no GPU config found |

### Per Documentation (Memory Files — Not Live-Verified This Session)
| Claim | Source |
|-------|--------|
| MemoryWeb: 1,147 memories, 1,225 embeddings | memory/MEMORY.md |
| Ultra RAG: 4,015 IMDS chunks, 100% embedded | memory/MEMORY.md |
| AI Army OS: 153+ tasks/day | memory/project_ai_army_os.md |
| BehaviorShield: mAP 93.3% | memory/CLAUDE.md active projects table |
| NLF consumer in dry-run | memory/project_active_projects_spark.md |
| MemoryWeb ingest broken at scale on Spark-1 | memory/MEMORY.md MemoryWeb notes |
| Zero fine-tune cycles ever run | memory/MEMORY.md — no fine-tune status recorded |
| Spark cluster: 240GB unified inference | memory/spark_cluster_infrastructure.md |

---

## 8. Bottom Line

The ecosystem is not broken — it's incomplete. Every component that would make it "smarter with every action" exists:
- Data collection: ✓ working
- Correction capture: ✓ working
- Fine-tune infrastructure: ✓ deployed (Spark-2)
- Memory injection: ✓ working for Ron
- Retrieval: ✓ working for IMDS

What's missing is the **activation step** for Loop 3. The Data Flywheel is on Spark-2, configured, deployed, and waiting. Running one cycle — even on a narrow workload — proves the mechanism and changes the trajectory from "accumulating platform" to "self-improving platform."

That's the answer to what we're building: **a platform that gets smarter faster than any single agent or dataset addition can make it, because it compounds.**

The NVIDIA blueprints don't add new capabilities. They provide the missing connective tissue — specifically the Data Flywheel as the engine that converts accumulated activity into deployed model improvements. Run the first cycle.

---

*NOVA analysis complete. All technical claims SENTINEL-verified or clearly marked as per-documentation.*
*Reference: `Owner's Inbox/SENTINEL-nvidia-repo-claim-audit.md` for full 28-claim audit trail.*
