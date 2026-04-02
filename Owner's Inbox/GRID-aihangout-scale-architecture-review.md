# GRID — Scale & Architecture Integrity Review
## aihangout.ai — v1.0.0

**Review date:** 2026-03-23
**Method:** Live API inspection via Playwright + behavioral analysis of observed test artifacts
**Scope:** Public surface — API endpoints, response structure, data integrity, infrastructure signals

---

## Scale Verdict: CONDITIONAL

The platform is functional at current micro-load (2–6 concurrent users). It will not survive a
meaningful traffic event without hitting at least three hard blockers first. None require an
architectural redesign — they are fixable in days, not months. But they are not optional fixes;
they are pre-growth requirements.

---

## Critical Issues

Ordered by severity. Fix before any marketing push or press coverage.

### 1. No rate limiting on write endpoints — confirmed via live test data in production

**Severity: Critical**

The production database contains the forensic evidence of its own vulnerability. Records with
`username: loadtest001` and `username: sec_rate_001` submitted 10 concurrent identical writes
and 10 sequential load-test problems on 2026-03-20, all of which succeeded and are now live in
the feed. The race condition test produced 5 duplicate records with identical titles
(`RACE_CONDITION_TEST_identical`, IDs 223–227) — all committed. This means:

- No duplicate submission guard (no unique constraint on title+user_id, or the constraint doesn't
  fire under concurrent load)
- No per-user write rate limiting on `/api/problems` POST
- No moderation gate blocking test accounts from polluting production data

Any bad actor — or a viral moment that triggers bot submissions — will fill the feed with garbage.
At 10 concurrent writes per second sustained for 5 minutes, you have 3,000 junk records. The
platform becomes unusable.

**Fix:** Add a per-user POST rate limit (e.g., 5 problems/hour via Redis or an in-memory token
bucket). Add a unique constraint at the DB level: `UNIQUE(user_id, title)` with a 60-second
deduplication window. Add a content hash check server-side before INSERT.

### 2. Unbounded `limit` parameter on list endpoints

**Severity: Critical**

Direct API call: `GET /api/problems?limit=242&offset=0` returned all 242 records in a single
response — 350KB+ of JSON. The server did not cap, reject, or paginate this. A single request
with `limit=10000` will attempt to load every record in the table into memory, serialize it, and
send it across a VPS connection (8GB RAM, shared).

Same pattern confirmed on `/api/problem-bank?limit=20&offset=0` — the limit parameter is
accepted without server-side enforcement of a maximum.

At 1,000 problems this is a slow response. At 10,000 problems this will OOM the Node/Python
process. At 50,000 problems it will take down the VPS.

**Fix:** Enforce `MAX_LIMIT = 50` server-side on all list endpoints. Ignore any client-supplied
value above that ceiling. This is one line of code per endpoint.

### 3. Test data in production — content integrity failure

**Severity: High (trust-killing)**

The live feed currently shows as its most recent 20 problems:
- 10x "Concurrent write test N" (user: loadtest001)
- 5x "Load test problem N" (user: loadtest001)
- 5x "RACE_CONDITION_TEST_identical" (user: sec_rate_001)

The Problem Bank contains:
- A QA Verification Report submitted as a problem (ID 23) — internal agent output treated as
  user content
- Duplicate "Full test: API coverage" records (IDs 20 and 21, identical title/description,
  different timestamps — a write-path test that fired twice)
- AI-to-AI conversation posts ("Hey Desktop Claude!") visible as problems

A real user landing on the platform today sees a feed dominated by test infrastructure. This is
not a scale issue — it is a first-impression issue that actively signals "this is not a real
platform yet." Fix it before any growth push: delete all test records, ban/hide the test accounts,
or add a `is_test` flag with a display filter.

### 4. Sequential integer IDs — full corpus enumerable without auth

**Severity: High**

Every problem, user, and (inferred) solution is addressable by sequential integer ID. IDs start
at 1 (`/api/problems/1` returns full record including user_id, created_at, all metadata).
Non-existent IDs return 404 cleanly, confirming enumerability.

A scraper can walk `/api/problems/1` through `/api/problems/999` in under 60 seconds with no
auth and extract the full platform corpus — every problem, every username, every solution, every
bounty, every `user_id`. The `user_id` field is exposed in every problem record and maps
directly to `/profile/username`.

This is also a business risk: a competitor can snapshot your entire content database daily.

**Fix (short term):** Add a per-IP rate limit on individual-record endpoints (100 req/min).
**Fix (long term):** Migrate to UUIDs or ULIDs for public-facing IDs. Keep integer primary keys
internally but never expose them in URLs or API responses. This is a schema migration — plan it
before the table has millions of rows.

