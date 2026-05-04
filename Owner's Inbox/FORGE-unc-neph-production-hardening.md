# Unc & Neph — Production Hardening Report

**Date:** 2026-04-28  
**Agents:** FORGE (build), CRUCIBLE (red team)  
**Verdict:** GO — 12/12 red team tests pass, 10/10 output files verified

---

## What Was Built

Static HTML studio site (3 pages) + FastAPI backend, hardened from prototype to production-ready.

**Project location:** `C:\Users\techai\unc-and-neph\`

---

## Phase 1 — Backend Critical Fixes

| Fix | File | Detail |
|-----|------|--------|
| python-dotenv loading | `backend/main.py` | `.env` was silently ignored — added `load_dotenv()` before all `os.getenv()` calls |
| DB session leak | `backend/database.py` | Converted `get_db()` to generator with `try/finally` — sessions now always close |
| FastAPI Depends injection | `backend/main.py` | All endpoints use `db: Session = Depends(get_db)` — removed direct `get_db()` calls |
| slowapi rate limiting | `backend/main.py` | `/api/contact`: 5/hr, `/api/subscribe` + `/api/unsubscribe`: 10/hr |
| Input length limits | `backend/main.py` | `Field(max_length=...)` on all Pydantic fields — name 120, email 254, body 5000, etc. |
| Body size limit | `backend/main.py` | `BodySizeLimitMiddleware` — 64KB max (HTTP 413) |
| Security headers | `backend/main.py` | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy, conditional HSTS |
| CORS ports | `backend/main.py` | Added `:3000`, `:5500`, `:8080` variants to default origins |
| Health check DB | `backend/main.py` | `/api/health` now executes `SELECT 1` — reports `ok`/`degraded` |
| Unsubscribe endpoint | `backend/main.py` | New `POST /api/unsubscribe` — always returns identical response (prevents email enumeration) |
| Docs hidden in prod | `backend/main.py` | `/docs` and `/redoc` return 404 when `APP_ENV=production` |
| slowapi Body fix | `backend/main.py` | Removed `from __future__ import annotations`, added `Body(...)` annotation, reordered `request` first — fixes FastAPI parameter binding with slowapi decorators |

---

## Phase 2 — Frontend Bug Fixes

| Fix | File | Detail |
|-----|------|--------|
| Subscribe false success | `about.html` | `catch` block now shows real error instead of fake success message |
| Contact button stuck | `about.html` | Button re-enabled + text reset after 5s success timeout |
| Journal nav link | `index.html`, `about.html`, `projects.html` | Greyed out `opacity:0.4; pointer-events:none` with "Coming soon" title |
| CTA mailto → form | `index.html` | Changed `mailto:hello@uncneph.build` → `about.html#contact` |
| Project CTA link | `projects.html` | Changed `index.html#contact` → `about.html#contact` |
| Form CSS extracted | `assets/site.css` | `.form-label` / `.form-input` moved from inline `<style>` in about.html |
| SEO meta tags | all 3 HTML files | Added `<meta name="description">`, `<meta property="og:*">`, favicon link |

---

## Phase 3 — Deployment Config

| File | Detail |
|------|--------|
| `.gitignore` | Covers `__pycache__/`, `*.db`, `.env`, `.venv/`, IDE files, OS artifacts |
| `backend/Dockerfile` | `python:3.12-slim`, pip install from requirements.txt, uvicorn on :8000, `/data` mount point |
| `docker-compose.yml` | Single `api` service, named volume for SQLite persistence, healthcheck, `restart: unless-stopped` |
| `backend/.env.example` | Updated with `APP_ENV=development`, correct CORS origins with ports |

---

## Phase 4 — Red Team Results (Layer 3.5)

**12/12 PASS** — Full checklist at `C:\Users\techai\unc-and-neph\RED_TEAM_CHECKLIST.md`

| Category | Result |
|----------|--------|
| XSS (stored) | PASS — JSON API, no rendering |
| SQL injection (email) | PASS — EmailStr rejected |
| SQL injection (name) | PASS — ORM parameterized |
| Input size limits | PASS — 422 on oversized fields |
| Rate limiting (contact 5/hr) | PASS — 429 enforced |
| Rate limiting (subscribe 10/hr) | PASS — 429 enforced |
| CORS lockdown | PASS — No header for evil origin |
| Missing fields | PASS — 422 |
| Email enumeration | PASS — Identical responses |
| Body size (879KB) | PASS — 413 from middleware |
| Duplicate subscribe | PASS — Graceful dedupe |

---

## Deployment Instructions

### Local dev
```bash
cd C:\Users\techai\unc-and-neph\backend
cp .env.example .env          # edit as needed
pip install -r requirements.txt
uvicorn main:app --port 8000
# Open index.html in browser (Live Server or any static server)
```

### Docker
```bash
cd C:\Users\techai\unc-and-neph
cp backend/.env.example backend/.env   # edit for production
docker compose up -d
# API available at http://localhost:8000
# Serve static files via nginx/Cloudflare/Netlify pointing at the project root
```

### Production env vars to set in `.env`
```
APP_ENV=production
ALLOWED_ORIGINS=https://uncneph.build,https://www.uncneph.build
NOTIFY_EMAIL=hello@uncneph.build
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=<sendgrid-key>
DATABASE_URL=sqlite:////data/unc_neph.db
MAX_BODY_SIZE=65536
```

---

## Governance

```
Audit log: C:\Users\techai\PKA testing\logs\task_audit.jsonl
10/10 output files verified on disk — all exist, all non-zero
```
