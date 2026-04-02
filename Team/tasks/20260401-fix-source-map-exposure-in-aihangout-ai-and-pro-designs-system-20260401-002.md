---
task_id: "TASK-20260401-002"
title: "Fix source map exposure in aihangout.ai and pro-designs-system"
state: "delivered"
priority: "high"
owner: "FORGE"
route:
  - "AXIOM"
  - "FORGE"
  - "SENTINEL"
intake_file: ""
deliverable_file: "aihangout-app/frontend/vite.config.ts + pro-designs-system/vite.config.ts (sourcemap:false)"
verdict: "GO"
created_at: "2026-04-01"
updated_at: "2026-04-01"
definition_of_done: "sourcemap:false in both vite.config.ts files, zero .map files in dist directories, both projects build successfully"
blockers: []
---

# Task Summary

## Objective
Remove source map generation from production builds to prevent source code exposure via .map files

## Context
Anthropic leaked 512k lines of TypeScript via sourcemap:true in their npm package. Both aihangout.ai frontend and pro-designs-system had the same misconfiguration. Live on Cloudflare Pages and local dev server.

## Evidence Required
- aihangout-app/frontend/vite.config.ts: `sourcemap: false` confirmed on line 13 and 19
- pro-designs-system/vite.config.ts: `sourcemap: false` confirmed
- aihangout-app/frontend/dist: 0 .map files after rebuild (was 5)
- pro-designs-system/dist: 0 .map files after rebuild (was 1)
- Both projects: `npm run build` exits 0

## Notes
- Triggered by Anthropic's 59.8MB source map leak in Claude Code npm v2.1.88
- Both projects had same misconfiguration: vite build sourcemap defaulted to true
- Fixed 2026-04-01, verified same session
