# Election Countdown Data Capture Hardening

Date: 2026-05-15

## Verdict
GO for Cloudflare Pages + D1 launch baseline after production D1 database creation, `wrangler.toml` database id replacement, and `ADMIN_SECRET` setup.

## What Changed
- Added Cloudflare Pages Functions backend under `Election Countdown/functions/api/[[path]].js`.
- Added D1 schema in `Election Countdown/schema.sql`.
- Added deployment config in `Election Countdown/wrangler.toml`.
- Added launch instructions in `Election Countdown/LAUNCH.md`.
- Added security/cache headers in `Election Countdown/_headers`.
- Added browser-side behavioral capture in `Election Countdown/index.html`.
- Removed prototype browser-only fallbacks from `Election Countdown/assets/index-DMSdeDRP.js` so auth and vote intent persistence require the backend instead of silently saving to localStorage.
- Added `privacy.html` and `terms.html`, linked from the app shell.
- Added `/api/health`, `/api/account` deletion, production admin-secret length enforcement, salted IP hashing support through `IP_HASH_SECRET`, bounded JSON bodies, and production-safe server errors.

## Data Now Captured
- Account registration and login sessions.
- Vote intent, state, optional city, age range, sex, and donor candidate field.
- Vote intent history: previous support, new support, previous state, new state, and payload snapshots.
- Countdown cycle changes, including previous countdown, next countdown, and dwell duration.
- Page view, heartbeat, visibility hidden/visible, and page exit timing.
- CTA clicks, Vote.gov clicks, already-registered clicks, shares/referrals/events.
- Admin analytics and CSV export.

## Verification
- `node --check functions/api/[[path]].js` passed.
- `npx wrangler d1 execute election-countdown --local --file=./schema.sql` passed.
- Local Pages runtime smoke test passed:
  - Register: 200
  - Save initial intent: 200
  - Change intent: 200
  - Track countdown flip: 200
  - Public stats: 200
  - Admin analytics: 200
  - CSV export: 200
- Browser pass against `http://127.0.0.1:8788/` had no console errors, failed requests, or 4xx/5xx responses.
- Replit/prototype cleanup verification passed: no Replit markers found, no old `ec_users` / `ec_vote_intent` browser fallback keys found, frontend bundle syntax check passed, and Cloudflare Pages smoke test still passed.
- Final hardening smoke passed: `/api/health`, homepage, privacy page, terms page, registration, initial intent, changed intent, tracking, admin analytics, CSV export, and account deletion all passed locally.
- Desktop and mobile browser pass had no console errors or failed requests.
- E2E report follow-up fixed: dialog close horizontal drift, Escape close fallback, quote restore, Copy Link feedback fallback, dark-theme persistence removal, canonical privacy/terms links, direct `/admin` route handoff to `/#/admin`, static first-paint fallback, mobile registration undo link, and remaining local vote-intent browser fallback removal.
- Authenticated Round 2 follow-up fixed: verification endpoints now fail closed with 503 while provider is unavailable; Verify Identity is hidden in the UI until real provider wiring exists; `/api/account` and `/api/intent/history` now expose profile/account and change-history data; profile page gets an account/details/history panel; vote-plan dialog gets required-field helper text; phone inputs are constrained; modal/logout scroll drift is reset globally; regular tracking events are queued and flushed through `/api/track/batch`.

## Launch Requirements
- Create real Cloudflare D1 database.
- Replace `REPLACE_WITH_D1_DATABASE_ID` in `wrangler.toml`.
- Run `schema.sql` against remote D1.
- Set `ADMIN_SECRET` as a Cloudflare Pages secret.
- Set `IP_HASH_SECRET` as a Cloudflare Pages secret.
- Confirm `/api/health` returns `"ok":true` on the production domain.
- Do not enable the Verify Identity menu until a real email/SMS provider is configured and the confirm endpoints update `email_verified` / `phone_verified`.
- After public domain is known, replace relative OpenGraph image URLs with absolute production URLs.
