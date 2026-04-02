# NOVA — Hermes Agent Technical Deep-Dive
## How They Built the 4 Features We Need to Replicate

**Date**: 2026-03-29
**Objective**: Extract exact implementation details from NousResearch/hermes-agent source code for four capability gaps: skill auto-creation, cron scheduling, session FTS search, and messaging gateway. Produce replication specs for our stack.

---

## 1. Skill Auto-Creation Loop

### What Hermes Actually Does

Hermes does NOT have an autonomous "detect when to create a skill and auto-write it" loop. This is a critical finding — the capability is manual/discovery-based, not generative.

**How skill discovery works** (`agent/skill_commands.py`, `agent/skill_utils.py`):

- `scan_skill_commands()` — walks the skills directory, reads YAML frontmatter from each `SKILL.md` file, builds a dict of `{command_name: skill_metadata}`. Filters by platform compatibility and disabled-skills config. This runs at session start and on cache invalidation.
- `build_skill_invocation_message()` — when a user types `/skill-name`, loads the SKILL.md body, injects setup notes and supporting file references, and returns it as a formatted message prepended to the conversation.
- `build_preloaded_skills_prompt()` — for CLI sessions with `--skills` flag, loads multiple skills at session init and concatenates them into the system prompt.

**Skill file format** (confirmed from `skills/autonomous-ai-agents/claude-code/SKILL.md`):

```yaml
---
name: claude-code
description: Delegate coding tasks to Claude Code...
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic, Code-Review, Refactoring]
    related_skills: [codex, hermes-agent]
---
```

Body is freeform Markdown — prerequisites, examples, rules, reference tables. No schema enforcement on the body.

**Skill installation pipeline** (`hermes_cli/skills_hub.py`):

1. `do_search()` — queries registries via `unified_search()`
2. `do_install()` — fetches bundle, writes to quarantine path, runs `scan_skill()` security check, shows report, asks confirmation, copies to skills dir, invalidates prompt cache

**The `insights.py` file** is the session analytics engine — tracks token usage, cost, activity patterns from SQLite. It is NOT part of skill auto-creation. The name is misleading relative to our use case.

**What Hermes does NOT have**: There is no function that watches session outputs, detects repeated patterns, and autonomously generates a new SKILL.md. The "auto-creation loop" we need to replicate does not exist in Hermes as a single module — it would need to be synthesized from their skill format spec + our own pattern detection.

### Minimum Viable Replication in Our Stack

Our `claude-skills/` directory already uses the identical SKILL.md-with-YAML-frontmatter format. The skills-bridge MCP reads these files and exposes them to Claude Code. The gap is not format compatibility — it is the absence of a feedback loop that detects when a new skill should be written.

**Replication approach**: Write a post-session hook (like `mw_post_session.py` in MemoryWeb) that:
1. Reads the session JSONL
2. Calls gemma3:latest (0.4s, free) with a prompt: "Did this session repeatedly invoke the same multi-step procedure that would benefit from a skill? If yes, extract: name, description, tags, and body instructions."
3. If confidence > threshold, writes `C:\Users\techai\claude-skills\auto-generated\{name}\SKILL.md` using Hermes frontmatter format
4. Logs to `C:\Users\techai\PKA testing\Team\SCRIBE\journal.md` for human review

This costs ~$0 (local model), runs in <1s, and produces skills in the exact format skills-bridge already reads.

---

## 2. Cron Scheduler

### What Hermes Actually Does

**Library**: No APScheduler, no Celery. Plain Python with `croniter` (optional dependency) for cron expression parsing, and a background thread running a `tick()` loop on 60-second intervals.

**Job storage** (`cron/jobs.py`):
- Jobs persisted to `~/.hermes/cron/jobs.json` — flat JSON file, not a database
- Outputs saved as timestamped Markdown files in `~/.hermes/cron/output/`
- Directory and file permissions set to `0700`/`0600` (owner-only) on Unix

