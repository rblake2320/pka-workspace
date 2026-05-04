# QuoteHub

Product folder for QuoteHub planning, build artifacts, implementation notes, and launch-readiness materials.

## Implementation

**Live at:** `C:\Users\techai\quotehub\`

```bash
cd C:\Users\techai\quotehub
npm run dev   # → http://localhost:5555
```

- **Hub App SPA:** http://localhost:5555/QuoteHub%20Hub%20App.html
- **API:** http://localhost:5555/api/v1
- **DB:** PostgreSQL 16 + pgvector on port 5433, db `quotehub`
- **Demo login:** `demo@quotehub.dev` / `Demo1234!`

16/17 endpoints passing. See `Owner's Inbox/QUOTEHUB-BUILD-COMPLETE.md` for full smoke test results.

## Current Contents

- `docs/QuoteHub Production Build Plan.md` — production build plan plus missing production-readiness checklist.

## Working Rule

Keep QuoteHub-specific documents and deliverables here instead of leaving them in Downloads or mixing them with unrelated PKA workspace artifacts.
