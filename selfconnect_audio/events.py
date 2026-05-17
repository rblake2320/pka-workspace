"""
Audio event dataclasses for the selfconnect-audio plugin.

All events are immutable (frozen=True). The event_id field mirrors the
message_id dedup pattern used in SelfConnect's framing layer.
"""

from __future__ import annotations

import dataclasses
import time
import uuid


def _now() -> float:
    return time.time()


def _uid() -> str:
    return str(uuid.uuid4())


@dataclasses.dataclass(frozen=True)
class AudioEvent:
    """Base class for all audio events."""
    timestamp: float = dataclasses.field(default_factory=_now)
    source: str = "audio"
    event_id: str = dataclasses.field(default_factory=_uid)


@dataclasses.dataclass(frozen=True)
class ToneDetected(AudioEvent):
    """A registered tone fingerprint was matched in the system audio stream."""
    fingerprint_name: str = ""       # e.g. "codex_ready"
    frequency_hz: float = 0.0       # dominant frequency of the detected tone
    duration_ms: float = 0.0        # duration of the matched segment
    confidence: float = 0.0         # 0.0–1.0 correlation score


@dataclasses.dataclass(frozen=True)
class SpeechTranscribed(AudioEvent):
    """STT produced a transcription (interim or final)."""
    text: str = ""
    language: str = "en"
    is_final: bool = True
    speaker_id: str | None = None


@dataclasses.dataclass(frozen=True)
class WakeWordHeard(AudioEvent):
    """Wake word detection fired."""
    keyword: str = ""
    confidence: float = 0.0


@dataclasses.dataclass(frozen=True)
class TTSCompleted(AudioEvent):
    """Text-to-speech playback finished."""
    text_spoken: str = ""
    voice_id: str = ""
    duration_ms: float = 0.0


@dataclasses.dataclass(frozen=True)
class CaptureBackendSwitched(AudioEvent):
    """WASAPI capture switched from primary to fallback backend."""
    from_backend: str = ""
    to_backend: str = ""
    reason: str = ""


@dataclasses.dataclass(frozen=True)
class CaptureDegraded(AudioEvent):
    """Capture pipeline has degraded (silent frames, device lost, etc.)."""
    reason: str = ""
    backend: str = ""


def event_to_dict(event: AudioEvent) -> dict:
    """Serialize an audio event to a plain dict for sending over the mesh."""
    d = dataclasses.asdict(event)
    d["event_class"] = type(event).__name__
    return d
