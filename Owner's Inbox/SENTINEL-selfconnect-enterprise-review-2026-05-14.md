# SENTINEL Review — selfconnect-enterprise

Date: 2026-05-14
Repository: https://github.com/rblake2320/selfconnect-enterprise.git
Reviewed commit: `d2f0894` (`master`, `origin/master`)
Verdict: HOLD for production classified deployment; GO for research/hardening baseline.

## Executive Assessment

SelfConnect Enterprise has a strong core security posture for a fast-moving research repo: 714 tests pass, the code documents its own known gaps, and the policy/ledger/classification modules are materially better than typical prototype governance code. The architecture is coherent: policy enforcement, classified profiles, egress/export guards, signed ledgers, operator controls, and adversarial tests all point in the same direction.

The production risk is that several claims in README/SECURITY/docs are stronger than what the runtime enforces. The top priority is not adding more tests; it is making the default production path impossible to misuse.

## Verification Performed

- `git fetch origin` confirmed local `master` matches `origin/master`.
- `python -m pytest -q`: `714 passed, 2 skipped`.
- `python -m pytest -q -rs`: skipped tests are both dependency-integrity checks because `selfconnect` is not installed as a distribution.
- `python -m ruff check .`: failed with 431 findings because the initialized `sdk/` submodule is linted.
- `python -m ruff check enterprise tests tools --statistics`: failed with 53 findings.
- Reviewed `enterprise/policy.py`, `enterprise/classified_mode.py`, `enterprise/observer.py`, `enterprise/ledger.py`, `enterprise/identity.py`, `enterprise/identity_cng.py`, `enterprise/transport.py`, `enterprise/registry.py`, `tools/wfp_policy.py`, README, SECURITY, changelog, and compliance gap docs.

## Findings

### P0 — Classified profile flags are not fully enforced by PolicyEnforcer

`ClassifiedModeProfile` declares `require_signed_policy`, `require_operator_approval_for`, `allowed_apps`, and `blocked_apps`, but `PolicyEnforcer.check()` only enforces the profile classification ceiling and the DPAPI rejection path.

Evidence:
- `enterprise/classified_mode.py:58` says unsigned policies fail closed when `require_signed_policy=True`.
- `enterprise/classified_mode.py:66-71` defines profile operator approval and app overlays.
- `enterprise/policy.py:333-350` only enforces profile classification and `identity_type == "dpapi"`.
- `enterprise/policy.py:364-367` still depends only on constructor argument `require_signature`.
- `enterprise/policy.py:376-405` checks policy-level app and approval fields, not profile overlays.

Proof run: constructing a profile with `require_signed_policy=True`, `require_operator_approval_for={"write_file"}`, and `blocked_apps={"cmd.exe"}` still allowed an unsigned `write_file` action against `cmd.exe` when `PolicyEnforcer(..., require_signature=False, profile=profile)` was used.

Impact: a caller can believe classified profile requirements are active while bypassing signature enforcement, app overlays, and mandatory operator approval. This undermines the "immutable deployment profile governs all runtime behavior" claim.

Fix: make profile constraints authoritative inside `PolicyEnforcer.__init__` and `check()`:
- if `profile.require_signed_policy`, force signature verification regardless of caller `require_signature=False`;
- reject missing/unknown identity type when CNG is required, not only explicit `"dpapi"`;
- merge/enforce profile `blocked_apps` and `allowed_apps`;
- OR profile `require_operator_approval_for` into policy-level approval requirements.

### P1 — LedgerObserver exports unverified JSONL entries

`LedgerObserver.extract()` reads raw JSONL, filters by fields, and emits training records without verifying ledger signatures or hash-chain integrity.

Evidence:
- `enterprise/observer.py:271` loads all entries through `_load_entries()`.
- `enterprise/observer.py:326-337` parses JSONL and silently drops malformed lines, but does not call ledger verification.
- README explicitly documents that injected entries can leak without `verify()` (`README.md:216-217`).

Impact: training data isolation is true only for honest ledger entries or for callers who remember to verify first and configure `allowed_policy_ids`. A malicious or compromised writer can inject an `allow` record directly into JSONL and get it into training output.

Fix: add a verified observer path as the production default. Accept a ledger object with `verify()` or require a signed-entry verifier before `extract()`. Keep raw JSONL mode only behind an explicit `unsafe_unverified=True` style flag.

