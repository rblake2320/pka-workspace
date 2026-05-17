"""
AudioPlugin — SelfConnect audio capabilities plugin.

Implements the SelfConnectPlugin contract from selfconnect_plugins.
Composes WASAPI loopback, tone detection, bus, and connector without
touching the SelfConnect core SDK or enterprise layer.

Tier: standard (all capabilities except voice_room)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)

# Allow selfconnect_plugins to be imported regardless of working directory
_HERE = Path(__file__).resolve().parent
_PLUGINS_PKG = _HERE.parent / "selfconnect_plugins"
if str(_PLUGINS_PKG.parent) not in sys.path:
    sys.path.insert(0, str(_PLUGINS_PKG.parent))

from selfconnect_plugins import SelfConnectPlugin, PluginContext  # noqa: E402

from .bus import AudioEventBus  # noqa: E402
from .health import HealthCheck  # noqa: E402
from .connector_auto import make_connector  # noqa: E402


class AudioPlugin(SelfConnectPlugin):
    name = "audio"
    version = "0.1.0"
    required_tier = "standard"

    def initialize(self, context: PluginContext) -> None:
        self._ctx = context
        cfg = context.config

        # Core event bus
        self._bus = AudioEventBus()
        self._bus.start()

        # Health
        self._health = HealthCheck()

        # Capture + tone detection (Phase 1 — always on if capture enabled)
        self._capture = None
        self._tone_detector = None
        # Config structure: capture.enabled (not capabilities.capture)
        capture_enabled = cfg.get("capture", {}).get("enabled", True)

        if capture_enabled:
            self._start_capture(context.config)

        # Connector — auto-detect SDK vs enterprise
        forced_mode = context.config.get("connector", "auto")
        self._connector = make_connector(context, self._bus, forced_mode=forced_mode)
        self._connector.start()

        # Wire health references
        self._health.attach(
            capture=self._capture,
            tone_detector=self._tone_detector,
            bus=self._bus,
            connector_mode=self._connector.mode,
        )

        if context.config.get("health", {}).get("pipe_enabled", True):
            self._health.start_pipe_server()

        self._health.print_status()

    def on_event(self, event: dict) -> None:
        """React to inbound mesh events (audio commands from other agents)."""
        topic = event.get("type", event.get("topic", ""))
        if topic.startswith("audio.cmd"):
            self._bus.publish(topic, event)

    def shutdown(self) -> None:
        if self._capture:
            self._capture.stop()
        self._connector.close()
        self._bus.stop()
        self._health.stop_pipe_server()
        log.info("AudioPlugin shut down")

    # ── Internal ───────────────────────────────────────────────────────────────

    def _start_capture(self, cfg: dict) -> None:
        from .capture.wasapi_loopback import WasapiLoopback
        from .capture.tone_detector import ToneDetector
        from .events import ToneDetected

        audio_cfg = cfg if isinstance(cfg, dict) else {}
        tone_cfg = audio_cfg.get("capture", {}).get("tone_detection", {})
        default_fp = str(_HERE / "capture" / "fingerprints.yaml")
        fp_path_raw = tone_cfg.get("fingerprints", default_fp)
        # Resolve relative paths against the config file location if known,
        # otherwise against the package directory.
        config_dir = Path(audio_cfg.get("_config_dir", str(_HERE)))
        fp_path = Path(fp_path_raw) if Path(fp_path_raw).is_absolute() else config_dir / fp_path_raw

        def on_tone(event: ToneDetected):
            self._bus.publish("audio.tone.detected", event)

        self._tone_detector = ToneDetector(fp_path, on_tone)

        def on_chunk(chunk):
            self._tone_detector.process_chunk(chunk)

        self._capture = WasapiLoopback(on_chunk, cfg.get("capture", {}))
        self._capture.start()
        log.info("AudioPlugin: WASAPI capture started")
