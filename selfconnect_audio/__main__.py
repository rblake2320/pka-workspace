"""
selfconnect-audio CLI entry point.

Commands:
  python -m selfconnect_audio                          run sidecar (default)
  python -m selfconnect_audio run                      run sidecar
  python -m selfconnect_audio calibrate                calibrate a tone fingerprint
    --tone <name>    name to store under (e.g. codex_ready)
    --duration <N>   seconds to record (default: 3)
    --config <path>  config file (default: audio_config.yaml)
  python -m selfconnect_audio status                   print health status and exit

Environment variables:
  SELFCONNECT_AUDIO_CONFIG   path to config YAML (overrides default)
"""

from __future__ import annotations

import argparse
import datetime
import logging
import signal
import sys
import time
from pathlib import Path

import numpy as np
import yaml

# Ensure parent dir is importable
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
for p in [str(_ROOT), str(_ROOT / "selfconnect"), str(_ROOT / "selfconnect-enterprise")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from .config import load_config
from .bus import AudioEventBus
from .health import HealthCheck
from .events import ToneDetected


def cmd_run(args) -> None:
    """Start the audio sidecar."""
    cfg = load_config(args.config)

    level = getattr(logging, cfg.get("log_level", "INFO").upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    log = logging.getLogger("selfconnect_audio")

    log.info("selfconnect-audio v%s starting", _version())

    # Build a minimal PluginContext from what's available at runtime
    context = _build_context(cfg)

    from .plugin import AudioPlugin
    plugin = AudioPlugin()
    plugin.initialize(context)

    # Graceful shutdown on Ctrl+C / SIGTERM
    def _shutdown(sig, frame):
        log.info("Shutting down...")
        plugin.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    log.info("Running. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)


def cmd_calibrate(args) -> None:
    """Record audio and write a tone fingerprint to fingerprints.yaml."""
    cfg = load_config(args.config)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")

    tone_name: str = args.tone
    duration: int = args.duration

    cap_cfg = cfg.get("capture", {})
    sample_rate: int = cap_cfg.get("sample_rate", 16000)
    fp_file = Path(
        cfg.get("capture", {}).get("tone_detection", {}).get(
            "fingerprints", str(_HERE / "capture" / "fingerprints.yaml")
        )
    )
    if not fp_file.is_absolute():
        fp_file = _HERE / fp_file

    print(f"\n[calibrate] Tone name:   {tone_name!r}")
    print(f"[calibrate] Record time: {duration}s")
    print(f"[calibrate] Output:      {fp_file}")
    print()
    print("Get ready — recording starts in 3 seconds.")
    print("Trigger the sound you want to fingerprint during the recording window.\n")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  Recording now!")

    # Capture audio
    frames: list[np.ndarray] = []
    capture_done = [False]

    def on_chunk(chunk: np.ndarray):
        if not capture_done[0]:
            frames.append(chunk.copy())

    from .capture.wasapi_loopback import WasapiLoopback
    cap = WasapiLoopback(on_chunk, cap_cfg)
    cap.start()
    time.sleep(duration)
    capture_done[0] = True
    cap.stop()

    if cap.backend_name == "failed":
        print("\n[calibrate] ERROR: No WASAPI loopback backend available.")
        print("  Check that your audio driver supports loopback recording.")
        sys.exit(1)

    if not frames:
        print("\n[calibrate] ERROR: No audio captured. Check your audio device.")
        sys.exit(1)

    audio = np.concatenate(frames)
    peak = float(np.abs(audio).max())
    print(f"\n  Captured {len(audio)} samples ({len(audio)/sample_rate:.1f}s), peak={peak:.4f}")

    if peak < 0.001:
        print("\n[calibrate] WARNING: Audio appears silent. Make sure the sound played during recording.")
        print("  The fingerprint will be saved but tone detection may not work.")

    # Compute spectral fingerprint
    fp_cfg = cfg.get("capture", {}).get("tone_detection", {})
    min_freq = 100.0
    max_freq = float(sample_rate // 2)

    hann = np.hanning(len(audio))
    spectrum = np.abs(np.fft.rfft(audio * hann))
    freqs = np.fft.rfftfreq(len(audio), d=1.0 / sample_rate)

    band_mask = (freqs >= min_freq) & (freqs <= max_freq)
    band_spectrum = spectrum[band_mask]
    band_freqs = freqs[band_mask]

    # Normalize
    peak_s = band_spectrum.max()
    if peak_s > 1e-9:
        band_spectrum = band_spectrum / peak_s

    # Find dominant frequency and band
    dom_idx = int(np.argmax(band_spectrum))
    dom_freq = float(band_freqs[dom_idx])
    # Narrow the fingerprint band to ±2 octaves around dominant
    fp_min = max(min_freq, dom_freq / 4)
    fp_max = min(max_freq, dom_freq * 4)

    # Resample envelope to 64 points for compact storage
    narrow_mask = (band_freqs >= fp_min) & (band_freqs <= fp_max)
    narrow_spectrum = band_spectrum[narrow_mask]
    if len(narrow_spectrum) == 0:
        narrow_spectrum = band_spectrum
    target_len = 64
    indices = np.linspace(0, len(narrow_spectrum) - 1, target_len)
    envelope = np.interp(indices, np.arange(len(narrow_spectrum)), narrow_spectrum)
    envelope_list = [round(float(x), 6) for x in envelope]

    duration_ms = round(len(audio) / sample_rate * 1000, 1)

    fingerprint = {
        "sample_rate": sample_rate,
        "window_ms": round(duration * 1000),
        "min_frequency_hz": round(fp_min, 1),
        "max_frequency_hz": round(fp_max, 1),
        "spectral_envelope": envelope_list,
        "duration_ms": duration_ms,
        "threshold": fp_cfg.get("min_confidence", 0.85),
        "calibrated_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    # Load existing fingerprints and merge
    existing: dict = {}
    if fp_file.exists():
        with open(fp_file, encoding="utf-8") as f:
            content = yaml.safe_load(f)
            if isinstance(content, dict):
                existing = {k: v for k, v in content.items() if isinstance(v, dict)}

    existing[tone_name] = fingerprint

    fp_file.parent.mkdir(parents=True, exist_ok=True)
    with open(fp_file, "w", encoding="utf-8") as f:
        yaml.dump(existing, f, default_flow_style=False, allow_unicode=True, sort_keys=True)

    print(f"\n  Dominant frequency: {dom_freq:.1f} Hz")
    print(f"  Fingerprint band:   {fp_min:.0f}–{fp_max:.0f} Hz")
    print(f"  Duration:           {duration_ms:.0f}ms")
    print(f"\n[calibrate] Fingerprint {tone_name!r} saved to {fp_file}")
    print(f"  Run 'python -m selfconnect_audio' to start listening.")


def cmd_status(args) -> None:
    """Print health status from a running sidecar via named pipe."""
    import json
    pipe_name = r"\\.\pipe\selfconnect-audio-health"
    try:
        import win32file
        handle = win32file.CreateFile(
            pipe_name, 0x80000000, 0, None, 3, 0, None
        )
        _, data = win32file.ReadFile(handle, 4096)
        win32file.CloseHandle(handle)
        status = json.loads(data)
        for key, value in status.items():
            print(f"  {key}: {value}")
    except ImportError:
        print("win32file not available — install pywin32 to query health pipe")
    except Exception as exc:
        print(f"Could not connect to health pipe: {exc}")
        print("Is the sidecar running? (python -m selfconnect_audio)")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _version() -> str:
    try:
        from . import __version__
        return __version__
    except Exception:
        return "unknown"


def _build_context(cfg: dict):
    """Build a PluginContext by probing available SelfConnect layers."""
    sdk_available = False
    enterprise_available = False
    sc_module = None
    ent_module = None

    try:
        import self_connect as sc_module  # type: ignore
        sdk_available = True
    except ImportError:
        pass

    try:
        from selfconnect_enterprise.enterprise import registry as ent_module  # type: ignore
        enterprise_available = True
    except ImportError:
        pass

    try:
        from selfconnect_plugins import PluginContext
    except ImportError:
        sys.path.insert(0, str(_ROOT))
        from selfconnect_plugins import PluginContext

    return PluginContext(
        sdk_available=sdk_available,
        enterprise_available=enterprise_available,
        list_windows=getattr(sc_module, "list_windows", None),
        find_target=getattr(sc_module, "find_target", None),
        send_frame=getattr(sc_module, "send_frame", None),
        build_frame=getattr(sc_module, "build_frame", None),
        get_text_uia=getattr(sc_module, "get_text_uia", None),
        send_data=getattr(ent_module, "send_data", None),
        discover_mesh=getattr(ent_module, "discover_mesh", None),
        stamp_birth_tag=getattr(ent_module, "stamp_birth_tag", None),
        edition="enterprise" if enterprise_available else "standard",
        config=cfg,
    )


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m selfconnect_audio",
        description="SelfConnect audio capabilities sidecar",
    )
    parser.add_argument("--config", default=None, help="Path to audio_config.yaml")
    sub = parser.add_subparsers(dest="command")

    # run (default)
    sub.add_parser("run", help="Start the audio sidecar (default)")

    # calibrate
    cal = sub.add_parser("calibrate", help="Record and fingerprint a tone")
    cal.add_argument("--tone", required=True, help="Fingerprint name (e.g. codex_ready)")
    cal.add_argument("--duration", type=int, default=3, help="Recording duration in seconds")

    # status
    sub.add_parser("status", help="Print health status of running sidecar")

    args = parser.parse_args()

    if args.command == "calibrate":
        cmd_calibrate(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()
