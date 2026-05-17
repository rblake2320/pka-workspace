"""Tests for ToneDetector: Goertzel pre-filter and FFT spectral fingerprint match."""

import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from selfconnect_audio.capture.tone_detector import ToneDetector, ACCUMULATE_CHUNKS
from selfconnect_audio.events import ToneDetected


SAMPLE_RATE = 16000
CHUNK_SIZE = 480  # 30ms


def _make_tone(freq: float, duration_s: float, amplitude: float = 0.8) -> np.ndarray:
    """Generate a pure sine wave."""
    t = np.linspace(0, duration_s, int(SAMPLE_RATE * duration_s), endpoint=False)
    return (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def _make_fingerprint(freq: float, sample_rate: int = SAMPLE_RATE) -> dict:
    """Build a synthetic fingerprint from a known tone."""
    duration = ACCUMULATE_CHUNKS * CHUNK_SIZE / sample_rate
    tone = _make_tone(freq, duration)
    hann = np.hanning(len(tone))
    spectrum = np.abs(np.fft.rfft(tone * hann))
    freqs = np.fft.rfftfreq(len(tone), d=1.0 / sample_rate)
    lo, hi = max(100, freq / 4), min(sample_rate // 2, freq * 4)
    mask = (freqs >= lo) & (freqs <= hi)
    band = spectrum[mask]
    peak = band.max()
    if peak > 1e-9:
        band = band / peak
    indices = np.linspace(0, len(band) - 1, 64)
    envelope = np.interp(indices, np.arange(len(band)), band)
    return {
        "sample_rate": sample_rate,
        "window_ms": int(duration * 1000),
        "min_frequency_hz": float(lo),
        "max_frequency_hz": float(hi),
        "spectral_envelope": [round(float(x), 6) for x in envelope],
        "duration_ms": round(duration * 1000, 1),
        "threshold": 0.80,
        "calibrated_at": "2026-05-15T00:00:00Z",
    }


def _make_detector_with_fp(freq: float, tmpdir: Path):
    fp = {"test_tone": _make_fingerprint(freq)}
    fp_path = tmpdir / "fps.yaml"
    with open(fp_path, "w") as f:
        yaml.dump(fp, f)
    detected = []
    detector = ToneDetector(fp_path, detected.append)
    return detector, detected


class TestToneDetectorGoertzel:
    def test_prefilter_passes_matching_freq(self):
        """Dominant frequency within fingerprint band should pass the prefilter."""
        freq = 1000.0
        fp = {"test": _make_fingerprint(freq)}
        with tempfile.TemporaryDirectory() as td:
            fp_path = Path(td) / "fp.yaml"
            with open(fp_path, "w") as f:
                yaml.dump(fp, f)
            detector = ToneDetector(fp_path, lambda e: None)
            # Generate a tone at the target freq
            chunk = _make_tone(freq, CHUNK_SIZE / SAMPLE_RATE)
            matches = detector._fingerprints_in_band(
                detector._goertzel_dominant_frequency(chunk)
            )
            assert "test" in matches

    def test_prefilter_rejects_silence(self):
        """Silent chunks should not pass the prefilter."""
        freq = 1000.0
        fp = {"test": _make_fingerprint(freq)}
        with tempfile.TemporaryDirectory() as td:
            fp_path = Path(td) / "fp.yaml"
            with open(fp_path, "w") as f:
                yaml.dump(fp, f)
            detector = ToneDetector(fp_path, lambda e: None)
            silent = np.zeros(CHUNK_SIZE, dtype=np.float32)
            dom_freq = detector._goertzel_dominant_frequency(silent)
            matches = detector._fingerprints_in_band(dom_freq)
            assert "test" not in matches


class TestToneDetectorFFT:
    def test_matching_tone_fires_event(self):
        """A known synthetic tone should match its own fingerprint."""
        freq = 880.0
        with tempfile.TemporaryDirectory() as td:
            detector, detected = _make_detector_with_fp(freq, Path(td))
            tone = _make_tone(freq, ACCUMULATE_CHUNKS * CHUNK_SIZE / SAMPLE_RATE)
            chunks = np.array_split(tone, ACCUMULATE_CHUNKS)
            for chunk in chunks:
                detector.process_chunk(chunk.astype(np.float32))
            assert len(detected) >= 1
            assert isinstance(detected[0], ToneDetected)
            assert detected[0].fingerprint_name == "test_tone"
            assert detected[0].confidence >= 0.80

    def test_different_tone_does_not_fire(self):
        """A tone at a very different frequency should not match the fingerprint."""
        target_freq = 880.0
        wrong_freq = 4000.0
        with tempfile.TemporaryDirectory() as td:
            detector, detected = _make_detector_with_fp(target_freq, Path(td))
            tone = _make_tone(wrong_freq, ACCUMULATE_CHUNKS * CHUNK_SIZE / SAMPLE_RATE)
            chunks = np.array_split(tone, ACCUMULATE_CHUNKS)
            for chunk in chunks:
                detector.process_chunk(chunk.astype(np.float32))
            assert len(detected) == 0

    def test_silence_does_not_fire(self):
        """Silent frames should never fire ToneDetected."""
        with tempfile.TemporaryDirectory() as td:
            detector, detected = _make_detector_with_fp(440.0, Path(td))
            for _ in range(ACCUMULATE_CHUNKS * 3):
                detector.process_chunk(np.zeros(CHUNK_SIZE, dtype=np.float32))
            assert len(detected) == 0

    def test_empty_fingerprints_no_crash(self):
        """Detector with no fingerprints must not crash."""
        with tempfile.TemporaryDirectory() as td:
            fp_path = Path(td) / "empty.yaml"
            with open(fp_path, "w") as f:
                f.write("# empty\n")
            detector = ToneDetector(fp_path, lambda e: None)
            for _ in range(10):
                chunk = np.random.randn(CHUNK_SIZE).astype(np.float32) * 0.1
                detector.process_chunk(chunk)  # must not raise

    def test_missing_fingerprints_file_no_crash(self):
        """Missing fingerprints file must not crash the detector."""
        detector = ToneDetector("/nonexistent/path/fps.yaml", lambda e: None)
        assert detector.fingerprints == {}
        detector.process_chunk(np.zeros(CHUNK_SIZE, dtype=np.float32))  # no crash

    def test_reload_fingerprints(self):
        """Hot-reload should update the fingerprint dict without restarting."""
        freq = 660.0
        with tempfile.TemporaryDirectory() as td:
            detector, detected = _make_detector_with_fp(freq, Path(td))
            assert "test_tone" in detector.fingerprints

            # Add a second fingerprint
            new_fp = dict(detector.fingerprints)
            new_fp["extra_tone"] = _make_fingerprint(freq * 2)
            fp_path = Path(td) / "fps.yaml"
            with open(fp_path, "w") as f:
                yaml.dump(new_fp, f)
            detector.reload_fingerprints(fp_path)
            assert "extra_tone" in detector.fingerprints


class TestToneDetectorFftMath:
    def test_fft_match_perfect_correlation(self):
        """A fingerprint matched against itself should score ~1.0."""
        freq = 440.0
        fp = _make_fingerprint(freq)
        with tempfile.TemporaryDirectory() as td:
            fp_path = Path(td) / "fp.yaml"
            with open(fp_path, "w") as f:
                yaml.dump({"t": fp}, f)
            detector = ToneDetector(fp_path, lambda e: None)
            # Use the exact same audio that generated the fingerprint
            duration = ACCUMULATE_CHUNKS * CHUNK_SIZE / SAMPLE_RATE
            tone = _make_tone(freq, duration)
            score, dom_freq, duration_ms = detector._fft_match(tone, fp)
            assert score > 0.90, f"Expected score > 0.90, got {score:.3f}"

    def test_fft_match_empty_envelope(self):
        """Fingerprint with empty envelope must return score=0.0, no crash."""
        fp = _make_fingerprint(440.0)
        fp["spectral_envelope"] = []
        with tempfile.TemporaryDirectory() as td:
            fp_path = Path(td) / "fp.yaml"
            with open(fp_path, "w") as f:
                yaml.dump({"t": fp}, f)
            detector = ToneDetector(fp_path, lambda e: None)
            tone = _make_tone(440.0, 0.2)
            score, _, _ = detector._fft_match(tone, fp)
            assert score == 0.0
