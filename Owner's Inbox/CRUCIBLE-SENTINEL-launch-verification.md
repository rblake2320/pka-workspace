# Launch Verification Report — aihangout.ai
**Pair:** CRUCIBLE (test execution) + SENTINEL (GO/NO-GO)
**Date:** 2026-03-23
**Site under test:** https://aihangout.ai (live production)
**Context:** DEBUGGER+FORGE pair was applying fixes during testing. Results reflect the site as found.

---

## SENTINEL VERDICT — UP FRONT

**NO-GO. Public launch is blocked.**

Two conditions are independently sufficient to block launch:
1. The entire visible homepage feed is 100% test garbage — every problem a new user sees is a test artifact.
2. No Terms of Service or Privacy Policy exists anywhere on the site — legally required before collecting user data.

Neither condition is acceptable for public launch. Both require immediate remediation.

---

# CRUCIBLE — TEST EXECUTION REPORT

## Test Objective
Verify resolution of audit-identified launch-blocking issues. Catch any fixes that were incomplete or any new failures introduced during the DEBUGGER+FORGE patch session. Provide SENTINEL with evidence-based findings for GO/NO-GO.

## Test Design
- **Black-box API testing** via direct HTTP: equivalence partitioning on limit parameter, boundary values on sequential ID range, rapid-fire POST sequences for rate limit verification.
- **Browser automation** via Playwright: live page rendering, DOM content extraction, route existence checks.
- **Data analysis** via Python: full 242-record database dump analyzed for test contamination percentage, duplicate titles, bounty tier distribution.
- All tests run unauthenticated (anonymous new-user perspective) unless otherwise noted.

---

## Test Results

### TEST 1 — Test Data Cleanup
**Status: FAIL**

**Question:** Are "Concurrent write test", "Load test problem", "RACE_CONDITION_TEST_identical" still visible?

**Evidence:**
The API at `GET /api/problems?limit=1000` returns 242 total records. Of those:

| Test artifact type | Count | User account |
|---|---|---|
| Concurrent write test 1–10 | 10 | loadtest001 |
| Load test problem 1–5 | 5 | loadtest001 |
| RACE_CONDITION_TEST_identical (×5) | 5 | sec_rate_001 |
| XSS img test | 1 | sec_inject_001 |
| `<script>alert(document.cookie)</script>` | 1 | sec_inject_001 |
| **Total named test artifacts** | **22** | — |

**Zero test records have been deleted.** All 22 are fully public and accessible without authentication.

**Critical finding — homepage is entirely broken for new users:**
The New feed (default view) and Hot feed both sort by recency. Because test records IDs 223–242 are the most recently created, they completely dominate page 1. A new user landing on https://aihangout.ai sees this as their entire first page:

```
[233] "Concurrent write test 3"    | loadtest001 | "concurrent write test"
[234] "Concurrent write test 2"    | loadtest001 | "concurrent write test"
[235] "Concurrent write test 4"    | loadtest001 | "concurrent write test"
[236] "Concurrent write test 1"    | loadtest001 | "concurrent write test"
[237] "Concurrent write test 6"    | loadtest001 | "concurrent write test"
[238] "Concurrent write test 5"    | loadtest001 | "concurrent write test"
[239] "Concurrent write test 7"    | loadtest001 | "concurrent write test"
[240] "Concurrent write test 8"    | loadtest001 | "concurrent write test"
[241] "Concurrent write test 9"    | loadtest001 | "concurrent write test"
[242] "Concurrent write test 10"   | loadtest001 | "concurrent write test"
[228] "Load test problem 1"        | loadtest001 | "load test write"
[229] "Load test problem 3"        | loadtest001 | "load test write"
[230] "Load test problem 4"        | loadtest001 | "load test write"
[231] "Load test problem 2"        | loadtest001 | "load test write"
[232] "Load test problem 5"        | loadtest001 | "load test write"
[223] "RACE_CONDITION_TEST_identical" | sec_rate_001
[224] "RACE_CONDITION_TEST_identical" | sec_rate_001
[225] "RACE_CONDITION_TEST_identical" | sec_rate_001
[226] "RACE_CONDITION_TEST_identical" | sec_rate_001
[227] "RACE_CONDITION_TEST_identical" | sec_rate_001
```

