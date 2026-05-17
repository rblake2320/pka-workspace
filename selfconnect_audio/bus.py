"""
AudioEventBus — thread-safe publish/subscribe event bus for the audio plugin.

Threading model:
  - Publishers (WASAPI capture thread, STT thread, etc.) call publish() — NON-BLOCKING.
    Events are placed on a queue.Queue; the caller never waits for dispatch.
  - A single dedicated dispatch thread pulls events from the queue and calls subscribers.
  - Subscriber registration uses a threading.Lock — safe to call from any thread.
  - Subscriber exceptions are caught and logged — they never crash the bus.

Pattern:
  bus = AudioEventBus()
  bus.start()
  bus.subscribe("tone.*", my_handler)    # glob-style topic matching
  bus.subscribe("*", catch_all)
  bus.publish("tone.detected", event)
  bus.stop()
"""

from __future__ import annotations

import fnmatch
import logging
import queue
import threading
from collections import defaultdict
from typing import Callable

log = logging.getLogger(__name__)

_STOP_SENTINEL = object()


class AudioEventBus:
    def __init__(self, maxsize: int = 1000):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._lock = threading.Lock()
        self._queue: queue.Queue = queue.Queue(maxsize=maxsize)
        self._dispatch_thread = threading.Thread(
            target=self._dispatch_loop, name="sc-audio-bus", daemon=True
        )
        self._started = False
        self._event_count = 0

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def start(self) -> None:
        if not self._started:
            self._dispatch_thread.start()
            self._started = True

    def stop(self, timeout: float = 2.0) -> None:
        """Signal the dispatch thread to stop and wait for it."""
        if self._started:
            # Blocking put for the sentinel — queue.Full must not block shutdown
            try:
                self._queue.put(_STOP_SENTINEL, timeout=1.0)
            except queue.Full:
                # Drain the queue so the sentinel can get through
                try:
                    while True:
                        self._queue.get_nowait()
                except queue.Empty:
                    pass
                self._queue.put(_STOP_SENTINEL)
            self._dispatch_thread.join(timeout=timeout)
            self._started = False

    # ── Publisher API ──────────────────────────────────────────────────────────

    def publish(self, topic: str, event) -> None:
        """
        Non-blocking publish. Places the event on the dispatch queue.

        If the queue is full, the event is dropped and a warning is logged.
        The WASAPI capture thread must never block here.
        """
        try:
            self._queue.put_nowait((topic, event))
        except queue.Full:
            log.warning("AudioEventBus queue full — dropping event on topic %r", topic)

    # ── Subscriber API ─────────────────────────────────────────────────────────

    def subscribe(self, pattern: str, handler: Callable) -> None:
        """
        Register a handler for events matching pattern.

        Pattern supports shell-style glob:
          "tone.detected"  — exact match
          "tone.*"         — all tone events
          "*"              — all events
        """
        with self._lock:
            self._subscribers[pattern].append(handler)

    def unsubscribe(self, pattern: str, handler: Callable) -> None:
        with self._lock:
            handlers = self._subscribers.get(pattern, [])
            if handler in handlers:
                handlers.remove(handler)

    # ── Stats ──────────────────────────────────────────────────────────────────

    @property
    def event_count(self) -> int:
        return self._event_count

    @property
    def queue_depth(self) -> int:
        return self._queue.qsize()

    # ── Internal ───────────────────────────────────────────────────────────────

    def _dispatch_loop(self) -> None:
        while True:
            item = self._queue.get()
            if item is _STOP_SENTINEL:
                break
            topic, event = item
            self._event_count += 1
            with self._lock:
                matched = self._match_handlers(topic)
            for handler in matched:
                try:
                    handler(event)
                except Exception:
                    log.exception("AudioEventBus handler %r raised on topic %r", handler, topic)

    def _match_handlers(self, topic: str) -> list[Callable]:
        handlers: list[Callable] = []
        for pattern, hs in self._subscribers.items():
            if fnmatch.fnmatch(topic, pattern):
                handlers.extend(hs)
        return handlers
