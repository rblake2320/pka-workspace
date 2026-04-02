# FORGE — Council Frontend Build Complete

**Delivered**: 2026-03-28
**Build status**: CLEAN — zero TypeScript errors, zero warnings
**Routes compiled**: 10/10

---

## Goal

Complete Next.js 15 frontend for the Council collaborative AI agent platform. Dark-only design system. Real-time debate view with SSE streaming. Digital twin support. Connects to FastAPI backend at localhost:8600.

---

## Architecture

```
/c/Users/techai/council/frontend/
├── app/
│   ├── globals.css              — Full design system (Council Violet #7C6BF2)
│   ├── layout.tsx               — Root layout: sidebar + topbar + toast + health poller
│   ├── page.tsx                 — Dashboard (stats, active councils, agent roster, health)
│   ├── agents/
│   │   ├── page.tsx             — Agent registry (All | PKA Team | Digital Twins | External tabs)
│   │   ├── new/page.tsx         — Create agent wizard (AI Agent vs Digital Twin modes)
│   │   └── [id]/page.tsx        — Agent detail (Overview | Memory | Twin Profile tabs)
│   ├── councils/
│   │   ├── page.tsx             — Council list with status filter tabs
│   │   ├── new/page.tsx         — 5-step council creation wizard
│   │   └── [id]/
│   │       ├── page.tsx         — LIVE DEBATE VIEW (three-panel, SSE streaming)
│   │       └── synthesis/page.tsx — Verdict card + position timeline
│   └── settings/page.tsx        — Models | API Keys | System tabs
├── components/
│   ├── ui/                      — 10 base components (button, badge, card, input,
│   │                              textarea, select, tabs, dialog, spinner, progress)
│   ├── agents/
│   │   ├── AgentAvatar.tsx      — Circular avatar with twin T-badge
│   │   └── AgentCard.tsx        — Debate panel card with thinking/speaking animations
│   ├── councils/
│   │   ├── MessageBubble.tsx    — Chat bubble with position badge, reply chain, CHANGED flash
│   │   ├── ThinkingIndicator.tsx — Scan-line + cycling phase text
│   │   ├── SynthesisPanel.tsx   — Always-visible right rail with live agreement meter
│   │   ├── PositionRail.tsx     — Round-by-round position timeline dots
│   │   └── VerdictCard.tsx      — Shareable synthesis output card
│   └── layout/
│       ├── Sidebar.tsx          — Desktop sticky + mobile overlay sidebar
│       ├── TopBar.tsx           — Mobile hamburger topbar
│       ├── ToastContainer.tsx   — Error/success toast stack (bottom-right)
│       └── HealthPoller.tsx     — 30s health polling, populates app store
└── lib/
    ├── types.ts                 — Full TypeScript types matching backend schemas exactly
    ├── api.ts                   — API client (fetch + envelope unwrap + APIError class)
    ├── sse.ts                   — SSE client (EventSource + exponential backoff reconnect)
    ├── stores.ts                — 3 Zustand stores: app, agents, council (live debate state)
    └── utils.ts                 — cn(), timeAgo, agentColor, positionColor, roleColor, etc.
```

---

## Implementation — What Was Built

### Design System
- Exact hex values as specified: `--bg-base: #0B0D14`, `--accent-primary: #7C6BF2`, all state colors
- Inter for UI chrome, JetBrains Mono for all agent names/labels
- Dark theme enforced globally — no media query, no toggle
- Custom keyframes: `pulse-violet`, `pulse-thinking`, `scan-line`, `flash-changed`, `fade-in`, `blink`

### Real-Time Debate View (`/councils/[id]`)
Three-panel layout:
- **Left (256px)**: Live agent roster. AgentCard animates per status: thinking = scan-line + blue pulse, speaking = violet pulse. Position badge updates per message. Position CHANGED flashes amber for 3s.
- **Center**: Message stream via SSE. MessageBubble supports reply chains, position badges, CHANGED callout (`[WAS: NO] → [NOW: CHANGED]`). ThinkingIndicator cycles "Reviewing prior positions... Evaluating evidence... Composing response...". Human input box at bottom (Enter sends, Shift+Enter newline).
- **Right (288px)**: SynthesisPanel always visible. Agreement level progress bar, per-agent positions, active disagreements pairs, provisional verdict if synthesis run, time compression display, Run Synthesis button.

### SSE Streaming (`lib/sse.ts`)
- Subscribes to `/api/councils/{id}/stream`
- Handles named event types: `message`, `typing`, `round_start`, `synthesis`, `status`
- Reconnect with exponential backoff (1s → 30s max)
- Auth via `?key=` query param in URL

### Zustand Stores (`lib/stores.ts`)
- `useAppStore`: API key (localStorage), health, sidebar state, toast queue
- `useAgentsStore`: agents list, selected agent
- `useCouncilStore`: active council, messages (deduped by ID), agent runtime states (status, position, positionChangedAt for flash), typing agents set, SSE connection state

### API Client (`lib/api.ts`)
- Base URL: NEXT_PUBLIC_API_URL, routed through Next.js rewrites in browser
- Unwraps `{ success, data }` envelope from backend automatically
- Throws `APIError(code, message, status)` on failures
- All functions: getAgents, createAgent, getAgent, updateAgent, deleteAgent, rotateAgentKey, getAgentMemory, getAgentStats, getCouncils, createCouncil, getCouncil, updateCouncil, getMessages, postMessage, runRound, pauseCouncil, resumeCouncil, endCouncil, synthesize, getSynthesis, getApiKeys, createApiKey, revokeApiKey, getHealth