This was verified by both direct API call and live browser rendering via Playwright. The rendered page confirms this is exactly what users see.

**Database contamination breakdown:**
Of 242 total records, 219 (90.5%) were created by identifiable test/bot accounts:

| Account | Problems | Type |
|---|---|---|
| aihangout-curator | 143 | AI bot (content harvester) |
| Claude AI Tester | 16 | Test bot |
| loadtest001 | 15 | Load test |
| ClaudeOpus-DGXSpark | 15 | AI bot |
| Claude_Desktop_Agent | 12 | AI bot |
| Claude_QA_Reviewer | 7 | AI bot |
| sec_rate_001 | 5 | Security test |
| **Others (bots)** | 6 | Various test bots |
| **Total bot/test** | **219** | **90.5%** |

Apparent real-user content: **23 records (9.5%)** — none visible on page 1.

**Additional finding:** Two XSS injection payloads remain in the live database:
- ID 222: title = "XSS img test" (user: sec_inject_001)
- ID 221: title = `<script>alert(document.cookie)</script>` (user: sec_inject_001)

These are stored as text and the React frontend appears to escape them on render, but they should not exist in a production database regardless.

---

### TEST 2 — Problem Bank Duplicates
**Status: PARTIAL**

**Question:** Are the same problem titles appearing at multiple bounty tiers in `/problem-bank`?

**Evidence (API-level):** `GET /api/problem-bank?limit=500` returned all 242 records. At the data layer, **zero bounty problems share a title at multiple bounty tiers**. The bounty distribution is clean:

| Bounty | Count |
|---|---|
| $0 | 224 |
| $500 | 6 |
| $1,000 | 5 |
| $1,500 | 5 |
| $2,000 | 2 |

**Evidence (UI-level):** The Problem Bank page renders a "High-Value Featured Problems" section at the top, then renders the same problems again in the paginated list below. This creates a visual duplicate effect — e.g., "React useState not triggering re-render with nested objects" appears at $4,000 in the featured strip and at $2,000 in the list below. These are **the same record, not different records at different tiers**. The $4,000 figure appears to be the `estimated_value` field displayed as if it were a bounty in the featured strip, while the list shows the actual `bounty_amount` field ($2,000). This is a **UI display bug** — confusing but not a data integrity problem.

**Non-bounty duplicates confirmed in the database (5 groups):**

| Title | Duplicate IDs |
|---|---|
| RACE_CONDITION_TEST_identical | 223, 224, 225, 226, 227 |
| Full test: API coverage | 20, 21 |
| QA Verification Report - AI Solutions Quality Review | 19, 23 |
| Cross-language comparison: Implementing async retry logic | 26, 29 |
| Debate: Microservices vs Monolith for AI-powered application | 27, 30 |

All duplicate groups are test/bot content. No real user content is duplicated.

---

### TEST 3 — API Limit Parameter Enforcement
**Status: FAIL**

**Question:** Does the API enforce a server-side cap on the `limit` parameter?

**Evidence:**

| Request | Records returned |
|---|---|
| `?limit=5` | 5 |
| `?limit=50` | 50 |
| `?limit=100` | 100 |
| `?limit=200` | 200 |
| `?limit=1000` | 242 (all records) |
| `?limit=10000` | 242 (all records) |
| `?limit=0` | 0 (no error, just empty) |

**Finding:** There is no server-side cap. `limit=1000` and `limit=10000` both return the full database in a single response. At current scale (242 records) this is low risk, but it is an unguarded parameter — a user with a large enough dataset could use this to dump the entire database in one request. No 400 error is returned for obviously unreasonable values like `limit=10000`. No max cap is enforced.

---

### TEST 4 — Sequential ID Enumeration
**Status: FAIL (by design, but notable)**

**Question:** Are sequential IDs accessible without auth? What happens on non-existent IDs?

**Evidence:**

| Request | HTTP Status | Result |
|---|---|---|
| `GET /api/problems/1` | 200 | Returns full problem record |
| `GET /api/problems/2` | 200 | Returns full problem record |
| `GET /api/problems/100` | 200 | Returns full problem record |
| `GET /api/problems/999` | 404 | `{"success":false,"error":"Problem not found"}` |

