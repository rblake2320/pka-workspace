# NOVA — Resizable Panels Research: Replit-Style Layout
**Date**: 2026-03-29
**For**: Ron (build decision: package vs. scratch)

---

## 1. Objective

Determine the best implementation path for a 3-column + 2-row Replit-style resizable panel layout in Next.js/React — specifically whether `react-resizable-panels` is worth adding or whether a scratch implementation is smarter.

---

## 2. Key Findings (ranked by decision impact)

### Finding 1 — `react-resizable-panels` is the clear winner. Install it.

- **Bundle**: 53 KB minified / **13.9 KB gzipped** (measured directly from v4.8.0 tarball). For context, that is smaller than a single optimized PNG icon. In a Next.js app bundle budget this is negligible.
- **Zero runtime dependencies** — confirmed from npm metadata (`deps: none`). Only peer dep is React itself.
- **5.1k GitHub stars**, maintained by Brian Vaughn (formerly on the React core team). Published yesterday (v4.8.0). Actively maintained, 196 versions published.
- **shadcn/ui ships it** as its `Resizable` primitive — that is the strongest signal of production-readiness in the React ecosystem today.

### Finding 2 — CSS-only `resize: horizontal` does NOT work for this layout

The CSS-only trick (`resize: horizontal` on a grid child) works for a single two-pane split where the user grabs a corner handle. It breaks down for:
- Multi-panel layouts (3 columns + nested 2 rows)
- Pixel-constrained min/max enforcement
- Keyboard accessibility
- The resize handle is the browser's native corner gripper — not a center-line drag handle

This approach is disqualified for your use case. Do not pursue it.

### Finding 3 — Monaco Editor requires one explicit call on resize; `automaticLayout: true` is a footgun

Monaco's `automaticLayout: true` uses a 100ms `setInterval` polling the container — it works unreliably with JS-driven resizes and degrades performance. The correct pattern:

```tsx
// In your panel's onResize callback:
editorRef.current?.layout()
```

`react-resizable-panels` exposes `onResize` on each `Panel`. Wire it directly. No `automaticLayout` needed.

### Finding 4 — Pointer event capture with Monaco is a real problem; `react-resizable-panels` solves it correctly

Monaco creates an overlay iframe/canvas that captures all pointer events. Pure-scratch implementations using `document.addEventListener('mousemove')` work, but they must be on `document` (not the panel element) to survive Monaco's capture. `react-resizable-panels` already does this correctly — it attaches to `document` and uses `pointermove` + `setPointerCapture`, which beats Monaco's event capture model. A scratch implementation has a high probability of producing a "drag stops when cursor enters Monaco" bug unless you implement the same pattern.

### Finding 5 — Pure-React scratch implementation is viable but ~100 lines of non-trivial state

The pattern is:

```tsx
const startDrag = (e: React.PointerEvent, index: number) => {
  e.currentTarget.setPointerCapture(e.pointerId) // KEY: beats Monaco
  const startX = e.clientX
  const startWidth = panelWidths[index]

  const onMove = (ev: PointerEvent) => {
    const delta = ev.clientX - startX
    setPanelWidths(w => clamp(w[index] + delta, min, max))
  }
  const onUp = () => {
    document.removeEventListener('pointermove', onMove)
    document.removeEventListener('pointerup', onUp)
  }
  document.addEventListener('pointermove', onMove)
  document.addEventListener('pointerup', onUp)
}
```

Issues you will have to solve yourself: keyboard accessibility (arrow keys on handles, WAI-ARIA `role="separator"`), collapse/expand, layout persistence, touch support, and the Monaco layout() call integration. All of this is already solved in `react-resizable-panels`.

### Finding 6 — `@radix-ui/react-separator` is not relevant here

It is a pure visual/semantic `<hr>` analog with `role="separator"` ARIA. It has no drag interaction, no resize behavior, no state. It is the wrong tool entirely.

### Finding 7 — Replit-style layout in `react-resizable-panels` maps directly to your spec

