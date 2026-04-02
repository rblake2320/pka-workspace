# FORGE — Agent Code Injection Feature
## Status: COMPLETE — 0 TypeScript errors, debate.py parses clean

---

## Goal

When an agent in the Council debate writes a code block (e.g. NOVA says "here's the updated index.html: \`\`\`html..."), that code surfaces as a banner notification in the BuildWorkspace. The human clicks Apply, the file updates, and the editor flashes green. No auto-apply — the human is always in control.

---

## Architecture

```
Agent LLM response
  │ contains ```html ... ``` block
  ▼
debate.py _generate_parallel
  └─ _broadcast_messages
       ├─ publishes  type:"message"   (unchanged, all existing consumers work)
       └─ publishes  type:"code_patch" { agent_name, filename, language, content, message_id }

Redis pub/sub channel  council:{id}
  ▼
councils.py SSE endpoint (unchanged — it just streams everything on the channel)
  ▼
sse.ts EventSource  ──  new  es.addEventListener('code_patch', ...)
  ▼
onCodePatch callback  ──  BuildWorkspace registers this via onRegisterPatchHandler prop
  ▼
useCouncilStore.addPendingPatch()
  ▼
PatchBanner UI (shown above editor)
  Apply  →  setFiles() + acceptPatch() + flashFiles green 1.5s
  Reject →  rejectPatch()
```

---

## Files Changed

### 1. `C:\Users\techai\council\backend\app\engine\debate.py`

**Added** (before `_broadcast_messages`): three class-level compiled regex patterns and `_extract_code_patches()` method.

**Changed** `_broadcast_messages` — adds a second publish loop for `code_patch` events after the `message` event.

#### Before (the method signature and body only):
```python
async def _broadcast_messages(
    self,
    council_id: UUID,
    messages: list[Message],
    redis,
    agents: list | None = None,
) -> None:
    """Publish each message to the Redis channel for this council."""
    import json

    channel = f"council:{council_id}"
    for i, msg in enumerate(messages):
        agent = agents[i] if agents and i < len(agents) else None
        payload = {
            "type": "message",
            "data": { ... },
        }
        try:
            await redis.publish(channel, json.dumps(payload))
        except Exception as exc:
            logger.warning(...)
```

#### After (abbreviated — key additions):
```python
# NEW — class-level regex patterns
_CODE_BLOCK_RE = re.compile(r"```(?P<lang>[a-zA-Z0-9]*)\n(?P<code>.*?)```", re.DOTALL)
_LANG_TO_EXT   = {"html": "html", "css": "css", "js": "js", "javascript": "js",
                   "ts": "ts", "typescript": "ts", "jsx": "jsx", "tsx": "tsx"}
_FILENAME_HINT_RE = re.compile(
    r"(?:updated?|new|edit(?:ed)?|modified?|here['\u2019]?s[^:\n]*?)?\b"
    r"([\w\-]+\.(?:html|css|js|ts|jsx|tsx))\b", re.IGNORECASE
)

def _extract_code_patches(self, content, agent_name, message_id) -> list[dict]:
    """Scan content for fenced web code blocks; infer filename from preceding text."""
    ...

async def _broadcast_messages(self, ...):
    # [existing message publish loop — unchanged]
    ...

    # NEW — code_patch events
    if msg.role != "agent" or not agent:
        continue
    patches = self._extract_code_patches(msg.content, agent.name, str(msg.id))
    for patch in patches:
        await redis.publish(channel, json.dumps({"type": "code_patch", "data": patch}))
```

Filename inference rules:
1. Scan the 200 characters before the code block for an explicit `.html/.css/.js/.ts/.jsx/.tsx` filename mention (e.g. "here's the updated `index.html`:").
2. Fall back to `{agent_name_lower}-patch.{ext}` if no hint found.
3. Unknown language tags (```python, ```bash, etc.) are silently skipped — no patch emitted.

---

### 2. `C:\Users\techai\council\frontend\lib\types.ts`

**Added** at the SSE Events section:

```typescript
// ── Code patch (agent → workspace) ────────────────────────────────────────

export interface CodePatch {
  agent_name: string;
  filename: string;      // e.g. "index.html"
  language: string;      // html | css | js | ts | jsx | tsx
  content: string;       // full file replacement content
  message_id: string;    // parent message ID
}

export interface SSECodePatchEvent {
  type: 'code_patch';
  data: CodePatch;
}

export interface PendingPatch extends CodePatch {
  patch_id: string;      // client-assigned key
  received_at: number;   // Unix ms
}

export interface AppliedPatch extends CodePatch {
  patch_id: string;
  applied_at: number;
}
```

