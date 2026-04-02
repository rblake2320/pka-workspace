# NVIDIA AI Blueprints — Tier 1 Implementation Complete
**Date:** 2026-03-23
**Routed by:** AXIOM → FORGE (build) + SENTINEL (validated) + HELM (coordination)

---

## What's Live Now

### 1. Safety Guardrails — Coder Agent (DEPLOYED + TESTED)
**Status: LIVE — 7/7 red-team tests passing**

The coder agent on Spark-1 previously wrote and committed code with zero output validation.
One hallucinated destructive command would have been catastrophic. Now fixed.

**What's deployed:**
- `~/ai-army-os/agent_guardrails.py` — pattern-based guardrail engine (8 BLOCK rules, 4 WARN rules)
- `~/ai-army-os/agents/coder.py` — patched to check every file before writing
- `~/ultra-rag/src/prompt_guard.py` — extended with output-side `validate_agent_output()`

**What it blocks:**
| Rule | Example |
|------|---------|
| `force_push` | `git push --force` in generated code |
| `hard_reset` | `git reset --hard` |
| `credential_files` | Reading `.env`, `.pem`, `.key`, `id_rsa` |
| `env_secret_dump` | `os.getenv("OPENAI_API_KEY")` |
| `shell_injection` | `subprocess.run(f"ls {user_input}")` |
| `recursive_delete` | `shutil.rmtree("/")` |
| `path_policy` | Writing outside allowed project directories |
| `size_limit` | >500KB single file, >2MB per task |

**Warnings (logged, not blocked):** eval/exec, external HTTP calls, chmod 777, pickle.loads

**Latency overhead:** ~0ms (pattern matching, no network call)

**NeMo Guardrails path forward:** Install `nemoguardrails` for AI-powered contextual checks on top of this.

---

### 2. Data Flywheel — Wired and Ready to Run
**Status: WIRED — 2,894 training examples ready, first cycle pending**

**What's deployed:**
- `~/data-flywheel/army_os_wiring.py` — pulls from 2 live production sources:
  - `rag.query_log` + chunks → 50 RAG query examples (weak supervision)
  - `army_os.tasks` (completed tasks) → 2,844 real prompt→response pairs
- `~/data-flywheel/nemo_curator_pipeline.py` — quality filter + Jaccard near-dedup
- `~/data-flywheel/fine_tune_trigger.py` — hardware-routed LoRA/QLoRA training with NIM teacher labeling
- `~/ai-army-os/llm_router.py` — `flywheel` tier added, `flywheel_complete()` method for A/B testing
- `~/ai-army-os/config.yaml` — flywheel model slot defined (commented, activates after first fine-tune)

**To run first fine-tune cycle:**
```bash
# On Spark-1
cd ~/data-flywheel
source .venv/bin/activate

# Step 1: Export dataset
python3 army_os_wiring.py --export
# → writes flywheel_data/flywheel_export_YYYYMMDD.jsonl (2,894 records)

# Step 2: NeMo Curator clean + dedup
python3 nemo_curator_pipeline.py --input flywheel_data/flywheel_export_*.jsonl
# → writes clean_data/curator_cleaned.jsonl

# Step 3: Fine-tune (requires Unsloth: pip install unsloth)
python3 fine_tune_trigger.py --input clean_data/curator_cleaned.jsonl --base-model qwen2.5-coder:32b
# → runs LoRA on Spark-1 (or Spark-2 for 32B+ models)

# Step 4: Import to Ollama + activate flywheel slot in config.yaml
bash ~/data-flywheel/fine_tune_runs/qwen2.5-coder_32b/import_to_ollama.sh
```

**Unsloth install (if needed):**
```bash
pip install unsloth  # CUDA 13.0 compatible
```

---

### 3. Video Search — Schema Live, Services Ready to Start
**Status: SCHEMA DEPLOYED — services need to start**

**pgvector schema** created on Spark-1 (memoryweb PostgreSQL):
- `video_library` — video metadata
- `video_frames` — per-frame CLIP embeddings (768-dim, HNSW index)

**Services to start:**

**Windows PC (RTX 5090) — CLIP embedding service:**
```bash
pip install transformers torch Pillow fastapi uvicorn
python3 "C:\Users\techai\PKA testing\clip_service.py"
# Starts on :8320, uses ~3GB VRAM (leaves 29GB for other work)
```

