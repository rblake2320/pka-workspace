# NeMo Synthetic Data Toolkit

Real NeMo Data Designer integration for reusable synthetic dataset generation in
this workspace.

## What it does

- exposes a template registry instead of one-off prompts
- generates real datasets via NVIDIA NeMo Data Designer
- exports config manifests for review and reuse
- ships BPC-focused and general API-abuse templates

## Install

```powershell
uv pip install "nemo-microservices[data-designer]"
```

Set your API key:

```powershell
$env:NVIDIA_API_KEY="..."
```

## Commands

List templates:

```powershell
python scripts\nemo_synth_cli.py list-templates
```

Validate environment:

```powershell
python scripts\nemo_synth_cli.py doctor
```

Describe a template:

```powershell
python scripts\nemo_synth_cli.py describe bpc_security_events
```

Export a reusable config manifest:

```powershell
python scripts\nemo_synth_cli.py export-config bpc_security_events `
  --output logs\bpc_security_template.json `
  --set tenant_name=BPC `
  --set system_name="BPC Protocol"
```

Preview generated rows:

```powershell
python scripts\nemo_synth_cli.py preview bpc_security_events `
  --num-records 10 `
  --output logs\bpc_security_preview.json `
  --output-format json `
  --set tenant_name=BPC `
  --set system_name="BPC Protocol"
```

Create a full job and save results:

```powershell
python scripts\nemo_synth_cli.py create api_abuse_patterns `
  --num-records 25 `
  --output logs\api_abuse_patterns.csv `
  --output-format csv `
  --set company_name=PKA `
  --set product_name="PKA Runtime"
```

## Included Templates

- `bpc_security_events`
- `api_abuse_patterns`

## Notes

- This tool does not fake generation. If the SDK or API key are missing, it fails.
- Hosted jobs are capped by template max-record limits to stay aligned with the
  current Data Designer hosted workflow.
