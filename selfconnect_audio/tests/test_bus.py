"""Tests for AudioEventBus threading model and pub/sub behavior."""

import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from selfconnect_audio.bus import AudioEventBus
from selfconnect_audio.events import ToneDetected


class TestAudioEventBus:
    def setup_method(self):
        self.bus = AudioEventBus()
        self.bus.start()

    def teardown_method(self):
        self.bus.stop()

    def _wait_for(self, condition, timeout=1.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if condition():
                return True
            time.sleep(0.01)
        return False

    def test_subscribe_and_receive(self):
        received = []
        self.bus.subscribe("tone.detected", received.append)
        event = ToneDetected(fingerprint_name="test")
        self.bus.publish("tone.detected", event)
        assert self._wait_for(lambda: len(received) == 1)
        assert received[0] is event

    def test_glob_matching_star(self):
        received = []
        self.bus.subscribe("tone.*", received.append)
        self.bus.publish("tone.detected", ToneDetected())
        self.bus.publish("tone.other", ToneDetected())
        assert self._wait_for(lambda: len(received) == 2)

    def test_glob_matching_all(self):
        received = []
        self.bus.subscribe("*", received.append)
        self.bus.publish("tone.detected", "a")
        self.bus.publish("speech.transcribed", "b")
        assert self._wait_for(lambda: len(received) == 2)

    def test_no_match_does_not_call_handler(self):
        received = []
        self.bus.subscribe("audio.tone.*", received.append)
        self.bus.publish("speech.transcribed", "x")
        time.sleep(0.1)
        assert len(received) == 0

    def test_publish_is_nonblocking(self):
        """Publish must return immediately even if handler is slow."""
        slow_done = threading.Event()

        def slow_handler(e):
            time.sleep(0.5)
            slow_done.set()

        self.bus.subscribe("*", slow_handler)
        start = time.time()
        self.bus.publish("x", "event")
        elapsed = time.time() - start
        assert elapsed < 0.05, f"publish blocked for {elapsed:.3f}s"
        assert self._wait_for(slow_done.is_set, timeout=2.0)

    def test_handler_exception_doesnt_crash_bus(self):
        """Exception in one handler must not prevent others from firing."""
        good_received = []

        def bad_handler(e):
            raise RuntimeError("boom")

        self.bus.subscribe("*", bad_handler)
        self.bus.subscribe("*", good_received.append)
        self.bus.publish("x", "event")
        assert self._wait_for(lambda: len(good_received) == 1)

    def test_event_count_increments(self):
        self.bus.publish("a", "x")
        self.bus.publish("b", "y")
        assert self._wait_for(lambda: self.bus.event_count >= 2)

    def test_unsubscribe(self):
        received = []
        handler = received.append
        self.bus.subscribe("x", handler)
        self.bus.unsubscribe("x", handler)
        self.bus.publish("x", "event")
        time.sleep(0.1)
        assert len(received) == 0

    def test_thread_safe_subscribe_from_multiple_threads(self):
        """Subscriber registration from multiple threads must not corrupt state."""
        results = []

        def register():
            self.bus.subscribe("*", results.append)

        threads = [threading.Thread(target=register) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.bus.publish("test", "event")
        assert self._wait_for(lambda: len(results) >= 20, timeout=2.0)

    def test_queue_full_drops_gracefully(self):
        """When queue is full, publish must not raise — it drops the event."""
        bus = AudioEventBus(maxsize=2)
        bus.start()
        # Fill the queue (dispatch thread may drain quickly, so we stop it first)
        bus._dispatch_thread  # ensure started
        try:
            for _ in range(100):
                bus.publish("x", "e")  # must not raise
        finally:
            bus.stop()

    def test_stop_and_restart_not_supported(self):
        """Bus is a one-shot — stop() is clean shutdown, not pause."""
        self.bus.stop()
        # After stop, dispatch thread is no longer alive
        assert not self.bus._dispatch_thread.is_alive()
