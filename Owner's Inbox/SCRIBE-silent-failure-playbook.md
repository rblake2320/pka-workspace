# Silent Failure Detection Playbook
**Author**: SCRIBE — AI Army Knowledge Capture Agent
**Date**: 2026-03-23
**Anchor Case**: aihangout.ai — Schema Column Mismatch, 100% write-path failure
**Status**: Production-ready. Ingest to Ultra RAG on publish.

---

## Preface

This playbook was written directly from a real production failure on aihangout.ai. One wrong column name in a SELECT query inside the auth middleware silently killed every authenticated write on the platform — stars, votes, posts, follows — while reads continued working and the UI appeared completely alive.

The bug was not loud. It did not crash the server. It did not trigger a 500 on the homepage. It returned structured error responses that looked like application behavior. That is what makes this class of failure uniquely dangerous.

Use this playbook before every production deploy and whenever a platform "feels" slow but isn't crashing.

---

## 1. What Is a Silent Failure?

A silent failure is a defect in which:

- The system continues operating and serving traffic
- No crash, no obvious 500, no smoke from the process supervisor
- But a subset of operations — usually writes, often authenticated paths — are failing 100% of the time
- The failures are swallowed, localized, or returned as structured error responses that do not alert monitoring

The key property: **the system believes it is healthy, or presents itself as healthy, while silently discarding or blocking work.**

Silent failures are distinct from performance degradation and from known-error states. The server is up. The logs may show errors — but nothing that trips the alert threshold. Users see the UI. Engineers see green dashboards. The data is not being written.

### Formal Definition

> A silent failure is any condition in which a user-initiated write, update, or state-change action fails without producing an observable signal at the system boundary (dashboard, alert, or on-call page), while the read path continues to function, creating a false picture of platform health.

---

## 2. Why Silent Failures Are the Most Dangerous

### The Loud Failure Contrast

When a server crashes or throws an unhandled 500, the failure is immediately observable:
- Users report it within minutes
- Error rates spike on the monitoring dashboard
- On-call is paged
- The blast radius is contained in time

That is the best-case failure mode. Loud failures are fast to detect and fast to fix.

### Why Silent Failures Are Worse — Five Reasons

**1. They build false confidence.**
The system is running. Engineers are not paged. The platform passed its last check. Everyone assumes production is healthy. Meanwhile, every star a user clicks is being silently discarded.

**2. They corrupt state slowly.**
In a write-failure scenario, the DB drifts from what users believe to be true. Star counts stop incrementing. Leaderboards freeze. User contributions vanish. By the time this is noticed, the damage may span days or weeks of missing data.

**3. They are discovered late — usually by users.**
Users notice before engineers do. "Why didn't my vote save?" Support tickets accumulate. The discovery mechanism is user frustration, not automated detection. That is the worst possible feedback loop.

**4. They leave no obvious trail.**
A schema mismatch like the aihangout.ai case leaves a stack trace in the worker logs — but those logs are not on a dashboard. You have to know to look. The error is real and present; it is just not surfaced.

**5. The blast radius is invisible until mapped.**
The aihangout.ai failure affected 100% of authenticated writes across the entire platform. But because each failure returned a structured response (an error object, not a server crash), the full scope was not obvious without explicitly testing every write action end-to-end.

### The Asymmetry That Makes This Dangerous

Read operations pass. Write operations fail. This asymmetry is precisely why standard health checks miss it. Every health check that tests `GET /api/feed`, `GET /api/problems`, or `GET /api/users/{id}` returns 200. The system is "healthy." Only a test that actually writes a row and then verifies it in the DB would have caught this.

Most health checks test reads. Most production incidents are write failures.

---

## 3. The 5 Most Common Silent Failure Patterns

### Pattern 1: Schema / Column Mismatch
**The aihangout.ai case.**

Code references a column that does not exist in the live database. The most common version: a column was renamed in a migration but the application code was not updated everywhere, or a new table was deployed to production without running migrations.

**How it presents**: Reads pass. Writes that touch the affected column fail with `SQLITE_ERROR: no such column` or equivalent. If auth middleware is the failure point, 100% of authenticated writes fail across the entire platform.

