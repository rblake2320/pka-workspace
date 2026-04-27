from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
from pathlib import Path

from .models import SamplerColumnSpec
from .provider import NemoDataDesignerProvider, ProviderError, dump_config, write_output
from .templates import TEMPLATE_REGISTRY, get_template
from .validators import lint_template, validate_rows


DEFAULT_BASE_URL = "https://ai.api.nvidia.com/v1/nemo/dd"


def _parse_context(args: argparse.Namespace) -> dict[str, object]:
    context: dict[str, object] = {}
    if args.context_json:
        context.update(json.loads(args.context_json))
    for item in args.set or []:
        if "=" not in item:
            raise SystemExit(f"invalid --set '{item}'. Expected key=value.")
        key, value = item.split("=", 1)
        context[key] = value
    return context


def _provider(args: argparse.Namespace, *, require_key: bool) -> NemoDataDesignerProvider:
    api_key = args.api_key or os.environ.get("NVIDIA_API_KEY") or ""
    if require_key and not api_key:
        raise SystemExit("NVIDIA_API_KEY is required. Set it or pass --api-key.")
    return NemoDataDesignerProvider(api_key=api_key, base_url=args.base_url)


def _materialize_context(template, context: dict[str, object]):
    effective = deepcopy(template)
    prefix_columns = []
    existing = {column.name for column in effective.columns}
    for key, value in context.items():
        if key in existing:
            continue
        prefix_columns.append(
            SamplerColumnSpec(
                name=key,
                sampler_type="category",
                params={"values": [str(value)]},
            )
        )
    effective.columns = prefix_columns + effective.columns
    return effective


def _resolve_template(args: argparse.Namespace):
    template = get_template(args.template)
    context = dict(template.context_defaults)
    context.update(_parse_context(args))
    return _materialize_context(template, context), context


def _write_validation_report(path: str | None, report) -> None:
    if not path:
        return
    Path(path).write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")


def _generate_validated_rows(provider: NemoDataDesignerProvider, template, *, mode: str, target_count: int, max_attempts: int):
    all_valid: list[dict[str, object]] = []
    attempts: list[dict[str, object]] = []
    for attempt in range(1, max_attempts + 1):
        remaining = target_count - len(all_valid)
        if remaining <= 0:
            break
        if mode == "preview":
            rows, meta = provider.preview(template, num_records=remaining)
        else:
            rows, meta = provider.create(template, num_records=remaining, wait_until_done=True)
        report = validate_rows(template.name, rows)
        all_valid.extend(report.valid_rows)
        attempts.append({
            "attempt": attempt,
            "requested_rows": remaining,
            "returned_rows": len(rows),
            "valid_rows": len(report.valid_rows),
            "invalid_rows": len(report.invalid_rows),
            "issues": [issue.to_dict() for issue in report.issues[:20]],
            "provider_meta": meta,
        })
    return all_valid[:target_count], attempts


def cmd_list(_: argparse.Namespace) -> int:
    for name, template in sorted(TEMPLATE_REGISTRY.items()):
        print(f"{name}: {template.description}")
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    template = get_template(args.template)
    print(json.dumps(template.to_dict(), indent=2))
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    template, _context = _resolve_template(args)
    issues = lint_template(template)
    payload = {
        "template": template.name,
        "issue_count": len(issues),
        "issues": [issue.to_dict() for issue in issues],
    }
    print(json.dumps(payload, indent=2))
    return 1 if any(issue.severity == "error" for issue in issues) else 0


def cmd_validate_output(args: argparse.Namespace) -> int:
    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = validate_rows(args.template, rows)
    _write_validation_report(args.report_output, report)
    print(json.dumps(report.to_dict(), indent=2))
    return 0 if report.ok else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    provider = _provider(args, require_key=False)
    payload = provider.validate_environment()
    payload["api_key_present"] = bool(args.api_key or os.environ.get("NVIDIA_API_KEY"))
    print(json.dumps(payload, indent=2))
    return 0


