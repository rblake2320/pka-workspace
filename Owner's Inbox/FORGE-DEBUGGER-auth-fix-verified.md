# FORGE-DEBUGGER: Auth Bug Fix — Verified in Production

**Date**: 2026-03-24
**Fix Status**: COMPLETE — live authenticated write confirmed, DB row exists

---

## Root Cause

Every authenticated request runs `authenticate()` in `src/worker.js`. The SELECT query included `created_at`, a column that does not exist in the production `users` table (which uses `join_date`). D1 threw `SQLITE_ERROR: no such column: created_at` on every call, killing all authenticated actions (vote, star, follow, post, bookmark, chat).

---

## The Exact Change

**File**: `C:\Users\techai\aihangout-app\src\worker.js`, line 675

**BEFORE:**
```sql
SELECT id, username, email, reputation, join_date, ai_agent_type, is_admin, created_at FROM users WHERE id = ?
```

**AFTER:**
```sql
SELECT id, username, email, reputation, join_date, ai_agent_type, is_admin FROM users WHERE id = ?
```

`created_at` removed. `join_date` kept. The two callers at lines 1194 and 1485 that use `user.join_date || user.created_at` now safely fall through to `join_date` alone — no other changes needed.

---

## Deploy Evidence

First deploy went to the wrong environment (default env, no D1/KV bindings). Corrected to `--env=production`:

```
npx wrangler deploy --env=production

Uploaded aihangout-ai (7.24 sec)
Deployed aihangout-ai triggers (4.32 sec)
  aihangout.ai/* (zone name: aihangout.ai)
  www.aihangout.ai/* (zone name: aihangout.ai)
Current Version ID: 9ae58f01-2d0b-4577-8a8c-0fe4caae0071
```

Bindings confirmed in deploy output:
- `env.AIHANGOUT_KV` (9cd27d12b2c341b3a5b77f47b69a89c0) — KV Namespace
- `env.AIHANGOUT_DB` (aihangout-database) — D1 Database

---

## Live Verification

### Step 1 — New Account Registration

```
POST https://aihangout.ai/api/auth/register
{"username":"forgetest1774314600","email":"forgetest1774314600@mailinator.com","password":"TestPass123"}

RESPONSE: {"success":true,"token":"eyJhbG...","user":{"id":234,"username":"forgetest1774314600",...}}
```

User ID: **234** — new account, JWT token obtained.

### Step 2 — Authenticated Write (Vote on Problem 220)

```
POST https://aihangout.ai/api/problems/220/vote
Authorization: Bearer eyJhbG...
{"vote":1}

RESPONSE: {"success":true,"upvotes":1}
```

This endpoint calls `authenticate()`, which ran the fixed SELECT query. It returned the user object successfully. The vote was cast and the upvote count incremented.

### Step 3 — D1 Row Confirmation

```sql
SELECT * FROM votes WHERE user_id = 234 ORDER BY id DESC LIMIT 5;
```

```json
{
  "id": 119,
  "user_id": 234,
  "target_type": "problem",
  "target_id": 220,
  "vote_type": "up",
  "created_at": "2026-03-24 01:09:17"
}
```

Row exists in `aihangout-database` (remote, ENAM region, served by v3-prod). The write completed. Authentication is working.

---

## Secondary Notes

- Lines 1194 and 1485 use `user.join_date || user.created_at` as a fallback for `checkNewAccountGate()`. Since `created_at` is no longer selected, this now resolves to `user.join_date` exclusively — correct behavior since that is the actual column.
- The `stars` table and star endpoint referenced in the task brief do not exist in the current production worker. The equivalent write action is `votes`, which was used for verification.
- The first `wrangler deploy` (without `--env=production`) deployed to a worker without D1/KV bindings and is functionally dead — only the `aihangout-ai` production worker on `aihangout.ai/*` matters and it is now fixed.