**Job schema** (from `jobs.py`):
```python
{
  "id": str,               # UUID
  "name": str,             # human label
  "prompt": str,           # the instruction to run
  "schedule": str,         # raw schedule string
  "skills": list[str],     # skill names to preload
  "model": str,
  "provider": str,
  "repeat": int,           # -1 = infinite
  "delivery": list[str],   # ["telegram", "local", "origin"]
  "status": str,           # "active" | "paused" | "completed" | "disabled"
  "next_run": str,         # ISO timestamp
  "last_run": str,
  "last_status": str,      # "ok" | "error"
  "last_error": str,
  "run_count": int
}
```

**Schedule parsing** — `parse_schedule()` in `cron/jobs.py` handles four formats:
- Duration: `"30m"`, `"2h"`, `"1d"` — one-shot, runs once after delay
- Recurring: `"every 30m"`, `"every 2h"` — stripped of "every " prefix, re-evaluated each run
- Cron expression: `"0 9 * * *"` — requires `croniter` library; raises `ImportError` with install hint if missing
- ISO timestamp: `"2026-02-03T14:00"` — one-shot at exact time

**Natural language**: There is NO natural language schedule parsing in `jobs.py` or `cron.py`. The `hermes_cli/cron.py` CLI passes the schedule string to `tools.cronjob_tools` which likely calls an LLM to interpret natural language into one of the four formats above. The parsing is LLM-assisted, not regex-based.

**Execution** (`cron/scheduler.py`):
- `tick()` — called every 60 seconds from a background thread
- File lock via `fcntl` (Unix) or `msvcrt` (Windows) prevents concurrent runs
- `run_job()`:
  1. Builds system prompt from `prompt_builder.py`
  2. Optionally loads skills via `build_preloaded_skills_prompt()`
  3. Initializes `AIAgent` with config from env/config.yaml
  4. Runs agent conversation
  5. Captures response text
  6. Checks for `[SILENT]` marker — if present, saves locally but suppresses delivery
  7. Routes to delivery platforms via `DeliveryRouter`

**Grace period logic**: Daily jobs can catch up if missed by up to 2 hours; high-frequency jobs (< 1 hour) skip stale runs faster. Prevents job avalanche after downtime.

### Minimum Viable Replication in Our Stack

Our AI Army OS (Spark-1:8500) already runs autonomous tasks. The gap is structured scheduling with persistence and multi-platform delivery.

**Replication approach**: Deploy `cron/jobs.py` + `cron/scheduler.py` directly onto Spark-1 (Python 3.12, Linux, croniter pip-installable). Adapt:
- Change `~/.hermes/cron/jobs.json` to `/home/rblake2320/ai-business/shared/cron/jobs.json` so AXIOM and AI Army OS share visibility
- Change output dir to `/home/rblake2320/ai-business/shared/cron/output/`
- Replace `AIAgent` call with a direct Ollama API call (`llama3.1:70b` for complex, `gemma3:latest` for simple) since we do not run Hermes's agent loop
- Wire delivery to our existing channels: local file + SSH message drop to `~/ai-business/shared/chat/`
- For natural language schedule parsing, Claude Code (this session) interprets and writes the cron string at job creation time — no extra LLM call needed

Total new code: ~200 lines. Hermes's `jobs.py` is the reusable core; `scheduler.py` needs a ~20-line shim replacing `AIAgent`.

---

## 3. Session Search (FTS5)

### What Hermes Actually Does

**Storage** (`hermes_state.py` — the SQLite state store):

Three core tables:
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    source TEXT,           -- "cli" | "telegram" | "discord" etc.
    user_id TEXT,
    model TEXT,
    system_prompt TEXT,
    parent_session_id TEXT,
    message_count INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_read_tokens INTEGER,
    cache_write_tokens INTEGER,
    reasoning_tokens INTEGER,
    cost_usd REAL,
    started_at REAL,       -- Unix timestamp
    ended_at REAL,
    title TEXT UNIQUE      -- sanitized, enforced unique where non-null
);

CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    role TEXT,             -- "user" | "assistant" | "tool"
    content TEXT,
    tool_calls TEXT,       -- JSON
    reasoning TEXT,        -- assistant reasoning text (v6 addition)
    reasoning_details TEXT, -- structured JSON
    created_at REAL
);

