from __future__ import annotations

import ctypes
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from i18n import t

SPI_SETCURSORS = 0x0057
CURSOR_REGISTRY_PATH = r"Control Panel\Cursors"
ALLOWED_CURSOR_EXTENSIONS = {".cur", ".ani"}
TEMPLATES_DIR = Path(__file__).resolve().parent / "cursor_templates"
WINDOWS_CURSOR_DIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Cursors"

EXPECTED_CURSOR_FILES = {
    "arrow": "Arrow",
    "help": "Help",
    "appstarting": "AppStarting",
    "wait": "Wait",
    "crosshair": "Crosshair",
    "ibeam": "IBeam",
    "nwpen": "NWPen",
    "no": "No",
    "sizens": "SizeNS",
    "sizewe": "SizeWE",
    "sizenwse": "SizeNWSE",
    "sizenesw": "SizeNESW",
    "sizeall": "SizeAll",
    "uparrow": "UpArrow",
    "hand": "Hand",
}

DEFAULT_WINDOWS_CURSOR_FILES = {
    "Arrow": ("aero_arrow.cur", "arrow_r.cur", "arrow_i.cur", "larrow.cur"),
    "Help": ("aero_helpsel.cur", "help_r.cur", "help_i.cur"),
    "AppStarting": ("aero_working.ani", "busy_r.cur", "lappstrt.cur"),
    "Wait": ("aero_busy.ani", "wait_r.cur", "busy_r.cur", "lwait.cur"),
    "Crosshair": ("cross_r.cur", "cross_i.cur", "lcross.cur"),
    "IBeam": ("beam_r.cur", "beam_i.cur", "libeam.cur"),
    "NWPen": ("aero_pen.cur", "pen_r.cur", "pen_i.cur"),
    "No": ("aero_unavail.cur", "no_r.cur", "no_i.cur", "lnodrop.cur"),
    "SizeNS": ("aero_ns.cur", "size4_r.cur", "size4_i.cur", "lns.cur"),
    "SizeWE": ("aero_ew.cur", "size3_r.cur", "size3_i.cur", "lwe.cur"),
    "SizeNWSE": ("aero_nwse.cur", "size1_r.cur", "size1_i.cur", "lnwse.cur"),
    "SizeNESW": ("aero_nesw.cur", "size2_r.cur", "size2_i.cur", "lnesw.cur"),
    "SizeAll": ("aero_move.cur", "move_r.cur", "move_i.cur", "lmove.cur"),
    "UpArrow": ("aero_up.cur", "up_r.cur", "up_i.cur"),
    "Hand": ("aero_link.cur", "link_i.cur", "link_im.cur", "link_il.cur"),
}

CURSOR_NAME_ALIASES = {
    "normalselect": "Arrow",
    "normal": "Arrow",
    "arrow": "Arrow",
    "select": "Arrow",
    "helpselect": "Help",
    "help": "Help",
    "workinginbackground": "AppStarting",
    "appstarting": "AppStarting",
    "starting": "AppStarting",
    "busy": "Wait",
    "wait": "Wait",
    "crosshair": "Crosshair",
    "precisionselect": "Crosshair",
    "precision": "Crosshair",
    "textselect": "IBeam",
    "text": "IBeam",
    "ibeam": "IBeam",
    "handwriting": "NWPen",
    "pen": "NWPen",
    "nwpen": "NWPen",
    "unavailable": "No",
    "nodrop": "No",
    "forbidden": "No",
    "notallowed": "No",
    "no": "No",
    "verticalresize": "SizeNS",
    "sizens": "SizeNS",
    "horizontalresize": "SizeWE",
    "sizewe": "SizeWE",
    "diagonalresize1": "SizeNWSE",
    "sizenwse": "SizeNWSE",
    "diagonalresize2": "SizeNESW",
    "sizenesw": "SizeNESW",
    "move": "SizeAll",
    "sizeall": "SizeAll",
    "allscroll": "SizeAll",
    "alternateselect": "UpArrow",
    "uparrow": "UpArrow",
    "linkselect": "Hand",
    "hand": "Hand",
    "link": "Hand",
    "正常选择": "Arrow",
    "正常": "Arrow",
    "箭头": "Arrow",
    "默认": "Arrow",
    "帮助选择": "Help",
    "帮助": "Help",
    "在后台工作": "AppStarting",
    "后台运行": "AppStarting",
    "后台": "AppStarting",
    "启动中": "AppStarting",
    "忙": "Wait",
    "等待": "Wait",
    "精确选择": "Crosshair",
    "十字": "Crosshair",
    "文本选择": "IBeam",
    "文本": "IBeam",
    "输入": "IBeam",
    "手写": "NWPen",
    "笔": "NWPen",
    "不可用": "No",
    "禁止": "No",
    "垂直大小": "SizeNS",
    "垂直调整": "SizeNS",
    "上下调整": "SizeNS",
    "水平大小": "SizeWE",
    "水平调整": "SizeWE",
    "左右调整": "SizeWE",
    "对角线1": "SizeNWSE",
    "左上右下调整": "SizeNWSE",
    "对角线2": "SizeNESW",
    "右上左下调整": "SizeNESW",
    "移动": "SizeAll",
    "全向移动": "SizeAll",
    "向上箭头": "UpArrow",
    "上箭头": "UpArrow",
    "链接选择": "Hand",
    "链接": "Hand",
}