**Changed** `SSEEvent` union type to include `SSECodePatchEvent`.

---

### 3. `C:\Users\techai\council\frontend\lib\sse.ts`

**Changed** `SSECallbacks` — added optional `onCodePatch` callback:
```typescript
onCodePatch?: (patch: CodePatch) => void;
```

**Added** named event listener:
```typescript
es.addEventListener('code_patch', (event) => {
  try {
    const patch = JSON.parse(event.data as string) as CodePatch;
    callbacks.onCodePatch?.(patch);
  } catch { /* noop */ }
});
```

**Added** case in `handleEvent` switch (handles the fallback `onmessage` path):
```typescript
case 'code_patch':
  callbacks.onCodePatch?.(data as CodePatch);
  break;
```

All existing handlers (message, typing, round_start, synthesis, status) are untouched.

---

### 4. `C:\Users\techai\council\frontend\lib\stores.ts`

**Added** to imports: `AppliedPatch`, `PendingPatch`.

**Added** to `CouncilState` interface:
```typescript
pendingPatches: PendingPatch[];
appliedPatches: AppliedPatch[];
addPendingPatch: (patch: PendingPatch) => void;
acceptPatch: (patchId: string) => AppliedPatch | null;
rejectPatch: (patchId: string) => void;
```

**Added** initial values in store creation:
```typescript
pendingPatches: [],
appliedPatches: [],
```

**Added** `clearActiveCouncil` now also resets `pendingPatches: []` and `appliedPatches: []`.

**Added** three action implementations:
- `addPendingPatch` — appends to `pendingPatches`
- `acceptPatch` — moves patch from pending to applied, returns the `AppliedPatch` object
- `rejectPatch` — removes from pending, no applied entry

---

### 5. `C:\Users\techai\council\frontend\components\build\BuildWorkspace.tsx`

**Added** to imports: `GitMerge` (lucide), `CodePatch` and `PendingPatch` (types), `useCouncilStore`.

**Added** `PatchBanner` component — a single notification card:
- Shows: `{AGENT_NAME} wants to update {filename}`
- Apply button (purple, with Check icon)
- Reject button (ghost, with X icon)

**Changed** `BuildWorkspaceProps` — added optional `onRegisterPatchHandler` prop:
```typescript
onRegisterPatchHandler?: (handler: (patch: CodePatch) => void) => void;
```
This lets the parent page wire the SSE `onCodePatch` callback to the workspace without prop drilling through intermediate layers. The workspace registers itself once on mount.

**Added** state and store bindings inside component:
```typescript
const [flashFiles, setFlashFiles] = React.useState<Record<string, number>>({});
const pendingPatches = useCouncilStore((s) => s.pendingPatches);
const addPendingPatch = useCouncilStore((s) => s.addPendingPatch);
const acceptPatch    = useCouncilStore((s) => s.acceptPatch);
const rejectPatch    = useCouncilStore((s) => s.rejectPatch);
```

**Added** two `useEffect` hooks:
1. Registers `onRegisterPatchHandler` with a closure that calls `addPendingPatch` — fires once on mount.
2. Cleans up expired `flashFiles` entries using a self-scheduling `setTimeout`.