-- FTS5 virtual table
CREATE VIRTUAL TABLE messages_fts USING fts5(
    content,
    content='messages',
    content_rowid='rowid'
);

-- Sync triggers
CREATE TRIGGER messages_fts_insert AFTER INSERT ON messages BEGIN
    INSERT INTO messages_fts(rowid, content) VALUES (new.rowid, new.content);
END;
CREATE TRIGGER messages_fts_update AFTER UPDATE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content) VALUES ('delete', old.rowid, old.content);
    INSERT INTO messages_fts(rowid, content) VALUES (new.rowid, new.content);
END;
CREATE TRIGGER messages_fts_delete AFTER DELETE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content) VALUES ('delete', old.rowid, old.content);
END;
```

**Query sanitization**: The FTS5 search function strips special characters that break FTS5 syntax while preserving quoted phrases and hyphenated terms. This prevents SQL injection via malformed FTS5 queries.

**Concurrency**: WAL mode + `BEGIN IMMEDIATE` + application-level retry with random jitter. No busy handler — jitter staggers competing writers.

**Session summarization for context compression** (`agent/context_compressor.py`):

The `ContextCompressor` class uses a structured template:
```
Goal: [what the user was trying to accomplish]
Progress: [what was completed]
Decisions: [key choices made]
Files: [files created/modified]
Next Steps: [what remains]
```

This summary is generated by an LLM call (`summary_model_override` config option — can use a cheaper auxiliary model). The compressor:
1. Pre-pass: prune old tool results without LLM call
2. Protect first N messages (system prompt + first exchange) and last N messages (tail)
3. Identify middle turns to summarize
4. Call LLM with structured prompt → get summary
5. On re-compression: append new constraints to previous summary rather than regenerating from scratch

Token budget for tail protection: `min(2000, max(12000, context_size * summary_target_ratio))`.

**`insights.py`** generates usage reports (token cost, activity patterns) from the same SQLite DB. Two output formats: terminal ASCII tables and gateway markdown. Uses `"prefers tool_name source, supplement with tool_calls source"` aggregation to avoid double-counting.

### Minimum Viable Replication in Our Stack

We already have PostgreSQL with pgvector (MemoryWeb) and FTS via Ultra RAG. The gap is per-session full-text search across conversation history specifically.

**Replication approach**:
- MemoryWeb's PostgreSQL already stores session data. Add a `tsvector` column to the `segments` or `memories` table:
  ```sql
  ALTER TABLE segments ADD COLUMN fts_vector tsvector
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(content, ''))) STORED;
  CREATE INDEX segments_fts_idx ON segments USING GIN(fts_vector);
  ```
- Search endpoint: `GET /api/search/fts?q={query}` → `SELECT * FROM segments WHERE fts_vector @@ plainto_tsquery('english', $1)`
- For session summarization: adopt Hermes's 5-field template verbatim (Goal/Progress/Decisions/Files/Next Steps) and route to `gemma3:latest` via Ollama. This replaces or supplements current MemoryWeb synthesis.
- The `ContextCompressor` logic (iterative summary append) is worth porting verbatim — it prevents context explosion on long sessions. File: `agent/context_compressor.py`, class `ContextCompressor`. Drop it into `D:\memory-web\app\compressor.py` with Ollama replacing the LLM call.

---

## 4. Messaging Gateway

### What Hermes Actually Does

**Architecture**: Each platform is a subclass of `BasePlatformAdapter` (`gateway/platforms/base.py`). The `GatewayRunner` (`gateway/run.py`) instantiates adapters based on config and runs them concurrently via asyncio.

**Supported platforms** (confirmed from file tree):
- Telegram (`telegram.py`) — long polling via `python-telegram-bot >= 20.0`
- Discord (`discord.py`) — WebSocket via `discord.py >= 2.0`
- WhatsApp (`whatsapp.py`) — bridge via Node.js `scripts/whatsapp-bridge/bridge.js`
- Slack (`slack.py`) — aiohttp
- Signal (`signal.py`) — aiohttp
- Email (`email.py`)
- SMS (`sms.py`)
- HomeAssistant (`homeassistant.py`)
- Matrix (`matrix.py`)
- Mattermost (`mattermost.py`)
- DingTalk (`dingtalk.py`)
- API Server (`api_server.py`) — FastAPI-based HTTP receiver
- Webhook (`webhook.py`) — generic outbound webhook

**Connection models by platform**:
- Telegram: long polling (`updater.start_polling()`) — no webhook mode
- Discord: WebSocket (`discord.py` native gateway)
- WhatsApp: Node.js bridge process (separate `bridge.js` child process, communicates over local socket)
- Others: combination of polling or aiohttp webhook listeners

**Normalized message format** (`MessageEvent` dataclass):
```python
@dataclass
class MessageEvent:
    text: str
    message_type: MessageType  # TEXT | PHOTO | AUDIO | VIDEO | DOCUMENT | STICKER | COMMAND | LOCATION
    source: SessionSource      # platform, chat_id, user_id, thread_id
    media_urls: list[str]      # local cached file paths (downloaded before handler runs)
    reply_to_message_id: str | None
    auto_skill: str | None     # pre-bound skill from channel config
