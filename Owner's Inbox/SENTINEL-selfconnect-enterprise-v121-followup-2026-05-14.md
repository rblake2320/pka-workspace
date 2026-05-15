# SENTINEL Follow-Up — selfconnect-enterprise v1.2.1

Date: 2026-05-14
Reviewed commit: `fa0d426`
Verdict: HOLD remains until residual items are fixed and pushed.

## What Is Closed

- P0 profile signature enforcement: mostly closed. `profile.require_signed_policy=True` now forces `_require_sig=True`.
- Profile app overlays: closed for calls that pass `app=...`.
- Profile operator approval overlay: closed as a decision flag.
- Identity path traversal: closed with slug validation and path containment checks.
- WM_COPYDATA size ceiling: closed on send and receive.
- Verified observer default: improved materially; raw extraction now requires `unsafe_unverified=True`.

## Verification

- Clean worktree at `fa0d426`.
- `python -m pytest -q`: `714 passed, 2 skipped`.
- `python -m ruff check enterprise tests tools`: FAIL, 4 unused import findings.

## Residual Findings

### P1 — Pushed commit is not ruff clean

The clean pushed commit still fails the exact CI lint command:

- `tests/test_enterprise/test_fuzz.py:28`: unused `generate_powershell`
- `tests/test_enterprise/test_resource_exhaustion.py:18`: unused `uuid`
- `tests/test_enterprise/test_resource_exhaustion.py:22`: unused `pytest`
- `tests/test_enterprise/test_resource_exhaustion.py:24`: unused `ControlPlane`

The main local worktree already contains these fixes unstaged, but they are not part of `fa0d426`.

### P1 — CNG-required profiles still allow omitted/unknown identity type

`PolicyEnforcer.check()` only rejects `identity_type == "dpapi"`. With `require_cng_identity=True`, both `identity_type=""` and `identity_type="unknown"` still allow the action when other checks pass.

Expected: require exact `identity_type == "cng"` when the profile requires CNG.

### P1 — LedgerObserver verifier is not bound to ledger_path

`LedgerObserver.extract()` calls `verifier.verify()`, but it does not ensure that the verifier represents the same file as `ledger_path`. A clean unrelated verifier can be supplied while extracting from a tampered raw JSONL file.

Expected: if verifier exposes `log_path`, require `Path(verifier.log_path).resolve() == ledger_path.resolve()`, or remove `ledger_path` from the verified constructor path and derive it from the verifier.

### P2 — CI dependency install is under-specified

`.github/workflows/ci.yml` installs `pip install -e .[full]`, but `pyproject.toml` only defines the `dev` extra. The workflow separately installs `ruff pytest`, but not `hypothesis`, which the tests import.

Expected: define a real `full`/`dev` extra including `hypothesis`, or change CI to `pip install -e .[dev]` after adding `hypothesis` to that extra.

## Current Verdict

The patch closes most of the original blockers, but not all. Production-ready should wait for one more commit that pushes the existing ruff fixes, requires exact CNG identity under classified profiles, binds observer verification to the observed ledger, and fixes CI dependency installation.
