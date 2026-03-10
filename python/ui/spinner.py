from __future__ import annotations

import itertools
import sys
import threading
import time
from typing import Optional


class LoadingSpinner:
    def __init__(self, text: str = "Loading") -> None:
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.text = text
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        # hide cursor
        sys.stdout.write("\x1B[?25l")
        sys.stdout.flush()
        for frame in itertools.cycle(self.frames):
            if self._stop_event.is_set():
                break
            sys.stdout.write(f"\r{frame} {self.text}...")
            sys.stdout.flush()
            time.sleep(0.08)
        # clear line & show cursor again
        sys.stdout.write("\r\x1B[K")
        sys.stdout.write("\x1B[?25h")
        sys.stdout.flush()

    def update_text(self, new_text: str) -> None:
        self.text = new_text

    def _stop(self, final_text: Optional[str] = None) -> None:
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join(timeout=1)
        if final_text:
            print(final_text)

    def stop(self, final_text: Optional[str] = None) -> None:
        self._stop(final_text)

    def succeed(self, text: str) -> None:
        self._stop(f"[OK] {text}")

    def fail(self, text: str) -> None:
        self._stop(f"[FAIL] {text}")

    def info(self, text: str) -> None:
        self._stop(f"[INFO] {text}")