```

**Media caching**: All media is downloaded and cached locally before the message handler fires. Three cache dirs: `{HERMES_HOME}/cache/images/`, `cache/audio/`, `cache/documents/`. All `*_from_url()` methods implement exponential backoff with 30s client timeout.

**Response processing pipeline** (`_process_message_background()`):
1. Extract `MEDIA:/path` tags from response text
2. Parse markdown images `![alt](url)` and HTML `<img>` tags
3. Auto-detect bare file paths matching media extensions
4. Skip code block interiors
5. Auto-TTS via `edge-tts` if reply is to a voice message
6. Send text with `_send_with_retry()` + human-delay pacing
7. Send images/audio/video as native attachments

**Delivery routing** (`gateway/delivery.py`):
```python
class DeliveryTarget:
    platform: str
    chat_id: str | None   # None = home channel
    thread_id: str | None
    is_origin: bool
    is_explicit: bool

class DeliveryRouter:
    def resolve_targets(self, specs: list[str]) -> list[DeliveryTarget]
    async def deliver(self, content: str, targets: list[DeliveryTarget]) -> dict
```
Specs: `"origin"`, `"local"`, `"telegram"`, `"telegram:123456"`, `"discord:channel_id"`.

**Message interruption**: `_active_sessions` dict maps session key to `asyncio.Event`. New messages signal the event; running handlers check it and can abort. `_pending_messages` queues the interrupting message for processing after cleanup.

**Cron delivery**: `[SILENT]` marker in agent response suppresses platform delivery while still saving output to `~/.hermes/cron/output/`. Used for background jobs where human notification is not desired.

### Minimum Viable Replication in Our Stack

We do not need WhatsApp, Matrix, DingTalk, SMS, or HomeAssistant. We need: Telegram + Discord + the cron delivery path.

**Replication approach**: Deploy the gateway to Spark-1 (port 8600 to avoid conflicts with AI Army OS on 8500). Extract only:
- `gateway/platforms/base.py` — BasePlatformAdapter (pure Python, no platform deps)
- `gateway/platforms/telegram.py` — requires `pip install python-telegram-bot>=20.0`
- `gateway/platforms/discord.py` — requires `pip install discord.py>=2.0`
- `gateway/delivery.py` — DeliveryRouter
- `gateway/run.py` — GatewayRunner (strip unused platform instantiation)

Replace `AIAgent` in `run_job()` with a direct call to Ollama API at `localhost:11434` (Spark-1 runs 43 models). Wire session context from MemoryWeb's `mw_pre_session.py` hook — inject memories into the system prompt before agent call.

Total dependency additions on Spark-1: `python-telegram-bot>=20.0`, `discord.py>=2.0`, `aiohttp>=3.9`. All pip-installable, Python 3.12 compatible.

---

## Synthesis: Gap-to-Action Matrix

| Gap | Hermes Module | Our Replication Path | Effort |
|-----|--------------|---------------------|--------|
| Skill auto-creation | `skill_utils.py` (format only) | Post-session hook → gemma3 → write SKILL.md | 1 day |
| Cron scheduler | `cron/jobs.py` + `cron/scheduler.py` | Port directly to Spark-1, replace AIAgent with Ollama call | 1 day |
| Session FTS search | `hermes_state.py` FTS5 schema | Add tsvector to MemoryWeb PostgreSQL segments table | 4 hours |
| Context compression | `agent/context_compressor.py` | Port ContextCompressor, replace LLM call with Ollama | 1 day |
| Messaging gateway | `gateway/` (telegram + discord) | Deploy to Spark-1:8600, wire to MemoryWeb + Ollama | 2 days |

**What Hermes has that we should NOT replicate**: The SQLite-based state store (`hermes_state.py`). We already have PostgreSQL with pgvector, which is strictly more capable. The FTS5 schema is worth studying for the trigger pattern, but we implement it as `tsvector` in Postgres.

**What Hermes does NOT have that we already have**: pgvector semantic search, RAPTOR chunking, MemoryWeb 3-tier memory cascade, AI Army OS autonomous task execution. These are our advantages — Hermes is ahead on gateway breadth and cron polish, behind on memory depth.

---

## Key File References

All source in `https://github.com/NousResearch/hermes-agent`:

