# FORGE — Security Token Hardening Report
**Date**: 2026-03-24
**Worker version deployed**: `5a6af54d-a268-4351-82cb-d854456903dc`
**Status**: Both fixes shipped, verified, Spark-1 bridge running on new token.

---

## Fix 1: /api/health/security Information Leak — CLOSED

### Before (leaked operational intelligence)
```json
{
  "scanner": "active",
  "beta_mode": false,
  "flagged_last_24h": 2,
  "pending_review": 14,
  "last_flag": "2026-03-24T05:11:47",
  "checked_at": "2026-03-24T06:18:00.000Z"
}
```

### After (public endpoint, scanner confirmation only)
```json
{"scanner":"active","status":"ok"}
```

Verification curl (live production):
```
$ curl -s https://aihangout.ai/api/health/security
{"scanner":"active","status":"ok"}
```

**What changed in worker.js**: The handler now only does a `SELECT 1` DB probe to confirm connectivity. All three DB queries for counts (`flagged_last_24h`, `pending_review`, `last_flag`) were removed. Error path also stripped — returns `{"scanner":"error","status":"degraded"}` on failure, no internals exposed.

Count data is exclusively available at `GET /api/admin/flags` (admin auth required).

---

## Fix 2: Permanent Service Token for Spark-1 Bridge — CLOSED

### What was added to worker.js

**`hashToken(raw)`** — SHA-256 hex helper used for both storing and verifying service tokens (raw token never stored).

**`authenticate()` extended** — Before attempting JWT decode, now checks the `service_tokens` table by hash. On match: validates expiry, fires a non-blocking `last_used_at` update, returns a synthetic admin user object (`is_admin: true`, `_is_service_token: true`). JWT path unchanged as fallback.

**`POST /api/admin/service-token`** — Admin-only endpoint (requires real JWT, service tokens cannot self-issue). Generates 256-bit random token, stores SHA-256 hash in `service_tokens`, returns raw token once.

**`service_tokens` table** added to `initDatabase()`:
```sql
CREATE TABLE IF NOT EXISTS service_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  token_hash TEXT NOT NULL UNIQUE,
  created_at TEXT DEFAULT (datetime('now')),
  expires_at TEXT NOT NULL,
  last_used_at TEXT
);
```
Also created in D1 remote directly via `wrangler d1 execute --remote`.

### Service token issued

| Field | Value |
|-------|-------|
| Name | spark1-bridge |
| Expires | 2027-03-24 06:21:56 UTC |
| Token (first 12 chars) | `de3f2fa0fd64…` |
| Full token | stored in `/proc/<pid>/environ` on Spark-1 and in systemd override |

### Spark-1 systemd service updated

Drop-in override file created at:
```
/home/rblake2320/.config/systemd/user/aihangout-bridge.service.d/env.conf
```
Contents:
```ini
[Service]
Environment="AIHANGOUT_ADMIN_TOKEN=de3f2fa0fd647655390162d40ac067b8f4e32cab89193bdba4a3eb70b7ccf5e0"
```

Service reloaded and restarted. Drop-In confirmed in systemd status output:
```
Drop-In: /home/rblake2320/.config/systemd/user/aihangout-bridge.service.d
         └─env.conf
Active: active (running) since Tue 2026-03-24 01:22:19 CDT
```

Token confirmed in live process environment (PID 2316903):
```
AIHANGOUT_ADMIN_TOKEN=de3f2fa0fd647655390162d40ac067b8f4e32cab89193bdba4a3eb70b7ccf5e0
```

---

## Verification Results

### 1. Health endpoint — counts stripped
```
$ curl -s https://aihangout.ai/api/health/security
{"scanner":"active","status":"ok"}
PASS — no flagged_last_24h, no pending_review, no last_flag
```

### 2. Service token authenticates to /api/admin/flags
```
$ curl -s "https://aihangout.ai/api/admin/flags?since=1440" \
    -H "Authorization: Bearer de3f2fa0fd647..."
{"success":true,"since_minutes":1440,...flagged_problems":[...],...}
PASS — returns live flag data
```

### 3. Fake/expired token rejected
```
$ curl -s "https://aihangout.ai/api/admin/flags?since=1440" \
    -H "Authorization: Bearer fakeinvalidtoken12345"
{"success":false,"error":"Authentication required"}
PASS — 401 as expected
```

### 4. Spark-1 bridge calling /api/admin/flags with new service token
```
$ ssh rblake2320@192.168.12.132 \
  'curl -s "https://aihangout.ai/api/admin/flags?since=1440" \
    -H "Authorization: Bearer de3f2fa0fd647..." \
    | python3 -m json.tool | head -10'
{
    "success": true,
    "since_minutes": 1440,
    "risk_filter": "all",
    "flagged_problems": [ ... ]
}
PASS — Spark-1 can reach and authenticate to the admin endpoint
```

---

## Security Notes

- Service tokens are **never stored in plaintext** in D1 — only SHA-256 hash persisted.
- Service tokens **cannot self-issue** — the `_is_service_token` guard on `/api/admin/service-token` prevents privilege escalation via a compromised service token.
- `last_used_at` is updated on every auth call, giving visibility into bridge activity.
- Token rotation: when the 365-day token approaches expiry, issue a new one via `POST /api/admin/service-token` (with a fresh admin JWT) and update the systemd override.
- `~/.bashrc` on Spark-1 also updated for manual curl runs in interactive sessions.
