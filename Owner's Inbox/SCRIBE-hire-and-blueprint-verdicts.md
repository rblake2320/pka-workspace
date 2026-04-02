# SCRIBE Hired + Blueprint Verdicts Implemented
**Date:** 2026-03-23
**Routing:** HELM → FORGE (local) + FORGE (Spark-1 runbook) → SCRIBE (hired)

---

## What Was Done (Local — Complete)

### 1. SCRIBE Agent Hired ✅
**File:** `PKA testing/.claude/agents/SCRIBE.md`

SCRIBE is live. It activates on three triggers:
- Self-learning confidence < 50% after research
- Task failure due to missing skill coverage
- 5+ KB entries in one domain without a matching skill

SCRIBE's four-step loop: **SCAN → DECIDE → BUILD → VALIDATE**. New skills start
as `PENDING`. Promoted to `ACTIVE` after 3+ confirmed successful uses.

### 2. Coverage Scanner Created ✅
**File:** `~/.claude/skills/self-learning/scripts/coverage_scan.py`

SCRIBE's primary tool. Scans:
- All `~/.claude/skills/*/SKILL.md` by keyword relevance
- `docker mcp catalog show` (312 servers)
- Installed CLIs via version probes
- `pip list` + `npm list -g` for domain-relevant packages
- Self-learning SQLite KB for accumulated entries

Returns structured JSON + human-readable summary. Decision logic built in:
UPDATE if 80%+ existing match, BRIDGE if tool exists, CREATE if nothing covers it.

**Usage:**
```bash
python ~/.claude/skills/self-learning/scripts/coverage_scan.py --domain "voice streaming"
python ~/.claude/skills/self-learning/scripts/coverage_scan.py --domain "NL-to-SQL" --json
```

### 3. CLAUDE.md Roster Updated ✅
SCRIBE added to Active Agent Roster with hire date 2026-03-23.

---

## What Needs to Happen on Spark-1 (FORGE Runbook)

These require SSH access to `rblake2320@192.168.12.132`. Run in order.

### Step A — LLM Router: ML-Based Classifier (Cherry-pick from NVIDIA LLM Router)

```bash
ssh rblake2320@192.168.12.132
cd ~/ai-army-os
pip install transformers torch --quiet
```

Add to `~/ai-army-os/llm_router.py` — new method `_classify_prompt()`:

```python
def _classify_prompt(self, prompt: str) -> tuple[str, str]:
    """
    Returns (task_category, complexity) using NVIDIA's classifier.
    Falls back to ('general', 'medium') if model not available.
    """
    try:
        from transformers import pipeline
        if not hasattr(self, '_classifier'):
            self._classifier = pipeline(
                "text-classification",
                model="nvidia/prompt-task-and-complexity-classifier",
                device=-1,  # CPU — classifier is lightweight
            )
        result = self._classifier(prompt[:512], truncation=True)[0]
        label = result['label']  # e.g. "CODE_GENERATION-COMPLEX"
        parts = label.split('-')
        task = parts[0].lower() if parts else 'general'
        complexity = parts[1].lower() if len(parts) > 1 else 'medium'
        return task, complexity
    except Exception:
        return 'general', 'medium'
```

Replace `_auto_select` simple tier lookup — prepend classifier call and map:

```python
TASK_MODEL_MAP = {
    'code_generation':   'qwen2.5-coder:32b',
    'code_review':       'qwen2.5-coder:32b',
    'reasoning':         'nemotron-3-nano',
    'math':              'nemotron-3-nano',
    'summarization':     'llama3.1:70b',
    'question_answering':'llama3.1:70b',
    'creative_writing':  'llama3.1:70b',
    'general':           'llama3.1:70b',
}
```

Add to `~/ai-army-os/config.yaml`:
```yaml
task_model_map:
  code_generation: "qwen2.5-coder:32b"
  code_review: "qwen2.5-coder:32b"
  reasoning: "nemotron-3-nano"
  math: "nemotron-3-nano"
  summarization: "llama3.1:70b"
  question_answering: "llama3.1:70b"
  creative_writing: "llama3.1:70b"
  general: "llama3.1:70b"
```

### Step B — Vanna.AI NL-to-SQL (Cherry-pick from AI Virtual Assistant)

```bash
pip install 'vanna[postgres]' --quiet
```

Create `~/ai-army-os/tools/sql_tool.py`:

