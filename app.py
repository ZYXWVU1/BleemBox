from __future__ import annotations

import ctypes
import tkinter as tk
from tkinter import ttk

from batch_rename_tool import BatchRenamerView
from pdf_text_tool import PDFTextScannerView
from qr_code_tool import QRCodeGeneratorView


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
        self.title("Bleem Box")
        self.geometry("1080x700")
        self.minsize(920, 620)
        self.configure(bg="#f4efe7")

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

        self.option_add("*Font", "{Segoe UI} 10")

        style.configure("Shell.TFrame", background="#f4efe7")
        style.configure("Sidebar.TFrame", background="#1d2a36")
        style.configure("Panel.TFrame", background="#f7f2eb")
        style.configure("Card.TFrame", background="#fffaf4", relief="flat")
        style.configure("Muted.TFrame", background="#efe5d7")

        style.configure(
            "AppTitle.TLabel",
            background="#1d2a36",
            foreground="#fffaf4",
            font=("Segoe UI Semibold", 22),
        )
        style.configure(
            "SidebarText.TLabel",
            background="#1d2a36",
            foreground="#cfd7df",
            font=("Segoe UI", 10),
        )
        style.configure(
            "SidebarBadge.TLabel",
            background="#304657",
            foreground="#f8d9b8",
            font=("Segoe UI Semibold", 9),
            padding=(10, 4),
        )
        style.configure(
            "Eyebrow.TLabel",
            background="#f7f2eb",
            foreground="#b45b30",
            font=("Segoe UI Semibold", 9),
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#f7f2eb",
            foreground="#1f2a33",
            font=("Segoe UI Semibold", 28),
        )
        style.configure(
            "SectionText.TLabel",
            background="#f7f2eb",
            foreground="#6b756d",
            font=("Segoe UI", 11),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#fffaf4",
            foreground="#1f2a33",
            font=("Segoe UI Semibold", 17),
        )
        style.configure(
            "CardText.TLabel",
            background="#fffaf4",
            foreground="#667074",
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardBadge.TLabel",
            background="#fffaf4",
            foreground="#c06836",
            font=("Segoe UI Semibold", 9),
        )
        style.configure(
            "FieldLabel.TLabel",
            background="#fffaf4",
            foreground="#30414d",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Status.TLabel",
            background="#f4e2d3",
            foreground="#8b4b25",
            font=("Segoe UI", 10),
        )
        style.configure(
            "PreviewText.TLabel",
            background="#fffaf4",
            foreground="#7a847b",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Nav.TButton",
            background="#1d2a36",
            foreground="#f4efe7",
            borderwidth=0,
            focuscolor="#1d2a36",
            anchor="w",
            padding=(16, 12),
            font=("Segoe UI Semibold", 10),
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
            font=("Segoe UI Semibold", 10),
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
            font=("Segoe UI Semibold", 10),
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
            font=("Segoe UI", 10),
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
            font=("Segoe UI", 10),
        )
        style.configure(
            "Clean.Treeview.Heading",
            background="#efe4d7",
            foreground="#24313b",
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Clean.Treeview",
            background=[("selected", "#f1d7c2")],
            foreground=[("selected", "#24313b")],
        )

    def _build_layout(self) -> None:
        # The layout is a sidebar on the left and a content area on the right.
        shell = ttk.Frame(self, style="Shell.TFrame", padding=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(shell, style="Sidebar.TFrame", padding=22)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        ttk.Label(sidebar, text="DESKTOP TOOLBOX", style="SidebarBadge.TLabel").pack(anchor="w")
        ttk.Label(sidebar, text="Bleem Box", style="AppTitle.TLabel").pack(anchor="w")
        ttk.Label(
            sidebar,
            text="Clean utilities for quick desktop tasks.",
            style="SidebarText.TLabel",
            justify="left",
            wraplength=190,
        ).pack(anchor="w", pady=(10, 24))

        ttk.Button(sidebar, text="Home", style="Nav.TButton", command=self.show_home).pack(fill="x", pady=(0, 8))
        ttk.Button(sidebar, text="Batch file renaming", style="Nav.TButton", command=self.show_renamer).pack(fill="x")
        ttk.Button(sidebar, text="QR code generator", style="Nav.TButton", command=self.show_qr_generator).pack(
            fill="x", pady=(8, 0)
        )
        ttk.Button(sidebar, text="PDF text scanner", style="Nav.TButton", command=self.show_pdf_scanner).pack(
            fill="x", pady=(8, 0)
        )

        self.content = ttk.Frame(shell, style="Panel.TFrame", padding=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        # Each tool is its own frame class now, which keeps this file focused on navigation.
        self.home_view = self._build_home_view(self.content)
        self.renamer_view = BatchRenamerView(self.content, self.show_home)
        self.qr_view = QRCodeGeneratorView(self.content, self.show_home)
        self.pdf_view = PDFTextScannerView(self.content, self.show_home)

    def _build_home_view(self, parent: ttk.Frame) -> ttk.Frame:
        # The home screen acts like a launcher for all tools in the toolbox.
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        intro = ttk.Frame(frame, style="Panel.TFrame", padding=(6, 6, 6, 22))
        intro.grid(row=0, column=0, sticky="ew")
        intro.columnconfigure(0, weight=1)

        ttk.Label(intro, text="Pick the utility you want to open.", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Label(
            intro,
            text="Each card opens directly into its workspace with the same updated design system across the app.",
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        cards = ttk.Frame(frame, style="Panel.TFrame", padding=6)
        cards.grid(row=1, column=0, sticky="nsew")
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.columnconfigure(2, weight=1)
        cards.rowconfigure(0, weight=1)

        renamer_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        renamer_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        ttk.Label(renamer_card, text="Batch File Renaming", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            renamer_card,
            text="Rename many files at once with a simple base name and instant preview.",
            style="CardText.TLabel",
            wraplength=250,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(renamer_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(renamer_card, text="Open Tool", style="Primary.TButton", command=self.show_renamer).pack(anchor="w")

        qr_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        qr_card.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)
        ttk.Label(qr_card, text="QR Code Generator", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            qr_card,
            text="Generate a QR code for a website, image link, or music link, then save it as a PNG.",
            style="CardText.TLabel",
            wraplength=260,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(qr_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(qr_card, text="Open Tool", style="Primary.TButton", command=self.show_qr_generator).pack(anchor="w")

        pdf_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        pdf_card.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=0)
        ttk.Label(pdf_card, text="PDF Text Scanner", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            pdf_card,
            text="Extract readable text from every PDF page, keep page breaks, and save the result as a TXT file.",
            style="CardText.TLabel",
            wraplength=260,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Frame(pdf_card, style="Card.TFrame").pack(fill="both", expand=True)
        ttk.Button(pdf_card, text="Open Tool", style="Primary.TButton", command=self.show_pdf_scanner).pack(anchor="w")

        return frame

    def _show_view(self, view: ttk.Frame) -> None:
        # Only one view should be visible at a time, so hide the others first.
        self.home_view.grid_forget()
        self.renamer_view.grid_forget()
        self.qr_view.grid_forget()
        self.pdf_view.grid_forget()
        view.grid(row=0, column=0, sticky="nsew")

    def show_home(self) -> None:
        self._show_view(self.home_view)

    def show_renamer(self) -> None:
        self._show_view(self.renamer_view)

    def show_qr_generator(self) -> None:
        self._show_view(self.qr_view)

    def show_pdf_scanner(self) -> None:
        self._show_view(self.pdf_view)


def run() -> None:
    enable_windows_dpi_awareness()
    app = ToolboxApp()
    app.mainloop()
