# VidIntel — Browser Test + Red Team Report
**Date:** 2026-04-27  
**Status: ALL GREEN — GO**

---

## What Was Built
VidIntel converts YouTube URLs or raw transcripts into structured AI output (Bullet Plan, SOP, Study Guide, Key Concepts) using:
- **Backend:** FastAPI + Celery + PostgreSQL + Redis (port 8001)
- **Frontend:** Next.js 15.5.15 App Router (port 3010)
- **LLM:** NVIDIA API (llama-3.1-8b-instruct) via OpenAI-compatible endpoint
- **Auth:** Self-contained local JWT auth (no Supabase SDK dependency)

---

## Browser Test Results

| Flow | Result |
|------|--------|
| Home page loads | PASS |
| Register new account | PASS |
| Navbar updates on auth (event-driven) | PASS |
| Paste transcript → select format → Process | PASS |
| Redirect to /processing/[jobId] with live progress bar | PASS |
| Celery worker processes with NVIDIA LLM | PASS |
| Auto-redirect to /output/[jobId] on completion | PASS |
| Structured Markdown output rendered with ReactMarkdown | PASS |
| Download .md → GET /api/jobs/{id}/download/md → 200 | PASS |
| Download .pdf → GET /api/jobs/{id}/download/pdf → 200 | PASS |
| History page shows all sessions | PASS |
| Sign Out → redirects to /login | PASS |
| Protected route (/history) while logged out → redirects to /login | PASS |

**All 13 browser flows: PASS**

---

## Red Team Results (CRUCIBLE Layer 3.5)

| # | Test | Response | Verdict |
|---|------|----------|---------|
| 1 | Auth bypass (no token) | 401 Not authenticated | **PASS** |
| 2 | Auth bypass (forged JWT wrong secret) | 401 Signature verification failed | **PASS** |
| 3 | SQL injection `admin'--` in email | 422 not valid email | **PASS** |
| 4 | SQL injection `' OR '1'='1` in email | 422 not valid email | **PASS** |
| 5 | XSS `<script>alert(1)</script>` in source | 202 accepted; output clean, no script tag | **PASS** |
| 6 | IDOR — access another user's job | 404 Job not found | **PASS** |
| 7 | Mass assignment (`is_admin: true` in register) | 201; JWT has no admin fields | **PASS** |
| 8 | Missing required field (no password) | 422 Field required | **PASS** |
| 9 | Oversized input (100KB source) | 422 String too long | **PASS** |
| 10 | Invalid UUID in path | 422 invalid UUID | **PASS** |

**10/10 PASS — No security defects found**

---

## Fixes Applied During This Session

1. **CRITICAL — `exporter.py` import** `from fpdf2 import fpdf` → `from fpdf import FPDF`
2. **CRITICAL — LLM key fallback chain** — Added NVIDIA API (OpenAI-compatible) as fallback when OPENAI/ANTHROPIC keys invalid; active key: `nvapi-...`
3. **CORS** — Added `http://localhost:3010` to `ALLOWED_ORIGINS`
4. **Backend port** — Moved from 8001 (8000 was taken by existing service)
5. **Celery engine** — Moved `create_engine()` to module-level (was per-task, causing pool exhaustion)
6. **Download endpoints** — Wired `GET /api/jobs/{id}/download/md` and `/pdf` into router
7. **Auth system** — Replaced Supabase SDK with self-contained FastAPI local auth (bcrypt + HS256 JWT)
8. **Navbar reactivity** — Added `vidintel-auth-changed` custom event so Navbar updates without page reload
9. **Next.js CVE** — Upgraded from 15.0.0 to 15.5.15
10. **OS env override** — OPENAI_API_KEY set at OS level was overriding `.env` empty value; fixed by starting processes with `OPENAI_API_KEY=""` explicitly

---

## Security Observations (LOW, non-blocking)

- JWT error message says "Signature verification failed" — minor info disclosure, could generalize to "Invalid token"
- SQLi defense is email-format validation (Pydantic), not query-level; safe now but future free-text endpoints need ORM parameterization explicitly confirmed
- XSS protection is incidental (LLM transforms input) — if any endpoint ever echoes raw source text, it should HTML-escape first

---

## Test Recording
`vidintel_full_flow.gif` — downloaded to browser Downloads folder (4.2MB, 38 frames)

---

## Services Required to Run
```bash
# Backend (from VidIntel/backend/)
OPENAI_API_KEY="" NVIDIA_API_KEY="nvapi-..." uvicorn app.main:app --host 0.0.0.0 --port 8001

# Celery worker
OPENAI_API_KEY="" NVIDIA_API_KEY="nvapi-..." celery -A app.tasks.celery_tasks.celery_app worker --pool=solo

# Frontend (from VidIntel/frontend/)
npm run dev -- --port 3010

# Dependencies: Redis on 6379, PostgreSQL on 5432 (db: vidintel, user: redteam/redteam)
```
