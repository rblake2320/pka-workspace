"""
Two-stage tone detector: Goertzel pre-filter → FFT spectral fingerprint match.

Stage 1 — Goertzel pre-filter (cheap, runs on every chunk):
  Computes the energy at each fingerprint's dominant frequency band.
  If no fingerprint has energy above its band threshold, the chunk is dropped.
  Cost: ~O(N) per chunk, minimal CPU.

Stage 2 — FFT spectral fingerprint match (accurate, fires only after Stage 1):
  Extracts the full spectral envelope using a Hann-windowed FFT.
  Correlates against the stored fingerprint using normalized cross-correlation.
  Returns a ToneDetected event if the score exceeds the fingerprint's threshold.
  This catches harmonic signatures, attack/decay shape, and duration —
  a pure Goertzel cannot do this.

Why two stages:
  The Codex "ready" chime is a synthesized tone with harmonics, not a pure sine.
  Goertzel is fast but only checks one frequency — it misses harmonics.
  FFT catches the full signature but is too expensive to run on every chunk.
  Two stages: Goertzel as a fast gate, FFT as the real match.

Fingerprint format (fingerprints.yaml):
  codex_ready:
    sample_rate: 16000
    window_ms: 200
    min_frequency_hz: 400
    max_frequency_hz: 4000
    spectral_envelope: [0.02, 0.05, ...]   # normalized FFT magnitudes
    duration_ms: 450
    threshold: 0.85
    calibrated_at: "2026-05-15T..."
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Callable

import numpy as np
import yaml

from ..events import ToneDetected

log = logging.getLogger(__name__)

# Number of consecutive chunks to accumulate before running the FFT match
# 30ms chunks × 7 = ~210ms window — long enough for most chime sounds
ACCUMULATE_CHUNKS = 7


class ToneDetector:
    """
    Processes PCM audio chunks and fires ToneDetected events on fingerprint matches.

    Usage:
        detector = ToneDetector(fingerprints_path, on_detected)
        # Call process_chunk() from the WASAPI capture thread (or bus subscription)
        detector.process_chunk(np.array([...], dtype=np.float32))
    """

    def __init__(
        self,
        fingerprints_path: str | Path,
        on_detected: Callable[[ToneDetected], None],
    ):
        self._on_detected = on_detected
        self._fingerprints: dict[str, dict] = {}
        self._window_buffer: list[np.ndarray] = []  # accumulates chunks for FFT
        self._hann_cache: dict[int, np.ndarray] = {}  # cached Hann windows

        path = Path(fingerprints_path)
        if path.exists():
            self._load_fingerprints(path)
        else:
            log.warning("Fingerprints file not found: %s — tone detection disabled until calibrated", path)

    @property
    def fingerprints(self) -> dict:
        return dict(self._fingerprints)

    def reload_fingerprints(self, path: str | Path) -> None:
        """Hot-reload fingerprints without restarting the detector."""
        self._load_fingerprints(Path(path))

    def process_chunk(self, chunk: np.ndarray) -> None:
        """
        Process one PCM chunk. Called from the capture thread — must be fast.

        chunk: float32 array of shape (N,), values in [-1.0, 1.0]
        """
        if not self._fingerprints:
            return

        # Stage 1: Goertzel pre-filter — any fingerprint have energy here?
        dominant_freq = self._goertzel_dominant_frequency(chunk)
        matching_names = self._fingerprints_in_band(dominant_freq)
        if not matching_names:
            self._window_buffer.clear()
            return

        # Accumulate chunks for Stage 2
        self._window_buffer.append(chunk)
        if len(self._window_buffer) < ACCUMULATE_CHUNKS:
            return

        # Stage 2: FFT spectral fingerprint match
        window = np.concatenate(self._window_buffer)
        self._window_buffer.clear()

        for name in matching_names:
            fp = self._fingerprints[name]
            score, dom_freq, duration_ms = self._fft_match(window, fp)
            if score >= fp.get("threshold", 0.85):
                log.debug("Tone detected: %r (score=%.3f, freq=%.1f Hz)", name, score, dom_freq)
                self._on_detected(ToneDetected(
                    fingerprint_name=name,
                    frequency_hz=dom_freq,
                    duration_ms=duration_ms,
                    confidence=score,
                ))

    # ── Stage 1: Goertzel pre-filter ───────────────────────────────────────────

    def _goertzel_energy(self, chunk: np.ndarray, target_freq: float, sample_rate: int) -> float:
        """Compute the Goertzel energy at target_freq for the given chunk."""
        N = len(chunk)
        k = round(N * target_freq / sample_rate)
        omega = 2 * np.pi * k / N
        coeff = 2 * np.cos(omega)
        s_prev, s_prev2 = 0.0, 0.0
        for x in chunk:
            s = float(x) + coeff * s_prev - s_prev2
            s_prev2, s_prev = s_prev, s
        power = s_prev2 ** 2 + s_prev ** 2 - coeff * s_prev * s_prev2
        return float(power)

    def _goertzel_dominant_frequency(self, chunk: np.ndarray) -> float:
        """Estimate the dominant frequency in this chunk using a coarse FFT."""
        if len(chunk) < 64:
            return 0.0
        spectrum = np.abs(np.fft.rfft(chunk))
        freqs = np.fft.rfftfreq(len(chunk), d=1.0 / 16000)
        # Ignore DC and sub-100Hz noise
        mask = freqs > 100
        if not mask.any():
            return 0.0
        idx = np.argmax(spectrum[mask])
        return float(freqs[mask][idx])

    def _fingerprints_in_band(self, dominant_freq: float) -> list[str]:
        """Return names of fingerprints whose frequency band contains dominant_freq."""
        if dominant_freq == 0.0:
            return []
        matches = []
        for name, fp in self._fingerprints.items():
            lo = fp.get("min_frequency_hz", 0)
            hi = fp.get("max_frequency_hz", 20000)
            if lo <= dominant_freq <= hi:
                matches.append(name)
        return matches

    # ── Stage 2: FFT spectral fingerprint match ────────────────────────────────

    def _fft_match(
        self, window: np.ndarray, fp: dict
    ) -> tuple[float, float, float]:
        """
        Compute the normalized cross-correlation between the window's spectral
        envelope and the stored fingerprint envelope.

        Returns (score, dominant_freq_hz, duration_ms).
        """
        sample_rate: int = fp.get("sample_rate", 16000)
        lo: float = fp.get("min_frequency_hz", 0.0)
        hi: float = fp.get("max_frequency_hz", sample_rate // 2)
        stored_envelope: list[float] = fp.get("spectral_envelope", [])

        # Apply Hann window to reduce spectral leakage
        n = len(window)
        hann = self._hann_cache.get(n)
        if hann is None:
            hann = np.hanning(n)
            self._hann_cache[n] = hann
        windowed = window * hann

        spectrum = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)

        # Restrict to the fingerprint's frequency band
        band_mask = (freqs >= lo) & (freqs <= hi)
        band_spectrum = spectrum[band_mask]

        # Normalize to [0, 1]
        peak = band_spectrum.max()
        if peak < 1e-9:
            return 0.0, 0.0, 0.0
        band_spectrum = band_spectrum / peak

        dominant_freq = float(freqs[band_mask][np.argmax(band_spectrum)])
        duration_ms = round(n / sample_rate * 1000, 1)

        if not stored_envelope:
            return 0.0, dominant_freq, duration_ms

        # Compare at the same resolution: downsample band_spectrum to 64 points
        # (same as stored fingerprint). Upsampling stored → full res inflates error.
        stored = np.array(stored_envelope, dtype=np.float32)
        n_pts = len(stored)
        if len(band_spectrum) != n_pts:
            indices = np.linspace(0, len(band_spectrum) - 1, n_pts)
            band_spectrum = np.interp(indices, np.arange(len(band_spectrum)), band_spectrum).astype(np.float32)

        # Normalized cross-correlation (Pearson)
        score = float(np.corrcoef(band_spectrum, stored)[0, 1])
        score = max(0.0, min(1.0, score))  # clamp to [0, 1]

        return score, dominant_freq, duration_ms

    # ── Fingerprint I/O ────────────────────────────────────────────────────────

    def _load_fingerprints(self, path: Path) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            self._fingerprints = {k: v for k, v in data.items() if isinstance(v, dict)}
            log.info("Loaded %d tone fingerprint(s) from %s", len(self._fingerprints), path)
        except Exception:
            log.exception("Failed to load fingerprints from %s", path)
            self._fingerprints = {}