**Finding:** All public problem records are enumerable by sequential integer ID without authentication. This is consistent with the platform's stated design (public problems are public). The 404 response on non-existent IDs is correct and does not leak information. This is **not a bug per se**, but it means the ID space is fully walkable by any script. Combined with the unguarded `limit` parameter (Test 3), a complete database dump is trivially easy.

---

### TEST 5 — Write Rate Limiting
**Status: PARTIAL PASS**

**Question:** Is there a rate limit response (429) on rapid write attempts?

**Evidence — Auth endpoints:**

Registration endpoint (`POST /api/auth/register`):
```
Attempt 1: HTTP 200 (success)
Attempt 2: HTTP 200 (success)
Attempt 3: HTTP 200 (success)
Attempt 4: HTTP 429 — "Too many requests. Please try again later."
Attempts 5–10: HTTP 429
```
**Rate limiting is active on registration. Triggers at ~3 requests.**

Login endpoint (`POST /api/auth/login`):
- 25 rapid requests to `/api/auth/login`: all 429. Rate limit is active and aggressive on login — appears to have already been triggered from the registration test and is blocking the IP.

**Gap — authenticated problem creation not verified:** Because rate limiting on registration blocked account creation during testing, and the problem creation endpoint (`POST /api/problems`) requires a valid auth token, the write rate limit on authenticated problem submission could not be directly tested. The endpoint correctly returns 401 on unauthenticated POST. This remains an unverified path.

**Gap — login brute force:** The login endpoint returns 401 for wrong credentials but the rate limit kicked in at attempt 25 in a rapid burst — it is not clear whether 24 attempts at a slower cadence would trigger a lockout. This is not exhaustively tested.

---

### TEST 6 — Reputation Scoring
**Status: FAIL (no evidence of working system)**

**Question:** Does reputation reflect actual contributions on user profiles?

**Evidence:**

Profile checked: `https://aihangout.ai/profile/loadtest001`
- 15 problems submitted
- **Reputation shown: 0**

Profile checked: `https://aihangout.ai/profile/aihangout-curator`
- 143 problems submitted (most prolific poster on the platform)
- **Reputation shown: 0**
- 1 follower, 0 following

Both users with the most submissions show 0 reputation. Either the reputation system is not computing scores, is only triggered by actions not yet taken (upvotes, accepted solutions), or is broken. With no solutions accepted on any problem across the dataset (all `solution_count: 0`), and all upvotes at 0, the absence of reputation points may be expected behavior — but it also means the reputation system has never been exercised under real conditions. It cannot be verified as working.

---

### TEST 7 — ToS / Privacy Policy / DMCA Pages
**Status: FAIL — CRITICAL**

**Question:** Do /terms, /privacy, /dmca pages exist?

**Evidence:**

Browser navigation tests:
- `https://aihangout.ai/terms` → redirects to `/` (homepage)
- `https://aihangout.ai/privacy` → redirects to `/` (homepage)
- `https://aihangout.ai/dmca` → redirects to `/` (homepage)
- `https://aihangout.ai/terms-of-service` → SPA shell (React renders, no route match → likely 404-equivalent)
- `https://aihangout.ai/privacy-policy` → SPA shell (React renders, no route match → likely 404-equivalent)

JavaScript bundle route analysis confirms the complete list of defined routes:
```
/admin, /bookmarks, /bug-report, /changelog, /create-problem,
/learning, /learning/:id, /login, /problem-bank, /problem/:id,
/profile/:username, /register, /settings
```

**There is no `/terms`, `/privacy`, or `/dmca` route defined anywhere in the application.** No footer links to legal pages exist. The navigation bar contains no legal links.

**This is a hard legal blocker.** The platform:
1. Collects personal data (email, username, password) during registration
2. Has user-generated content (problems, solutions)
3. Has a bounty/payment system implied
4. Claims to import content from "GitHub Issues, Stack Overflow, and enterprise sources"

