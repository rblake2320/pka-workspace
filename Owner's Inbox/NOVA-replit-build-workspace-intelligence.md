# NOVA Research Report: Replit Build Workspace — Implementation Intelligence
**Date**: 2026-03-29 | **Agent**: NOVA | **Feeds**: FORGE (Build Workspace embedded in Council platform)

---

## Objective

Identify the specific, implementable patterns from Replit's editor that FORGE should
replicate in the Monaco-based Build Workspace embedded in the AI Council debate platform
(Next.js). Seven concrete questions answered with source-backed findings.

---

## Key Findings (ranked by decision impact)

**Finding 1 — Console capture is not built-in — it must be injected into the iframe.**
Replit intercepts console output by overriding `console.log/warn/error/info` inside the
running iframe and routing them to the parent via `window.parent.postMessage()`. You cannot
read the iframe's console from the outside. The parent then renders a styled panel.
This is the #1 pattern difference from what most builders assume.

**Finding 2 — Replit uses a custom tree structure for pane layout, not a library.**
They wrote low-level mouse-event handlers on top of a multi-node tree (using Jotai state),
deliberately avoiding all third-party split-pane libraries for fine-grained control.
For FORGE, the right choice is `react-resizable-panels` (bvaughn) — the de-facto standard
used by shadcn/ui and widely deployed in Next.js. It handles SSR cookie persistence,
keyboard accessibility, and min/max constraints with minimal code.

**Finding 3 — AI code injection must use `executeEdits`, not `setValue`.**
`setValue` destroys the undo stack. `executeEdits` applies edits as single undo-able
operations with proper range tracking. For streaming AI code injection, the correct
pattern is: append chunks to the model via `executeEdits` as they arrive from the AI stream,
with decorations applied to highlight newly injected lines before the user accepts.

**Finding 4 — Replit's Shell tab is a real xterm.js terminal, not simulated.**
For a frontend-only (HTML/CSS/JS) project, the Shell shows a live bash shell but the
actual user code output (console.log) never appears there — it appears only in the
DevTools / Preview panel. The "Console" tab below the editor is the correct pattern
for frontend-only workspaces.

**Finding 5 — Replit's top 5 sticky features are: instant run, multiplayer editing,
integrated hosting, zero-setup environment, and now Agent 3 autonomous multi-file edit.**
The "zero-setup" factor dominates. For an embedded workspace inside Council, the analog
is: code runs instantly in the iframe, no save step, no deploy step, no config step.
Frictionless from edit to preview.

---

## Evidence and Answers Per Question

---

### Q1 — Replit's Top 5 Most-Used Sticky Features

Based on 2025 retrospective, user reviews, and comparative analysis:

**1. Zero-friction run** — No setup, no local install, code runs instantly in browser.
For an embedded workspace: auto-run on file change (or a single Run button) is the
equivalent. The instant feedback loop is the hook.

**2. Integrated live preview** — Webview is front and center, not buried. Replit moved
the Preview pane to replace the old "Progress" drawer in 2025 to eliminate the "where
is my output?" problem. Layout principle: preview is always visible alongside the editor,
never a second tab.

**3. Real-time multiplayer** — Not relevant for single-user Council workspace, but the
principle applies: changes to the editor are reflected immediately everywhere, including
the live preview. No manual refresh.

**4. AI agent (Agent 3 / Ghostwriter)** — In 2026 this is the primary value driver.
Agent 3 can work autonomously for up to 200 minutes, spawns subagents, tests its own
code, operates in Economy/Power/Turbo effort modes. For the Council workspace: the
AI agent is the Council's FORGE agent — it should be able to inject code directly
into the Monaco editor and show the diff before applying.

**5. Integrated hosting + database** — The workspace is not just an editor; you can
deploy with one click. For embedded workspace: the "Download merged HTML" button is
the analog — the frictionless export path.