### Digital Twin Support
- `agents/new/page.tsx`: Two-tab form — AI Agent mode (standard) vs Digital Twin mode (adds twin_of, authorization level radio, domain multiselect, twin_profile fields)
- `agents/[id]/page.tsx`: Twin Profile tab shows authorization scope visualized, accuracy score as Progress dial, expertise badges, non-negotiables list
- Agent cards show "T" badge overlay on avatar, twin_of field displayed

---

## Validation Method

### Start the stack
```bash
# Backend (from /c/Users/techai/council/backend)
pip install -e .
council  # starts FastAPI on :8600

# Frontend
cd /c/Users/techai/council/frontend
cp .env.local.example .env.local
npm run dev  # starts on :3000
```

### Validation checklist
1. **Build passes**: `npm run build` — confirmed 0 errors, 0 warnings (run 2026-03-28)
2. **Dashboard loads**: `http://localhost:3000` — stats row, health panel, agent list
3. **Create agent**: `/agents/new` → AI Agent tab → fill form → submit → key modal appears → navigates to agent detail
4. **Create twin**: `/agents/new` → Digital Twin tab → fill twin_of + domains → submit
5. **Create council**: `/councils/new` → 5-step wizard → selects agents → creates → redirects to live view
6. **Live debate**: `/councils/{id}` — three panels visible (desktop), SSE connects (WiFi icon green), Run Round triggers agent cards to animate thinking state
7. **Message send**: Type in input box → Enter → message appears in stream
8. **Synthesis**: Click Synthesize → right panel shows provisional verdict → `/councils/{id}/synthesis` shows VerdictCard with vote tally
9. **Mobile**: At `< 1024px` sidebar collapses, hamburger appears; at `< 1280px` synthesis rail hides
10. **Error handling**: Kill backend → toasts appear, no page crash, SSE reconnects when backend returns

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| SSE CORS on different port | Medium | Next.js rewrites proxy `/api/*` so browser stays same-origin; also backend has CORS middleware |
| Zustand hydration mismatch (SSR) | Low | All stores initialized client-side; `localStorage` access guarded with `typeof window !== 'undefined'` |
| Message deduplication on SSE reconnect | Low | `appendMessage` checks `if (s.messages.some((m) => m.id === msg.id)) return {}` |
| Agent runtime states lost on page refresh | Low | Page reload re-fetches messages and re-derives positions from message metadata |
| Tailwind v4 + CSS custom properties | Low | Tested — Tailwind v4's `@import "tailwindcss"` co-exists with CSS custom props cleanly |
| QueryClientProvider per-page | Note | Each page has its own `QueryClient` instance. Acceptable for this SPA pattern; promotes isolation |

---

## Deployment Notes

**Environment**:
```
NEXT_PUBLIC_API_URL=http://localhost:8600   # or VPS URL
NEXT_PUBLIC_WS_URL=ws://localhost:8600
```

**Dev**:
```bash
cd /c/Users/techai/council/frontend
npm run dev
```

**Production build**:
```bash
npm run build
npm start   # port 3000
```

**With backend running on Spark-1** (replace port/tunnel as needed):
```
NEXT_PUBLIC_API_URL=https://api.council.yourdomain.app
```

---

## Files Created/Modified

All files at `/c/Users/techai/council/frontend/`:

| File | Status |
|------|--------|
| `app/globals.css` | Replaced — full design system |
| `app/layout.tsx` | Replaced — new sidebar + toast + health |
| `app/page.tsx` | Replaced — dashboard |
| `app/agents/page.tsx` | Replaced — agent registry |
| `app/agents/new/page.tsx` | Created |
| `app/agents/[id]/page.tsx` | Created |
| `app/councils/page.tsx` | Replaced — council list |
| `app/councils/new/page.tsx` | Created |
| `app/councils/[id]/page.tsx` | Replaced — live debate view |
| `app/councils/[id]/synthesis/page.tsx` | Replaced — verdict |
| `app/settings/page.tsx` | Replaced — settings |
| `next.config.ts` | Updated — rewrites + turbopack root |
| `.env.local.example` | Created |
| `lib/types.ts` | Created |
| `lib/api.ts` | Created |
| `lib/sse.ts` | Created |
| `lib/stores.ts` | Created |
| `lib/utils.ts` | Created |
| `components/ui/button.tsx` | Created |
| `components/ui/badge.tsx` | Created |
| `components/ui/card.tsx` | Created |
| `components/ui/input.tsx` | Created |
| `components/ui/textarea.tsx` | Created |
| `components/ui/select.tsx` | Created |
| `components/ui/tabs.tsx` | Created |
| `components/ui/dialog.tsx` | Created |
| `components/ui/spinner.tsx` | Created |
| `components/ui/progress.tsx` | Created |
| `components/agents/AgentAvatar.tsx` | Created |
| `components/agents/AgentCard.tsx` | Created |
| `components/councils/MessageBubble.tsx` | Created |
| `components/councils/ThinkingIndicator.tsx` | Created |
| `components/councils/SynthesisPanel.tsx` | Created |
| `components/councils/PositionRail.tsx` | Created |
| `components/councils/VerdictCard.tsx` | Created |
| `components/layout/Sidebar.tsx` | Created |
| `components/layout/TopBar.tsx` | Created |
| `components/layout/ToastContainer.tsx` | Created |
| `components/layout/HealthPoller.tsx` | Created |
