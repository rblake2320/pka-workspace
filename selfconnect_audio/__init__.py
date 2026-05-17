"""
selfconnect-audio — Audio capabilities plugin for SelfConnect.

Provides WASAPI loopback capture, tone fingerprint detection, and (in later
phases) STT, TTS, wake word, and multi-agent voice rooms.

Zero modifications to selfconnect/ or selfconnect-enterprise/.

Usage:
    python -m selfconnect_audio                  # run sidecar
    python -m selfconnect_audio calibrate --tone codex_ready --duration 3
"""

__version__ = "0.1.0"

from .plugin import AudioPlugin
from .bus import AudioEventBus
from .events import (
    ToneDetected,
    SpeechTranscribed,
    WakeWordHeard,
    TTSCompleted,
    CaptureBackendSwitched,
    CaptureDegraded,
)

__all__ = [
    "AudioPlugin",
    "AudioEventBus",
    "ToneDetected",
    "SpeechTranscribed",
    "WakeWordHeard",
    "TTSCompleted",
    "CaptureBackendSwitched",
    "CaptureDegraded",
    "__version__",
]
