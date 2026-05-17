"""Abstract TTSProvider interface (Phase 3 implementations go here)."""

from __future__ import annotations
from abc import ABC, abstractmethod


class TTSProvider(ABC):
    """
    Abstract text-to-speech provider.

    Phase 3 implementations: elevenlabs_tts.py, coqui_local.py
    """

    @abstractmethod
    def speak(self, text: str, voice_id: str | None = None) -> None:
        """Synthesize and play text. Blocks until playback completes."""

    @abstractmethod
    def stop(self) -> None:
        """Interrupt current playback and release resources."""