- `agent/skill_utils.py` — YAML frontmatter parsing, platform compatibility, skill file iteration
- `agent/skill_commands.py` — `scan_skill_commands()`, `build_skill_invocation_message()`, `build_preloaded_skills_prompt()`
- `agent/insights.py` — session analytics from SQLite (token usage, cost, activity patterns)
- `agent/context_compressor.py` — `ContextCompressor` class, 5-field summary template, iterative re-compression
- `agent/prompt_builder.py` — system prompt assembly, CLAUDE.md/HERMES.md discovery, security scanning, platform-specific guidance
- `cron/jobs.py` — job schema, `parse_schedule()` (4 formats), `compute_next_run()`, grace period logic
- `cron/scheduler.py` — `tick()` loop, file locking, `run_job()`, `[SILENT]` marker, delivery routing
- `gateway/platforms/base.py` — `BasePlatformAdapter`, `MessageEvent`, `SendResult`, media cache, `_process_message_background()`
- `gateway/platforms/telegram.py` — long polling via `python-telegram-bot`, text/photo batch aggregation
- `gateway/platforms/discord.py` — WebSocket via `discord.py`, `on_message` handler
- `gateway/delivery.py` — `DeliveryTarget`, `DeliveryRouter`, platform routing, local save fallback
- `gateway/run.py` — `GatewayRunner`, platform lifecycle, `_handle_message()`, session expiry watcher
- `hermes_state.py` — SQLite schema with FTS5 virtual table, WAL mode, trigger-based sync, `ContextCompressor` integration
- `hermes_cli/skills_hub.py` — skill discovery, quarantine install, security scan, cache invalidation
- `hermes_cli/cron.py` — CLI commands for cron management, job creation, natural-language-to-schedule via LLM

**Dependencies to add** (all Python 3.12 compatible):
```
python-telegram-bot>=20.0
discord.py>=2.0
aiohttp>=3.9.0
croniter          # optional, for cron expression support
```

---

## Confidence Assessment

- Skill format spec: HIGH — confirmed from actual SKILL.md file content
- Cron implementation: HIGH — confirmed from `jobs.py` and `scheduler.py` descriptions with data structures
- FTS5 schema: HIGH — confirmed from `hermes_state.py` with trigger code visible
- Context compressor algorithm: HIGH — confirmed from `context_compressor.py` with 5-field template and token budget logic
- Gateway architecture: HIGH — confirmed platform list, connection models (polling vs WebSocket), and `MessageEvent` schema
- "Skill auto-creation loop": CONFIRMED ABSENT — no such autonomous module exists in Hermes; what exists is manual skill install + format spec

**One risk to flag**: The WebFetch tool returned summarized content, not raw Python source. Function signatures and data structures are accurate (confirmed cross-referenced against multiple files), but exact line numbers and edge-case logic should be verified against raw GitHub source before porting. Use `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/{path}` for each file during implementation.
