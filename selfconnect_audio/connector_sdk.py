"""
SDK-mode connector — integrates the audio plugin with SelfConnect's core SDK.

Uses: build_frame / send_frame (outbound audio events → mesh)
      MessageListener.on() (inbound audio commands ← mesh)

Topic namespace: all audio frames use topic="audio.*"
  audio.tone.detected       ToneDetected events
  audio.speech.transcribed  SpeechTranscribed events
  audio.wakeword.heard      WakeWordHeard events
  audio.tts.completed       TTSCompleted events
  audio.cmd.*               Inbound commands FROM mesh agents

Zero modifications to self_connect.py. This module is a sidecar that
composes the public SDK API, following the pattern in pka_mesh_bridge.py.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Callable

from .bus import AudioEventBus
from .events import AudioEvent, event_to_dict

log = logging.getLogger(__name__)

# Topic prefix for all audio frames
AUDIO_TOPIC_PREFIX = "audio"


class SDKConnector:
    """
    Routes audio events to the SelfConnect mesh and inbound audio commands
    from the mesh to the AudioEventBus.

    Requires:
        send_frame(target, from_hwnd, payload, topic)
        MessageListener(own_hwnd)  with .on(handler)
        list_windows()
        find_target(keyword)
    """

    def __init__(self, context, bus: AudioEventBus):
        self._ctx = context
        self._bus = bus
        self._own_hwnd: int | None = None
        self._listener = None
        self._mode = "sdk"

    @property
    def mode(self) -> str:
        return self._mode

    def start(self) -> None:
        """Discover own window, start MessageListener, subscribe audio events to outbound."""
        if not self._ctx.sdk_available:
            log.warning("SDKConnector: SDK not available — connector inactive")
            return

        self._own_hwnd = self._discover_own_hwnd()
        if self._own_hwnd is None:
            log.warning("SDKConnector: could not discover own HWND — outbound disabled")

        self._start_listener()

        # Subscribe audio events → send to mesh
        self._bus.subscribe("audio.tone.*", self._send_event)
        self._bus.subscribe("audio.speech.*", self._send_event)
        self._bus.subscribe("audio.wakeword.*", self._send_event)
        self._bus.subscribe("audio.tts.*", self._send_event)

        log.info("SDKConnector started (own_hwnd=%s)", self._own_hwnd)

    def close(self) -> None:
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass

    # ── Outbound: audio events → mesh ─────────────────────────────────────────

    def _send_event(self, event: AudioEvent) -> None:
        """Send an audio event to all discovered mesh peers."""
        if self._own_hwnd is None or self._ctx.send_frame is None:
            return

        payload = json.dumps(event_to_dict(event))
        event_class = type(event).__name__.lower().replace("detected", ".detected") \
                       .replace("transcribed", ".transcribed") \
                       .replace("heard", ".heard") \
                       .replace("completed", ".completed")
        topic = f"{AUDIO_TOPIC_PREFIX}.{event_class}"

        try:
            windows = self._ctx.list_windows() if self._ctx.list_windows else []
        except Exception:
            windows = []

        for window in windows:
            hwnd = getattr(window, "hwnd", None) or (window if isinstance(window, int) else None)
            if hwnd and hwnd != self._own_hwnd:
                try:
                    self._ctx.send_frame(hwnd, self._own_hwnd, payload, topic)
                except Exception as exc:
                    log.debug("send_frame to hwnd=%s failed: %s", hwnd, exc)

    # ── Inbound: mesh commands → bus ───────────────────────────────────────────

    def _start_listener(self) -> None:
        """Start MessageListener to receive audio commands from mesh peers."""
        if self._own_hwnd is None:
            return
        try:
            # Import MessageListener lazily (SDK may not be on path at module load time)
            sc = self._import_sc()
            if sc is None:
                return
            self._listener = sc.MessageListener(self._own_hwnd)
            self._listener.on(self._handle_frame)
            self._listener.start()
            log.info("SDKConnector: MessageListener started on hwnd=%s", self._own_hwnd)
        except Exception:
            log.exception("SDKConnector: failed to start MessageListener")

    def _handle_frame(self, frame: dict) -> None:
        """Receive a parsed frame from MessageListener and publish to bus if audio topic."""
        topic = frame.get("topic", "")
        if not topic.startswith(f"{AUDIO_TOPIC_PREFIX}.cmd"):
            return  # not an audio command, ignore
        try:
            payload = json.loads(frame.get("payload", "{}"))
        except json.JSONDecodeError:
            payload = {}
        self._bus.publish(topic, {**payload, "_frame": frame})

    # ── Discovery ──────────────────────────────────────────────────────────────

    def _discover_own_hwnd(self) -> int | None:
        """Find this process's terminal window HWND.

        Priority order:
        1. GetConsoleWindow() — returns the console HWND of the current process.
           Reliable for any process attached to a Windows console (cmd, PowerShell,
           Windows Terminal ConPTY). Returns 0 if no console is attached.
        2. pid match via list_windows() — for processes whose WindowTarget exposes .pid.
        3. No fallback to windows[0] — that would silently return the wrong window.
        """
        # 1. Console window via Win32 (most reliable for terminal sidecars)
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                log.debug("SDKConnector: own HWND via GetConsoleWindow = %s", hwnd)
                return hwnd
        except Exception as exc:
            log.debug("GetConsoleWindow failed: %s", exc)

        # 2. pid match via list_windows()
        try:
            import os
            pid = os.getpid()
            if self._ctx.list_windows is None:
                return None
            windows = self._ctx.list_windows()
            for w in windows:
                w_pid = getattr(w, "pid", None)
                if w_pid == pid:
                    hwnd = getattr(w, "hwnd", None)
                    log.debug("SDKConnector: own HWND via pid match = %s", hwnd)
                    return hwnd
        except Exception as exc:
            log.debug("HWND pid-match discovery failed: %s", exc)

        return None

    def _import_sc(self):
        """Lazy import of self_connect module."""
        try:
            import importlib
            return importlib.import_module("self_connect")
        except ImportError:
            return None