### P1 — Identity storage accepts path traversal via agent_name

`AgentIdentity._storage_paths()` and `CngIdentity._storage_paths()` build paths with `(data_dir or default) / agent_name` without constraining `agent_name`.

Evidence:
- `enterprise/identity.py:285-292`
- `enterprise/identity_cng.py:215-222`
- `tests/test_enterprise/test_pentest_injection.py:262-272` documents that `"../../escape-agent"` writes outside `data_dir`, but the test still passes.

Impact: if `agent_name` ever comes from config, a mesh peer, user input, or generated task metadata, identity public/private material can be written outside the intended identity root.

Fix: validate agent names against a narrow slug pattern or resolve and assert the final path remains under the intended base directory.

### P1 — WM_COPYDATA payload size limit is documented but not enforced

The docs state a 64KB payload limit, but `send_data()` sends whatever JSON size is produced and `CopyDataListener._handle_copydata()` allocates `cbData` bytes without checking a ceiling.

Evidence:
- `enterprise/registry.py:417` documents "Up to 64KB per message."
- `enterprise/registry.py:429-434` serializes and sets `cbData=len(raw)` with no guard.
- `enterprise/transport.py:278` reads `ctypes.string_at(cds.lpData, cds.cbData)` with no max-size validation.

Impact: oversized local messages can create memory/latency problems and undefined delivery behavior. A local adversarial process can use this as a denial-of-service vector against the listener thread.

Fix: define `MAX_COPYDATA_BYTES = 64 * 1024`, enforce it before `SendMessageW`, and reject inbound `cbData` above the same ceiling before allocation.

### P2 — Test and lint posture is overstated

The README claims a clean audited posture, but the repo does not currently provide a reproducible lint command that passes after submodule checkout.

Evidence:
- `README.md:8` claims `714 tests passing`.
- `README.md:186` repeats `714 tests`.
- `CHANGELOG.md:57-64` says v1.2.0 moved from 632 to 674 tests, stale relative to the current 714-test state.
- `python -m ruff check .` fails with 431 findings, largely from the initialized `sdk/` submodule.
- `python -m ruff check enterprise tests tools --statistics` still fails with 53 findings.
- No `.github/workflows/` directory exists in this checkout, so the "continuously audited" claim is not backed by visible CI configuration in the repo.

Impact: reviewers will distrust the strong security language if the reproducible commands do not match it.

Fix: add a CI workflow and pin the exact verification commands. Either exclude `sdk/` from root lint or make it explicit that lint scope is `enterprise/ tests/ tools/`, then clean that scoped lint set.

### P2 — Supply-chain hard gates skip when dependencies are not installed as distributions

The passing suite includes two skipped dependency-integrity tests:

- `test_selfconnect_commit_matches_pyproject` skipped because `selfconnect` is not installed as a distribution.
- `test_selfconnect_transitive_deps_scanned` skipped for the same reason.

Impact: the suite can report green even when the pinned git dependency is not installed in the form the integrity tests expect.

Fix: make CI install the package through the same path production uses, or convert these tests to inspect the checked-out submodule / direct git metadata instead of installed distribution metadata.

## Strengths

- Deny-by-default policy model is clean and easy to reason about.
- Test count and adversarial coverage are unusually strong for a young repo.
- Security docs are candid about several real limitations.
- WFP PowerShell generation has meaningful injection hardening.
- CNG path and classification labels give the repo a credible regulated-deployment direction.
- The submodule pin is explicit and checked into `.gitmodules`/gitlink.

## Recommended Next Sequence

1. Fix P0 profile enforcement first. This is the biggest mismatch between claims and runtime behavior.
2. Make verified ledger observation the default production path.
3. Sanitize identity path inputs.
4. Enforce WM_COPYDATA size limits on send and receive.
5. Add CI with exact commands for pytest, ruff, and dependency audit.
6. Update README/CHANGELOG/SECURITY so every posture claim maps to a command and passing output.

## Final Verdict

This is a credible security-governance substrate, not just a demo. It should not be marketed as production classified-ready until profile enforcement and verified observer extraction are fixed. Once those are closed, the repo will have a much stronger claim: not just many tests, but tests and defaults that make unsafe use hard.
