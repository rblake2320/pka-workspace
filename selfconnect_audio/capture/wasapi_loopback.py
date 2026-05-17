"""
WASAPI system audio loopback capture.

Captures everything playing through the default speaker (system output) as
a mono 16 kHz PCM stream. Designed for tone detection and STT input.

Backend priority:
  1. soundcard  — cleanest API, but can return silent frames on some
     Windows/RTX driver configurations (Python 3.11+).
  2. PyAudioWPatch — patches PortAudio directly for WASAPI loopback;
     more reliable on RTX systems but more verbose.

Switching: on startup we record 500ms of audio. If the peak amplitude is
below 0.001 (effectively silent), we switch backends and log which one
is active. This is the difference between 30 minutes of debugging and 2.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable

import numpy as np

log = logging.getLogger(__name__)

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 30
CHUNK_FRAMES = int(SAMPLE_RATE * CHUNK_MS / 1000)  # 480 frames

# Amplitude below which 500ms of audio is considered "silent" (driver bug)
SILENCE_THRESHOLD = 0.001
SILENCE_CHECK_FRAMES = SAMPLE_RATE // 2  # 500ms


class WasapiLoopback:
    """
    Captures system audio output as a streaming PCM source.

    Usage:
        def on_chunk(chunk: np.ndarray):
            ...  # shape: (CHUNK_FRAMES,), dtype float32, range [-1, 1]

        cap = WasapiLoopback(on_chunk)
        cap.start()
        # ...
        cap.stop()
    """

    def __init__(self, on_chunk: Callable[[np.ndarray], None], config: dict | None = None):
        cfg = config or {}
        self._on_chunk = on_chunk
        self._sample_rate: int = cfg.get("sample_rate", SAMPLE_RATE)
        self._chunk_ms: int = cfg.get("chunk_ms", CHUNK_MS)
        self._chunk_frames: int = int(self._sample_rate * self._chunk_ms / 1000)
        self._thread = threading.Thread(target=self._run, name="sc-audio-capture", daemon=True)
        self._stop_event = threading.Event()
        self._backend_name: str = "none"
        self._device_name: str = "unknown"

    # ── Public API ─────────────────────────────────────────────────────────────

    @property
    def backend_name(self) -> str:
        return self._backend_name

    @property
    def device_name(self) -> str:
        return self._device_name

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join(timeout=3.0)

    # ── Backend detection ──────────────────────────────────────────────────────

    @staticmethod
    def _try_soundcard() -> tuple[str, object] | None:
        """Try soundcard loopback. Returns (device_name, recorder_context) or None."""
        try:
            import soundcard as sc
            speaker = sc.default_speaker()
            loopback = speaker.loopback()
            device_name = str(speaker.name)

            # 500ms silence check
            with loopback.recorder(samplerate=SAMPLE_RATE, channels=CHANNELS) as rec:
                chunk = rec.record(numframes=SILENCE_CHECK_FRAMES)
                if chunk.ndim > 1:
                    chunk = chunk[:, 0]
                if np.abs(chunk).max() > SILENCE_THRESHOLD:
                    return device_name, ("soundcard", speaker)
                else:
                    log.warning(
                        "soundcard loopback returned silent frames (peak=%.6f) "
                        "— will try PyAudioWPatch fallback",
                        np.abs(chunk).max(),
                    )
                    return None
        except Exception as exc:
            log.debug("soundcard not available or failed: %s", exc)
            return None

    @staticmethod
    def _try_pyaudiowpatch() -> tuple[str, object] | None:
        """Try PyAudioWPatch loopback. Returns (device_name, pa_instance) or None."""
        try:
            import pyaudiowpatch as pyaudio

            pa = pyaudio.PyAudio()
            # Find the default WASAPI loopback device
            wasapi_info = pa.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers_index = wasapi_info["defaultOutputDevice"]
            device_info = pa.get_device_info_by_index(default_speakers_index)
            device_name = device_info.get("name", "unknown")

            # Verify it opens without error
            stream = pa.open(
                format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=SAMPLE_RATE // 2,
                input_device_index=device_info["loopback_device_info"]["index"],
            )
            stream.close()
            return device_name, ("pyaudiowpatch", pa, device_info)
        except Exception as exc:
            log.debug("pyaudiowpatch not available or failed: %s", exc)
            return None

    # ── Capture loops ──────────────────────────────────────────────────────────

    def _run(self) -> None:
        """Detect backend, then run the appropriate capture loop."""
        backend_info = self._try_soundcard()
        if backend_info:
            device_name, ctx = backend_info
            self._backend_name = "soundcard"
            self._device_name = device_name
            log.info("Audio capture: using soundcard backend (device=%r)", device_name)
            self._run_soundcard(ctx)
            return

        backend_info = self._try_pyaudiowpatch()
        if backend_info:
            device_name, ctx = backend_info
            self._backend_name = "pyaudiowpatch"
            self._device_name = device_name
            log.info("Audio capture: using PyAudioWPatch backend (device=%r)", device_name)
            self._run_pyaudiowpatch(ctx)
            return

        log.error(
            "Audio capture: neither soundcard nor PyAudioWPatch could provide "
            "a working WASAPI loopback stream. Check your audio driver and "
            "that 'Stereo Mix' or loopback is enabled in Windows Sound settings."
        )
        self._backend_name = "failed"

    def _run_soundcard(self, ctx) -> None:
        import soundcard as sc
        _, speaker = ctx
        loopback = speaker.loopback()
        with loopback.recorder(samplerate=self._sample_rate, channels=CHANNELS) as rec:
            while not self._stop_event.is_set():
                chunk = rec.record(numframes=self._chunk_frames)
                if chunk.ndim > 1:
                    chunk = chunk[:, 0]
                self._on_chunk(chunk.astype(np.float32))

    def _run_pyaudiowpatch(self, ctx) -> None:
        import pyaudiowpatch as pyaudio
        _, pa, device_info = ctx
        loopback_idx = device_info["loopback_device_info"]["index"]
        stream = pa.open(
            format=pyaudio.paFloat32,
            channels=CHANNELS,
            rate=self._sample_rate,
            input=True,
            frames_per_buffer=self._chunk_frames,
            input_device_index=loopback_idx,
        )
        try:
            while not self._stop_event.is_set():
                raw = stream.read(self._chunk_frames, exception_on_overflow=False)
                chunk = np.frombuffer(raw, dtype=np.float32)
                self._on_chunk(chunk)
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()
