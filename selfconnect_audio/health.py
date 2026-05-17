"""
Health check for the selfconnect-audio sidecar.

Provides:
  - health.status()  → dict  (always available, no deps)
  - HealthServer     → exposes status via a Windows named pipe (queryable by other tools)

When WASAPI silently fails to enumerate the loopback device, the health dict
shows capture_active=False and the backend name, cutting debug time significantly.

Named pipe: \\\\.\\pipe\\selfconnect-audio-health
Query with: python -c "import json,win32pipe,win32file; h=win32file.CreateFile(r'\\\\.\\pipe\\selfconnect-audio-health',0x80000000,0,None,3,0,None); print(json.loads(win32file.ReadFile(h,4096)[1]))"
"""

from __future__ import annotations

import json
import logging
import threading
import time
from typing import TYPE_CHECKING

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .bus import AudioEventBus
    from .capture.wasapi_loopback import WasapiLoopback
    from .capture.tone_detector import ToneDetector


class HealthCheck:
    """Collects and returns the audio plugin's runtime health."""

    PIPE_NAME = r"\\.\pipe\selfconnect-audio-health"

    def __init__(self):
        self._start_time = time.time()
        self._capture: WasapiLoopback | None = None
        self._tone_detector: ToneDetector | None = None
        self._bus: AudioEventBus | None = None
        self._connector_mode: str = "none"
        self._pipe_server: _PipeServer | None = None

    def attach(
        self,
        capture=None,
        tone_detector=None,
        bus=None,
        connector_mode: str = "none",
    ) -> None:
        """Wire up references after components are initialized."""
        self._capture = capture
        self._tone_detector = tone_detector
        self._bus = bus
        self._connector_mode = connector_mode

    def status(self) -> dict:
        capture = self._capture
        tone = self._tone_detector
        bus = self._bus

        return {
            "status": "running",
            "uptime_seconds": round(time.time() - self._start_time, 1),
            "capture_backend": getattr(capture, "backend_name", "none"),
            "capture_active": getattr(capture, "is_alive", lambda: False)(),
            "capture_device": getattr(capture, "device_name", "unknown"),
            "fingerprints_loaded": len(getattr(tone, "fingerprints", {})),
            "events_fired": getattr(bus, "event_count", 0),
            "bus_queue_depth": getattr(bus, "queue_depth", 0),
            "connector": self._connector_mode,
        }

    def print_status(self) -> None:
        s = self.status()
        print(
            f"[selfconnect-audio] status=running | "
            f"backend={s['capture_backend']} active={s['capture_active']} "
            f"device={s['capture_device']!r} | "
            f"fingerprints={s['fingerprints_loaded']} | "
            f"events={s['events_fired']} | "
            f"connector={s['connector']}"
        )

    def start_pipe_server(self) -> None:
        """Start a named-pipe server so other processes can query health."""
        try:
            self._pipe_server = _PipeServer(self.PIPE_NAME, self.status)
            self._pipe_server.start()
            log.info("Health pipe listening at %s", self.PIPE_NAME)
        except Exception:
            log.warning("Could not start health pipe server (win32pipe not available?)")

    def stop_pipe_server(self) -> None:
        if self._pipe_server:
            self._pipe_server.stop()


class _PipeServer:
    """Minimal Windows named-pipe server that serves one JSON response per connection."""

    def __init__(self, pipe_name: str, status_fn):
        self._pipe_name = pipe_name
        self._status_fn = status_fn
        self._thread = threading.Thread(target=self._serve, name="sc-audio-health-pipe", daemon=True)
        self._running = False

    def start(self) -> None:
        self._running = True
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _serve(self) -> None:
        try:
            import win32pipe
            import win32file
            import pywintypes
        except ImportError:
            log.debug("win32pipe not available — health pipe server disabled")
            return

        while self._running:
            try:
                pipe = win32pipe.CreateNamedPipe(
                    self._pipe_name,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                    1, 65536, 65536, 0, None,
                )
                win32pipe.ConnectNamedPipe(pipe, None)
                data = json.dumps(self._status_fn()).encode()
                win32file.WriteFile(pipe, data)
                win32file.CloseHandle(pipe)
            except Exception:
                time.sleep(0.5)