**Sources**: [Replit 2025 in Review](https://blog.replit.com/2025-replit-in-review) |
[Replit Review 2026 - Hackceleration](https://hackceleration.com/replit-review/) |
[Taskade Review](https://www.taskade.com/blog/replit-review)

---

### Q2 — Console Output UX Pattern

**The pattern:**
1. The preview iframe loads user-written HTML/JS
2. Before the user code runs, a script block is injected at the top of the iframe's
   HTML that overrides `console.log`, `console.warn`, `console.error`, `console.info`
3. Each override calls the original method (so browser DevTools still works), then
   posts a structured message to the parent via `window.parent.postMessage()`
4. The parent listens for `message` events and appends styled rows to a Console panel

**Injection code to insert at top of iframe srcdoc:**
```javascript
// Injected before user code runs
['log', 'warn', 'error', 'info'].forEach(method => {
  const originalMethod = console[method];
  console[method] = function(...args) {
    originalMethod.apply(console, args);
    parent.postMessage(
      { type: 'console', level: method, message: args.join(' ') },
      window.location.origin
    );
  };
});

// Catch runtime errors
window.onerror = function(message, source, lineno, colno, error) {
  parent.postMessage(
    { type: 'console', level: 'error', message: `${message} (line ${lineno})` },
    window.location.origin
  );
};
```

**Parent listener:**
```javascript
window.addEventListener('message', (event) => {
  if (event.source !== iframeRef.current?.contentWindow) return;
  if (event.data?.type !== 'console') return;
  appendConsoleEntry(event.data.level, event.data.message);
});
```

**UX styling rule**: Color-code by level.
- `log` → `#E8E8F0` (normal text)
- `warn` → `#F5A623` (amber)
- `error` → `#F05A5A` (red), bold
- `info` → `#5BBCF7` (blue)

Replit also integrated native DevTools for HTML/CSS/JS repls in 2025 so users can
use browser DevTools inside the preview pane — but that is a native browser feature,
not something to build. The console panel pattern above is the lightweight correct
approach for an embedded workspace.

**Sources**: [CyberAngles iframe console capture](https://www.cyberangles.org/blog/capture-console-log-of-an-iframe/) |
[Replit DevTools blog](https://blog.replit.com/devtools) |
[Replit Console improvements](https://blog.replit.com/new-and-improved-console)

---

### Q3 — AI Agent Code Injection into Monaco: The Correct Pattern

**Answer: streaming line-by-line into the editor using `executeEdits`, not `setValue`,
with ghost-text decorations showing incoming changes before acceptance.**

**Three-phase pattern used by Replit Ghostwriter inline (confirmed from blog):**

**Phase 1 — Streaming to the editor:**
AI response tokens arrive from the server stream. As each chunk arrives, insert it
at the current cursor position or end of file using `executeEdits`. This gives the
effect of the AI "typing" into the editor in real time.

```javascript
// As each AI chunk arrives:
editor.executeEdits('ai-agent', [{
  range: new monaco.Range(
    model.getLineCount(),           // last line
    model.getLineMaxColumn(model.getLineCount()), // end of last line
    model.getLineCount(),
    model.getLineMaxColumn(model.getLineCount())
  ),
  text: incomingChunk,
  forceMoveMarkers: true
}]);
```

**Phase 2 — Ghost-text decoration during streaming:**
While AI is inserting, apply a decoration to the newly added lines so they appear
visually distinct (slightly dimmed, or colored background). This signals "this is
AI output, not your own code yet."

```javascript
// Apply decoration to AI-injected range
const decorations = editor.deltaDecorations([], [{
  range: aiInsertedRange,
  options: {
    className: 'ai-ghost-text',   // CSS: opacity 0.7, background: rgba(124,107,242,0.08)
    isWholeLine: true
  }
}]);
```

**Phase 3 — Accept/Reject diff view:**
After streaming completes, Replit shows a line-by-line diff view (original vs
AI-suggested). User accepts → decorations cleared, code committed. Reject → `undo()`
the entire `executeEdits` batch.

**Critical rule: never use `setValue` for AI injection.**
`setValue` destroys the undo stack. `pushEditOperations` preserves it but is more
complex. `executeEdits` is the correct middle ground — applies as a single undoable
operation, preserves history.

**For bulk replace (e.g., agent replaces an entire file):**
Use `executeEdits` with a range spanning the full document.
```javascript
const fullRange = model.getFullModelRange();
editor.executeEdits('ai-agent', [{ range: fullRange, text: newContent }]);
```

**Sources**:
[Replit Ghostwriter inline blog](https://blog.replit.com/ghostwriter-inline) |
[Monaco executeEdits discussion](https://github.com/microsoft/monaco-editor/discussions/4155) |
[FreeCodeCamp Replit clone tutorial](https://www.freecodecamp.org/news/how-to-build-a-replit-clone-with-socketio-monaco-editor-and-copilotkit/)

---

### Q4 — Monaco Inline Error Display: Best Open-Source Pattern

**The canonical pattern is `monaco.editor.setModelMarkers()` with `IMarkerData`.**
This is what every LSP-backed editor uses. It produces squiggly underlines with
hover tooltips — the same visual as VS Code.

**Full implementation:**
```javascript
// On content change, validate and set markers
model.onDidChangeContent(() => {
  const markers = validateCode(model.getValue());
  monaco.editor.setModelMarkers(model, 'runtime-errors', markers);
});

// Marker shape
const markers = [{
  startLineNumber: 3,
  startColumn: 1,
  endLineNumber: 3,
  endColumn: model.getLineLength(3) + 1,
  message: 'Uncaught ReferenceError: x is not defined',
  severity: monaco.MarkerSeverity.Error,  // Error | Warning | Info | Hint
  source: 'Runtime'
}];
```

**For runtime errors from the iframe** (since you can't statically analyze runtime
behavior), the pattern is:
1. Capture the error from `window.onerror` in the iframe (line number included)
2. postMessage it to the parent with `{ level: 'error', message, lineno }`
3. In the parent, call `setModelMarkers` with `startLineNumber: lineno` so the
   squiggle appears on the exact line that crashed

**Severity → squiggle color mapping (Monaco defaults):**
- `Error` → red squiggle
- `Warning` → yellow squiggle
- `Info` → blue squiggle
- `Hint` → green dots

**Clear markers on next successful run:**
```javascript
monaco.editor.setModelMarkers(model, 'runtime-errors', []);
```

**Best open-source reference**: `monaco-marker-data-provider` npm package provides
a cleaner API layer over the raw `setModelMarkers` for continuous validation.

**Sources**: [IMarkerData API reference](https://microsoft.github.io/monaco-editor/typedoc/interfaces/editor.IMarkerData.html) |
[StudyRaid Monaco inline errors](https://app.studyraid.com/en/read/15534/540334/displaying-inline-errors-and-warnings-in-monaco) |
[monaco-marker-data-provider npm](https://www.npmjs.com/package/monaco-marker-data-provider)

---

### Q5 — Resizable Panes: How Replit Does It and What FORGE Should Use

**What Replit built:**
Custom low-level mouse-event handlers on a multi-node tree (not any external library).
They used Jotai to hold drag state and deliberately suppress React re-renders during
drag for performance. They use conical sections (not just rectangular hit targets) for
drag handles to make dragging more ergonomic. The drag handle doubles as a tab handle —
dragging a tab drags the entire pane.

**What FORGE should use instead (right call for Next.js):**
`react-resizable-panels` by bvaughn — the library shadcn/ui ships as its resizable
primitive. It handles SSR layout persistence via cookies, keyboard accessibility
(arrow keys to resize), min/max pixel and percentage constraints, and `data-*` attributes
for CSS styling.

**Implementation for 3-column layout:**
```tsx
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';

<PanelGroup direction="horizontal" autoSaveId="build-workspace-layout">
  {/* File Tree */}
  <Panel defaultSize={15} minSize={10} maxSize={25}>
    <FileTree />
  </Panel>

  <PanelResizeHandle className="w-1 bg-[#1E2240] hover:bg-[#7C6BF2] cursor-col-resize transition-colors" />

  {/* Monaco Editor */}
  <Panel defaultSize={43} minSize={20}>
    <MonacoEditor />
  </Panel>

  <PanelResizeHandle className="w-1 bg-[#1E2240] hover:bg-[#7C6BF2] cursor-col-resize transition-colors" />

  {/* Live Preview */}
  <Panel defaultSize={42} minSize={15}>
    <LivePreview />
  </Panel>
</PanelGroup>
```

**Key details:**
- `autoSaveId` persists layout to localStorage automatically
- The drag handle is a 4px-wide div — 1px visible line, hover expands to 4px
  (use `::after` pseudo-element or padding trick)
- Hover state should flash the Council accent color (`#7C6BF2`) to signal
  the handle is draggable
- Double-click on handle: reset to default sizes (add `onDoubleClick` calling
  `panelRef.current.resize(defaultSize)`)

**Sources**: [Replit Splits blog](https://blog.replit.com/splits) |
[react-resizable-panels GitHub](https://github.com/bvaughn/react-resizable-panels) |
[shadcn Resizable](https://www.shadcn.io/ui/resizable)

---

### Q6 — Replit Shell Tab: Real Terminal or Simulated?

**Answer: real xterm.js terminal connected to a real Linux bash shell.**

Replit open-sourced their fork of xterm.js at `github.com/replit/xterm`. In 2025 they
shipped "Shell2" — a rewrite that is 200x faster and natively multiplayer. Each shell
tab is a persistent PTY process on the container.

**For frontend-only (HTML/CSS/JS) projects specifically:**
- The Shell tab shows a real bash shell for the project container
- Running the project (clicking Run) starts a static file server, not a node process
- `console.log` output does NOT appear in the Shell tab — it only appears in the
  Preview panel's DevTools or the Console panel
- The Shell is useful for: `npm install`, `git` commands, file inspection — not
  for watching frontend runtime output

**What to build for the Council workspace (frontend-only context):**

Do NOT build a fake terminal. Instead, build three distinct tabs below the editor:

| Tab | Contents | Implementation |
|-----|----------|----------------|
| **Console** | Runtime console.log / warn / error output from the iframe | postMessage pattern (Q2 above) |
| **Errors** | Parsed runtime errors with line numbers | Feeds Monaco setModelMarkers (Q4 above) |
| **Network** (optional) | Fetch/XHR calls made by the running code | PerformanceObserver or iframe override |

This is the correct UX for a frontend-only embedded workspace. A real xterm terminal
would be unused complexity.

**Sources**: [Replit Shell2 blog](https://blog.replit.com/shell2) |
[Replit Tabbed Shell](https://blog.replit.com/tabbed-shell) |
[Replit console-shell docs](https://docs.replit.com/replit-workspace/workspace-features/console-shell) |
[replit/xterm GitHub](https://github.com/replit/xterm)

---

### Q7 — CSS/Layout Patterns: Sidebar, Tabbar, Preview Panel

Replit's RUI design system uses CSS custom properties throughout, component-level
theming, and a utility library (`rcss`) for spacing and layout. The actual hex values
are not publicly documented, but the visual inspection pattern and community analysis
yield the following reference values.

**Replit dark theme (inspected from published screenshots and community themes):**

| Element | Approximate Color | CSS Variable Name (Replit internal) |
|---------|-------------------|-------------------------------------|
| Base background | `#0E1117` | `--background` |
| Panel/sidebar bg | `#141721` | `--background-higher` |
| Active tab bg | `#1C2030` | `--background-highest` |
| Border/divider | `#2A2F45` | `--outline-default` |
| Primary text | `#F0F0F0` | `--foreground-default` |
| Secondary text | `#8B93A8` | `--foreground-dimmer` |
| Primary accent | `#5865F2` (Replit uses a blue-violet) | `--primary-default` |

**Layout CSS patterns to match:**

**Sidebar (file tree):**
```css
.file-tree {
  background: var(--bg-surface);          /* #111320 */
  border-right: 1px solid var(--border-subtle); /* #1E2240 */
  overflow-y: auto;
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
}

.file-tree-item {
  padding: 4px 8px 4px 16px;
  cursor: pointer;
  border-radius: 4px;
  color: var(--text-secondary);
}

.file-tree-item:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.file-tree-item.active {
  background: rgba(124, 107, 242, 0.12);  /* accent glow */
  color: var(--accent-primary);
}
```

**Tab bar (file tabs above Monaco):**
```css
.tab-bar {
  display: flex;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  overflow-x: auto;
  scrollbar-width: none;        /* hide scrollbar */
  min-height: 36px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 14px;
  font-size: 12px;
  color: var(--text-secondary);
  border-right: 1px solid var(--border-subtle);
  cursor: pointer;
  white-space: nowrap;
  position: relative;
}

.tab.active {
  color: var(--text-primary);
  background: var(--bg-base);
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: var(--accent-primary);   /* #7C6BF2 — active tab indicator */
}

.tab .close-btn {
  opacity: 0;
  transition: opacity 0.15s;
}

.tab:hover .close-btn {
  opacity: 1;
}
```

**Preview panel header:**
```css
.preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  font-size: 12px;
  color: var(--text-secondary);
}

.preview-url-bar {
  flex: 1;
  background: var(--bg-base);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  color: var(--text-muted);
}
```

**Monaco editor background must match the workspace:**
```javascript
// In Monaco editor options:
monaco.editor.create(container, {
  theme: 'vs-dark',          // use as base then override
  fontSize: 14,
  fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  fontLigatures: true,
  lineHeight: 22,
  padding: { top: 12 },
  minimap: { enabled: false },          // Replit hides minimap by default
  scrollBeyondLastLine: false,
  renderLineHighlight: 'gutter',        // subtle line highlight
  overviewRulerLanes: 0,               // cleaner look without overview ruler marks
});

// Override Monaco theme to match workspace colors:
monaco.editor.defineTheme('council-dark', {
  base: 'vs-dark',
  inherit: true,
  rules: [],
  colors: {
    'editor.background': '#0B0D14',
    'editor.lineHighlightBackground': '#111320',
    'editorGutter.background': '#0B0D14',
    'editor.selectionBackground': '#2E3460',
    'editor.inactiveSelectionBackground': '#1E2240',
    'editorLineNumber.foreground': '#3D4166',
    'editorLineNumber.activeForeground': '#7C6BF2',
  }
});
monaco.editor.setTheme('council-dark');
```

**Sources**: [Replit RUI design system blog](https://blog.replit.com/rui-eng) |
[Replit themes docs](https://docs.replit.com/replit-workspace/replit-themes) |
[Replit dark mode blog](https://blog.replit.com/dark_mode) |
[@replit/ui npm package](https://www.npmjs.com/package/@replit/ui)

---

## Risks

1. **iframe postMessage origin restriction**: The console override pattern requires
   the iframe `srcdoc` to know the parent origin at inject time. In production (HTTPS),
   use `window.location.origin`. In local dev (localhost), this may differ. Use `*`
   only during development — never in production.

2. **Monaco `executeEdits` range math**: If the AI stream is inserting at the wrong
   range (e.g., off-by-one on line count), inserts will corrupt the document.
   Test with multi-line files immediately. The `model.getLineCount()` and
   `model.getLineMaxColumn(n)` calls must be fresh on each chunk insertion, not cached.

3. **`react-resizable-panels` v2 breaking changes**: The library had a major API change
   at v2. Shadcn/ui uses v2. Confirm version alignment before installing. The
   `autoSaveId` prop is v2-only.

4. **Replit's actual hex values are not publicly documented.** The colors in Q7 are
   synthesized from screenshots, community themes, and the published RUI system blog.
   They are directionally correct but not pixel-exact. Use them as a starting point
   and adjust against the Council's existing design tokens from the prior NOVA report
   (`#0B0D14` base, `#7C6BF2` accent).

5. **Shell tab complexity**: A real xterm.js terminal requires a backend process
   (PTY, websocket connection). For a frontend-only embedded workspace, this is wasted
   infrastructure. The Console tab pattern (Q2/Q6) delivers 90% of the value at 5%
   of the complexity.

---

## Recommendation

Single ranked answer: Build in this order.

1. **Console panel first** (Q2 pattern) — highest perceived-quality delta, easiest
   to ship. Inject the postMessage override into the iframe srcdoc, render a styled
   panel below the editor with color-coded log levels. 2-hour build.

2. **Resizable panels** (Q5 pattern) — swap the current fixed-width CSS to
   `react-resizable-panels` with `autoSaveId`. Users immediately notice when they
   can resize; they notice even more when the layout persists across sessions. 1-hour swap.

3. **Monaco theme + tab bar CSS** (Q7 pattern) — apply the `council-dark` theme and
   the tab bar CSS. Visual quality signal. 1-hour build.

4. **Runtime error squiggles** (Q4 pattern) — wire `window.onerror` in the iframe
   to `setModelMarkers` in Monaco. Shows errors on the exact line that crashed.
   3-hour build (includes testing edge cases).

5. **AI code injection** (Q3 pattern) — implement `executeEdits` streaming + diff
   decoration. This is the highest-complexity item — do it last, after the rest
   of the workspace foundation is solid.

Do NOT build a Shell tab for a frontend-only workspace. It is misdirected effort.

---

## Next Actions

1. **FORGE**: Implement the console postMessage pattern from Q2. Start with
   `srcdoc` injection — it is simpler than a separate iframe URL approach.
   Inject the 4-method override + `window.onerror` before the user's HTML runs.

2. **FORGE**: Swap to `react-resizable-panels` v2. Install `shadcn add resizable`
   if shadcn is already in the stack — it gives you the component pre-wired.

3. **FORGE**: Apply the `council-dark` Monaco theme (Q7 code block above).
   Copy-paste ready, no additional dependencies.

4. **FORGE**: When implementing AI injection, test `executeEdits` with a streaming
   fetch (`ReadableStream` from the Council AI API) — append chunks as they arrive.
   The undo-stack preservation is critical; validate it before shipping.

5. **NOVA (if needed)**: If FORGE wants the full postMessage security model
   (origin validation, message schema, event filtering), flag it — 20-minute
   follow-up spec.

---

*Sources summary:*
- [Replit 2025 in Review](https://blog.replit.com/2025-replit-in-review)
- [Replit Splits (pane layout)](https://blog.replit.com/splits)
- [Replit Ghostwriter inline](https://blog.replit.com/ghostwriter-inline)
- [Replit DevTools for HTML/CSS/JS](https://blog.replit.com/devtools)
- [Replit Console improvements](https://blog.replit.com/new-and-improved-console)
- [Replit Shell2](https://blog.replit.com/shell2)
- [Replit RUI design system](https://blog.replit.com/rui-eng)
- [CyberAngles iframe console capture](https://www.cyberangles.org/blog/capture-console-log-of-an-iframe/)
- [IMarkerData API reference](https://microsoft.github.io/monaco-editor/typedoc/interfaces/editor.IMarkerData.html)
- [monaco-marker-data-provider npm](https://www.npmjs.com/package/monaco-marker-data-provider)
- [react-resizable-panels GitHub](https://github.com/bvaughn/react-resizable-panels)
- [shadcn Resizable](https://www.shadcn.io/ui/resizable)
- [FreeCodeCamp Replit clone tutorial](https://www.freecodecamp.org/news/how-to-build-a-replit-clone-with-socketio-monaco-editor-and-copilotkit/)
- [replit/xterm GitHub](https://github.com/replit/xterm)
- [@replit/ui npm package](https://www.npmjs.com/package/@replit/ui)

*Deliverable: NOVA research complete. Handed to FORGE for Build Workspace implementation.*
