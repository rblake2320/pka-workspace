"""Abstract STTProvider interface (Phase 2 implementations go here)."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable


class STTProvider(ABC):
    """
    Abstract speech-to-text provider.

    Phase 2 implementations: whisper_local.py, openai_realtime.py
    """

    @abstractmethod
    def start(self, on_transcribed: Callable) -> None:
        """Start listening. Call on_transcribed(SpeechTranscribed) for each result."""

    @abstractmethod
    def stop(self) -> None:
        """Stop listening and release resources."""
