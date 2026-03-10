from __future__ import annotations

import sys


class ProgressBar:
    def __init__(self, total: int, title: str = "Progress") -> None:
        self.total = max(total, 1)
        self.current = 0
        self.title = title
        self.bar_length = 30

    def update(self, current: int, status: str = "") -> None:
        self.current = max(0, min(current, self.total))
        ratio = self.current / self.total
        percentage = int(ratio * 100)
        filled_length = int(ratio * self.bar_length)
        empty_length = self.bar_length - filled_length
        bar = "#" * filled_length + "-" * empty_length
        progress = f"{self.current}/{self.total}"
        sys.stdout.write(
            f"\r{self.title}: [{bar}] {percentage}% ({progress}) {status}"
        )
        sys.stdout.flush()
        if self.current >= self.total:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def increment(self, status: str = "") -> None:
        self.update(self.current + 1, status)