**Why it survives code review**: The column exists in the dev database. The SELECT works in dev. The test suite runs against dev. Production has a different schema because the migration was missed or partial.

**Detection signal**: Look for DB errors in worker logs. In Cloudflare Workers / D1, check the Workers logs via the dashboard. Search for `no such column`, `column does not exist`, `unknown column`.

---

### Pattern 2: Swallowed Exceptions

The try/catch block catches the error, logs it at `console.error`, and then returns `{ success: true }` or a 200 response. The caller receives a success signal. The write never happened.

**How it presents**: API returns 200. Client-side shows "saved." DB has no new row. No alert fires. The log entry exists but is not monitored.

**Why it survives code review**: The developer intended to handle errors gracefully. "We don't want the whole request to fail just because X failed." The intent is reasonable. The implementation is missing the critical step: if you catch and don't rethrow, you must verify the fallback path actually did the work.

**Detection signal**: Search the codebase for `catch` blocks that do not rethrow and do not return an explicit error response. Any `catch (e) { log(e); return success; }` is a landmine.

---

### Pattern 3: Async Write Without Await

An async write is dispatched but not awaited. The function returns before the write completes. The caller receives a success response. The write may complete eventually, or it may fail silently, or — in edge runtimes with short execution windows like Cloudflare Workers — it may be killed before it finishes.

```
// Dangerous pattern
async function postSolution(data) {
  db.run('INSERT INTO solutions ...', data)  // no await
  return { success: true }                   // returns immediately
}
```

**How it presents**: Intermittent write failures. Under load or in edge runtimes, the missing `await` is lethal. In a development environment with low latency, it may appear to work because the write completes before the process moves on.

**Detection signal**: Search for database write calls (INSERT, UPDATE, DELETE) that are not preceded by `await`. In Cloudflare Workers, any unawaited promise in a request handler that completes before the worker exits is silently dropped.

---

### Pattern 4: Wrong Environment Configuration

The production deployment is pointed at a staging or development database. Writes succeed — but they go somewhere else. The production DB stays empty. Reads from production return no data or stale data.

**How it presents**: Writes appear to succeed (the API returns 200, the DB write actually happened). But the data never appears on the production platform because reads are coming from the correct production DB and the writes went to dev. The mismatch can manifest as "data disappears after I post it" or "other users can't see what I just did."

**Detection signal**: After every deploy, verify the DB binding in the runtime config. For Cloudflare Workers, check `wrangler.toml` — the `[[d1_databases]]` binding must point to the production database ID, not a preview or dev binding. Cross-reference the database ID in the Workers dashboard against the production D1 database list.

---

### Pattern 5: Middleware Auth Failure Returning Null User

The auth middleware fails — token expired, missing header, DB error during user lookup — and instead of throwing or returning a 401, it returns `null` as the user object. Downstream handlers check `if (user)` and skip the write path rather than throwing. The response comes back as a success or a generic error, but no write happened.

**How it presents**: The write action appears to fail with a generic error (or sometimes succeeds silently with no effect). Refreshing the auth token does not help because the failure is in the middleware logic, not the token itself. Auth logs show repeated failures but at a rate that does not trip alert thresholds.

**The aihangout.ai connection**: The actual aihangout.ai failure was this pattern combined with Pattern 1. The `authenticate()` function queried `SELECT ... created_at FROM users WHERE id = ?` — the column `created_at` does not exist in production (the column is `join_date`). D1 threw `SQLITE_ERROR: no such column: created_at` on every auth call. Auth returned a failure. Every authenticated write was blocked.

**Detection signal**: Alert on auth middleware failure rate, not just total error rate. If auth fails N times in M seconds for any reason, that is a P1 signal — the entire write path may be down.

---

## 4. Detection Checklist — Before It Becomes a User Problem

Run this checklist on every production deploy. It takes 10 minutes. It would have caught the aihangout.ai failure in the first post-deploy test.

### Pre-Deploy (Schema Validation)

- [ ] Diff the `CREATE TABLE` schema in the migration file against the live DB schema
- [ ] For every column referenced in application code, verify it exists in the live table
- [ ] For Cloudflare D1: run `wrangler d1 execute <DB_NAME> --command "PRAGMA table_info(users);"` and compare against every `SELECT` that touches the `users` table
- [ ] Check every environment binding in `wrangler.toml` — confirm production DB IDs, not preview IDs
- [ ] Verify that `await` precedes every database write call in the codebase

