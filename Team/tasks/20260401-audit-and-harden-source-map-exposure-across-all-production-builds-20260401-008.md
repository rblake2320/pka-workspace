---
task_id: "TASK-20260401-008"
title: "Audit and harden source map exposure across all production builds"
state: "delivered"
priority: "high"
owner: "FORGE"
route:
  - "AXIOM"
  - "FORGE"
  - "SENTINEL"
intake_file: ""
deliverable_file: "aihangout-app/frontend/dist/ (0 .map files, commit 5ddd094) + pro-designs-system/dist/ (0 .map files)"
verdict: "GO"
created_at: "2026-04-01"
updated_at: "2026-04-01"
definition_of_done: "All production Vite builds have sourcemap:false, zero .map files in dist/, builds verified with npm run build exits 0"
blockers: []
---

# Task Summary

## Objective
Identify and eliminate source map (.map file) exposure in all production web builds following the Anthropic Claude Code npm v2.1.88 source leak incident.

## Context
Triggered by Anthropic leaking 512k lines of TypeScript via sourcemap:true in Claude Code npm v2.1.88 (59.8MB). Audited all local web projects for same misconfiguration. Found: aihangout-app/frontend and pro-designs-system both had sourcemap defaulting to true. Fixed both vite.config.ts files. Rebuilt both dist/ directories with zero .map files. Also verified Council, PKA workspace, and other projects not using Vite or not exposing dist/.

## Evidence Required
- aihangout-app/frontend/vite.config.ts: sourcemap:false confirmed on build block (line 13)
- pro-designs-system/vite.config.ts: sourcemap:false confirmed on build block
- aihangout-app/frontend/dist/: 0 .map files after rebuild (verified: find dist/ -name "*.map" | wc -l = 0)
- pro-designs-system/dist/: 0 .map files after rebuild (verified: find dist/ -name "*.map" | wc -l = 0)
- npm run build: exits 0 on both projects
- git commit 5ddd094 pushed to rblake2320/aihangout-platform master — Cloudflare Pages rebuild triggered
- Anthropic v2.1.88 leak: 59.8MB source map, 512k lines TypeScript exposed via npm package — we were configured the same way before this fix
- GitHub Actions workflow created: pro-designs-system/.github/workflows/build-check.yml — build gate on push/PR to main

## Notes
- Five stale .map files removed from aihangout-app CDN: index-DFcZHlPX.js.map, state-BFxGOZ4W.js.map, ui-D9kWSrJ0.js.map, utils-CXbonkIM.js.map, vendor-D7tVPH2t.js.map
- Council platform not affected — backend-only Python project, no Vite build
- PKA workspace not affected — no Vite build target
- wrangler.toml also staged but not committed (not in scope for this task)
