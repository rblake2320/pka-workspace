"""
Audio plugin configuration loader.

Loads from a YAML file and merges with defaults. The config file path
defaults to selfconnect-audio/audio_config.yaml but can be overridden
via CLI --config flag or the SELFCONNECT_AUDIO_CONFIG env var.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

_DEFAULTS = {
    "connector": "auto",
    "target_hwnd": 0,
    "target_title": "",
    "capture": {
        "enabled": True,
        "device": "default",
        "sample_rate": 16000,
        "channels": 1,
        "chunk_ms": 30,
        "tone_detection": {
            "enabled": True,
            "fingerprints": str(Path(__file__).parent / "capture" / "fingerprints.yaml"),
            "min_confidence": 0.85,
        },
    },
    "stt": {"enabled": False, "provider": "whisper_local"},
    "tts": {"enabled": False, "provider": "elevenlabs"},
    "wakeword": {"enabled": False, "keywords": ["hey selfconnect"], "sensitivity": 0.7},
    "health": {"pipe_enabled": True},
    "log_level": "INFO",
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base, returning a new dict."""
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: str | Path | None = None) -> dict:
    """
    Load and merge audio plugin config from YAML.

    Resolution order:
      1. path argument
      2. SELFCONNECT_AUDIO_CONFIG env var
      3. selfconnect-audio/audio_config.yaml (sibling of this file)
      4. Built-in defaults
    """
    search_path = (
        Path(path) if path
        else Path(os.environ.get("SELFCONNECT_AUDIO_CONFIG", ""))
        if os.environ.get("SELFCONNECT_AUDIO_CONFIG")
        else Path(__file__).parent / "audio_config.yaml"
    )

    if search_path.exists():
        with open(search_path, encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        merged = _deep_merge(_DEFAULTS, user_config)
        # Inject config dir so relative paths (e.g. fingerprints) resolve correctly
        merged["_config_dir"] = str(search_path.parent.resolve())
        return merged

    return dict(_DEFAULTS)
