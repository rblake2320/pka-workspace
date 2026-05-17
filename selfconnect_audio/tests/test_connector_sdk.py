"""Tests for SDKConnector (mocks the SelfConnect SDK public API)."""

import sys
import json
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from selfconnect_audio.bus import AudioEventBus
from selfconnect_audio.events import ToneDetected, event_to_dict
from selfconnect_audio.connector_sdk import SDKConnector


def _make_context(windows=None, send_frame=None, list_windows=None):
    ctx = MagicMock()
    ctx.sdk_available = True
    ctx.enterprise_available = False

    mock_window = MagicMock()
    mock_window.hwnd = 1001
    mock_window.pid = 9999

    ctx.list_windows = list_windows or (lambda: [mock_window])
    ctx.send_frame = send_frame or MagicMock()
    ctx.find_target = MagicMock()
    ctx.build_frame = MagicMock()
    ctx.config = {}
    return ctx


class TestSDKConnectorOutbound:
    def test_tone_event_triggers_send_frame(self):
        """ToneDetected events on bus should call send_frame for mesh peers."""
        sent = []
        ctx = _make_context(send_frame=lambda hwnd, own, payload, topic: sent.append((hwnd, topic)))
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)

        # Patch _discover_own_hwnd to return a known hwnd
        connector._own_hwnd = 2000
        bus.subscribe("audio.tone.*", connector._send_event)

        event = ToneDetected(fingerprint_name="codex_ready", confidence=0.95)
        bus.publish("audio.tone.detected", event)

        deadline = time.time() + 1.0
        while time.time() < deadline and not sent:
            time.sleep(0.01)

        bus.stop()
        assert len(sent) >= 1
        hwnd, topic = sent[0]
        assert hwnd == 1001   # the mock window's hwnd
        assert "audio" in topic

    def test_no_send_when_sdk_unavailable(self):
        """If sdk_available is False, start() should not crash or send."""
        ctx = _make_context()
        ctx.sdk_available = False
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)
        connector.start()  # should not raise
        bus.stop()

    def test_send_frame_exception_doesnt_crash(self):
        """send_frame raising should be caught and logged, not propagated."""
        def bad_send(*args, **kwargs):
            raise RuntimeError("network error")

        ctx = _make_context(send_frame=bad_send)
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)
        connector._own_hwnd = 2000
        bus.subscribe("audio.tone.*", connector._send_event)

        event = ToneDetected(fingerprint_name="x")
        bus.publish("audio.tone.detected", event)
        time.sleep(0.1)  # should not raise
        bus.stop()


class TestSDKConnectorInbound:
    def test_audio_cmd_frame_published_to_bus(self):
        """Inbound frame with audio.cmd topic should be published to bus."""
        ctx = _make_context()
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)

        received = []
        bus.subscribe("audio.cmd.*", received.append)

        # Simulate a frame arriving from MessageListener
        frame = {
            "topic": "audio.cmd.speak",
            "payload": json.dumps({"text": "hello from agent A"}),
            "message_id": "abc123",
        }
        connector._handle_frame(frame)

        deadline = time.time() + 1.0
        while time.time() < deadline and not received:
            time.sleep(0.01)

        bus.stop()
        assert len(received) == 1
        assert received[0]["text"] == "hello from agent A"

    def test_non_audio_frame_ignored(self):
        """Frames with non-audio topics must not be published to bus."""
        ctx = _make_context()
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)

        received = []
        bus.subscribe("*", received.append)

        frame = {
            "topic": "mesh.heartbeat",
            "payload": "{}",
            "message_id": "xyz",
        }
        connector._handle_frame(frame)
        time.sleep(0.1)
        bus.stop()
        assert len(received) == 0

    def test_invalid_json_payload_handled(self):
        """Invalid JSON payload in inbound frame must not raise."""
        ctx = _make_context()
        bus = AudioEventBus()
        bus.start()
        connector = SDKConnector(ctx, bus)

        frame = {"topic": "audio.cmd.speak", "payload": "not-json", "message_id": "1"}
        connector._handle_frame(frame)  # must not raise
        bus.stop()


class TestAutoConnector:
    def test_auto_picks_sdk_when_enterprise_unavailable(self):
        from selfconnect_audio.connector_auto import make_connector, SDKConnector
        ctx = _make_context()
        ctx.sdk_available = True
        ctx.enterprise_available = False
        bus = AudioEventBus()
        bus.start()
        conn = make_connector(ctx, bus, forced_mode="auto")
        bus.stop()
        assert isinstance(conn, SDKConnector)

    def test_auto_returns_null_when_nothing_available(self):
        from selfconnect_audio.connector_auto import make_connector, NullConnector
        ctx = _make_context()
        ctx.sdk_available = False
        ctx.enterprise_available = False
        bus = AudioEventBus()
        bus.start()
        conn = make_connector(ctx, bus, forced_mode="auto")
        bus.stop()
        assert isinstance(conn, NullConnector)

    def test_forced_sdk_mode(self):
        from selfconnect_audio.connector_auto import make_connector, SDKConnector
        ctx = _make_context()
        ctx.sdk_available = True
        ctx.enterprise_available = True
        bus = AudioEventBus()
        bus.start()
        conn = make_connector(ctx, bus, forced_mode="sdk")
        bus.stop()
        assert isinstance(conn, SDKConnector)
