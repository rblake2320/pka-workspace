// editor.jsx — the per-step editor (the core working surface)

const { Screenshot, SCR_W, SCR_H } = window.AGSOP_SCR;

function StepRow({ step, idx, total, active, onClick, onToggle, onMoveUp, onMoveDown, density }) {
  const isCompact = density === "compact";
  const padY = isCompact ? "6px" : "10px";
  const isFallback = step.kind === "tn3270";
  const displayName = step.name || step.auto_text || (step.ocr_text ? `Click on "${step.ocr_text}" in ${step.window_title}` : "(unnamed step)");

  return (
    <div
      className={`step-row ${active ? "active" : ""} ${!step.enabled ? "disabled" : ""}`}
      onClick={onClick}
      style={{ padding: `${padY} 12px` }}
    >
      <div className="step-row-handle" title="Drag to reorder (visual only)">⋮⋮</div>
      <div className="step-row-seq">{String(step.seq).padStart(2, "0")}</div>
      <div className="step-row-body">
        <div className="step-row-name">{displayName}</div>
        <div className="step-row-meta">
          <span className="mono">{step.timestamp}</span>
          <span className="dot">·</span>
          {isFallback ? (
            <span className="badge badge-fallback">TN3270 · OCR</span>
          ) : (
            <span className="badge badge-uia">UIA · {step.control_type}</span>
          )}
          {step.sensitive && <span className="badge badge-redact">SENSITIVE</span>}
          {step.redactions.length > 0 && <span className="badge badge-redact">{step.redactions.length} redaction{step.redactions.length > 1 ? "s" : ""}</span>}
        </div>
      </div>
      <div className="step-row-actions" onClick={(e) => e.stopPropagation()}>
        <button className="iconbtn" title="Move up" disabled={idx === 0} onClick={onMoveUp}>↑</button>
        <button className="iconbtn" title="Move down" disabled={idx === total - 1} onClick={onMoveDown}>↓</button>
        <button
          className={`iconbtn ${step.enabled ? "" : "off"}`}
          title={step.enabled ? "Disable step" : "Enable step"}
          onClick={onToggle}
        >{step.enabled ? "●" : "○"}</button>
      </div>
    </div>
  );
}

function StepList({ steps, activeIdx, setActiveIdx, onUpdate, density }) {
  const enabledCount = steps.filter(s => s.enabled).length;
  const totalCount = steps.length;
  return (
    <div className="step-list">
      <div className="step-list-header">
        <div>
          <div className="step-list-title">Steps</div>
          <div className="step-list-sub mono">{enabledCount}/{totalCount} included · drag to reorder</div>
        </div>
      </div>
      <div className="step-list-scroll">
        {steps.map((s, i) => (
          <StepRow
            key={s.id}
            step={s}
            idx={i}
            total={steps.length}
            active={i === activeIdx}
            density={density}
            onClick={() => setActiveIdx(i)}
            onToggle={() => onUpdate(i, { enabled: !s.enabled })}
            onMoveUp={() => onUpdate(null, { _move: { from: i, to: i - 1 } })}
            onMoveDown={() => onUpdate(null, { _move: { from: i, to: i + 1 } })}
          />
        ))}
      </div>
    </div>
  );
}

// ── Canvas with drag-redaction ─────────────────────────────────────────────