**Spark-1 — Video Search API:**
```bash
ssh rblake2320@192.168.12.132
pip install asyncpg fastapi uvicorn httpx opencv-python-headless
python3 /home/rblake2320/video-search/video_api.py
# Starts on :8310
```

**Add to Cloudflare tunnel:**
```bash
ssh rblake2320@192.168.12.132 "sudo nano /etc/cloudflared/config.yml"
# Add: - hostname: video.ultrarag.app
#        service: http://localhost:8310
sudo systemctl restart cloudflared
```

**Usage after start:**
```bash
# Ingest a video
curl -X POST http://192.168.12.132:8310/api/video/ingest \
  -d '{"video_path": "/path/to/meeting.mp4", "title": "City Council 2026-03"}'

# Search
curl "http://192.168.12.132:8310/api/video/search?q=budget+vote&top_k=5"
```

---

## Files in `C:\Users\techai\PKA testing\`

| File | Purpose |
|------|---------|
| `agent_guardrails.py` | Guardrail engine (deployed to Spark-1) |
| `patch_coder.py` | Script that patched coder.py (for reference) |
| `army_os_wiring.py` | Data Flywheel source connector |
| `nemo_curator_pipeline.py` | NeMo Curator data cleaning pass |
| `fine_tune_trigger.py` | LoRA fine-tune launcher with NIM teacher |
| `clip_service.py` | CLIP embedding service for RTX 5090 |
| `video_search_setup.py` | Full Video Search setup orchestrator |

---

## Cross-Domain Flags for VENTURE + LEGAL

**VENTURE — flag immediately:**
1. **CivicMind + Video Search** — cities record hundreds of hours of council meetings.
   No competitor offers searchable video. Once video_api.py is running, you can demo
   "search 200 hours of council meetings in 2 seconds" to any municipality.
   Cost: $0 marginal (runs on existing Spark-1 infrastructure).

2. **Data Flywheel + HASP Standard** — the wiring pattern (production queries →
   curator → fine-tune → deploy → loop) is the "how agents improve" spec that HASP
   needs. Document this as the HASP Continuous Learning Annex.

**LEGAL — patent candidates:**
1. **Distributed Data Flywheel architecture** — multi-source (RAG + autonomous task
   execution) prompt→response extraction → heterogeneous GPU cluster fine-tuning →
   Ollama deployment with A/B routing. No prior art that crosses all four boundaries.

2. **Agent Safety Guardrails for Autonomous Code Commit** — pattern-based + AI-powered
   output validation before git operations. Specific to agentic code-writing, not just
   content moderation.

3. **Municipal Video Intelligence** — sovereign (on-prem) natural language search over
   municipal meeting recordings with CLIP + pgvector + jurisdictional isolation.

---

## Week 1 Remaining Actions

| Day | Task | Owner | Status |
|-----|------|-------|--------|
| Mon ✅ | Guardrails + wiring deployed | FORGE | **DONE** |
| Tue | Run first flywheel export cycle | Ron/FORGE | Ready to run |
| Wed | NeMo Curator clean + fine-tune launch | FORGE | Awaiting Unsloth install |
| Thu | Start CLIP service + Video Search API | Ron | Ready to start |
| Fri | A/B test flywheel model + video search POC | FORGE + SENTINEL | Pending |

---

## Verification Commands

```bash
# 1. Guardrails working
ssh rblake2320@192.168.12.132 "python3 /home/rblake2320/ai-army-os/agent_guardrails.py"
# Expected: 7/7 passed

# 2. Flywheel data count
ssh rblake2320@192.168.12.132 "cd ~/data-flywheel && source .venv/bin/activate && python3 army_os_wiring.py --dry-run"
# Expected: 2,894 records

# 3. Video schema
ssh rblake2320@192.168.12.132 "source ~/data-flywheel/.venv/bin/activate && python3 -c \"import psycopg2; conn=psycopg2.connect('postgresql://memoryweb:memoryweb@localhost:5432/memoryweb'); cur=conn.cursor(); cur.execute(\\\"SELECT COUNT(*) FROM video_library\\\"); print('video_library ready:', cur.fetchone()[0], 'videos')\""

# 4. LLM router has flywheel
ssh rblake2320@192.168.12.132 "grep -c flywheel ~/ai-army-os/llm_router.py"
# Expected: 8
```
