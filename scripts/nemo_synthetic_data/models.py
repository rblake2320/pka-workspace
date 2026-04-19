from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class InferenceSpec:
    temperature: float = 0.6
    top_p: float = 0.95
    max_tokens: int = 1024


@dataclass(slots=True)
class ModelSpec:
    alias: str
    model: str
    inference: InferenceSpec = field(default_factory=InferenceSpec)


@dataclass(slots=True)
class ColumnSpec:
    name: str
    kind: str = field(init=False)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SamplerColumnSpec(ColumnSpec):
    sampler_type: str
    params: dict[str, Any]
    convert_to: str | None = None
    kind: str = field(init=False, default="sampler")


@dataclass(slots=True)
class LLMTextColumnSpec(ColumnSpec):
    prompt: str
    model_alias: str
    system_prompt: str | None = None
    kind: str = field(init=False, default="llm_text")


@dataclass(slots=True)
class TemplateSpec:
    name: str
    description: str
    purpose: str
    tags: list[str]
    models: list[ModelSpec]
    columns: list[ColumnSpec]
    default_records: int = 10
    max_records: int = 100
    context_defaults: dict[str, Any] = field(default_factory=dict)
    context_help: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "purpose": self.purpose,
            "tags": list(self.tags),
            "models": [asdict(item) for item in self.models],
            "columns": [item.to_dict() for item in self.columns],
            "default_records": self.default_records,
            "max_records": self.max_records,
            "context_defaults": dict(self.context_defaults),
            "context_help": dict(self.context_help),
        }
