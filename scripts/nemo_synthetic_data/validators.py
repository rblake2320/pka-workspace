from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import LLMTextColumnSpec, SamplerColumnSpec, TemplateSpec


@dataclass(slots=True)
class ValidationIssue:
    severity: str
    message: str
    row_index: int | None = None
    field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "message": self.message,
            "row_index": self.row_index,
            "field": self.field,
        }


@dataclass(slots=True)
class ValidationReport:
    ok: bool
    valid_rows: list[dict[str, Any]]
    invalid_rows: list[dict[str, Any]]
    issues: list[ValidationIssue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "valid_count": len(self.valid_rows),
            "invalid_count": len(self.invalid_rows),
            "issues": [issue.to_dict() for issue in self.issues],
        }


def lint_template(template: TemplateSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    llm_columns = 0
    for column in template.columns:
        if column.name in seen:
            issues.append(ValidationIssue("error", f"duplicate column name '{column.name}'", field=column.name))
        seen.add(column.name)
        if isinstance(column, SamplerColumnSpec):
            if column.sampler_type == "category":
                values = column.params.get("values", [])
                if not values:
                    issues.append(ValidationIssue("error", "category sampler must define values", field=column.name))
            if column.sampler_type == "subcategory":
                parent = column.params.get("category")
                if not parent:
                    issues.append(ValidationIssue("error", "subcategory sampler must define parent category", field=column.name))
                elif parent not in seen:
                    issues.append(ValidationIssue("error", f"subcategory parent '{parent}' must appear earlier", field=column.name))
        if isinstance(column, LLMTextColumnSpec):
            llm_columns += 1
            if not column.prompt.strip():
                issues.append(ValidationIssue("error", "llm text column prompt cannot be empty", field=column.name))
    if llm_columns == 0:
        issues.append(ValidationIssue("warning", "template has no llm columns"))
    if template.max_records > 100:
        issues.append(ValidationIssue("warning", "template max_records exceeds hosted guidance of 100"))
    return issues


def _base_row_checks(row: dict[str, Any], row_index: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for key, value in row.items():
        if key.endswith("__reasoning_trace"):
            issues.append(ValidationIssue("error", "reasoning trace leaked into output", row_index=row_index, field=key))
        if isinstance(value, str) and not value.strip():
            issues.append(ValidationIssue("error", "empty string value", row_index=row_index, field=key))
    return issues


def _validate_bpc_security_row(row: dict[str, Any], row_index: int) -> list[ValidationIssue]:
    issues = _base_row_checks(row, row_index)
    expected = row.get("expected_verdict")
    traffic = row.get("traffic_pattern")
    if traffic == "normal" and expected != "allow":
        issues.append(ValidationIssue("error", "normal traffic must map to allow", row_index=row_index, field="expected_verdict"))
    if traffic == "replay_attempt" and expected != "replay_detected":
        issues.append(ValidationIssue("error", "replay_attempt must map to replay_detected", row_index=row_index, field="expected_verdict"))
    return issues


def _validate_verification_claim_row(row: dict[str, Any], row_index: int) -> list[ValidationIssue]:
    issues = _base_row_checks(row, row_index)
    profile = row.get("verification_profile")
    expected_http = row.get("expected_http_status")
    expected_error = row.get("expected_error_code")
    allowed = {
        "oversized_headers_signature": (400, "invalid_signed_data"),
        "oversized_headers_pair_id": (400, "invalid_signed_data"),
        "pair_lockout_flood": (401, "pair_locked"),
        "scope_read_post_block": (403, "scope_violation"),
        "scope_rw_delete_block": (403, "scope_violation"),
        "scope_admin_delete_allow": (200, "allow"),
        "revocation_reuse_block": (401, "pair_revoked"),
        "nonce_lru_replay_detected": (401, "replay_detected"),
        "nonce_lru_allow_burst": (200, "allow"),
    }
    pair = allowed.get(str(profile))
    if pair is None:
        issues.append(ValidationIssue("error", f"unknown verification profile '{profile}'", row_index=row_index, field="verification_profile"))
        return issues
    if (expected_http, expected_error) != pair:
        issues.append(
            ValidationIssue(
                "error",
                f"verification profile '{profile}' must map to {pair[0]} / {pair[1]}, got {expected_http} / {expected_error}",
                row_index=row_index,
                field="expected_http_status",
            )
        )
    return issues


def validate_rows(template_name: str, rows: list[dict[str, Any]]) -> ValidationReport:
    issues: list[ValidationIssue] = []
    valid_rows: list[dict[str, Any]] = []
    invalid_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(rows):
        row_issues = _base_row_checks(row, idx)
        if template_name == "bpc_security_events":
            row_issues = _validate_bpc_security_row(row, idx)
        elif template_name == "bpc_verification_claims":
            row_issues = _validate_verification_claim_row(row, idx)
        if row_issues:
            issues.extend(row_issues)
            invalid_rows.append(row)
        else:
            valid_rows.append(row)
    return ValidationReport(ok=not issues, valid_rows=valid_rows, invalid_rows=invalid_rows, issues=issues)
