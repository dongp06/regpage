from __future__ import annotations

RESET = "\x1b[0m"


def gradient(
    text: str,
    start_rgb: tuple[int, int, int] = (0, 200, 255),
    end_rgb: tuple[int, int, int] = (180, 100, 255),
) -> str:
    """Apply a simple left‑to‑right RGB gradient to the given text."""
    if not text:
        return text

    r1, g1, b1 = start_rgb
    r2, g2, b2 = end_rgb
    n = len(text)
    out_parts: list[str] = []

    for i, ch in enumerate(text):
        t = i / (n - 1) if n > 1 else 1.0
        r = round(r1 + (r2 - r1) * t)
        g = round(g1 + (g2 - g1) * t)
        b = round(b1 + (b2 - b1) * t)
        out_parts.append(f"\x1b[38;2;{r};{g};{b}m{ch}")

    return "".join(out_parts) + RESET