CURSOR_ROLE_KEYWORDS = {
    "Arrow": (
        "normalselect",
        "normal",
        "arrow",
        "select",
        "正常选择",
        "正常",
        "箭头",
        "默认",
    ),
    "Help": ("helpselect", "help", "帮助选择", "帮助"),
    "AppStarting": ("workinginbackground", "appstarting", "starting", "在后台工作", "后台运行", "后台", "启动中"),
    "Wait": ("busy", "wait", "忙", "等待"),
    "Crosshair": ("crosshair", "precisionselect", "precision", "精确选择", "十字"),
    "IBeam": ("textselect", "text", "ibeam", "文本选择", "文本", "输入"),
    "NWPen": ("handwriting", "pen", "nwpen", "手写", "笔"),
    "No": ("unavailable", "nodrop", "forbidden", "notallowed", "no", "不可用", "禁止"),
    "SizeNS": ("verticalresize", "sizens", "垂直大小", "垂直调整", "上下调整"),
    "SizeWE": ("horizontalresize", "sizewe", "水平大小", "水平调整", "左右调整"),
    "SizeNWSE": ("diagonalresize1", "sizenwse", "对角线1", "左上右下调整", "左上右下"),
    "SizeNESW": ("diagonalresize2", "sizenesw", "对角线2", "右上左下调整", "右上左下"),
    "SizeAll": ("move", "sizeall", "allscroll", "移动", "全向移动"),
    "UpArrow": ("alternateselect", "uparrow", "向上箭头", "上箭头"),
    "Hand": ("linkselect", "hand", "link", "链接选择", "链接"),
}

TEMPLATE_README = """Drop your cursor files into this folder to build a full cursor skin pack.

Supported file types:
- .cur
- .ani

Use these exact file names:
- arrow
- help
- appstarting
- wait
- crosshair
- ibeam
- nwpen
- no
- sizens
- sizewe
- sizenwse
- sizenesw
- sizeall
- uparrow
- hand

Example:
- arrow.cur
- wait.ani
- hand.cur

You do not need every file. The app will apply whichever files it finds.
"""

SINGLE_TEMPLATE_README = """Put a single .cur or .ani file in this folder if you want a quick test file.

The Mouse Cursor Skins tool can apply any selected cursor file as your main arrow cursor.
"""


@dataclass(frozen=True)
class CursorPreset:
    name: str
    description: str
    cursor_path: Path


def ensure_cursor_template_files() -> Path:
    full_pack_dir = TEMPLATES_DIR / "full_skin_pack_template"
    single_cursor_dir = TEMPLATES_DIR / "single_cursor_template"

    full_pack_dir.mkdir(parents=True, exist_ok=True)
    single_cursor_dir.mkdir(parents=True, exist_ok=True)

    readme_path = full_pack_dir / "README.txt"
    if not readme_path.exists():
        readme_path.write_text(TEMPLATE_README, encoding="utf-8")

    single_readme_path = single_cursor_dir / "README.txt"
    if not single_readme_path.exists():
        single_readme_path.write_text(SINGLE_TEMPLATE_README, encoding="utf-8")

    for file_stem in EXPECTED_CURSOR_FILES:
        placeholder_path = full_pack_dir / f"{file_stem}_put_cursor_here.txt"
        if not placeholder_path.exists():
            placeholder_path.write_text(
                f"Replace this file with a real cursor file named {file_stem}.cur or {file_stem}.ani\n",
                encoding="utf-8",
            )

    return TEMPLATES_DIR


