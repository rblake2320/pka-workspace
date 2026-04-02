# Repository Alignment

## Current State

Local workspace path:
- `C:\Users\techai\PKA testing`

Current parent git root:
- `C:/Users/techai`

Current parent remote:
- `https://github.com/rblake2320/council.git`

Dedicated PKA repo:
- `https://github.com/rblake2320/pka-workspace.git`
- Verified branch: `main`
- Verified HEAD at time of review: `312986bc7dca9e93310383b4e0e1d8cfdb103aed`

## Important Reality

This local workspace is not yet operating as a standalone git repository.
It is nested under a larger parent repo.

That means:
- parent `git status` is noisy and unsafe for PKA-only release work
- parent remote actions are not a safe proxy for PKA release actions
- local versioning must remain file-driven until PKA is split or synced cleanly

## Remote Repo Shape

The dedicated `pka-workspace` repo currently contains:
- top-level PKA-related files
- an older nested `PKA testing/` subtree

This indicates the remote still needs normalization into a clean standalone layout.

## Recommended Target Shape

The dedicated repo should use this workspace root as repo root:

```text
pka-workspace/
  README.md
  CLAUDE.md
  VERSION
  CHANGELOG.md
  RELEASE_PROCESS.md
  GOLD_STANDARD_ROADMAP.md
  CONTEXT_SNAPSHOT_2026-04-01.md
  Team/
  Team Inbox/
  Owner's Inbox/
  scripts/
```

Avoid keeping `PKA testing/` as a nested subfolder inside the dedicated repo.

## Migration Recommendation

1. Clone `pka-workspace` to a clean standalone directory
2. Move the current contents of `C:\Users\techai\PKA testing` to the repo root
3. Preserve any remote-only files that still matter
4. Add the PKA-local `.gitignore`
5. Run:
   - `python scripts\pka_process_audit.py`
   - `python scripts\pka_e2e_test.py`
6. Commit as the first normalized baseline release

## Release Rule

Do not call the repo aligned until:
- PKA is its own git root
- the dedicated remote is the active remote
- the E2E test passes from that standalone repo