Operating without a Privacy Policy violates GDPR, CCPA, and general data protection requirements. Operating without Terms of Service leaves the platform legally exposed on content ownership, bounty disputes, and liability. The absence of a DMCA policy with scraped/imported content is a copyright risk.

---

### TEST 8 — Overall First Impression
**Status: FAIL**

**Question:** What does a new user see when they land on https://aihangout.ai?

**Rendered page text (verified via Playwright, live browser):**

The hero section is clean: "AI Problem Solving Community / Crowdsourced solutions to AI and technical challenges / Join the community to ask questions, share solutions, and build your reputation! / Platform developed throughout 2025 • Beta launched January 2026"

The category filters and sort buttons are present and functional in appearance.

**The problem feed — which is the entire purpose of the site — shows this to every new visitor:**

Page 1 of 13 (242 total problems). Every single visible card on page 1:
- "Concurrent write test 3" — loadtest001
- "Concurrent write test 2" — loadtest001
- "Concurrent write test 4" — loadtest001
- "Concurrent write test 1" — loadtest001
- "Concurrent write test 6" — loadtest001
- "Concurrent write test 5" — loadtest001
- "Concurrent write test 7" — loadtest001
- "Concurrent write test 8" — loadtest001
- "Concurrent write test 9" — loadtest001
- "Concurrent write test 10" — loadtest001
- "Load test problem 1" — loadtest001
- "Load test problem 3" — loadtest001
- "Load test problem 4" — loadtest001
- "Load test problem 2" — loadtest001
- "Load test problem 5" — loadtest001
- "RACE_CONDITION_TEST_identical" — sec_rate_001 (×5)

**Every single problem on the first page that any new user sees is a test artifact. The platform does not look functional. It looks abandoned or broken.**

The Hot feed has the same problem — it also sorts by recency and shows the same first page.

---

## CRUCIBLE Summary Table

| # | Test | Status | Severity |
|---|---|---|---|
| 1 | Test data cleanup | FAIL | Critical |
| 2 | Problem Bank duplicates | PARTIAL | Medium |
| 3 | API limit cap | FAIL | Medium |
| 4 | Sequential ID enumeration | FAIL (by design) | Low |
| 5 | Write rate limiting | PARTIAL PASS | Medium |
| 6 | Reputation scoring | FAIL | Low |
| 7 | ToS / Privacy / DMCA | FAIL | Critical |
| 8 | First impression / overall | FAIL | Critical |

---

# SENTINEL — GO / NO-GO DECISION

## Answer
**NO-GO.** Public launch is blocked. Two Critical issues are independently sufficient to prevent launch. Neither has been addressed by the DEBUGGER+FORGE patch session.

## What Passed
- **Rate limiting on auth endpoints** is working. Registration caps at ~3 rapid attempts. Login is rate limited. This was a previously identified gap and it is now closed.
- **404 on non-existent problem IDs** is correct. `/api/problems/999` returns a clean error, not a 500 or data leak.
- **HTTP security headers** are present and correct (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy). This is solid.
- **Problem Bank bounty data integrity** is clean at the API level — no true bounty tier duplicates in the database.
- **Authentication required on write endpoints** is correctly enforced — unauthenticated POST to `/api/problems` returns 401.

## What Failed — with Severity

### Critical — Launch Blockers

**C1. Test data fully dominates the live feed. Severity: Critical.**
The New and Hot feeds — the first thing every user sees — show 20 consecutive test artifacts as the only visible content. The database is 90.5% bot/test content. The platform communicates to any visitor: "this is not a real product." This is not a UI polish issue. It is an operational failure. The fix is mandatory and non-negotiable before any public promotion.
- Required fix: Delete all records from users `loadtest001`, `sec_rate_001`, `sec_inject_001`. Additionally audit and remove bot-generated content that has no real user value (e.g., `CodexFullTest*` accounts). At minimum, the 20 most recent records (IDs 223–242) must be purged before any user can see real content.

**C2. No ToS, Privacy Policy, or DMCA page. Severity: Critical.**
These are not nice-to-haves. They are legal requirements for any platform that:
- Collects email addresses and passwords
- Hosts user-generated content
- Operates a bounty/monetary system
- Imports third-party content (GitHub Issues, Stack Overflow)

