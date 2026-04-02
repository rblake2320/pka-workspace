# Release Process

This workspace now has an internal version line even if it is currently nested inside a larger git repository.

## Current Constraint
`PKA testing/` is not its own git root today.
The active git root is the parent directory and the current remote points to a different project.

That means:
- versioning inside PKA must be tracked explicitly in files
- repo-level remote changes should not be made from inside this workspace without an intentional repo split or dedicated submodule/repo

## Dedicated Repo

Dedicated target repo:
- `https://github.com/rblake2320/pka-workspace.git`

See `REPO_ALIGNMENT.md` for the exact migration target and current mismatch between local and remote structure.

## Release Rules

1. Update `VERSION`
2. Add a new entry to `CHANGELOG.md`
3. Run:
   - `python scripts/pka_process_audit.py`
   - `python scripts/pka_e2e_test.py`
   - `python scripts/pka_resilience_test.py`
   - `python scripts/pka_full_validation.py`
4. Confirm `Team/handoff.md` and `Team/status.md` reflect reality
5. Confirm `Owner's Inbox/DELIVERY_MANIFEST.md` is current
6. Generate updated observability output with `python scripts/pka_observability.py`
7. Only call a version "green" if the validation suite passed on the real workspace

## Versioning Scheme

Use semantic-style versions:
- `MAJOR`: operating model or compatibility break
- `MINOR`: meaningful capability expansion
- `PATCH`: fixes, clarifications, hardening with no workflow break

## Recommended Git Future State

Best path:
- move `PKA testing/` into its own repository
- give it its own remote
- tag releases from that dedicated repo

If that is not done yet, treat `VERSION` and `CHANGELOG.md` as the source of truth.
