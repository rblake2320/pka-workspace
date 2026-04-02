# FORGE — SENTINEL NO-GO Fixes Applied
Date: 2026-03-25

All 9 items addressed. Status per fix below.

---

## FIX 1 — CRITICAL: Security Headers
**Status: DONE**

Created `C:/Users/techai/aihangout-app/frontend/public/_headers` (new file — `public/` dir did not exist, created it).

Headers applied:
- Content-Security-Policy (default-src self, script-src self+unsafe-inline, fonts, img, connect-src to aihangout.ai and api.aihangout.ai)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security: max-age=31536000; includeSubDomains
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()

The `_headers` file is the Cloudflare Pages static header mechanism. It must be present in the `dist/` output after build. Because Vite copies from `frontend/public/` to `frontend/dist/` at build time, placing it in `public/` ensures it lands in `dist/` automatically.

**Risk note:** The `unsafe-inline` in `script-src` and `style-src` is necessary given the current React+Vite build does not use nonces. This is acceptable for now but should be tightened with CSP nonces in a future hardening pass.

---

## FIX 2 — HIGH: Remove Debug Route
**Status: DONE**

In `src/worker.js` line 8658, the `GET /api/debug/test-scrapers` handler now returns 404 immediately unless `env.ENVIRONMENT === 'development'`. The guard is the first statement in the handler body, before any scraper code runs.

---

## FIX 3 — HIGH: Persistent AI Agents Notice
**Status: DONE**

Added to `frontend/src/App.tsx` footer, inside a dedicated `<div>` below the existing copyright/links row:

```
This platform includes content posted by AI agents. All AI-generated posts are labeled.
```

Styled `text-xs text-gray-400` — unobtrusive but present on every page.

---

## FIX 4 — HIGH: Strip Bounty Coming-Soon Disclaimer
**Status: DONE**

Applied Option A (runtime sanitizer). Two locations in `src/worker.js`:

1. `GET /api/problems` (list route, ~line 1346): regex strips `--- **Bounty Program (Coming Soon):**` block from all returned descriptions before the JSON response is built.
2. `GET /api/problems/:id` (single problem route, ~line 1414): same sanitizer applied to the single problem object.

Pattern used: `/\s*---\s*\*\*Bounty Program \(Coming Soon\):\*\*.*?(?=---|$)/gs`

This is a runtime fix — no D1 mutation required, no downtime, catches all existing and future harvested content with this pattern.

---

## FIX 5 — MEDIUM: Category Normalization
**Status: DONE**

Three locations in `src/worker.js`:

1. `GET /api/problems` list route: `normalizeCategory()` applied to every returned problem's `category` field.
2. `GET /api/problems/:id` single route: `normalizeCategorySingle()` applied to the returned problem object.
3. `POST /api/problems` write path (~line 1594): `normalizeCategoryIngest()` computes `normalizedCategory` before the INSERT, and the `category` bind parameter was changed from `category.trim()` to `normalizedCategory.trim()`.

Normalization map: `ai-ml`, `ai_ml`, `aiml` → `AI/ML`. Other values pass through unchanged.

---

## FIX 6 — MEDIUM: /how-bounties-work Page
**Status: DONE**

Created `frontend/src/pages/HowBountiesWorkPage.tsx` with four sections:
- Posting a Bounty
- Earning a Bounty
- Disputes
- Problem Bank Values

Wired into `frontend/src/App.tsx`:
- Import added
- Route `<Route path="/how-bounties-work" element={<HowBountiesWorkPage />} />` added before the wildcard

---

## FIX 7 — LOW: Proper 404 Page
**Status: DONE**

Created `frontend/src/pages/NotFoundPage.tsx` — renders "404 / This page does not exist. / Back to home" link.

In `frontend/src/App.tsx`:
- `NotFoundPage` imported
- Wildcard route changed from `<Navigate to="/" />` to `<NotFoundPage />`

This means unknown routes now get a proper 404 page instead of a silent redirect to home — correct behavior for SEO and user experience.

---

## FIX 8 — LOW: Typo in TermsPage.tsx
**Status: DONE**

`frontend/src/pages/TermsPage.tsx` line 24: `font-semibent` corrected to `font-semibold`.

All 10 section headings in TermsPage now have consistent `font-semibold` styling.

---

## FIX 9 — AI Tooltip Misleading Copy
**Status: DONE**

`frontend/src/components/ProblemCard.tsx` line 142:

Changed:
> "Solutions are still human-validated."

To:
> "Solutions are community-reviewed."

This is accurate. Harvested problems sourced from GitHub Issues or Stack Overflow are not individually reviewed by a human before posting. "Community-reviewed" correctly describes the actual state.

---

## Deploy Command

```bash
cd C:/Users/techai/aihangout-app

# Build worker + frontend (copies public/_headers to dist/ automatically via Vite)
npm run build

# Deploy to production
npx wrangler deploy --env production
```

`npm run build` runs both `build:worker` (esbuild) and `build:frontend` (Vite). The `_headers` file placed in `frontend/public/` will be copied to `frontend/dist/` by Vite's static asset pipeline automatically.

Wrangler version confirmed: 4.62.0. Build command confirmed via `package.json`.

---

## Files Modified

- `C:/Users/techai/aihangout-app/frontend/public/_headers` — **CREATED**
- `C:/Users/techai/aihangout-app/src/worker.js` — FIX 2, 4, 5
- `C:/Users/techai/aihangout-app/frontend/src/App.tsx` — FIX 3, 6, 7
- `C:/Users/techai/aihangout-app/frontend/src/pages/HowBountiesWorkPage.tsx` — **CREATED** (FIX 6)
- `C:/Users/techai/aihangout-app/frontend/src/pages/NotFoundPage.tsx` — **CREATED** (FIX 7)
- `C:/Users/techai/aihangout-app/frontend/src/pages/TermsPage.tsx` — FIX 8
- `C:/Users/techai/aihangout-app/frontend/src/components/ProblemCard.tsx` — FIX 9

---

## Residual Risks

1. **CSP `unsafe-inline`** — Acceptable now but should be replaced with hash-based or nonce-based CSP in a future sprint. Requires Vite build changes.
2. **Bounty regex** — The regex targets the known exact format. If harvested content uses a slightly different heading format, it won't match. A broader cleanup pass on the D1 database (Option B) remains a valid follow-up to permanently remove the data.
3. **`_headers` in dist** — Vite copies all `public/` contents to `dist/` at build time. If a future build config change removes this behavior, the headers file would stop being deployed. Verify after first build.
4. **Category normalization** — The map only covers `ai-ml`/`ai_ml`/`aiml`. Other malformed categories (e.g. `webdev`, `web-dev`, `Web Dev`) would pass through unnormalized. A complete audit of category values in D1 is recommended.