### Post-Deploy (Write-Path Verification)

- [ ] Register a fresh test account (do not reuse existing session tokens)
- [ ] Perform **every write action** the platform supports, end-to-end:
  - Post a problem / solution / comment
  - Star a post
  - Vote on a post
  - Follow a user
  - Update a profile field
- [ ] After each write: query the DB directly to confirm the row exists and the count field updated
- [ ] Verify with a fresh auth token on each action — do not rely on a cached session
- [ ] Check the worker logs immediately after write actions — search for any DB error strings
- [ ] For auth-gated writes: confirm the auth middleware is resolving a valid user object (not null, not undefined)

### Ongoing (Continuous Signal)

- [ ] Set an alert on auth middleware failure rate — any sustained failure > 1% in a 5-minute window is P1
- [ ] Set an alert on write-endpoint error rate separately from read-endpoint error rate
- [ ] Verify monitoring dashboards are testing write paths, not only reads
- [ ] Review catch blocks quarterly — any catch that does not rethrow or return a typed error is a candidate for silent failure

---

## 5. The Write-Path Test Template

Use this template for every write action on any platform. Fill it in before deploying. Run it after deploying. Automate it as soon as the platform has CI.

```
=== WRITE-PATH TEST ===

ACTION: [human-readable name, e.g. "Star a problem"]
PLATFORM: [e.g. aihangout.ai / Cloudflare Workers + D1]
DATE: [YYYY-MM-DD]
TESTER: [who ran it]

--- PRE-CONDITION ---
DB state before test:
  [SQL query to establish baseline, e.g.]
  SELECT stars_count FROM problems WHERE id = 'PROBLEM_ID';
  Expected: stars_count = 0

--- AUTHENTICATION ---
Auth method: [e.g. Bearer token, session cookie]
Token freshness: [e.g. generated N minutes ago — must be fresh]
Test account: [e.g. test+write@yourdomain.com — dedicated write-test account]

--- API CALL ---
Endpoint: POST https://yourdomain.com/api/problems/PROBLEM_ID/star
Headers:
  Authorization: Bearer {TOKEN}
  Content-Type: application/json
Body: {} (or as required)

Full curl:
  curl -X POST https://yourdomain.com/api/problems/PROBLEM_ID/star \
    -H "Authorization: Bearer {TOKEN}" \
    -H "Content-Type: application/json" \
    -v

--- EXPECTED RESPONSE ---
Status: 200
Body: { "success": true, "stars_count": 1 }

--- DB VERIFICATION ---
Query:
  SELECT stars_count, updated_at
  FROM problems
  WHERE id = 'PROBLEM_ID';

Expected:
  stars_count = 1
  updated_at = [within last 60 seconds]

Secondary check (junction table, if applicable):
  SELECT * FROM problem_stars
  WHERE problem_id = 'PROBLEM_ID' AND user_id = 'TEST_USER_ID';
  Expected: 1 row

--- VERDICT ---
[ ] PASS — DB matches expected, response correct, no errors in worker logs
[ ] FAIL — describe what didn't match

If FAIL:
  Worker log error: [paste exact error string]
  Root cause hypothesis: [schema mismatch / swallowed exception / missing await / env config / auth failure]
  Escalate to: FORGE (fix) → SENTINEL (verify) → SCRIBE (document pattern)

=== END WRITE-PATH TEST ===
```

### Running the Full Suite

For a platform with N write actions, create N copies of this template. Run them in sequence, post-deploy, before announcing the deploy is live. This is the minimum viable write-path regression suite.

Name the files: `write-test-[action-name].txt` and commit them to the repo under `tests/write-path/`.

---

## 6. Self-Heal Pattern — Wiring This Into Continuous Monitoring

This section describes the architecture conceptually. Implementation is platform-specific.

### Layer 1: Post-Deploy Smoke Test (Automated)

