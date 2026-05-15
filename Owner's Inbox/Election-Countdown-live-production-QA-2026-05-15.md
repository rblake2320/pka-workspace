# Election Countdown Live Production QA - 2026-05-15

## Verdict
GO for public countdown, account creation, vote-intent capture, vote-intent change history, profile/account API, stats, and event tracking on Cloudflare Pages + D1.

HOLD only for real identity verification claims until an email/SMS provider is wired. The UI currently hides Verify Identity and the API fails closed with HTTP 503, so it does not falsely verify users.

## Production Target
- Live URL: https://election-countdown-38g.pages.dev
- Latest pushed commit: `6faed72 Include intent in account profile API`
- Manual Pages deployment after commit: `https://268ef3d8.election-countdown-38g.pages.dev`

## Live Checks Passed
- `/api/health`: `ok:true`, `database:true`, `adminSecret:true`, `ipHashSecret:true`, `mode:"production"`.
- Synthetic account registration returned 200.
- Auth session returned the synthetic user from `/api/auth/user`.
- Vote intent saved as `undecided/NC`.
- Vote intent updated to `independent/NC`.
- `/api/intent` returned the updated current intent.
- `/api/intent/history` returned 2 history rows.
- `/api/account` returned user, current intent, `intentHistory`, and `history` alias with 2 rows.
- `/api/verify/status` returned `providerConfigured:false`.
- `/api/verify/email/confirm` returned HTTP 503 with `verification_provider_not_configured`.
- `/api/track/batch` stored 2 events.
- `/api/track/share` returned `ok:true`.
- `/api/admin/analytics` without an admin secret returned 401.
- Synthetic account deletion returned 200.
- Post-delete `/api/intent` returned 401.
- Stats returned to 0 after removing all synthetic QA accounts.
- Public routes `/`, `/privacy`, and `/terms` returned 200.

## Follow-Up Production Fixes Applied
- Added auth compatibility endpoints: `/api/auth/login`, `/api/auth/logout`, `/api/auth/signout`, `/api/auth/me`, `/api/auth/session`, and `/api/me`.
- Added `/api/intent/aggregate` as a compatibility alias for public stats.
- Added Cloudflare `_redirects` for `/admin`, `/profile`, and `/donor-analytics` to their SPA hash routes.
- Replaced developer-facing profile deletion API copy with user-facing Share and Log out controls in the profile details panel.
- Changed Verify Identity from hidden/dead UI to a friendly "Verification coming soon" notice backed by `/api/verify/status`.
- Added a reactive client-side confirmation for the "I'm already registered" action.
- Added same-origin CSRF protection for session/account/intent state changes: vote-intent POST, logout aliases, and account deletion now reject foreign `Origin`/`Referer`.
- Added a persistent logged-in homepage action panel so registration status and vote-plan actions stay visible even when an intent already exists.
- Standardized injected profile intent display to user-facing labels such as `Republican` instead of raw values such as `red`.
- Rewrote injected profile history entries into prose.
- Added Home, Share, and Log out actions to the profile header area.

## Follow-Up Production Checks Passed
- `/api/auth/login`: 200 with synthetic account.
- `/api/auth/logout`: 200 and cleared session.
- `/api/auth/signout`: 200 and cleared session.
- `/api/auth/me`, `/api/auth/session`, `/api/auth/user`, and `/api/me`: returned the signed-in synthetic user.
- `/api/intent/aggregate`: 200.
- `/admin`: 302 to `/#/admin`.
- `/profile`: 302 to `/#/profile`.
- Synthetic alias QA account was deleted after the test.
- Bad credentials on `/api/auth/login` return 401 with generic `Invalid email or password`.
- Foreign-origin `/api/intent`, `/api/auth/logout`, and `/api/account` state changes return 403.
- Same-origin `/api/intent`, `/api/auth/logout`, and `/api/account` state changes succeed.

## Not Fully Verified
- Admin analytics/export with the real `ADMIN_SECRET` was not tested because the secret was not available in the workspace.
- In-app browser automation was blocked by a local Node REPL startup issue; the live URL was opened in the system browser and public pages were smoke-checked by HTTP.
- A stats total of 1 remains after Codex cleanup. Direct D1 inspection showed it belongs to `rblake2320@me.com` with intent `red`, state `AL`, city `Montgomery`.

## Cleanup
- Removed synthetic QA account `codex-live-qa-1778829676@example.com`.
- Removed leftover synthetic QA account `codex-live-qa-1778829505@example.com`.
- Removed leftover synthetic CSRF QA accounts, including `codex-final-qa-1778831348@example.com` and `codex-csrf-qa-1778831259@example.com`.
- Production stats total after Codex cleanup: 1, belonging to Ron's account.