---

## Growth Ceiling

**Current state:** 242 problems, 6 concurrent users (observed), VPS with 8GB RAM.

| Load event | Estimated ceiling | What breaks first |
|---|---|---|
| 50 concurrent users | Survivable | Nothing critical yet |
| 200 concurrent users | Marginal | WebSocket connection count, guest heartbeat poll frequency |
| 500 concurrent users | Failure zone | DB connection pool exhaustion (if not using a pooler like PgBouncer), unbounded limit queries cause OOM |
| Viral spike (5,000 req/min) | Full outage | VPS CPU + RAM saturated; no queue, no backpressure, no CDN for API responses |
| 10,000 problems in DB | Degraded | Unbounded limit queries become multi-second; no evidence of indexes on filter columns (category, status, sortBy) |
| 100,000 problems | Rewrite required | Sequential integer enumeration becomes a liability; tag storage (malformed JSON strings) breaks search |

**The 8GB RAM VPS is the hardware ceiling.** It can handle a small community indefinitely if
the application is well-behaved. It cannot handle a spike. There is no horizontal scaling path
on a single VPS — no load balancer, no second instance.

The practical growth ceiling before infrastructure must change: approximately 500 daily active
users with normal usage patterns, or any single viral moment above ~1,000 simultaneous visitors.

---

## Debt Register

These are known issues that don't require immediate fixes but need a timeline.

| Issue | Risk | Fix deadline |
|---|---|---|
| Tags stored as malformed serialized JSON strings | Search/filter on tags will break or return wrong results; data is corrupt | Before tag-based features ship |
| `user_id` exposed in all API responses | PII enumeration risk; enables user graph reconstruction | Before reaching 10k users |
| No health endpoint observed | Cannot detect app crashes automatically; restart requires manual intervention | This week |
| Live user count via polling (`/api/live/count`) | Every guest fires a POST heartbeat + GET count on interval; at 500 users this is 1,000 req/min of internal overhead | Before 200 DAU |
| No evidence of DB connection pooling config | If using raw connections per request, will hit PostgreSQL's max_connections ceiling under moderate load | Before 100 concurrent users |
| Problem Bank and main feed share the same data source (total: 242 both) | One content moderation action affects both views; test data in one pollutes the other | Before content curation features ship |
| No CDN caching on API responses | Every page load hits the VPS origin; static-ish list responses (Hot, Top sort) could be cached 60s with massive throughput improvement | Before any growth push |

---

## Recommended Fixes

In priority order — specific actions, not suggestions.

**This week (before any marketing):**
1. Delete all test records from production: `DELETE FROM problems WHERE user_id IN (SELECT id FROM users WHERE username IN ('loadtest001', 'sec_rate_001'))`. Verify Problem Bank no longer shows QA reports or AI-to-AI posts.
2. Add server-side limit cap: in every list handler, `const safeLimit = Math.min(parseInt(limit) || 20, 50)`. One line per endpoint.
3. Add per-user write rate limit: Redis `INCR user:{id}:posts:hourly` with 3600s TTL, reject if > 5.

**Within 2 weeks:**
4. Add duplicate submission guard: hash `(user_id + title)` and check against a recent-submissions cache (Redis SET with 5-min TTL) before INSERT.
5. Add per-IP rate limit on `/api/problems/:id` (individual record fetch): 100 req/min max.
6. Fix tag storage: tags are currently stored as literal strings like `"{\"indicators\":[\"testing\""` — this is double-serialized JSON. Normalize to a proper junction table or a clean JSON array column.

**Within 30 days:**
7. Add a health endpoint (`GET /api/health` returning `{status: "ok", db: "ok"}`) and wire it to an uptime monitor (UptimeRobot free tier is sufficient).
8. Verify PgBouncer or equivalent connection pooler is in place. If not, add it — this is the single most important scalability addition before 100 concurrent users.
9. Plan UUID migration for public-facing IDs. Don't do it yet — do it before the table exceeds 50k rows.

---

## Re-check Criteria

GRID will upgrade this verdict from CONDITIONAL to PASS when:
1. Unbounded `limit` is capped server-side (verifiable by calling `?limit=10000` and confirming it returns ≤ 50 records)
2. Test data is purged from production
3. A write rate limit is confirmed on the problems POST endpoint (attempt 10 rapid posts and confirm rejection after threshold)
4. A health endpoint exists and returns 200

The remaining debt items move this from CONDITIONAL to a clean architecture — they do not block a PASS on the critical path.

---

*GRID — Scale & Architecture Integrity*
*Delivered to Owner's Inbox per standing protocol*
