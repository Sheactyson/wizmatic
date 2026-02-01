# capture_thread.py
import threading
import time
from utils.frames import FrameBundle

class FrameSource:
    def __init__(self, capture, hz=60):
        self.capture = capture
        self.hz = hz
        self.dt = 1.0 / hz
        self.latest = None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            t0 = time.perf_counter()
            frame = self.capture.read()
            if frame is not None:
                bundle = FrameBundle(frame)
                with self._lock:
                    self.latest = bundle
            elapsed = time.perf_counter() - t0
            sleep_for = self.dt - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    def get_latest(self):
        with self._lock:
            return self.latest

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=1.0)
