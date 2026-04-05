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
from ui_fonts import ui_font, ui_font_family
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
    """Main window that hosts the toolbox home screen and each tool view."""

    def __init__(self) -> None:
        super().__init__()
        self.title(t("app.window_title"))
        self.geometry("1260x840")
        self.minsize(1080, 760)
        self.configure(bg="#f4efe7")
        self.main_shell: ttk.Frame | None = None
        self.language_var = tk.StringVar(value=LANGUAGE_LABELS[get_language()])
        self.current_view_name = "home"

        try:
            self.tk.call("tk", "scaling", self.winfo_fpixels("1i") / 72.0)
        except tk.TclError:
            pass

        # The app shell owns the styles, sidebar, and navigation between tool screens.
        self._build_styles()
        self._build_layout()
        self.show_home()

    def _build_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        self.option_add("*Font", f"{{{ui_font_family()}}} 10")

        style.configure("Shell.TFrame", background="#f4efe7")
        style.configure("Sidebar.TFrame", background="#1d2a36")
        style.configure("Panel.TFrame", background="#f7f2eb")
        style.configure("Card.TFrame", background="#fffaf4", relief="flat")
        style.configure("Muted.TFrame", background="#efe5d7")

        style.configure(
            "AppTitle.TLabel",
            background="#1d2a36",
            foreground="#fffaf4",
            font=ui_font(22, bold=True),
        )
        style.configure(
            "SidebarText.TLabel",
            background="#1d2a36",
            foreground="#cfd7df",
            font=ui_font(10),
        )
        style.configure(
            "SidebarBadge.TLabel",
            background="#304657",
            foreground="#f8d9b8",
            font=ui_font(9, bold=True),
            padding=(10, 4),
        )
        style.configure(
            "ToolbarLabel.TLabel",
            background="#f7f2eb",
            foreground="#5e666d",
            font=ui_font(10, bold=True),
        )
        style.configure(
            "Eyebrow.TLabel",
            background="#f7f2eb",
            foreground="#b45b30",
            font=ui_font(9, bold=True),
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#f7f2eb",
            foreground="#1f2a33",
            font=ui_font(28, bold=True),
        )
        style.configure(
            "SectionText.TLabel",
            background="#f7f2eb",
            foreground="#6b756d",
            font=ui_font(11),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#fffaf4",
            foreground="#1f2a33",
            font=ui_font(17, bold=True),
        )
        style.configure(
            "CardText.TLabel",
            background="#fffaf4",
            foreground="#667074",
            font=ui_font(10),
        )
        style.configure(
            "MutedField.TLabel",
            background="#efe5d7",
            foreground="#30414d",
            font=ui_font(10, bold=True),
        )
        style.configure(
            "MutedTitle.TLabel",
            background="#efe5d7",
            foreground="#1f2a33",
            font=ui_font(17, bold=True),
        )
        style.configure(
            "CardBadge.TLabel",
            background="#fffaf4",
            foreground="#c06836",
            font=ui_font(9, bold=True),
        )
        style.configure(
            "FieldLabel.TLabel",
            background="#fffaf4",
            foreground="#30414d",
            font=ui_font(10, bold=True),
        )
        style.configure(
            "Status.TLabel",
            background="#f4e2d3",
            foreground="#8b4b25",
            font=ui_font(10),
        )
        style.configure(
            "PreviewText.TLabel",
            background="#fffaf4",
            foreground="#7a847b",
            font=ui_font(10),
        )

        style.configure(
            "Nav.TButton",
            background="#1d2a36",
            foreground="#f4efe7",
            borderwidth=0,
            focuscolor="#1d2a36",
            anchor="w",
            padding=(16, 12),
            font=ui_font(10, bold=True),
        )
        style.map(
            "Nav.TButton",
            background=[("active", "#304657"), ("pressed", "#304657")],
            foreground=[("active", "#fffaf4")],
        )

        style.configure(
            "Primary.TButton",
            background="#c76838",
            foreground="#fffaf4",
            borderwidth=0,
            focuscolor="#c76838",
            padding=(18, 11),
            font=ui_font(10, bold=True),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#d67745"), ("pressed", "#b55a2e")],
            foreground=[("active", "#fffaf4")],
        )

        style.configure(
            "Secondary.TButton",
            background="#ece1d3",
            foreground="#24313b",
            borderwidth=0,
            focuscolor="#ece1d3",
            padding=(16, 11),
            font=ui_font(10, bold=True),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#e5d6c4"), ("pressed", "#dbcab6")],
        )

        style.configure(
            "Modern.TEntry",
            fieldbackground="#fffdf9",
            foreground="#1f2a33",
            bordercolor="#dbcab6",
            lightcolor="#dbcab6",
            darkcolor="#dbcab6",
            relief="flat",
            padding=(10, 8),
        )
        style.map(
            "Modern.TEntry",
            bordercolor=[("focus", "#c76838")],
            lightcolor=[("focus", "#c76838")],
            darkcolor=[("focus", "#c76838")],
        )

        style.configure(
            "Modern.TCheckbutton",
            background="#fffaf4",
            foreground="#30414d",
            font=ui_font(10),
        )
        style.map(
            "Modern.TCheckbutton",
            background=[("active", "#fffaf4")],
            foreground=[("active", "#30414d")],
        )

        style.configure(
            "Clean.Treeview",
            background="#fffdf9",
            fieldbackground="#fffdf9",
            foreground="#22303a",
            borderwidth=0,
            rowheight=36,
            font=ui_font(10),
        )
        style.configure(
            "Clean.Treeview.Heading",
            background="#efe4d7",
            foreground="#24313b",
            borderwidth=0,
            font=ui_font(10, bold=True),
        )
        style.map(
            "Clean.Treeview",
            background=[("selected", "#f1d7c2")],
            foreground=[("selected", "#24313b")],
        )

    def _build_layout(self) -> None:
        # The layout is a sidebar on the left and a content area on the right.
        if self.main_shell is not None:
            self.main_shell.destroy()

        self.title(t("app.window_title"))
        self.main_shell = ttk.Frame(self, style="Shell.TFrame", padding=18)
        self.main_shell.pack(fill="both", expand=True)
        self.main_shell.columnconfigure(1, weight=1)
        self.main_shell.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self.main_shell, style="Sidebar.TFrame", padding=22)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        ttk.Label(sidebar, text=t("app.sidebar_badge"), style="SidebarBadge.TLabel").pack(anchor="w")
        ttk.Label(sidebar, text=t("app.window_title"), style="AppTitle.TLabel").pack(anchor="w")
        ttk.Label(
            sidebar,
            text=t("app.sidebar_subtitle"),
            style="SidebarText.TLabel",
            justify="left",
            wraplength=190,
        ).pack(anchor="w", pady=(10, 24))

        ttk.Button(sidebar, text=t("app.nav_home"), style="Nav.TButton", command=self.show_home).pack(fill="x", pady=(0, 8))
        ttk.Button(sidebar, text=t("app.nav_renamer"), style="Nav.TButton", command=self.show_renamer).pack(fill="x")
        ttk.Button(sidebar, text=t("app.nav_qr"), style="Nav.TButton", command=self.show_qr_generator).pack(
            fill="x", pady=(8, 0)
        )
        ttk.Button(sidebar, text=t("app.nav_pdf"), style="Nav.TButton", command=self.show_pdf_scanner).pack(
            fill="x", pady=(8, 0)
        )
        ttk.Button(sidebar, text=t("app.nav_pdf_merge"), style="Nav.TButton", command=self.show_pdf_merger).pack(
            fill="x", pady=(8, 0)
        )
        ttk.Button(sidebar, text=t("app.nav_wheel"), style="Nav.TButton", command=self.show_wheel_spinner).pack(
            fill="x", pady=(8, 0)
        )
        ttk.Button(sidebar, text=t("app.nav_cursor"), style="Nav.TButton", command=self.show_cursor_skins).pack(
            fill="x", pady=(8, 0)
        )

        content_shell = ttk.Frame(self.main_shell, style="Panel.TFrame", padding=0)
        content_shell.grid(row=0, column=1, sticky="nsew")
        content_shell.columnconfigure(0, weight=1)
        content_shell.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(content_shell, style="Panel.TFrame", padding=(10, 4, 10, 10))
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.columnconfigure(0, weight=1)

        ttk.Label(toolbar, text=t("app.language"), style="ToolbarLabel.TLabel").grid(row=0, column=1, sticky="e", padx=(0, 8))
        language_switch = ttk.Combobox(
            toolbar,
            state="readonly",
            width=10,
            values=[LANGUAGE_LABELS["zh"], LANGUAGE_LABELS["en"]],
            textvariable=self.language_var,
        )
        language_switch.grid(row=0, column=2, sticky="e")
        language_switch.bind("<<ComboboxSelected>>", self._handle_language_change)

        self.content = ttk.Frame(content_shell, style="Panel.TFrame", padding=0)
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        # Each tool is its own frame class now, which keeps this file focused on navigation.
        self.home_view = self._build_home_view(self.content)
        self.renamer_view = BatchRenamerView(self.content, self.show_home)
        self.qr_view = QRCodeGeneratorView(self.content, self.show_home)
        self.pdf_view = PDFTextScannerView(self.content, self.show_home)
        self.pdf_merge_view = PDFMergeToolView(self.content, self.show_home)
        self.wheel_view = WheelSpinnerToolView(self.content, self.show_home)
        self.cursor_view = CursorSkinToolView(self.content, self.show_home)

    def _build_home_view(self, parent: ttk.Frame) -> ttk.Frame:
        # The home screen acts like a launcher for all tools in the toolbox.
        frame = ScrollablePanel(parent, canvas_background="#f7f2eb")
        surface = frame.content
        surface.columnconfigure(0, weight=1)
        surface.rowconfigure(2, weight=1)

        intro = ttk.Frame(surface, style="Panel.TFrame", padding=(16, 10, 16, 20))
        intro.grid(row=0, column=0, sticky="ew")
        intro.columnconfigure(0, weight=1)

        ttk.Label(intro, text=t("home.title"), style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Label(
            intro,
            text=t("home.subtitle"),
            style="SectionText.TLabel",
            wraplength=820,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        quick_jump = ttk.Frame(surface, style="Card.TFrame", padding=22)
        quick_jump.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        quick_jump.columnconfigure(0, weight=1)
        quick_jump.columnconfigure(1, weight=1)
        quick_jump.columnconfigure(2, weight=1)

        ttk.Label(quick_jump, text=t("home.quick_jump"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            quick_jump,
            text=t("home.quick_jump_help"),
            style="CardText.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 18))

        quick_buttons = (
            (t("home.card_renamer_title"), self.show_renamer),
            (t("home.card_qr_title"), self.show_qr_generator),
            (t("home.card_pdf_title"), self.show_pdf_scanner),
            (t("home.card_pdf_merge_title"), self.show_pdf_merger),
            (t("home.card_wheel_title"), self.show_wheel_spinner),
            (t("home.card_cursor_title"), self.show_cursor_skins),
        )
        for index, (label, command) in enumerate(quick_buttons):
            ttk.Button(quick_jump, text=label, style="Secondary.TButton", command=command).grid(
                row=2 + (index // 3),
                column=index % 3,
                sticky="ew",
                padx=(0, 12) if index % 3 != 2 else 0,
                pady=(0, 12),
            )

        cards = ttk.Frame(surface, style="Panel.TFrame", padding=(16, 0, 16, 16))
        cards.grid(row=2, column=0, sticky="nsew")
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.rowconfigure(0, weight=1)
        cards.rowconfigure(1, weight=1)
        cards.rowconfigure(2, weight=1)
        cards.rowconfigure(3, weight=1)

        renamer_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        renamer_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        ttk.Label(renamer_card, text=t("home.card_renamer_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            renamer_card,
            text=t("home.card_renamer_text"),
            style="CardText.TLabel",
            wraplength=250,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(renamer_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(renamer_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_renamer).pack(anchor="w")

        qr_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        qr_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        ttk.Label(qr_card, text=t("home.card_qr_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            qr_card,
            text=t("home.card_qr_text"),
            style="CardText.TLabel",
            wraplength=300,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(qr_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(qr_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_qr_generator).pack(anchor="w")

        pdf_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        pdf_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(18, 0))
        ttk.Label(pdf_card, text=t("home.card_pdf_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            pdf_card,
            text=t("home.card_pdf_text"),
            style="CardText.TLabel",
            wraplength=300,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(pdf_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(pdf_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_pdf_scanner).pack(anchor="w")

        cursor_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        cursor_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(18, 0))
        ttk.Label(cursor_card, text=t("home.card_cursor_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            cursor_card,
            text=t("home.card_cursor_text"),
            style="CardText.TLabel",
            wraplength=300,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(cursor_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(cursor_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_cursor_skins).pack(anchor="w")

        pdf_merge_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        pdf_merge_card.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=0, pady=(18, 0))
        ttk.Label(pdf_merge_card, text=t("home.card_pdf_merge_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            pdf_merge_card,
            text=t("home.card_pdf_merge_text"),
            style="CardText.TLabel",
            wraplength=650,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(pdf_merge_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(pdf_merge_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_pdf_merger).pack(anchor="w")

        wheel_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        wheel_card.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=0, pady=(18, 0))
        ttk.Label(wheel_card, text=t("home.card_wheel_title"), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            wheel_card,
            text=t("home.card_wheel_text"),
            style="CardText.TLabel",
            wraplength=650,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(wheel_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(wheel_card, text=t("home.open_tool"), style="Primary.TButton", command=self.show_wheel_spinner).pack(anchor="w")

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
        self.cursor_view.grid_forget()
        view.grid(row=0, column=0, sticky="nsew")

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

    def show_cursor_skins(self) -> None:
        self.current_view_name = "cursor_skins"
        self._show_view(self.cursor_view)


def run() -> None:
    enable_windows_dpi_awareness()
    app = ToolboxApp()
    app.mainloop()