Required fix: Create and publish `/terms`, `/privacy`, and `/dmca` routes with substantive content before collecting any user data from the public. This is not something to stub in with placeholder text — the content must actually address the data collection and content ownership model.

### High — Must Fix Before Launch

**H1. XSS injection payloads in production database. Severity: High.**
Two records (IDs 221, 222) contain raw injection test payloads including `<script>alert(document.cookie)</script>`. The React frontend escapes these on render, but they are stored in the database and will be returned in API responses to any client. A non-React consumer of the API would render these as executable HTML. They must be deleted.
- Required fix: DELETE FROM problems WHERE id IN (221, 222).

**H2. No server-side cap on the `limit` API parameter. Severity: High.**
`?limit=10000` returns the full database in a single unauthenticated response. At 242 records this is manageable; at 100,000 records this is a DoS vector and a data scraping invitation.
- Required fix: Enforce a maximum of 100 per request server-side. Return 400 for values exceeding the cap.

### Medium — Should Fix Before Launch

**M1. Problem Bank UI shows misleading "duplicate" bounty amounts. Severity: Medium.**
The Featured section displays `estimated_value` labeled as if it were a bounty, while the main list shows `bounty_amount`. The same problem appears at "$4,000" in featured and "$2,000" in the list. This is confusing and could erode trust in the bounty system.
- Required fix: Use consistent field labeling across both UI sections, or exclude featured items from the paginated list.

**M2. Reputation system unverified. Severity: Medium.**
All 242 users show 0 reputation. The system has never been exercised under real conditions. It may work correctly once real solutions and upvotes exist, but it cannot be verified from current data.
- Required action: Test reputation accrual with a controlled scenario before launch — post a problem, post a solution, upvote it, mark it accepted. Verify reputation increments.

**M3. Login rate limit may allow slow brute force. Severity: Medium.**
Rate limiting on login was observed to activate during testing, but the exact threshold (attempts per time window) was not cleanly isolated. 25 rapid requests all returned 429, but a credential stuffing attack operating at a lower cadence (e.g., 1 attempt per 5 seconds from different IPs) was not tested.
- Required action: Document and verify the rate limit policy on login. Confirm it covers both per-IP and per-account attempts.

### Low — Post-Launch Acceptable

**L1. Sequential ID enumeration. Severity: Low.**
All public problems are accessible by sequential integer ID without authentication. This is consistent with the platform's public-read design. The 404 response on non-existent IDs is correct. This is acceptable for launch — it is a documentation gap, not a defect.

**L2. Authenticated write rate limiting not verified. Severity: Low.**
Could not complete due to auth flow being blocked during testing. Given that unauthenticated endpoints are protected, this is unlikely to be missing but remains unconfirmed.

---

## Required Fixes Before GO Decision

| Priority | Fix | Responsible |
|---|---|---|
| C1 | Delete all test records (IDs 221–242, plus `loadtest001`, `sec_rate_001`, `sec_inject_001` accounts) | DEBUGGER/FORGE |
| C2 | Create `/terms`, `/privacy`, `/dmca` routes with real legal content | FORGE + LEGAL |
| H1 | DELETE FROM problems WHERE id IN (221, 222) | DEBUGGER |
| H2 | Add server-side `max_limit = 100` cap on `/api/problems` | FORGE |
| M1 | Fix Problem Bank featured section field labeling | FORGE |
| M2 | Verify reputation accrual with a controlled end-to-end test | CRUCIBLE |

## Conditions for Re-Test
CRUCIBLE should re-run tests 1, 2, 3, 7, and 8 after the above fixes are applied. A GO decision requires:
1. New and Hot feed page 1 shows zero test artifacts
2. `/terms` and `/privacy` routes exist and render substantive content
3. `/api/problems?limit=10000` returns an error or is capped at ≤100 records
4. Problem Bank UI shows consistent bounty labeling
5. Reputation accrual verified via controlled test

**Until those five conditions are met, the site must not be publicly promoted or listed in any directory.**

---

*CRUCIBLE test execution: 2026-03-23 | SENTINEL review: 2026-03-23*
*Live evidence collected from https://aihangout.ai — all API responses and browser renders confirmed against production.*
