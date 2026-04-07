from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox

from i18n import t

PROJECT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"
CORE_MODULES = ("qrcode", "PIL", "pypdf", "pypdfium2")


def _required_modules() -> tuple[str, ...]:
    required = list(CORE_MODULES)

    if sys.platform == "win32":
        required.extend(
            (
                "winrt.windows.foundation",
                "winrt.windows.globalization",
                "winrt.windows.graphics.imaging",
                "winrt.windows.media.ocr",
                "winrt.windows.storage.streams",
            )
        )
    elif sys.version_info < (3, 13):
        required.append("rapidocr_onnxruntime")

    return tuple(required)


def _missing_modules() -> list[str]:
    missing: list[str] = []
    for module_name in _required_modules():
        try:
            module_spec = importlib.util.find_spec(module_name)
        except ModuleNotFoundError:
            module_spec = None

        if module_spec is None:
            missing.append(module_name)
    return missing


def ensure_dependencies() -> None:
    """Install app dependencies before importing the full UI."""
    if getattr(sys, "frozen", False):
        return

    if not REQUIREMENTS_FILE.exists():
        return

    missing = _missing_modules()
    if not missing:
        return

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            cwd=PROJECT_DIR,
        )
    except subprocess.CalledProcessError as exc:
        messagebox.showerror(
            t("app.window_title"),
            t(
                "main.install_error",
                command=f"{sys.executable} -m pip install -r {REQUIREMENTS_FILE}",
                error=exc,
            ),
        )
        raise SystemExit(exc.returncode) from exc


if __name__ == "__main__":
    # Install missing packages first so importing the app does not fail on first run.
    ensure_dependencies()

    from app import run

    # Small launcher file so the toolbox can be started with `python main.py`.
    run()
