"""
Enterprise-mode connector — integrates the audio plugin with selfconnect-enterprise.

Uses: send_data(target_hwnd, payload)   — WM_COPYDATA transport (up to 64KB, atomic)
      CopyDataListener.register()        — receive audio commands
      stamp_birth_tag()                  — register in enterprise mesh discovery
      discover_mesh()                    — find peers to notify

Data type constant: 0x5C10 ("SelfConnect Audio" — arbitrary, must be unique)

Zero modifications to selfconnect-enterprise/. Composes enterprise public API only.
"""

from __future__ import annotations

import json
import logging

from .bus import AudioEventBus
from .events import AudioEvent, event_to_dict

log = logging.getLogger(__name__)

SC_AUDIO_DATA_TYPE = 0x5C10   # WM_COPYDATA dwData tag for audio plugin
AUDIO_TOPIC_PREFIX = "audio"


class EnterpriseConnector:
    """
    Routes audio events via the enterprise WM_COPYDATA transport and
    registers the audio sidecar in the enterprise mesh.
    """

    def __init__(self, context, bus: AudioEventBus):
        self._ctx = context
        self._bus = bus
        self._listener = None
        self._mode = "enterprise"

    @property
    def mode(self) -> str:
        return self._mode

    def start(self) -> None:
        if not self._ctx.enterprise_available:
            log.warning("EnterpriseConnector: enterprise not available — connector inactive")
            return

        self._start_listener()
        self._register_birth_tag()

        # Subscribe audio events → send to mesh peers
        self._bus.subscribe("audio.tone.*", self._send_event)
        self._bus.subscribe("audio.speech.*", self._send_event)
        self._bus.subscribe("audio.wakeword.*", self._send_event)
        self._bus.subscribe("audio.tts.*", self._send_event)

        log.info("EnterpriseConnector started")

    def close(self) -> None:
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass

    # ── Outbound ───────────────────────────────────────────────────────────────

    def _send_event(self, event: AudioEvent) -> None:
        if self._ctx.send_data is None or self._ctx.discover_mesh is None:
            return
        payload = event_to_dict(event)
        try:
            peers = self._ctx.discover_mesh()
        except Exception:
            peers = []
        for peer in peers:
            hwnd = getattr(peer, "hwnd", None)
            if hwnd:
                try:
                    self._ctx.send_data(hwnd, payload)
                except Exception as exc:
                    log.debug("EnterpriseConnector send_data to hwnd=%s failed: %s", hwnd, exc)

    # ── Inbound ────────────────────────────────────────────────────────────────

    def _start_listener(self) -> None:
        try:
            from selfconnect_enterprise.enterprise.transport import CopyDataListener
            self._listener = CopyDataListener()
            self._listener.register(SC_AUDIO_DATA_TYPE, self._handle_message)
            self._listener.start()
            log.info("EnterpriseConnector: CopyDataListener started (dtype=0x%04X)", SC_AUDIO_DATA_TYPE)
        except Exception:
            log.exception("EnterpriseConnector: failed to start CopyDataListener")

    def _handle_message(self, sender_hwnd: int, payload: dict) -> None:
        """Receive a WM_COPYDATA message and publish to bus if it's an audio command."""
        msg_type = payload.get("type", "")
        if msg_type.startswith(f"{AUDIO_TOPIC_PREFIX}.cmd"):
            self._bus.publish(msg_type, {**payload, "_sender_hwnd": sender_hwnd})

    def _register_birth_tag(self) -> None:
        if self._ctx.stamp_birth_tag is None:
            return
        try:
            self._ctx.stamp_birth_tag(
                agent_id="audio-sidecar",
                agent_type="audio",
                model="selfconnect-audio",
            )
            log.info("EnterpriseConnector: birth tag stamped (agent_id=audio-sidecar)")
        except Exception as exc:
            log.debug("stamp_birth_tag failed (non-critical): %s", exc)
