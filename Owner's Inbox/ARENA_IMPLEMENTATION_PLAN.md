# Arena Platform -- Production Implementation Plan

Goal: Replace the broken Replit prototype with a fully functional civic debate
platform. Backend on Express+SQLite, frontend on React+Vite, JWT auth,
all 10 broken items fixed, deployed on Replit with production build.

Trigger: Ron's request to rebuild Arena from prototype evaluation.

Success Criterion: All 10 evaluated defects resolved. App serves from Express
(not Vite dev server). Auth works. Every button does something real. Races
show distinct data. Strategy page is admin-only. Deployed on Replit.

Target directory: `C:\Users\techai\arena-platform\`

---

## Parallel Execution Map

Three FORGE agents can work simultaneously on Workstreams A, B, and C.
Workstream D (integration + deploy) depends on all three completing.

```
Time -->
                                                          
FORGE-A: [Database + Auth API] -------->|
FORGE-B: [Core API Routes] ----------->|---> FORGE-D: [Integration + Deploy]
FORGE-C: [Frontend Rebuild] ---------->|
```

---

## Workstream A: Database Schema + Auth System

**Owner:** FORGE-A
**Output:** `server/db/schema.sql`, `server/db/seed.sql`, `server/auth.js`,
`server/middleware/auth.js`
**Definition of Done:** Database initializes with seed data. Register/login
endpoints return valid JWTs. Auth middleware rejects invalid tokens.

### A1. Database Schema

File: `server/db/schema.sql`

All tables use INTEGER PRIMARY KEY (SQLite auto-increment). Timestamps are
TEXT in ISO-8601 format (SQLite has no native datetime).

```sql
-- Users & Auth
CREATE TABLE users (
  id            INTEGER PRIMARY KEY,
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  display_name  TEXT NOT NULL,
  role          TEXT NOT NULL DEFAULT 'voter',  -- voter | campaign | admin
  is_verified   INTEGER NOT NULL DEFAULT 0,     -- voter verification status
  avatar_url    TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Races
CREATE TABLE races (
  id            INTEGER PRIMARY KEY,
  title         TEXT NOT NULL,           -- "Alabama Senate Race 2026"
  state         TEXT NOT NULL,           -- "AL"
  office        TEXT NOT NULL,           -- "Senate" | "House" | "Governor"
  district      TEXT,                    -- null for statewide
  status        TEXT NOT NULL DEFAULT 'active',  -- active | completed | upcoming
  election_date TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Candidates (one per party per race)
CREATE TABLE candidates (
  id            INTEGER PRIMARY KEY,
  race_id       INTEGER NOT NULL REFERENCES races(id),
  user_id       INTEGER REFERENCES users(id),  -- nullable until campaign claims
  name          TEXT NOT NULL,
  party         TEXT NOT NULL,           -- "Democrat" | "Republican" | "Independent"
  photo_url     TEXT,
  bio           TEXT,
  responsiveness_index REAL NOT NULL DEFAULT 100.0,  -- 0-100, drops on unanswered challenges
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Ads
CREATE TABLE ads (
  id            INTEGER PRIMARY KEY,
  race_id       INTEGER NOT NULL REFERENCES races(id),
  candidate_id  INTEGER NOT NULL REFERENCES candidates(id),
  title         TEXT NOT NULL,
  description   TEXT,
  video_url     TEXT,                    -- YouTube/Vimeo URL
  thumbnail_url TEXT,
  platform      TEXT NOT NULL DEFAULT 'arena',  -- arena | tv | digital | radio
  spend_cents   INTEGER NOT NULL DEFAULT 0,     -- track in cents to avoid float
  status        TEXT NOT NULL DEFAULT 'active',
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Rebuttals (linked to a specific ad)
CREATE TABLE rebuttals (
  id            INTEGER PRIMARY KEY,
  ad_id         INTEGER NOT NULL REFERENCES ads(id),
  candidate_id  INTEGER NOT NULL REFERENCES candidates(id),  -- the opponent responding
  title         TEXT NOT NULL,
  description   TEXT,
  video_url     TEXT,
  thumbnail_url TEXT,
  spend_cents   INTEGER NOT NULL DEFAULT 0,
  status        TEXT NOT NULL DEFAULT 'active',
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Verdicts (one per user per ad)
CREATE TABLE verdicts (
  id            INTEGER PRIMARY KEY,
  ad_id         INTEGER NOT NULL REFERENCES ads(id),
  user_id       INTEGER NOT NULL REFERENCES users(id),
  choice        TEXT NOT NULL,           -- 'ad' | 'rebuttal'
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(ad_id, user_id)                -- one vote per user per ad
);

-- Challenges
CREATE TABLE challenges (
  id            INTEGER PRIMARY KEY,
  race_id       INTEGER NOT NULL REFERENCES races(id),
  challenger_id INTEGER NOT NULL REFERENCES candidates(id),
  target_id     INTEGER NOT NULL REFERENCES candidates(id),
  title         TEXT NOT NULL,
  description   TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'open',  -- open | answered | expired
  response_text TEXT,
  responded_at  TEXT,
  expires_at    TEXT NOT NULL,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Charity Pool (phase 1: simple ledger)
CREATE TABLE charity_pool (
  id            INTEGER PRIMARY KEY,
  race_id       INTEGER NOT NULL REFERENCES races(id),
  contributor_type TEXT NOT NULL,        -- 'ad_fee' | 'rebuttal_fee' | 'donation'
  amount_cents  INTEGER NOT NULL,
  description   TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Notifications
CREATE TABLE notifications (
  id            INTEGER PRIMARY KEY,
  user_id       INTEGER NOT NULL REFERENCES users(id),
  type          TEXT NOT NULL,           -- 'challenge' | 'verdict' | 'rebuttal' | 'system'
  title         TEXT NOT NULL,
  body          TEXT,
  is_read       INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- User settings (key-value per user)
CREATE TABLE user_settings (
  id            INTEGER PRIMARY KEY,
  user_id       INTEGER NOT NULL REFERENCES users(id),
  setting_key   TEXT NOT NULL,
  setting_value TEXT NOT NULL,
  UNIQUE(user_id, setting_key)
);
```

### A2. Seed Data

File: `server/db/seed.sql`

Three distinct races with different states, candidates, ads, rebuttals, and
challenges. This directly fixes defect #2 (all races showing identical data).

```
Race 1: Alabama Senate — Doug Jones (D) vs Katie Britt (R)
Race 2: Georgia Governor — Stacey Abrams (D) vs Brian Kemp (R)
Race 3: Pennsylvania House District 7 — Susan Wild (D) vs Lisa Scheller (R)

Each race gets:
- 2 candidates
- 3-4 ads per candidate (with distinct YouTube URLs)
- 1-2 rebuttals
- 1 open challenge, 1 answered challenge
- Sample verdicts (to show percentage splits)
- Charity pool entries

1 admin user: admin@arena.app / Arena2026!
1 verified voter: jane@arena.app / Voter2026!
1 campaign user: campaign@arena.app / Campaign2026!
```

### A3. Database Initialization

File: `server/db/init.js`

```javascript
// Uses better-sqlite3
// On startup: if arena.db does not exist, run schema.sql then seed.sql
// Exports: db instance (singleton)
// Functions: getDb()
```

### A4. Auth Routes + Middleware

File: `server/routes/auth.js`

| Method | Path | Body | Response | Auth |
|--------|------|------|----------|------|
| POST | /api/auth/register | {email, password, displayName} | {token, user} | No |
| POST | /api/auth/login | {email, password} | {token, user} | No |
| GET | /api/auth/me | -- | {user} | Yes |
| PUT | /api/auth/me | {displayName, avatarUrl} | {user} | Yes |

File: `server/middleware/auth.js`

```
// Exports: requireAuth, optionalAuth, requireRole(role)
// requireAuth: reads Authorization: Bearer <token>, verifies JWT, attaches req.user
// requireRole('admin'): checks req.user.role === 'admin', 403 otherwise
// optionalAuth: same as requireAuth but does not 403 if missing
```

JWT secret: from `process.env.JWT_SECRET` or fallback to random generated on
first run (stored in arena.db pragma or .env).

Password hashing: bcrypt with 10 rounds.

---

## Workstream B: Core API Routes

**Owner:** FORGE-B
**Depends on:** A1 schema definition (shared as spec, not runtime dependency --
FORGE-B can code against the schema doc while FORGE-A builds it)
**Output:** `server/routes/races.js`, `server/routes/ads.js`,
`server/routes/verdicts.js`, `server/routes/challenges.js`,
`server/routes/analytics.js`, `server/routes/settings.js`,
`server/routes/notifications.js`, `server/routes/charity.js`
**Definition of Done:** All routes return correct JSON. Postman/curl tests pass
for every endpoint.

### B1. Races API

File: `server/routes/races.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/races | [{id, title, state, office, status, candidateCount}] | No |
| GET | /api/races/:id | {race, candidates[], ads[], challenges[], charityTotal} | No |
| POST | /api/races | {race} | admin |
| PUT | /api/races/:id | {race} | admin |

### B2. Ads + Rebuttals API

File: `server/routes/ads.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/races/:raceId/ads | [{ad, rebuttals[], verdictSummary}] | No |
| GET | /api/ads/:id | {ad, rebuttals[], verdictSummary} | No |
| POST | /api/races/:raceId/ads | {ad} | campaign |
| POST | /api/ads/:adId/rebuttals | {rebuttal} | campaign |

`verdictSummary` shape: `{adVotes: 45, rebuttalVotes: 55, totalVotes: 100}`

### B3. Verdicts API

File: `server/routes/verdicts.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| POST | /api/ads/:adId/verdict | {verdict} | verified voter |
| GET | /api/ads/:adId/verdicts | {adVotes, rebuttalVotes, total, userVote?} | optionalAuth |

Constraint: only users with `is_verified = 1` can cast verdicts.
One vote per user per ad (upsert on UNIQUE constraint).

### B4. Challenges API

File: `server/routes/challenges.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/races/:raceId/challenges | [{challenge, challenger, target}] | No |
| POST | /api/races/:raceId/challenges | {challenge} | campaign |
| PUT | /api/challenges/:id/respond | {challenge} | campaign (target only) |

When a challenge expires unanswered (checked on read via `expires_at`):
- Set status = 'expired'
- Reduce target candidate's `responsiveness_index` by 5 points

### B5. Analytics API

File: `server/routes/analytics.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/races/:raceId/analytics | {totalSpend, spendByCandidate, spendByPlatform, verdictTrends} | No |
| GET | /api/analytics/overview | {totalRaces, totalAds, totalSpend, totalVerdicts} | No |

All computed from ads/rebuttals/verdicts tables. No separate analytics store.

### B6. Strategy API (admin-only)

File: `server/routes/strategy.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/strategy/landscape | {races with full competitive data} | admin |

This fixes defect #10 (strategy page publicly accessible).

### B7. User Settings API

File: `server/routes/settings.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/settings | {settings object} | Yes |
| PUT | /api/settings | {settings object} | Yes |

Settings stored as key-value pairs. Frontend sends/receives flat object like:
`{emailNotifications: true, theme: 'dark', language: 'en'}`

### B8. Notifications API

File: `server/routes/notifications.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/notifications | [{notification}] | Yes |
| PUT | /api/notifications/:id/read | {notification} | Yes |
| PUT | /api/notifications/read-all | {count} | Yes |

### B9. Charity Pool API

File: `server/routes/charity.js`

| Method | Path | Response | Auth |
|--------|------|----------|------|
| GET | /api/races/:raceId/charity | {total, entries[]} | No |

---

## Workstream C: Frontend Rebuild

**Owner:** FORGE-C
**Depends on:** API contract from B (shared as spec -- FORGE-C codes against
the route table while FORGE-B builds the endpoints)
**Output:** All files under `client/src/`
**Definition of Done:** All pages render with real data from API. Auth flow
works. All buttons trigger API calls. No hardcoded data remains.

### C1. Project Structure

```
client/
  src/
    main.jsx
    App.jsx
    api/
      client.js          -- axios instance with JWT interceptor
      auth.js            -- register, login, getMe
      races.js           -- getRaces, getRace
      ads.js             -- getAds, createAd, createRebuttal
      verdicts.js        -- castVerdict, getVerdicts
      challenges.js      -- getChallenges, createChallenge, respondToChallenge
      analytics.js       -- getRaceAnalytics, getOverview
      settings.js        -- getSettings, updateSettings
      notifications.js   -- getNotifications, markRead
      charity.js         -- getCharityPool
    context/
      AuthContext.jsx     -- provides {user, token, login, logout, register}
    hooks/
      useAuth.js
      useRaces.js
      useAds.js
      useNotifications.js
    pages/
      HomePage.jsx        -- race listing
      RacePage.jsx        -- single race with tabs (Ads, Challenges, Charity, Analytics)
      LoginPage.jsx       -- login form
      RegisterPage.jsx    -- register form
      MyArenaPage.jsx     -- user's verdicts, watched races (fixes defect #9)
      SettingsPage.jsx    -- profile, verification, notifications (fixes defect #8)
      StrategyPage.jsx    -- admin-only with auth gate (fixes defect #10)
      NotFoundPage.jsx    -- 404
    components/
      Layout.jsx          -- nav bar, search, user menu
      ProtectedRoute.jsx  -- redirects to /login if not authed
      AdminRoute.jsx      -- redirects if not admin
      RaceCard.jsx        -- card for race listing
      AdCard.jsx          -- ad with video player + rebuttal side-by-side
      VideoPlayer.jsx     -- react-player wrapper (fixes defect #6)
      VerdictBar.jsx      -- percentage bar with "Convincing" buttons (fixes defect #5)
      ChallengeCard.jsx   -- challenge display + respond button
      SearchBar.jsx       -- filters races by title/state (fixes defect #7)
      CharityPool.jsx     -- charity tab content
      AnalyticsPanel.jsx  -- spend charts
    utils/
      formatCurrency.js
      formatDate.js
  index.html
  vite.config.js
  tailwind.config.js
```

### C2. API Client

File: `client/src/api/client.js`

```javascript
// axios instance
// baseURL: '/api' (relative -- works in dev proxy and production)
// Request interceptor: attach Authorization header from localStorage token
// Response interceptor: on 401, clear token and redirect to /login
```

### C3. Auth Context

File: `client/src/context/AuthContext.jsx`

```
// On mount: check localStorage for token, call GET /api/auth/me
// Provides: { user, token, isLoading, login(email, pw), register(email, pw, name), logout() }
// login/register: call API, store token in localStorage, set user state
// logout: clear localStorage, set user null
```

### C4. Routing

File: `client/src/App.jsx`

```
/                   -> HomePage (public)
/login              -> LoginPage (public)
/register           -> RegisterPage (public)
/race/:id           -> RacePage (public)
/my-arena           -> MyArenaPage (ProtectedRoute)
/settings           -> SettingsPage (ProtectedRoute)
/strategy           -> StrategyPage (AdminRoute)
*                   -> NotFoundPage
```

React Router v6. No more /race/1, /race/2, /race/3 hardcoded routes --
dynamic `:id` parameter fetches from API. Fixes defect #2.

### C5. Key Component Behaviors

**AdCard.jsx** -- Fixes defects #5 and #6
- Renders ad video via react-player (YouTube/Vimeo URL)
- If rebuttal exists, renders side-by-side (ad left, rebuttal right)
- "Convincing" button on each side calls POST /api/ads/:adId/verdict
- VerdictBar shows live percentage split
- "Buy Rebuttal Slot" button opens modal -> POST /api/ads/:adId/rebuttals

**ChallengeCard.jsx** -- Fixes defect #5
- "Issue Challenge" button -> POST /api/races/:raceId/challenges
- "Respond" button (visible to target candidate) -> PUT /api/challenges/:id/respond
- Shows countdown to expiry
- Shows responsiveness_index impact

**SearchBar.jsx** -- Fixes defect #7
- Client-side filter on race list by title and state
- Debounced input, no API call needed (race list is small)

**SettingsPage.jsx** -- Fixes defect #8
- Loads GET /api/settings on mount
- Saves PUT /api/settings on change
- Shows voter verification status from user object
- Notification preference toggles

**MyArenaPage.jsx** -- Fixes defect #9
- Shows user's cast verdicts with links to the ads
- Shows races the user has interacted with

### C6. Search Implementation

The SearchBar in the Layout component filters the race list. Since we expect
<100 races initially, this is client-side filtering on the HomePage. The
search bar in the nav triggers navigation to `/` with a query param
`?q=search+term` that HomePage reads.

---

## Workstream D: Integration, Build Config, and Deploy

**Owner:** FORGE-D (or any FORGE agent after A+B+C complete)
**Depends on:** Workstreams A, B, C all complete
**Output:** `server/index.js`, `vite.config.js` (production), `.replit`,
`replit.nix`, `package.json` (root)
**Definition of Done:** `npm run build && npm start` serves the full app.
Health endpoint returns 200. All pages load. Replit deploy works.

### D1. Express Server Entry Point

File: `server/index.js`

```javascript
// 1. Initialize database (run schema + seed if first run)
// 2. Express app
// 3. Middleware: express.json(), cors (dev only), helmet
// 4. Mount routes:
//    /api/auth      -> auth.js
//    /api/races     -> races.js
//    /api/ads       -> ads.js  (also handles /api/races/:raceId/ads)
//    /api/challenges -> challenges.js
//    /api/analytics -> analytics.js
//    /api/strategy  -> strategy.js
//    /api/settings  -> settings.js
//    /api/notifications -> notifications.js
//    /api/charity   -> charity.js
// 5. Health endpoint: GET /api/health -> {status: 'ok', timestamp, version}
// 6. Static serving: express.static('client/dist')
// 7. SPA fallback: all non-/api routes serve index.html
// 8. Listen on process.env.PORT || 3000
```

This fixes defect #1 (no more Vite dev server in production) and
defect #4 (/api returns JSON, not HTML).

### D2. Vite Config (Production)

File: `client/vite.config.js`

```javascript
export default defineConfig({
  root: 'client',
  build: {
    outDir: 'dist',       // outputs to client/dist/
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://localhost:3000'  // dev only
    }
  }
})
```

### D3. Package.json (Root)

File: `package.json`

```json
{
  "name": "arena-platform",
  "version": "1.0.0",
  "scripts": {
    "dev:server": "node --watch server/index.js",
    "dev:client": "cd client && npx vite",
    "dev": "concurrently \"npm run dev:server\" \"npm run dev:client\"",
    "build": "cd client && npx vite build",
    "start": "node server/index.js",
    "seed": "node server/db/seed-runner.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "better-sqlite3": "^9.4.3",
    "jsonwebtoken": "^9.0.2",
    "bcrypt": "^5.1.1",
    "helmet": "^7.1.0",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
```

Client package.json (separate):
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "react-player": "^2.14.1",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.12",
    "tailwindcss": "^3.4.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33"
  }
}
```

### D4. Replit Config

File: `.replit`
```toml
run = "npm start"
entrypoint = "server/index.js"

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "npm run build && npm start"]
deploymentTarget = "cloudrun"

[[ports]]
localPort = 3000
externalPort = 80
```

File: `replit.nix`
```nix
{ pkgs }: {
  deps = [
    pkgs.nodejs-20_x
    pkgs.nodePackages.npm
  ];
}
```

### D5. Environment Variables (Replit Secrets)

```
JWT_SECRET=<generate 64-char random string>
NODE_ENV=production
PORT=3000
```

---

## Defect Resolution Map

| # | Defect | Fix Location | Workstream |
|---|--------|-------------|------------|
| 1 | Dev server exposed publicly | D1: Express serves static build | D |
| 2 | All races show same data | A2: distinct seed data + C4: dynamic routing | A + C |
| 3 | No auth, hardcoded user | A4: JWT auth + C3: AuthContext | A + C |
| 4 | /api returns HTML | D1: API routes mounted before SPA fallback | D |
| 5 | Dead buttons | C5: all buttons wired to API calls | C |
| 6 | Videos don't play | C5: react-player with real URLs | C |
| 7 | Search does nothing | C6: client-side filter | C |
| 8 | Settings don't persist | B7 + C5: settings API + SettingsPage | B + C |
| 9 | /my-arena 404s | C4 + C5: MyArenaPage route + component | C |
| 10 | Strategy publicly accessible | B6 + C4: admin-only API + AdminRoute | B + C |

---

## File Inventory (Complete)

```
arena-platform/
  package.json
  .replit
  replit.nix
  .env.example
  server/
    index.js
    db/
      schema.sql
      seed.sql
      init.js
      seed-runner.js
    middleware/
      auth.js
    routes/
      auth.js
      races.js
      ads.js
      verdicts.js
      challenges.js
      analytics.js
      strategy.js
      settings.js
      notifications.js
      charity.js
  client/
    package.json
    index.html
    vite.config.js
    tailwind.config.js
    postcss.config.js
    src/
      main.jsx
      App.jsx
      index.css
      api/
        client.js
        auth.js
        races.js
        ads.js
        verdicts.js
        challenges.js
        analytics.js
        settings.js
        notifications.js
        charity.js
      context/
        AuthContext.jsx
      hooks/
        useAuth.js
        useRaces.js
        useAds.js
        useNotifications.js
      pages/
        HomePage.jsx
        RacePage.jsx
        LoginPage.jsx
        RegisterPage.jsx
        MyArenaPage.jsx
        SettingsPage.jsx
        StrategyPage.jsx
        NotFoundPage.jsx
      components/
        Layout.jsx
        ProtectedRoute.jsx
        AdminRoute.jsx
        RaceCard.jsx
        AdCard.jsx
        VideoPlayer.jsx
        VerdictBar.jsx
        ChallengeCard.jsx
        SearchBar.jsx
        CharityPool.jsx
        AnalyticsPanel.jsx
      utils/
        formatCurrency.js
        formatDate.js

Total: ~50 files
```

---

## Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| better-sqlite3 native build fails on Replit | Low | Replit Nix has build tools; fallback to sql.js (pure WASM) if needed |
| bcrypt native build fails on Replit | Medium | Fallback to bcryptjs (pure JS, slightly slower, same API) |
| Seed data YouTube URLs go stale | Low | Use well-known political ad URLs; if dead, react-player shows placeholder |
| Vite proxy config conflicts with Express in dev | Low | Standard pattern; dev:server on 3000, dev:client on 5173 with proxy |
| Concurrent FORGE agents produce incompatible interfaces | Medium | This doc IS the contract; all agents code against these exact route specs and response shapes |

---

## Dependencies (Explicit)

- FORGE-A and FORGE-B can start simultaneously. FORGE-B codes against the
  schema spec in this document (section A1), not against FORGE-A's runtime output.
- FORGE-C can start simultaneously. FORGE-C codes against the API route specs
  in this document (sections B1-B9), not against FORGE-B's runtime output.
- FORGE-D cannot start until A, B, and C are complete. FORGE-D wires the
  pieces together, resolves any interface mismatches, and validates the
  production build.
- CRUCIBLE testing begins after FORGE-D completes integration.

---

## Agent Assignment Summary

| Step | Agent | Task | Depends On | Definition of Done |
|------|-------|------|------------|-------------------|
| 1 | FORGE-A | Database schema, seed data, auth routes, auth middleware | -- | DB initializes, auth endpoints return valid JWTs |
| 2 | FORGE-B | All core API routes (races, ads, verdicts, challenges, analytics, settings, notifications, charity, strategy) | Schema spec (this doc) | All routes return correct JSON per spec |
| 3 | FORGE-C | Frontend rebuild: routing, auth context, all pages, all components, API client layer | API spec (this doc) | All pages render, all buttons fire API calls, no hardcoded data |
| 4 | FORGE-D | Express entry point, Vite build config, Replit config, integration testing | Steps 1-3 complete | `npm run build && npm start` serves full app, health endpoint 200 |
| 5 | CRUCIBLE | Full test pass: all 10 defects verified resolved, auth flow, data integrity, admin gate | Step 4 complete | Test report with GO/NO-GO verdict |
| 6 | SENTINEL | Security audit: JWT validation, SQL injection, XSS, admin route protection | Step 5 GO | Security sign-off |

---

## Definition of Done (Overall)

The Arena platform is done when:

1. `npm run build && npm start` on Replit serves the app on port 3000
2. Three races load with distinct data (different states, candidates, ads)
3. User can register, login, and logout
4. Verified voters can cast verdicts; percentage bars update
5. Campaign users can post ads, rebuttals, and challenges
6. Search filters races by name/state
7. Settings persist across sessions
8. /my-arena shows user's activity
9. /strategy is accessible only to admin users
10. /api/health returns JSON `{status: 'ok'}`
11. No Vite dev server in production
12. CRUCIBLE test report: all 10 original defects resolved
13. SENTINEL security audit: no critical findings
