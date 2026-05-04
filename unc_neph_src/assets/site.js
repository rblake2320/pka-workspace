// Unc & Neph — shared site JS: reveal-on-scroll, tweaks panel, theme persistence

(function () {
  const DEFAULTS = /*EDITMODE-BEGIN*/{
    "theme": "dark",
    "accent": "mint",
    "tagline": "Build the vibe. Ship the vision.",
    "heroVariant": "collage",
    "showTerminal": true,
    "showSpline": true
  }/*EDITMODE-END*/;

  const ACCENTS = {
    mint:   { '--accent': '#7cf9c9', '--accent-2': '#9ab8ff' },
    cyan:   { '--accent': '#6cd5ff', '--accent-2': '#b79dff' },
    violet: { '--accent': '#b498ff', '--accent-2': '#6cd5ff' },
    amber:  { '--accent': '#ffc071', '--accent-2': '#ff8a8a' },
    lime:   { '--accent': '#c7f06a', '--accent-2': '#7cf9c9' }
  };
  const TAGLINES = [
    'Build the vibe. Ship the vision.',
    'Ideas to code. Code to product.',
    'From idea spark to shipped product.',
    'Learning fast. Building faster.',
    'Family-built. Future-focused.'
  ];

  const state = JSON.parse(JSON.stringify(DEFAULTS));
  try {
    const stored = localStorage.getItem('unc-neph-tweaks');
    if (stored) Object.assign(state, JSON.parse(stored));
  } catch (e) {}

  function applyTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
  }
  function applyAccent() {
    const vars = ACCENTS[state.accent] || ACCENTS.mint;
    for (const k in vars) document.documentElement.style.setProperty(k, vars[k]);
  }
  function applyTagline() {
    document.querySelectorAll('[data-tagline]').forEach(el => { el.textContent = state.tagline; });
  }
  function applyHero() {
    document.querySelectorAll('[data-hero-variant]').forEach(el => {
      el.style.display = (el.getAttribute('data-hero-variant') === state.heroVariant) ? '' : 'none';
    });
    document.querySelectorAll('.hero-variant-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.v === state.heroVariant);
    });
  }
  function applyTerminal() {
    document.querySelectorAll('[data-terminal]').forEach(el => {
      el.style.display = state.showTerminal ? '' : 'none';
    });
  }

  function apply() {
    applyTheme(); applyAccent(); applyTagline(); applyHero(); applyTerminal();
  }

  function persist() {
    try { localStorage.setItem('unc-neph-tweaks', JSON.stringify(state)); } catch (e) {}
    try {
      window.parent.postMessage({ type: '__edit_mode_set_keys', edits: state }, '*');
    } catch (e) {}
  }

  function set(key, val) {
    state[key] = val;
    apply();
    persist();
    renderTweaks();
  }

  // --- Reveal on scroll ---
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
  }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
    apply();
  });

  // --- Tweaks panel ---
  function renderTweaks() {
    const panel = document.getElementById('tweaks-panel');
    if (!panel) return;
    panel.innerHTML = `
      <h5>Tweaks</h5>
      <div class="tweak-row">
        <label>theme</label>
        <div class="tweak-opts">
          <button data-k="theme" data-v="dark" class="${state.theme==='dark'?'active':''}">Dark</button>
          <button data-k="theme" data-v="light" class="${state.theme==='light'?'active':''}">Light</button>
        </div>
      </div>
      <div class="tweak-row">
        <label>accent</label>
        <div class="swatch-row">
          ${Object.keys(ACCENTS).map(k => `
            <div class="swatch ${state.accent===k?'active':''}" data-accent="${k}"
              style="background: linear-gradient(135deg, ${ACCENTS[k]['--accent']} 0 50%, ${ACCENTS[k]['--accent-2']} 50% 100%)"
              title="${k}"></div>
          `).join('')}
        </div>
      </div>
      <div class="tweak-row">
        <label>tagline</label>
        <div class="tweak-opts" style="flex-direction:column; align-items:stretch;">
          ${TAGLINES.map(t => `
            <button data-k="tagline" data-v="${t.replace(/"/g,'&quot;')}" class="${state.tagline===t?'active':''}" style="text-align:left;">${t}</button>
          `).join('')}
        </div>
      </div>
      <div class="tweak-row">
        <label>hero layout</label>
        <div class="tweak-opts">
          <button data-k="heroVariant" data-v="collage" class="hero-variant-btn ${state.heroVariant==='collage'?'active':''}">Collage</button>
          <button data-k="heroVariant" data-v="network" class="hero-variant-btn ${state.heroVariant==='network'?'active':''}">Network</button>
          <button data-k="heroVariant" data-v="wordmark" class="hero-variant-btn ${state.heroVariant==='wordmark'?'active':''}">Wordmark</button>
        </div>
      </div>
      <div class="tweak-row">
        <label>terminal strip</label>
        <div class="tweak-opts">
          <button data-k="showTerminal" data-v="true" class="${state.showTerminal?'active':''}">Show</button>
          <button data-k="showTerminal" data-v="false" class="${!state.showTerminal?'active':''}">Hide</button>
        </div>
      </div>
      <div class="tweak-row">
        <label>3D scene (home)</label>
        <div class="tweak-opts">
          <button data-k="showSpline" data-v="true" class="${state.showSpline?'active':''}">On</button>
          <button data-k="showSpline" data-v="false" class="${!state.showSpline?'active':''}">Off</button>
        </div>
      </div>
    `;
    panel.querySelectorAll('button[data-k]').forEach(b => {
      b.addEventListener('click', () => {
        let v = b.dataset.v;
        if (v === 'true') v = true;
        else if (v === 'false') v = false;
        set(b.dataset.k, v);
      });
    });
    panel.querySelectorAll('.swatch').forEach(s => {
      s.addEventListener('click', () => set('accent', s.dataset.accent));
    });
  }

  // --- Edit mode contract ---
  window.addEventListener('message', (e) => {
    if (!e.data || typeof e.data !== 'object') return;
    if (e.data.type === '__activate_edit_mode') {
      document.getElementById('tweaks-panel')?.classList.add('open');
      renderTweaks();
    }
    if (e.data.type === '__deactivate_edit_mode') {
      document.getElementById('tweaks-panel')?.classList.remove('open');
    }
  });
  try { window.parent.postMessage({ type: '__edit_mode_available' }, '*'); } catch (e) {}
})();
