from __future__ import annotations

import random

from i18n import t


def parse_wheel_items(raw_text: str) -> list[str]:
    """Turn multiline or comma-separated user input into clean wheel entries."""
    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    parts: list[str] = []

    for line in normalized_text.split("\n"):
        for piece in line.split(","):
            cleaned_piece = piece.strip()
            if cleaned_piece:
                parts.append(cleaned_piece)

    if not parts:
        raise ValueError(t("logic.wheel.no_items"))

    return parts


def choose_winner_index(items: list[str]) -> int:
    """Pick one item index at random."""
    if not items:
        raise ValueError(t("logic.wheel.no_items"))
    return random.randrange(len(items))