def expected_template_file_names() -> str:
    lines = [f"- {name}.cur or {name}.ani" for name in EXPECTED_CURSOR_FILES]
    return "\n".join(lines)


def starter_cursor_presets() -> list[CursorPreset]:
    candidates = (
        (
            t("cursor.preset_aero_arrow"),
            t("cursor.preset_aero_arrow_desc"),
            "aero_arrow.cur",
        ),
        (
            t("cursor.preset_modern_arrow"),
            t("cursor.preset_modern_arrow_desc"),
            "arrow_r.cur",
        ),
        (
            t("cursor.preset_large_arrow"),
            t("cursor.preset_large_arrow_desc"),
            "arrow_l.cur",
        ),
        (
            t("cursor.preset_extra_large_arrow"),
            t("cursor.preset_extra_large_arrow_desc"),
            "aero_arrow_xl.cur",
        ),
    )

    presets: list[CursorPreset] = []
    for name, description, file_name in candidates:
        cursor_path = WINDOWS_CURSOR_DIR / file_name
        if cursor_path.exists():
            presets.append(CursorPreset(name=name, description=description, cursor_path=cursor_path))
    return presets


def is_windows_supported() -> bool:
    return sys.platform == "win32"


def apply_arrow_cursor(cursor_path: str | Path) -> str:
    path = _validate_cursor_file(cursor_path)
    _write_registry_values({"Arrow": path})
    return t("logic.cursor.apply_arrow", name=path.name)


def apply_cursor_skin_folder(folder_path: str | Path) -> str:
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(t("logic.cursor.invalid_folder"))

    entries = _load_folder_entries(folder)
    if not entries:
        raise ValueError(t("logic.cursor.no_roles_found"))

    _write_registry_values(entries)
    return t("logic.cursor.apply_folder", count=len(entries), name=folder.name)


def reset_cursor_skin_to_default() -> str:
    entries: dict[str, Path] = {}

    for registry_name, candidate_files in DEFAULT_WINDOWS_CURSOR_FILES.items():
        cursor_path = _find_existing_windows_cursor(candidate_files)
        if cursor_path is not None:
            entries[registry_name] = cursor_path

    if not entries:
        raise RuntimeError(t("logic.cursor.default_missing"))

    _write_registry_values(entries)
    return t("logic.cursor.default_restored")


def _validate_cursor_file(cursor_path: str | Path) -> Path:
    path = Path(cursor_path)
    if not path.is_file():
        raise ValueError(t("logic.cursor.invalid_file"))
    if path.suffix.lower() not in ALLOWED_CURSOR_EXTENSIONS:
        raise ValueError(t("logic.cursor.invalid_format"))
    return path


def _load_folder_entries(folder: Path) -> dict[str, Path]:
    entries: dict[str, Path] = {}

    for child in sorted(folder.rglob("*")):
        if not child.is_file() or child.suffix.lower() not in ALLOWED_CURSOR_EXTENSIONS:
            continue

        registry_name = _resolve_registry_name(child.stem)
        if registry_name is None or registry_name in entries:
            continue

        entries[registry_name] = child

    return entries


def _resolve_registry_name(file_stem: str) -> str | None:
    normalized_name = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", file_stem.lower())

    if normalized_name in EXPECTED_CURSOR_FILES:
        return EXPECTED_CURSOR_FILES[normalized_name]

    exact_match = CURSOR_NAME_ALIASES.get(normalized_name)
    if exact_match is not None:
        return exact_match

    for registry_name, keywords in CURSOR_ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized_name:
                return registry_name

    return None


def _find_existing_windows_cursor(file_names: tuple[str, ...]) -> Path | None:
    for file_name in file_names:
        cursor_path = WINDOWS_CURSOR_DIR / file_name
        if cursor_path.exists():
            return cursor_path
    return None


def _write_registry_values(entries: dict[str, Path]) -> None:
    if not is_windows_supported():
        raise RuntimeError(t("logic.cursor.windows_only_runtime"))

    import winreg

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        CURSOR_REGISTRY_PATH,
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        for registry_name, cursor_path in entries.items():
            winreg.SetValueEx(key, registry_name, 0, winreg.REG_SZ, str(cursor_path))

    if not ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0):
        raise ctypes.WinError()
