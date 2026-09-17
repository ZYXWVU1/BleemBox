"""Run with python -B tests/ui_smoke.py; captures only the app window."""
from pathlib import Path
import sys
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if (ROOT / ".ui-test-deps").exists():
    sys.path.insert(0, str(ROOT / ".ui-test-deps"))

from PIL import ImageGrab
from app import ToolboxApp, enable_windows_dpi_awareness
from i18n import set_language, LANGUAGE_LABELS
from scrollable_panel import ScrollablePanel
from website_launcher_logic import WebsiteButtonProfile


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def main():
    artifacts = ROOT / "artifacts" / "ui"
    artifacts.mkdir(parents=True, exist_ok=True)
    errors = []
    overflow = []
    enable_windows_dpi_awareness()
    with patch("website_launcher_tool.load_website_profiles", return_value=[
        WebsiteButtonProfile("test", "Study", ["https://example.com"])
    ]):
        app = ToolboxApp()
        app.report_callback_exception = lambda *args: errors.append("".join(traceback.format_exception(*args)))
        app.attributes("-topmost", True)
        jobs = [(language, size, view) for language in ("zh", "en")
                for size in ("1280x860", "1000x700")
                for view in app.nav_buttons]

        def capture(language, size, view):
            for widget in descendants(app.content):
                if not widget.winfo_viewable():
                    continue
                parent = widget.master
                if widget.winfo_x() + widget.winfo_width() > parent.winfo_width() + 3:
                    overflow.append((language, size, view, str(widget), widget.winfo_class(),
                                     widget.winfo_x(), widget.winfo_width(), parent.winfo_width()))
            box = (app.winfo_rootx(), app.winfo_rooty(),
                   app.winfo_rootx() + app.winfo_width(), app.winfo_rooty() + app.winfo_height())
            ImageGrab.grab(bbox=box).save(artifacts / f"{language}-{size}-{view}.png")
            selected = [name for name, button in app.nav_buttons.items()
                        if button.cget("style") == "ActiveNav.TButton"]
            assert selected == [view], selected
            print(f"PASS {language} {size} {view}", flush=True)
            app.after(10, step)

        def step():
            if not jobs:
                app.qr_view.qr_input_var.set("https://example.com")
                app.qr_view.generate_qr_code()
                assert app.qr_view.qr_image is not None
                assert not app.qr_view.save_button.instate(["disabled"])
                # Navigation must retain current form values.
                app.show_home()
                app.show_qr_generator()
                assert app.qr_view.qr_input_var.get() == "https://example.com"
                # Rebinding must not accumulate repeated wheel callbacks.
                panel = next(w for w in descendants(app.qr_view) if isinstance(w, ScrollablePanel))
                before = panel.canvas.bind("<MouseWheel>")
                panel.refresh_scroll_bindings()
                assert before == panel.canvas.bind("<MouseWheel>")
                assert not app.wheel_view.items_text.bind("<MouseWheel>")
                app.destroy()
                return
            language, size, view = jobs.pop(0)
            if app.language_var.get() != LANGUAGE_LABELS[language]:
                app.language_var.set(LANGUAGE_LABELS[language])
                app._handle_language_change(None)
            app.geometry(size + "+30+30")
            getattr(app, "show_" + view)()
            app.after(450, lambda: capture(language, size, view))

        app.after(50, step)
        app.mainloop()
    print("CALLBACK ERRORS:", errors)
    print("HORIZONTAL OVERFLOW:", overflow)
    assert not errors, errors
    assert not overflow, overflow
    print("PASS: 32 page/language/size checks, QR generation, navigation state, nested scrolling")


if __name__ == "__main__":
    main()