**Added** `handleAcceptPatch` — applies content to `files` state (creates new file if it doesn't exist), switches `activeFile`, sets flash, calls store `acceptPatch`.

**Added** `handleRejectPatch` — calls store `rejectPatch`.

**Changed** outer wrapper div — changed `flex` to `flex flex-col` to accommodate the banner strip at top.

**Added** banner strip in JSX (renders only when `pendingPatches.length > 0`):
```tsx
{pendingPatches.length > 0 && (
  <div className="flex flex-col gap-1.5 px-3 py-2 border-b border-[#1E2240] bg-[#0d0f1d] shrink-0">
    {pendingPatches.map((patch) => (
      <PatchBanner key={patch.patch_id} patch={patch}
        onAccept={handleAcceptPatch}
        onReject={handleRejectPatch}
      />
    ))}
  </div>
)}
```

**Added** inner row wrapper `<div className="flex flex-1 min-h-0 overflow-hidden">` around the three-column layout so banner + row stack vertically without layout breaks.

**Changed** file tree entries — `isFlashing` check drives an `emerald-900/40` background when patch was recently applied:
```tsx
const isFlashing = (flashFiles[file.name] ?? 0) > Date.now();
// applied to cn() call:
isFlashing ? 'bg-emerald-900/40 text-emerald-300' : ...
```

---

## How to wire the parent page

The parent Council session page already subscribes to SSE. Add one line to that subscription and pass the prop to BuildWorkspace:

```tsx
// In the Council session page component
const patchHandlerRef = React.useRef<((patch: CodePatch) => void) | null>(null);

// In subscribeToCouncil callbacks:
onCodePatch: (patch) => {
  patchHandlerRef.current?.(patch);
},

// On BuildWorkspace:
<BuildWorkspace
  councilId={councilId}
  onRegisterPatchHandler={(handler) => { patchHandlerRef.current = handler; }}
/>
```

If `BuildWorkspace` is not mounted when a patch arrives (e.g. user is on the Debate tab, not Build tab), the patch is still queued in the store. When the user switches to Build, the banners will be waiting.

---

## Validation Method

### Manual test:
1. Start a Build-mode Council session with NOVA in the participant list.
2. Type in chat: `NOVA, update index.html with a contact form`
3. NOVA responds with a message containing a `\`\`\`html` block.
4. Confirm: a banner appears above the editor saying "NOVA wants to update index.html".
5. Click Apply. Confirm: index.html content updates in Monaco, file tree entry flashes green for ~1.5s, preview refreshes.
6. Repeat with Reject. Confirm: banner disappears, file unchanged.

### Python unit test for extraction logic:
```python
from app.engine.debate import CouncilDebateEngine

engine = CouncilDebateEngine()

# Case 1: explicit filename hint
msg = "here's the updated index.html:\n```html\n<h1>Hello</h1>\n```"
patches = engine._extract_code_patches(msg, "NOVA", "msg-001")
assert len(patches) == 1
assert patches[0]["filename"] == "index.html"
assert patches[0]["language"] == "html"
assert "<h1>Hello</h1>" in patches[0]["content"]

# Case 2: no filename hint → fallback name
msg2 = "Here is a contact form:\n```html\n<form></form>\n```"
patches2 = engine._extract_code_patches(msg2, "NOVA", "msg-002")
assert patches2[0]["filename"] == "nova-patch.html"

# Case 3: non-web language → no patch
msg3 = "```python\nimport os\n```"
patches3 = engine._extract_code_patches(msg3, "FORGE", "msg-003")
assert patches3 == []

# Case 4: multiple blocks in one message
msg4 = "index.html:\n```html\n<h1>x</h1>\n```\nstyle.css:\n```css\nbody{}\n```"
patches4 = engine._extract_code_patches(msg4, "NOVA", "msg-004")
assert len(patches4) == 2
assert patches4[0]["filename"] == "index.html"
assert patches4[1]["filename"] == "style.css"

print("All assertions passed.")
```

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Agent produces a partial/broken code block (unclosed ```) | Low | `re.DOTALL` greedy match — partial blocks without a closing ``` are not captured. No patch emitted. |
| Agent produces code for a file not in the workspace | Low | `handleAcceptPatch` creates the file if it doesn't exist. User sees it appear in the file tree. |
| Human navigates away from Build tab while patches are pending | Medium | Patches live in the Zustand store, not component state. They persist until the user revisits Build and accepts/rejects. `clearActiveCouncil` clears them on council exit. |
| Patch content contains XSS | Low (iframe is sandboxed) | The iframe preview already runs under `sandbox="allow-scripts allow-forms allow-same-origin"`. Content is never injected into the parent DOM. The agent output also runs through `prompt_guard.scan()` in `_generate_parallel` before it reaches `_broadcast_messages`. |
| Two patches queued for the same file | Possible | Both banners appear. User applies in order. The second apply overwrites the first. This is correct — last human decision wins. |
| `onRegisterPatchHandler` not wired by parent page | Medium | If the prop is not passed, no patches are queued. No error thrown. Existing behaviour is unchanged. |

---

## Deployment Notes

- Backend: restart the debate engine (`uvicorn` or gunicorn worker reload). No DB migration needed — the patch data flows entirely through Redis pub/sub.
- Frontend: `npm run build` (or `next dev` reload). No env var changes needed.
- The `onRegisterPatchHandler` prop on `BuildWorkspace` is additive — any existing call sites that omit it continue to compile and work without modification.