Every deploy triggers a smoke test suite that exercises the write path. The test:
1. Creates or uses a dedicated smoke-test account with a fresh token
2. Executes every registered write action against production
3. Queries the DB directly after each write to verify the row
4. Reports PASS/FAIL per action to a status endpoint
5. If any action fails: blocks the deploy from being marked "stable" and fires an alert

The key principle: the smoke test must verify the DB directly. A 200 response from the API is not sufficient evidence that the write succeeded.

### Layer 2: Schema Validation Pre-Deploy (Automated)

Before the deploy artifact is promoted to production:
1. Extract all SQL SELECT/INSERT/UPDATE/DELETE statements from the application code (static analysis or a registry)
2. Run each statement against the production DB schema in a dry-run / explain mode
3. If any statement references a column that does not exist in the live schema, fail the deploy and surface the diff

For Cloudflare D1, this can be implemented as a `wrangler` pre-deploy hook that runs `PRAGMA table_info()` on every table and cross-references against a column manifest checked into the repo.

### Layer 3: Auth Failure Rate Alerting (Real-Time)

The auth middleware is the choke point for every authenticated write. Wire it:
- Emit a metric on every auth call: success, failure, reason
- Alert immediately if auth failure rate exceeds 1% over a 5-minute window
- Alert immediately on any `no such column` or equivalent DB error string in worker logs
- These are P1 signals — do not wait for user reports

### Layer 4: Agent-Triggered Diagnosis Pipeline

When monitoring detects a silent failure signal:

```
MONITORING ALERT fires
       |
       v
AXIOM receives alert
       |
       v
AXIOM dispatches NOVA (initial triage)
  → NOVA: What changed in the last deploy?
  → NOVA: Which endpoints are failing? Pattern?
  → NOVA: Auth failure or application logic failure?
       |
       v
AXIOM dispatches FORGE (root cause + fix)
  → FORGE: Reproduce the failure
  → FORGE: Identify the specific failure pattern (from this playbook)
  → FORGE: Propose minimal fix
       |
       v
AXIOM dispatches SENTINEL (verify fix)
  → SENTINEL: Run write-path test suite against staging with fix applied
  → SENTINEL: Confirm all N write actions PASS
  → SENTINEL: Sign off on production deploy
       |
       v
AXIOM dispatches SCRIBE (knowledge capture)
  → SCRIBE: Document the pattern, the detection test, the fix
  → SCRIBE: Ingest to Ultra RAG
  → SCRIBE: Update this playbook if a new pattern was found
```

This pipeline converts a production incident into a shared learning event in under one hour.

### Layer 5: Write/Read Metric Separation

Most monitoring treats all API traffic as a single error rate. Separate it:
- `error_rate_reads` — GET endpoints
- `error_rate_writes` — POST, PUT, PATCH, DELETE endpoints

Alert thresholds should be independent. A platform where reads work and writes fail will show a low overall error rate, which is why the aggregate metric is misleading. The write-specific error rate will be elevated and will catch the failure faster.

---

## 7. Share the Fix Forward

When a silent failure is found and fixed, the fix is not complete until this four-step closure is done.

### Step 1: Classify the Pattern

Map the failure to one of the 5 patterns in Section 3, or document a new pattern if it doesn't fit. Name it. "Schema column mismatch in auth middleware" is precise enough to search for later. "Something broke in auth" is not.

### Step 2: Write the Detection Test That Would Have Caught It

Not a description of the test — the actual test artifact. For the aihangout.ai case:

```
ACTION: Authenticate and star a problem
PRE-CONDITION: SELECT stars_count FROM problems WHERE id = 'X' → 0
API CALL: POST /api/problems/X/star (with fresh Bearer token)
EXPECTED: 200, { success: true }
DB CHECK: SELECT stars_count FROM problems WHERE id = 'X' → 1
VERDICT: FAIL → DB shows 0
WORKER LOG: "SQLITE_ERROR: no such column: created_at"
ROOT CAUSE: authenticate() SELECT references users.created_at, column is users.join_date in production
```

That test, written before deploy, would have caught the failure in the first post-deploy check.

### Step 3: Add to Regression Suite

The detection test becomes a permanent regression test. It runs on every future deploy. The specific failure that caused this incident can never silently reappear without tripping the test.

