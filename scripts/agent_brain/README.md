# Agent Brain

Autonomous LLM runtime for the PKA workspace. Powered by local SLMs, Spark Ollama models, tunnel Ollama models, or cloud OpenAI-compatible LLMs.

## What It Does

- **ReAct loop**: think → tool call → observe → repeat (max 25 iterations)
- **Internet access**: DuckDuckGo search + web fetch
- **8 built-in tools**: web_search, web_fetch, file_read, file_write, memory_read, memory_write, shell_exec, ssh_exec
- **Provider routing**: local Ollama, Spark Ollama, tunnel Ollama, and cloud OpenAI-compatible APIs
- **Model routing**: qwen3 8B (fast) → qwen3-fast-hermes (tool-calling) → llama3.1:70b/cloud (deep reasoning)
- **Persistent memory**: MEMORY.md survives across sessions
- **Context compression**: Hermes-pattern summarizer kicks in at 85% context window
- **PKA integration**: consumes job queue via `pka_runtime.py`

## Quick Start

```bash
# One-shot task
python -m scripts.agent_brain run "Search for the latest RTX 5090 benchmarks"

# Force a local SLM on localhost Ollama
python -m scripts.agent_brain run "Summarize VERSION" --model local

# Force a cloud OpenAI-compatible LLM
python -m scripts.agent_brain run "Plan the next validation pass" --model cloud

# Interactive chat
python -m scripts.agent_brain chat

# Job queue consumer (picks up queued PKA jobs)
python -m scripts.agent_brain worker

# Status check
python -m scripts.agent_brain status
python -m scripts.agent_brain status --model cloud
```

## Models

| Key | Model | Latency | Use |
|-----|-------|---------|-----|
| Key | Provider | Model | Use |
|-----|----------|-------|-----|
| local | local Ollama | `AGENT_BRAIN_LOCAL_MODEL` or `imds-v2:latest` | Local SLM on `127.0.0.1:11434` |
| local-imds | local Ollama | `imds-v2:latest` | Installed local SLM on this workstation |
| gemma3 | Spark Ollama | `qwen3:latest` | Fast summarization/classification alias |
| qwen3-8b | Spark Ollama | `qwen3:latest` | Fast tool-calling |
| qwen3 | Spark Ollama | `qwen3-fast-hermes:latest` | Tool-calling default |
| llama70b | Spark Ollama | `llama3.1:70b` | Deep reasoning/analysis |
| deepseek | Spark Ollama | `deepseek-r1:32b` | Step-by-step reasoning |
| cloud | OpenAI-compatible | `AGENT_BRAIN_OPENAI_COMPAT_MODEL` or `gpt-4o-mini` | Cloud fallback/large model |

Override: `--model local`, `--model cloud`, any configured key, or a raw model tag on the default provider.

## Tools

| Tool | Description |
|------|-------------|
| `web_search` | DuckDuckGo search (no API key) |
| `web_fetch` | Fetch and strip a web page |
| `file_read` | Read any file inside PKA workspace |
| `file_write` | Write files (scope-enforced, secret-scanned) |
| `memory_read` | Read persistent memory sections |
| `memory_write` | Update persistent memory |
| `shell_exec` | Run shell commands (sandboxed, blocklisted) |
| `ssh_exec` | SSH to Spark-1 or Spark-2 |

## Safety

- Writes blocked outside `C:\Users\techai\PKA testing\`
- CLAUDE.md, owner.md, root MEMORY.md → read-only
- Owner's Inbox remains writable for deliverables, with secret scanning before writes
- Shell blocklist: rm -rf, format, shutdown, etc.
- Secret detection via pka_guardrails.py before every write
- 25 iteration cap per task
- All tool calls logged to `data/logs/agent_YYYYMMDD.jsonl`

## Endpoints

Spark primary: `http://192.168.12.132:11434`
Spark fallback: `http://ollama.ultrarag.app`
Local Ollama: `http://127.0.0.1:11434`
Cloud OpenAI-compatible: `https://api.openai.com`

Overrides:

```powershell
$env:AGENT_BRAIN_LOCAL_OLLAMA="http://127.0.0.1:11434"
$env:AGENT_BRAIN_LOCAL_MODEL="imds-v2:latest"
$env:AGENT_BRAIN_LOCAL_TOOLS="0"

$env:AGENT_BRAIN_OPENAI_COMPAT_BASE_URL="https://api.openai.com"
$env:AGENT_BRAIN_OPENAI_COMPAT_MODEL="gpt-4o-mini"
$env:AGENT_BRAIN_OPENAI_COMPAT_API_KEY_ENV="OPENAI_API_KEY"
$env:OPENAI_API_KEY="..."
```

Data isolation rule: cloud models are available only when explicitly selected or configured. Do not send `CLAUDE.md`, root `MEMORY.md`, `owner.md`, or Owner's Inbox contents to public/cloud models. Agent Brain withholds its local memory block from cloud providers by default; set `AGENT_BRAIN_ALLOW_CLOUD_MEMORY=1` only when that is intentional.

Tool use is model-dependent. Local SLMs that reject tool schemas still run inside the brain for direct reasoning/chat. Set `AGENT_BRAIN_LOCAL_TOOLS=1` only for local models confirmed to support OpenAI/Ollama tool calling.

## Structure

```
scripts/agent_brain/
├── __main__.py   CLI
├── agent.py      ReAct loop
├── llm.py        Ollama client + model router
├── context.py    Context compression
├── memory.py     Persistent memory engine
├── worker.py     PKA job queue consumer
├── config.py     All configuration
└── tools/        8 tool implementations
    └── data/     Runtime state (gitignored)
```
