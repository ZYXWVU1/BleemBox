from __future__ import annotations

from i18n import get_language


def ui_font_family() -> str:
    if get_language() == "zh":
        return "Microsoft YaHei UI"
    return "Segoe UI"


def ui_font(size: int, *, bold: bool = False) -> tuple[str, int] | tuple[str, int, str]:
    family = ui_font_family()
    if bold:
        return (family, size, "bold")
    return (family, size)