For schema-related failures specifically: add the affected column to the column manifest that the pre-deploy schema validator checks. The specific column mismatch that caused the incident is now impossible to deploy without an explicit failure signal.

### Step 4: Ingest to Shared Knowledge Base

Post the pattern, the detection test, and the fix to Ultra RAG under the `personal` collection (or `production-incidents` if a dedicated collection exists). Tag it with the platform name, the failure class, and the date.

Every agent in the AI Army can then query Ultra RAG for "silent failure" or "schema mismatch" or "auth middleware failure" and retrieve this case study with its detection method and fix.

The knowledge does not stay in one agent's context. It becomes institutional memory.

---

## Appendix A: The aihangout.ai Case Study — Full Timeline

**Platform**: aihangout.ai (Cloudflare Workers + D1 SQLite)

**Production schema**: `users` table has column `join_date`

**Application code** (`authenticate()` function):
```sql
SELECT id, email, username, join_date, ... FROM users WHERE id = ?
-- Bug version:
SELECT id, email, username, created_at, ... FROM users WHERE id = ?
```

**Failure mode**: D1 throws `SQLITE_ERROR: no such column: created_at` on every call to `authenticate()`. Auth middleware returns a failure. Every authenticated write (star, vote, post, follow) is blocked. Reads — which do not call `authenticate()` — work normally.

**Observable state at time of discovery**:
- Homepage: working
- Feed: working
- Problem detail pages: working
- POST /api/problems/X/star: error
- POST /api/solutions: error
- POST /api/votes: error
- POST /api/follows: error

**Discovery method**: Manual end-to-end testing of write paths. Not automated. Not monitoring. Human tester clicked "star" and observed the error response.

**Time in production before discovery**: Unknown. Could have been live since initial deployment.

**Fix**: Remove `created_at` from the SELECT in `authenticate()`. One line change. Redeploy.

**Fix time**: Minutes once the root cause was identified.

**What would have caught it in < 5 minutes**:
A post-deploy write-path test that starred one problem with a fresh token and then queried `SELECT stars_count FROM problems WHERE id = X` would have returned `stars_count = 0` and flagged the failure immediately.

**What was missing**:
- No post-deploy write-path smoke test
- No schema column validation in the deploy pipeline
- No auth failure rate alerting separate from overall error rate
- Testing coverage was read-only

---

## Appendix B: Quick Reference — Silent Failure Signals

| Signal | What It Might Mean |
|--------|-------------------|
| Reads work, writes fail | Auth middleware failure, schema mismatch on write path |
| DB error strings in logs, no alert fired | Error swallowed in catch block, alert threshold too high |
| Users reporting "my post disappeared" | Wrong environment config (writes going to dev DB) |
| API returns 200 but no DB row | Async write without await, swallowed exception |
| Auth failures spiking quietly | Column mismatch in user lookup, expired signing key |
| Counter fields not incrementing | DB constraint violation swallowed, counter update not awaited |

---

## Appendix C: Cloudflare Workers / D1 Specific Notes

Cloudflare Workers run in an edge runtime with specific constraints that amplify silent failure risk:

1. **Execution lifetime is bounded**: Unawaited promises that haven't resolved when the worker completes are silently killed. Always await DB writes.

2. **Preview vs. Production D1 bindings**: `wrangler dev` uses preview databases by default. Production deploys use the binding in `wrangler.toml`. Verify the database ID in the dashboard against the expected production D1 database. They are different databases.

3. **D1 error messages are precise**: `SQLITE_ERROR: no such column: X` tells you exactly which column is missing. The error is not ambiguous — it is just not surfaced to monitoring unless you explicitly log and alert on worker error strings.

4. **Workers logs are short-lived**: Worker invocation logs are not stored indefinitely. Check them immediately after a suspicious write failure, not hours later.

5. **Auth middleware is the blast radius multiplier**: Because every authenticated endpoint passes through auth, a failure in auth middleware is a platform-wide write outage, not an isolated endpoint failure. Instrument it accordingly.

---

*Playbook version 1.0 — 2026-03-23*
*Written by SCRIBE from a real production incident on aihangout.ai*
*Ingest target: Ultra RAG, collection: personal*
*Next review: after next production incident or quarterly, whichever is first*
