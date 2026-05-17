"""Tests for audio event dataclasses."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from selfconnect_audio.events import (
    ToneDetected, SpeechTranscribed, WakeWordHeard, TTSCompleted,
    CaptureBackendSwitched, CaptureDegraded, AudioEvent, event_to_dict,
)


class TestAudioEvents:
    def test_tone_detected_defaults(self):
        e = ToneDetected()
        assert e.fingerprint_name == ""
        assert e.confidence == 0.0
        assert e.source == "audio"
        assert e.event_id != ""

    def test_tone_detected_immutable(self):
        import pytest
        e = ToneDetected(fingerprint_name="codex_ready", confidence=0.92)
        with pytest.raises((AttributeError, TypeError)):
            e.confidence = 0.5  # type: ignore

    def test_unique_event_ids(self):
        ids = {ToneDetected().event_id for _ in range(100)}
        assert len(ids) == 100

    def test_timestamps_monotonic(self):
        t1 = ToneDetected().timestamp
        time.sleep(0.01)
        t2 = ToneDetected().timestamp
        assert t2 >= t1

    def test_speech_transcribed(self):
        e = SpeechTranscribed(text="hello", language="en", is_final=True)
        assert e.text == "hello"
        assert e.is_final is True

    def test_wake_word_heard(self):
        e = WakeWordHeard(keyword="hey selfconnect", confidence=0.95)
        assert e.keyword == "hey selfconnect"

    def test_event_to_dict(self):
        e = ToneDetected(fingerprint_name="codex_ready", confidence=0.9)
        d = event_to_dict(e)
        assert d["event_class"] == "ToneDetected"
        assert d["fingerprint_name"] == "codex_ready"
        assert d["confidence"] == 0.9
        assert "timestamp" in d
        assert "event_id" in d

    def test_all_event_types_serializable(self):
        events = [
            ToneDetected(fingerprint_name="x"),
            SpeechTranscribed(text="hi"),
            WakeWordHeard(keyword="yo"),
            TTSCompleted(text_spoken="done"),
            CaptureBackendSwitched(from_backend="soundcard", to_backend="pyaudiowpatch"),
            CaptureDegraded(reason="silent"),
        ]
        for e in events:
            d = event_to_dict(e)
            assert isinstance(d, dict)
            assert "event_class" in d