```tsx
<PanelGroup direction="horizontal">

  {/* Column 1: File Tree */}
  <Panel defaultSize={14} minSize={10} maxSize={25}>
    <FileTree />
  </Panel>
  <PanelResizeHandle />

  {/* Column 2: Editor + Console (nested vertical group) */}
  <Panel minSize={25}>
    <PanelGroup direction="vertical">
      <Panel minSize={20}>  {/* Editor */}
        <MonacoEditor onResize={() => editorRef.current?.layout()} />
      </Panel>
      <PanelResizeHandle />
      <Panel defaultSize={20} minSize={10} maxSize={50}>  {/* Console */}
        <Console />
      </Panel>
    </PanelGroup>
  </Panel>
  <PanelResizeHandle />

  {/* Column 3: Live Preview */}
  <Panel defaultSize={42} minSize={22}>
    <Preview />
  </Panel>

</PanelGroup>
```

Note: `react-resizable-panels` v2+ uses **percentage-based sizes** by default. Your px specs (min 120px, default 176px, etc.) need to be converted to percentages relative to total container width, OR you use the `minSizePixels` prop added in recent versions. At 1920px viewport: 176px ≈ 9%, 120px ≈ 6%, 300px ≈ 16%, 280px ≈ 15%.

---

## 3. Evidence

| Claim | Source / Basis |
|-------|----------------|
| 13.9 KB gzipped | Measured directly: `gzip -c react-resizable-panels.js` on v4.8.0 dist |
| 53 KB minified | Measured: `wc -c` on dist file |
| Zero dependencies | `npm show react-resizable-panels`: `deps: none` |
| 5.1k GitHub stars | GitHub repo — confirmed |
| shadcn/ui uses it | shadcn.io/docs/components/resizable — confirmed |
| Monaco automaticLayout polling issue | microsoft/monaco-editor issue #2057 |
| Pointer capture fix pattern | `setPointerCapture` MDN + GitHub issues on scratch implementations |
| CSS resize limitation | MDN resize property, jhey tweet demo — corner-only, no center-line drag |
| `@radix-ui/react-separator` is visual-only | Radix UI docs — confirmed |
| Keyboard accessibility (WAI-ARIA) | react-resizable-panels README — role="separator", arrow key support |

Sources rated HIGH confidence. All primary sources checked.

---

## 4. Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Percentage-based sizes make pixel constraints awkward | Medium | Use `minSizePixels` prop (added ~v2.1) or compute % from ResizeObserver on container |
| Monaco layout() not called on resize | Medium | Wire `onResize` on the editor Panel explicitly; do not rely on `automaticLayout` |
| v4.x API breaking change vs older tutorials | Low | Official docs at react-resizable-panels.vercel.app reflect current API; changelog is detailed |
| Bundle size regression | Negligible | 13.9 KB gzip is below any reasonable threshold |
| Drag-into-Monaco pointer event swallow | Low | Library uses `setPointerCapture` which wins; only at-risk if building scratch |

---

## 5. Recommendation

**Install `react-resizable-panels`. Do not build from scratch.**

Rationale:
1. 13.9 KB gzip is zero budget concern.
2. The library already solves the two hardest problems for this specific layout: Monaco pointer event capture and keyboard accessibility (WAI-ARIA `role="separator"` + arrow key resize).
3. Scratch implementation to match the feature parity (keyboard, touch, collapse, layout persistence) would be 200-400 lines of non-trivial code that CRUCIBLE would need to test exhaustively.
4. Brian Vaughn's authorship + shadcn/ui adoption = highest-trust signal in the React component ecosystem.

If bundle budget were severely constrained (< 5 KB budget) or the layout were a simple 2-pane split with no accessibility requirement, a scratch implementation would be justified. Neither condition is true here.

---

## 6. Next Actions

1. `npm install react-resizable-panels` — zero setup beyond this.
2. Convert your px specs to percentages OR use `minSizePixels` prop for the min constraints.
3. On the Monaco Panel, add `onResize={() => editorRef.current?.layout()}` and disable `automaticLayout`.
4. Style the `<PanelResizeHandle>` as a 4px wide drag bar — it renders a `<div>` you fully control with CSS (headless).
5. Optional: add `collapsible` to the File Tree panel for Replit-style collapse-to-zero behavior.
6. Hand to CRUCIBLE for drag + keyboard + Monaco resize regression test before shipping.