```python
"""
sql_tool.py — Natural Language to SQL via Vanna.AI
Connects to existing PostgreSQL databases. Adds structured data retrieval
as a new tool in AI Army OS alongside unstructured RAG.
"""
import vanna
from vanna.remote import VannaDefault


class NLSQLTool:
    def __init__(self, pg_url: str, model: str = "vanna"):
        self.vn = VannaDefault(model=model, api_key=None)  # local mode
        self.vn.connect_to_postgres(url=pg_url)

    def train_on_schema(self):
        """One-time training: ingest table schemas + sample queries."""
        df_info = self.vn.run_sql("SELECT table_name, column_name, data_type "
                                  "FROM information_schema.columns "
                                  "WHERE table_schema NOT IN ('pg_catalog','information_schema')")
        self.vn.train(documentation=df_info.to_string())

    def ask(self, question: str) -> dict:
        """Translate natural language question to SQL and execute it."""
        sql = self.vn.generate_sql(question)
        try:
            result = self.vn.run_sql(sql)
            return {"sql": sql, "rows": result.to_dict(orient="records"), "error": None}
        except Exception as e:
            return {"sql": sql, "rows": [], "error": str(e)}


# Tool registration for AI Army OS
PG_URL = "postgresql://postgres:%3FBooker78%21@localhost:5432/postgres"

_tool = None

def get_tool():
    global _tool
    if _tool is None:
        _tool = NLSQLTool(pg_url=PG_URL)
    return _tool

def nl_to_sql(question: str) -> dict:
    """AI Army OS tool entry point. Call with natural language question."""
    return get_tool().ask(question)
```

Create `~/ultra-rag/src/sentiment.py`:

```python
"""
sentiment.py — Lightweight sentiment classifier via LLM prompt.
No new dependencies. Uses existing Ollama/LLM infrastructure.
"""
import requests

SYSTEM_PROMPT = (
    "You are a sentiment classifier. Respond with exactly one word: "
    "POSITIVE, NEGATIVE, or NEUTRAL. No explanation."
)

OLLAMA_URL = "http://localhost:11434/api/generate"


def classify_sentiment(text: str, model: str = "gemma3:latest") -> str:
    """Returns POSITIVE, NEGATIVE, or NEUTRAL."""
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": text,
            "system": SYSTEM_PROMPT,
            "stream": False,
        }, timeout=15)
        return resp.json().get("response", "NEUTRAL").strip().upper()
    except Exception:
        return "NEUTRAL"
```

### Step C — Nemotron Voice Agent (Cloud-Hybrid Mode)

```bash
cd ~
git clone https://github.com/NVIDIA-Blueprints/nemotron-voice-agent.git
cd nemotron-voice-agent
cp config/env.example .env
```

Edit `.env`:
```
# LLM: point at local Ollama on Spark-1
NVIDIA_LLM_URL=http://localhost:11434/v1
NVIDIA_LLM_MODEL=llama3.1:70b

# ASR/TTS: NIM cloud (free tier)
NVIDIA_ASR_URL=https://grpc.nvcf.nvidia.com:443
NVIDIA_TTS_URL=https://grpc.nvcf.nvidia.com:443
NVIDIA_API_KEY=<your NIM key from build.nvidia.com>

# Pipecat orchestrator
PIPECAT_PORT=9000
```

Start (no GPU needed for orchestrator):
```bash
docker-compose up -d pipecat-orchestrator pipecat-ui
# Skip any container that requires local NIM GPU allocation
```

Add to Cloudflare tunnel config on Spark-1
(`/etc/cloudflared/config.yml` — append):
```yaml
  - hostname: voice.ultrarag.app
    service: http://localhost:9000
```

Restart tunnel: `sudo systemctl restart cloudflared`

---

## Blueprint Verdict Summary (for reference)

| Blueprint | Decision | What Gets Built |
|-----------|----------|-----------------|
| Nemotron Voice Agent | CONDITIONAL DEPLOY | Cloud-hybrid (NIM ASR/TTS + local LLM) on Spark-1 |
| AIQ Research Agent | SKIP | Concept only: use FreshQA eval methodology for Data Flywheel benchmarks |
| NVIDIA LLM Router | CHERRY-PICK | `_classify_prompt()` in existing `llm_router.py` |
| AI Virtual Assistant | CHERRY-PICK | Vanna.AI NL-to-SQL tool + sentiment classifier prompt |

---

## Verification Checklist

- [ ] `python ~/.claude/skills/self-learning/scripts/coverage_scan.py --domain "voice streaming"` — runs and returns JSON
- [ ] Voice agent: `voice.ultrarag.app` → speak → hear response
- [ ] LLM Router: 10 diverse prompts → task category logged in routing decisions
- [ ] NL-to-SQL: "how many tasks completed this week?" → SQL + result returned
- [ ] SCRIBE: trigger self-learning on unknown domain → coverage scan runs → skill in `PENDING`

---

*Delivered by FORGE (local). Spark-1 steps require SSH and are documented as a runbook.*