def cmd_export_config(args: argparse.Namespace) -> int:
    provider = _provider(args, require_key=False)
    template, context = _resolve_template(args)
    payload = {
        "template": template.to_dict(),
        "context": context,
        "provider_manifest": provider.build_manifest(template),
        "base_url": args.base_url,
    }
    dump_config(Path(args.output), payload)
    print(f"Wrote config manifest to {args.output}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    provider = _provider(args, require_key=True)
    template, _context = _resolve_template(args)
    if args.num_records > template.max_records:
        raise SystemExit(
            f"template '{template.name}' supports at most {template.max_records} records per job"
        )

    lint_issues = lint_template(template)
    if any(issue.severity == "error" for issue in lint_issues):
        raise SystemExit(json.dumps({"template": template.name, "lint_errors": [issue.to_dict() for issue in lint_issues]}, indent=2))

    try:
        if args.validate:
            rows, attempts = _generate_validated_rows(
                provider,
                template,
                mode=args.mode,
                target_count=args.num_records,
                max_attempts=args.max_attempts,
            )
            meta = {
                "provider": "nemo",
                "mode": args.mode,
                "rows": len(rows),
                "attempts": attempts,
                "validated": True,
            }
            if len(rows) < args.num_records:
                raise SystemExit(json.dumps(meta, indent=2))
        else:
            if args.mode == "preview":
                rows, meta = provider.preview(template, num_records=args.num_records)
            else:
                rows, meta = provider.create(template, num_records=args.num_records, wait_until_done=True)
            if args.validate_output_rows:
                report = validate_rows(template.name, rows)
                _write_validation_report(args.report_output, report)
                if not report.ok and args.reject_invalid:
                    raise SystemExit(json.dumps(report.to_dict(), indent=2))
                rows = report.valid_rows if args.reject_invalid else rows
                meta["validation"] = report.to_dict()
    except ProviderError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        write_output(Path(args.output), rows, args.output_format)
        print(f"Wrote {len(rows)} rows to {args.output}")
    else:
        print(json.dumps(rows[: min(3, len(rows))], indent=2))
    if args.meta_output:
        Path(args.meta_output).write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Real NeMo Data Designer toolkit with reusable dataset templates."
    )
    parser.add_argument("--api-key")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list-templates", help="List available templates")
    list_parser.set_defaults(func=cmd_list)

    describe = sub.add_parser("describe", help="Describe a template")
    describe.add_argument("template")
    describe.set_defaults(func=cmd_describe)

    lint = sub.add_parser("lint-template", help="Lint a template definition")
    lint.add_argument("template")
    lint.add_argument("--context-json")
    lint.add_argument("--set", action="append")
    lint.set_defaults(func=cmd_lint)

    validate_cmd = sub.add_parser("validate-output", help="Validate generated output rows for a template")
    validate_cmd.add_argument("template")
    validate_cmd.add_argument("--input", required=True)
    validate_cmd.add_argument("--report-output")
    validate_cmd.set_defaults(func=cmd_validate_output)

    doctor = sub.add_parser("doctor", help="Validate SDK and auth environment")
    doctor.set_defaults(func=cmd_doctor)

    export = sub.add_parser("export-config", help="Export template manifest and provider config")
    export.add_argument("template")
    export.add_argument("--output", required=True)
    export.add_argument("--context-json")
    export.add_argument("--set", action="append")
    export.set_defaults(func=cmd_export_config)

    for name in ("preview", "create"):
        cmd = sub.add_parser(name, help=f"{name.title()} a dataset using NeMo Data Designer")
        cmd.add_argument("template")
        cmd.add_argument("--num-records", type=int, default=10)
        cmd.add_argument("--output")
        cmd.add_argument("--output-format", choices=["json", "jsonl", "csv"], default="json")
        cmd.add_argument("--meta-output")
        cmd.add_argument("--context-json")
        cmd.add_argument("--set", action="append")
        cmd.add_argument("--validate", action="store_true", help="Regenerate until enough valid rows are collected")
        cmd.add_argument("--max-attempts", type=int, default=3)
        cmd.add_argument("--validate-output-rows", action="store_true", help="Validate returned rows once")
        cmd.add_argument("--reject-invalid", action="store_true", help="Drop or fail on invalid rows when validating output")
        cmd.add_argument("--report-output")
        cmd.set_defaults(func=cmd_generate, mode=name)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
