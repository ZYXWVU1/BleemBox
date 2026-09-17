from __future__ import annotations

import ctypes
import tkinter as tk
from tkinter import ttk

from batch_rename_tool import BatchRenamerView
from cursor_skin_tool import CursorSkinToolView
from i18n import LANGUAGE_LABELS, get_language, set_language, t
from pdf_merge_tool import PDFMergeToolView
from pdf_text_tool import PDFTextScannerView
from qr_code_tool import QRCodeGeneratorView
from scrollable_panel import ScrollablePanel
from ui_theme import PAGE, apply_theme, fit_text
from website_launcher_tool import WebsiteLauncherToolView
from wheel_spinner_tool import WheelSpinnerToolView


def enable_windows_dpi_awareness() -> None:
    """Ask Windows to render Tk at native DPI so text stays sharp."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class ToolboxApp(tk.Tk):
    """A quiet desktop workspace with persistent tool navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.title(t("app.window_title"))
        self.geometry("1280x860")
        self.minsize(1000, 700)
        self.configure(bg=PAGE)
        self.main_shell = None
        self.language_var = tk.StringVar(value=LANGUAGE_LABELS[get_language()])
        self.current_view_name = "home"
        try:
            self.tk.call("tk", "scaling", self.winfo_fpixels("1i") / 72.0)
        except tk.TclError:
            pass
        self._build_styles()
        self._build_layout()
        self.show_home()

    def _build_styles(self):
        apply_theme(self)

    def _build_layout(self):
        if self.main_shell is not None:
            self.main_shell.destroy()
        self.title(t("app.window_title"))
        self.main_shell = ttk.Frame(self, style="Shell.TFrame")
        self.main_shell.pack(fill="both", expand=True)
        self.main_shell.columnconfigure(1, weight=1)
        self.main_shell.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self.main_shell, style="Sidebar.TFrame", padding=(16, 28, 16, 20))
        sidebar.grid(row=0, column=0, sticky="ns")
        ttk.Label(sidebar, text="Bleem Box", style="AppTitle.TLabel").pack(anchor="w", padx=12)
        ttk.Label(sidebar, text=t("app.workspace"), style="SidebarText.TLabel").pack(
            anchor="w", padx=12, pady=(6, 28))
        self.nav_buttons = {}
        nav = (
            ("home", "app.nav_home", self.show_home),
            ("renamer", "app.nav_renamer", self.show_renamer),
            ("qr_generator", "app.nav_qr", self.show_qr_generator),
            ("pdf_scanner", "app.nav_pdf", self.show_pdf_scanner),
            ("pdf_merger", "app.nav_pdf_merge", self.show_pdf_merger),
            ("wheel_spinner", "app.nav_wheel", self.show_wheel_spinner),
            ("web_launcher", "app.nav_web_launcher", self.show_web_launcher),
            ("cursor_skins", "app.nav_cursor", self.show_cursor_skins),
        )
        for name, key, command in nav:
            if name == "renamer":
                ttk.Separator(sidebar).pack(fill="x", padx=12, pady=16)
            button = ttk.Button(sidebar, text=t(key), style="Nav.TButton", command=command, width=21)
            button.pack(fill="x", pady=3)
            self.nav_buttons[name] = button
        footer = ttk.Frame(sidebar, style="Sidebar.TFrame")
        footer.pack(side="bottom", fill="x", padx=8)
        ttk.Label(footer, text=t("app.language"), style="SidebarText.TLabel").pack(anchor="w", pady=(0, 8))
        language_switch = ttk.Combobox(footer, state="readonly", width=16,
            values=[LANGUAGE_LABELS["zh"], LANGUAGE_LABELS["en"]], textvariable=self.language_var)
        language_switch.pack(fill="x")
        language_switch.bind("<<ComboboxSelected>>", self._handle_language_change)

        self.content = ttk.Frame(self.main_shell, style="Panel.TFrame", padding=(24, 28, 20, 20))
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.home_view = self._build_home_view(self.content)
        self.renamer_view = BatchRenamerView(self.content, self.show_home)
        self.qr_view = QRCodeGeneratorView(self.content, self.show_home)
        self.pdf_view = PDFTextScannerView(self.content, self.show_home)
        self.pdf_merge_view = PDFMergeToolView(self.content, self.show_home)
        self.wheel_view = WheelSpinnerToolView(self.content, self.show_home)
        self.web_launcher_view = WebsiteLauncherToolView(self.content, self.show_home)
        self.cursor_view = CursorSkinToolView(self.content, self.show_home)
        for view in (self.renamer_view, self.qr_view, self.pdf_view, self.pdf_merge_view,
                     self.wheel_view, self.web_launcher_view, self.cursor_view):
            fit_text(view)

    def _build_home_view(self, parent):
        frame = ScrollablePanel(parent, canvas_background=PAGE)
        surface = frame.content
        surface.columnconfigure(0, weight=1)
        intro = ttk.Frame(surface, style="Panel.TFrame", padding=(4, 0, 4, 24))
        intro.grid(row=0, column=0, sticky="ew")
        ttk.Label(intro, text=t("home.title"), style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(intro, text=t("home.subtitle"), style="SectionText.TLabel").pack(anchor="w", pady=(8, 0))
        cards = ttk.Frame(surface, style="Panel.TFrame")
        cards.grid(row=1, column=0, sticky="ew")
        tools = (
            ("renamer", "01", self.show_renamer),
            ("qr", "02", self.show_qr_generator),
            ("pdf", "03", self.show_pdf_scanner),
            ("pdf_merge", "04", self.show_pdf_merger),
            ("wheel", "05", self.show_wheel_spinner),
            ("web_launcher", "06", self.show_web_launcher),
            ("cursor", "07", self.show_cursor_skins),
        )
        self.home_cards = []
        descriptions = []
        for key, number, command in tools:
            card = ttk.Frame(cards, style="Card.TFrame", padding=20)
            card.columnconfigure(0, weight=1)
            ttk.Label(card, text=number, style="CardBadge.TLabel").grid(row=0, column=0, sticky="w")
            title = ttk.Label(card, text=t(f"home.card_{key}_title"), style="CardTitle.TLabel", wraplength=240)
            title.grid(row=1, column=0, sticky="w", pady=(12, 8))
            description = ttk.Label(card, text=t(f"home.card_{key}_text"),
                                    style="CardText.TLabel", wraplength=240, justify="left")
            description.grid(row=2, column=0, sticky="nw")
            card.rowconfigure(2, weight=1)
            ttk.Button(card, text=t("home.open_tool") + "  →", style="Secondary.TButton",
                       command=command).grid(row=3, column=0, sticky="w", pady=(18, 0))
            self.home_cards.append(card)
            descriptions.append((title, description))
        layout = {"width": None}

        def arrange(event):
            if event.widget is not frame.canvas or layout["width"] == event.width:
                return
            layout["width"] = event.width
            columns = 3 if event.width >= 900 else 2 if event.width >= 620 else 1
            for col in range(3):
                cards.columnconfigure(col, weight=1 if col < columns else 0,
                                      uniform="cards" if col < columns else "")
            width = max(160, event.width // columns - 64)
            for index, card in enumerate(self.home_cards):
                card.grid(row=index // columns, column=index % columns, sticky="nsew",
                          padx=(0, 12) if index % columns < columns - 1 else 0, pady=(0, 12))
                for label in descriptions[index]:
                    label.configure(wraplength=width)
        frame.canvas.bind("<Configure>", arrange, add="+")
        frame.refresh_scroll_bindings()
        return frame

    def _handle_language_change(self, _event: tk.Event) -> None:
        label_to_code = {label: code for code, label in LANGUAGE_LABELS.items()}
        selected_code = label_to_code.get(self.language_var.get(), "zh")
        current_view_name = self.current_view_name
        set_language(selected_code)
        self.language_var.set(LANGUAGE_LABELS[selected_code])
        self._build_styles()
        self._build_layout()
        getattr(self, f"show_{current_view_name}", self.show_home)()

    def _show_view(self, view: ttk.Frame) -> None:
        # Only one view should be visible at a time, so hide the others first.
        self.home_view.grid_forget()
        self.renamer_view.grid_forget()
        self.qr_view.grid_forget()
        self.pdf_view.grid_forget()
        self.pdf_merge_view.grid_forget()
        self.wheel_view.grid_forget()
        self.web_launcher_view.grid_forget()
        self.cursor_view.grid_forget()
        view.grid(row=0, column=0, sticky="nsew")
        for name, button in self.nav_buttons.items():
            button.configure(style="ActiveNav.TButton" if name == self.current_view_name else "Nav.TButton")

    def show_home(self) -> None:
        self.current_view_name = "home"
        self._show_view(self.home_view)

    def show_renamer(self) -> None:
        self.current_view_name = "renamer"
        self._show_view(self.renamer_view)

    def show_qr_generator(self) -> None:
        self.current_view_name = "qr_generator"
        self._show_view(self.qr_view)

    def show_pdf_scanner(self) -> None:
        self.current_view_name = "pdf_scanner"
        self._show_view(self.pdf_view)

    def show_pdf_merger(self) -> None:
        self.current_view_name = "pdf_merger"
        self._show_view(self.pdf_merge_view)

    def show_wheel_spinner(self) -> None:
        self.current_view_name = "wheel_spinner"
        self._show_view(self.wheel_view)

    def show_web_launcher(self) -> None:
        self.current_view_name = "web_launcher"
        self._show_view(self.web_launcher_view)

    def show_cursor_skins(self) -> None:
        self.current_view_name = "cursor_skins"
        self._show_view(self.cursor_view)


def run() -> None:
    enable_windows_dpi_awareness()
    app = ToolboxApp()
    app.mainloop()
