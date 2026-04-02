# Repository Alignment

## Current State — ALIGNED (as of v0.7.0)

Local workspace path:
- `C:\Users\techai\PKA testing`

Git root (standalone):
- `C:/Users/techai/PKA testing`  (verified: `git rev-parse --show-toplevel`)

Active remote:
- `https://github.com/rblake2320/pka-workspace.git`
- Branch: `main`
- HEAD at v0.7.0 initial commit

## What Changed in v0.7.0

Previously: PKA testing was nested inside the parent home-dir repo
(`C:\Users\techai\.git`, remote `council.git`).  This created risks:
- `git status` was noisy with hundreds of untracked home-dir files
- Any `git add .` from home dir could commit NTUSER.DAT, `.ssh/`, `.aws/`
- PKA versioning was file-driven because git was unsafe to use

**Now**: `git init` was run inside `PKA testing/`, creating a clean standalone
`.git` here.  The parent repo index was cleaned with `git rm -r --cached "PKA testing/"`.
The local bare backup of the old remote is at `C:\Users\techai\pka-workspace-backup.git`.

## Repo Shape (clean)

```text
pka-workspace/ (= C:\Users\techai\PKA testing\)
  README.md
  CLAUDE.md
  VERSION
  CHANGELOG.md
  RELEASE_PROCESS.md
  REPO_ALIGNMENT.md
  .gitignore
  Team/
  Team Inbox/
  Owner's Inbox/
  scripts/
  .claude/agents/
```

## Release Rule

The repo is aligned.  All future PKA releases should:
1. `cd "C:\Users\techai\PKA testing"`
2. `git add` / `git commit`
3. `git push origin main`

Do NOT reference the parent home-dir repo for PKA versioning.

## Doctor Check

`pka_doctor.py check_git_boundary` verifies that
`git rev-parse --show-toplevel` equals `ROOT` (derived from
`Path(__file__).resolve().parent.parent`).  This check passes post-v0.7.0.