function Canvas({ step, onAddRedaction, onRemoveRedaction, showClick, accent }) {
  const wrapRef = React.useRef(null);
  const [drawing, setDrawing] = React.useState(null); // {x, y, w, h} in normalized coords
  const [hoverIdx, setHoverIdx] = React.useState(-1);

  const getNorm = (e) => {
    const r = wrapRef.current.getBoundingClientRect();
    return {
      x: Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)),
      y: Math.max(0, Math.min(1, (e.clientY - r.top) / r.height)),
    };
  };

  const onDown = (e) => {
    if (e.button !== 0) return;
    const p = getNorm(e);
    setDrawing({ x: p.x, y: p.y, w: 0, h: 0, sx: p.x, sy: p.y });

    const move = (ev) => {
      const q = getNorm(ev);
      const x = Math.min(p.x, q.x);
      const y = Math.min(p.y, q.y);
      const w = Math.abs(q.x - p.x);
      const h = Math.abs(q.y - p.y);
      setDrawing({ x, y, w, h, sx: p.x, sy: p.y });
    };
    const up = (ev) => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
      const q = getNorm(ev);
      const x = Math.min(p.x, q.x);
      const y = Math.min(p.y, q.y);
      const w = Math.abs(q.x - p.x);
      const h = Math.abs(q.y - p.y);
      setDrawing(null);
      if (w > 0.01 && h > 0.01) {
        onAddRedaction({ x, y, w, h, label: "" });
      }
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  };

  return (
    <div className="canvas-outer">
      <div className="canvas-toolbar">
        <div className="canvas-tool-group">
          <span className="mono dim">CANVAS</span>
          <span className="kbd">DRAG</span>
          <span className="dim">to redact</span>
        </div>
        <div className="canvas-tool-group">
          <span className="mono dim">{SCR_W}×{SCR_H}</span>
          <span className="dot">·</span>
          <span className="mono dim">{step.window_class || "—"}</span>
        </div>
      </div>
      <div className="canvas-frame">
        <div
          ref={wrapRef}
          className="canvas-wrap"
          onPointerDown={onDown}
          style={{ cursor: "crosshair" }}
        >
          <Screenshot step={step} redactions={step.redactions} showClick={showClick} />
          {/* live drag rectangle */}
          {drawing && (drawing.w > 0.005 || drawing.h > 0.005) && (
            <div
              className="redact-live"
              style={{
                left: `${drawing.x * 100}%`,
                top: `${drawing.y * 100}%`,
                width: `${drawing.w * 100}%`,
                height: `${drawing.h * 100}%`,
                borderColor: accent,
              }}
            >
              <span className="redact-live-tag mono" style={{ background: accent }}>
                {(drawing.w * SCR_W).toFixed(0)}×{(drawing.h * SCR_H).toFixed(0)}
              </span>
            </div>
          )}
          {/* hover overlays for existing redactions to enable removal */}
          {step.redactions.map((r, i) => (
            <div
              key={i}
              className={`redact-overlay ${hoverIdx === i ? "hover" : ""}`}
              style={{
                left: `${r.x * 100}%`,
                top: `${r.y * 100}%`,
                width: `${r.w * 100}%`,
                height: `${r.h * 100}%`,
              }}
              onPointerEnter={() => setHoverIdx(i)}
              onPointerLeave={() => setHoverIdx(-1)}
              onClick={(e) => { e.stopPropagation(); onRemoveRedaction(i); }}
              onPointerDown={(e) => e.stopPropagation()}
              title="Click to remove redaction"
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// ── TN3270 fallback side-by-side ───────────────────────────────────────────

function FallbackPanel({ step }) {
  if (step.kind !== "tn3270") return null;
  const cr = step.context_region;
  return (
    <div className="fallback-panel">
      <div className="fallback-header">
        <span className="badge badge-fallback">TN3270 FALLBACK</span>
        <span className="dim mono">UIA returned empty · capturing context region + OCR</span>
      </div>
      <div className="fallback-grid">
        <div className="fallback-col">
          <div className="fallback-col-label mono">CONTEXT REGION · {cr.w}×{cr.h}px @ ({cr.x},{cr.y})</div>
          <div className="fallback-region-frame">
            <svg viewBox={`${cr.x} ${cr.y} ${cr.w} ${cr.h}`} preserveAspectRatio="xMidYMid meet" style={{ width: "100%", display: "block", background: "#000" }}>
              <Screenshot step={step} redactions={[]} showClick={true} />
            </svg>
          </div>
        </div>
        <div className="fallback-col">
          <div className="fallback-col-label mono">OCR EXTRACTION</div>
          <div className="fallback-ocr">
            <div className="fallback-ocr-text mono">{step.ocr_text || "(none)"}</div>
            <div className="fallback-ocr-meta mono">
              <div><span className="dim">engine:</span> tesseract 5.3.3 (offline)</div>
              <div><span className="dim">conf:</span> 92.4%</div>
              <div><span className="dim">window:</span> {step.window_title}</div>
              <div><span className="dim">class:</span> {step.window_class}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Inspector ──────────────────────────────────────────────────────────────

function Inspector({ step, onChange, savingState }) {
  const [localName, setLocalName] = React.useState(step.name || step.auto_text || "");
  const [localUser, setLocalUser] = React.useState(step.user_text || "");

  React.useEffect(() => {
    setLocalName(step.name || step.auto_text || "");
    setLocalUser(step.user_text || "");
  }, [step.id]);

  // debounced commit
  const commitName = React.useCallback((v) => {
    onChange({ name: v });
  }, [onChange]);
  const commitUser = React.useCallback((v) => {
    onChange({ user_text: v });
  }, [onChange]);

  return (
    <div className="inspector">
      <div className="inspector-header">
        <div className="inspector-title">Step {step.seq}</div>
        <div className={`save-indicator save-${savingState}`}>
          <span className="save-dot" />
          {savingState === "saving" ? "saving…" : savingState === "saved" ? "saved" : "auto-save"}
        </div>
      </div>

      <div className="ins-field">
        <label className="ins-label">Step text <span className="dim">— shown in exports</span></label>
        <input
          className="ins-input"
          value={localName}
          placeholder={step.auto_text || "(auto-generated)"}
          onChange={(e) => { setLocalName(e.target.value); commitName(e.target.value); }}
        />
        {!localName && step.auto_text && (
          <div className="ins-hint mono">auto: {step.auto_text}</div>
        )}
      </div>

      <div className="ins-field">
        <label className="ins-label">SME notes <span className="dim">— optional, appears below the step</span></label>
        <textarea
          className="ins-textarea"
          value={localUser}
          rows={3}
          placeholder="e.g. Confirm the entry. The system will assign a control number."
          onChange={(e) => { setLocalUser(e.target.value); commitUser(e.target.value); }}
        />
      </div>

      <div className="ins-grid">
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">WINDOW</div>
          <div className="ins-cell-value">{step.window_title}</div>
        </div>
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">CLASS</div>
          <div className="ins-cell-value mono">{step.window_class}</div>
        </div>
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">AUTOMATION ID</div>
          <div className="ins-cell-value mono">{step.automation_id || "— (fallback)"}</div>
        </div>
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">CONTROL</div>
          <div className="ins-cell-value mono">{step.control_type || "— (fallback)"}</div>
        </div>
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">CLICK</div>
          <div className="ins-cell-value mono">({step.click.x}, {step.click.y})</div>
        </div>
        <div className="ins-cell">
          <div className="ins-cell-label mono dim">TIME</div>
          <div className="ins-cell-value mono">{step.timestamp}</div>
        </div>
      </div>

      {step.redactions.length > 0 && (
        <div className="ins-field">
          <label className="ins-label">Redactions <span className="dim">— click on canvas to remove</span></label>
          <div className="ins-redactions">
            {step.redactions.map((r, i) => (
              <div key={i} className="ins-redaction-row">
                <span className="badge badge-redact">REDACTED</span>
                <span className="mono dim">
                  {(r.x * SCR_W).toFixed(0)},{(r.y * SCR_H).toFixed(0)} · {(r.w * SCR_W).toFixed(0)}×{(r.h * SCR_H).toFixed(0)}
                </span>
                {r.label && <span className="mono">{r.label}</span>}
                <button
                  className="iconbtn"
                  onClick={() => onChange({ _removeRedaction: i })}
                  title="Remove"
                >×</button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

window.AGSOP_EDITOR = { StepList, Canvas, FallbackPanel, Inspector };
