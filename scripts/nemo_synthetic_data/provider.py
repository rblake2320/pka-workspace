from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import LLMTextColumnSpec, SamplerColumnSpec, TemplateSpec


class ProviderError(RuntimeError):
    pass


class NemoDataDesignerProvider:
    def __init__(self, *, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def _load_sdk(self) -> dict[str, Any]:
        try:
            from nemo_microservices.data_designer.essentials import (
                CategorySamplerParams,
                DataDesignerConfigBuilder,
                InferenceParameters,
                LLMTextColumnConfig,
                ModelConfig,
                NeMoDataDesignerClient,
                PersonSamplerParams,
                SamplerColumnConfig,
                SamplerType,
                SubcategorySamplerParams,
                UniformSamplerParams,
            )
        except ImportError as exc:
            raise ProviderError(
                'NeMo SDK is not installed. Install with: uv pip install "nemo-microservices[data-designer]"'
            ) from exc

        return {
            "CategorySamplerParams": CategorySamplerParams,
            "DataDesignerConfigBuilder": DataDesignerConfigBuilder,
            "InferenceParameters": InferenceParameters,
            "LLMTextColumnConfig": LLMTextColumnConfig,
            "ModelConfig": ModelConfig,
            "NeMoDataDesignerClient": NeMoDataDesignerClient,
            "PersonSamplerParams": PersonSamplerParams,
            "SamplerColumnConfig": SamplerColumnConfig,
            "SamplerType": SamplerType,
            "SubcategorySamplerParams": SubcategorySamplerParams,
            "UniformSamplerParams": UniformSamplerParams,
        }

    def build_manifest(self, template: TemplateSpec) -> dict[str, Any]:
        return {
            "columns": [column.to_dict() for column in template.columns],
            "model_configs": [
                {
                    "alias": model.alias,
                    "model": model.model,
                    "inference_parameters": asdict(model.inference),
                }
                for model in template.models
            ],
        }

    def preview(self, template: TemplateSpec, *, num_records: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        sdk = self._load_sdk()
        config_builder = self._build_builder(template, sdk)
        config_builder.validate()
        client = sdk["NeMoDataDesignerClient"](
            base_url=self.base_url,
            default_headers={"Authorization": f"Bearer {self.api_key}"},
        )
        preview = client.preview(config_builder, num_records=num_records)
        dataset = getattr(preview, "dataset", None)
        if dataset is None:
            raise ProviderError("preview returned no dataset")
        records = self._to_records(dataset)
        return records, {"provider": "nemo", "mode": "preview", "rows": len(records)}

    def create(
        self,
        template: TemplateSpec,
        *,
        num_records: int,
        wait_until_done: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        sdk = self._load_sdk()
        config_builder = self._build_builder(template, sdk)
        config_builder.validate()
        client = sdk["NeMoDataDesignerClient"](
            base_url=self.base_url,
            default_headers={"Authorization": f"Bearer {self.api_key}"},
        )
        job_result = client.create(
            config_builder,
            num_records=num_records,
            wait_until_done=wait_until_done,
        )
        dataset = job_result.load_dataset()
        records = self._to_records(dataset)
        return records, {
            "provider": "nemo",
            "mode": "create",
            "rows": len(records),
            "job_id": getattr(job_result, "job_id", None),
        }

    def validate_environment(self) -> dict[str, Any]:
        sdk = self._load_sdk()
        return {
            "sdk_loaded": True,
            "base_url": self.base_url,
            "available_sdk_symbols": sorted(key for key in sdk.keys() if key != "NeMoDataDesignerClient"),
        }

    def _build_builder(self, template: TemplateSpec, sdk: dict[str, Any]) -> Any:
        builder = sdk["DataDesignerConfigBuilder"](
            [
                sdk["ModelConfig"](
                    alias=model.alias,
                    model=model.model,
                    inference_parameters=sdk["InferenceParameters"](
                        temperature=model.inference.temperature,
                        top_p=model.inference.top_p,
                        max_tokens=model.inference.max_tokens,
                    ),
                )
                for model in template.models
            ]
        )
        for column in template.columns:
            if isinstance(column, SamplerColumnSpec):
                builder.add_column(self._build_sampler_column(column, sdk))
            elif isinstance(column, LLMTextColumnSpec):
                builder.add_column(
                    sdk["LLMTextColumnConfig"](
                        name=column.name,
                        prompt=column.prompt,
                        system_prompt=column.system_prompt,
                        model_alias=column.model_alias,
                    )
                )
            else:
                raise ProviderError(f"unsupported column type: {type(column)!r}")
        return builder

    def _build_sampler_column(self, column: SamplerColumnSpec, sdk: dict[str, Any]) -> Any:
        params = column.params
        sampler_type = column.sampler_type
        if sampler_type == "category":
            native_params = sdk["CategorySamplerParams"](**params)
            native_type = sdk["SamplerType"].CATEGORY
        elif sampler_type == "subcategory":
            native_params = sdk["SubcategorySamplerParams"](**params)
            native_type = sdk["SamplerType"].SUBCATEGORY
        elif sampler_type == "uniform":
            native_params = sdk["UniformSamplerParams"](**params)
            native_type = sdk["SamplerType"].UNIFORM
        elif sampler_type == "person":
            native_params = sdk["PersonSamplerParams"](**params)
            native_type = sdk["SamplerType"].PERSON
        else:
            raise ProviderError(f"unsupported sampler type: {sampler_type}")
        kwargs = {
            "name": column.name,
            "sampler_type": native_type,
            "params": native_params,
        }
        if column.convert_to:
            kwargs["convert_to"] = column.convert_to
        return sdk["SamplerColumnConfig"](**kwargs)

    def _to_records(self, dataset: Any) -> list[dict[str, Any]]:
        if hasattr(dataset, "to_dict"):
            try:
                rows = list(dataset.to_dict(orient="records"))
                return [self._sanitize_row(row) for row in rows]
            except TypeError:
                pass
        if isinstance(dataset, list):
            return [self._sanitize_row(row) for row in dataset]
        raise ProviderError("could not convert generated dataset to records")

    @staticmethod
    def _sanitize_row(row: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in row.items() if not key.endswith("__reasoning_trace")}


def write_output(path: Path, rows: list[dict[str, Any]], fmt: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return
    if fmt == "jsonl":
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")
        return
    if fmt == "csv":
        if not rows:
            path.write_text("", encoding="utf-8")
            return
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return
    raise ProviderError(f"unsupported output format: {fmt}")


def dump_config(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
