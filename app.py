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
        self.title("Desktop Toolbox")
        self.geometry("1080x700")
        self.minsize(920, 620)
        self.configure(bg="#dbe4ea")

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

        style.configure("Shell.TFrame", background="#dbe4ea")
        style.configure("Sidebar.TFrame", background="#17324d")
        style.configure("Panel.TFrame", background="#f6f8fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Hero.TFrame", background="#12304a")

        style.configure(
            "AppTitle.TLabel",
            background="#17324d",
            foreground="#f8fafc",
            font=("Segoe UI Semibold", 20),
        )
        style.configure(
            "SidebarText.TLabel",
            background="#17324d",
            foreground="#c8d6e5",
            font=("Segoe UI", 10),
        )
        style.configure(
            "HeroTitle.TLabel",
            background="#12304a",
            foreground="#ffffff",
            font=("Segoe UI Semibold", 24),
        )
        style.configure(
            "HeroText.TLabel",
            background="#12304a",
            foreground="#d9e6f2",
            font=("Segoe UI", 11),
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#f6f8fb",
            foreground="#1f2937",
            font=("Segoe UI Semibold", 22),
        )
        style.configure(
            "SectionText.TLabel",
            background="#f6f8fb",
            foreground="#526071",
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#16324f",
            font=("Segoe UI Semibold", 15),
        )
        style.configure(
            "CardText.TLabel",
            background="#ffffff",
            foreground="#617182",
            font=("Segoe UI", 10),
        )
        style.configure(
            "FieldLabel.TLabel",
            background="#ffffff",
            foreground="#334155",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Status.TLabel",
            background="#eef4f8",
            foreground="#35516c",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Nav.TButton",
            background="#17324d",
            foreground="#f8fafc",
            borderwidth=0,
            focuscolor="#17324d",
            padding=(14, 10),
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Nav.TButton",
            background=[("active", "#244868"), ("pressed", "#244868")],
            foreground=[("active", "#ffffff")],
        )

        style.configure(
            "Primary.TButton",
            background="#1f6aa5",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="#1f6aa5",
            padding=(18, 10),
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#2b7ebb"), ("pressed", "#195886")],
            foreground=[("active", "#ffffff")],
        )

        style.configure(
            "Secondary.TButton",
            background="#e6edf3",
            foreground="#1f2937",
            borderwidth=0,
            focuscolor="#e6edf3",
            padding=(16, 10),
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#d5e0e8"), ("pressed", "#c8d4dd")],
        )

        style.configure(
            "Clean.Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#1f2937",
            borderwidth=0,
            rowheight=32,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Clean.Treeview.Heading",
            background="#eaf1f6",
            foreground="#16324f",
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Clean.Treeview",
            background=[("selected", "#d8e9f7")],
            foreground=[("selected", "#16324f")],
        )

    def _build_layout(self) -> None:
        # The layout is a sidebar on the left and a content area on the right.
        shell = ttk.Frame(self, style="Shell.TFrame", padding=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(shell, style="Sidebar.TFrame", padding=22)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        ttk.Label(sidebar, text="Bleem Box", style="AppTitle.TLabel").pack(anchor="w")
        ttk.Label(
            sidebar,
            text="Open one place,\nlaunch the tools you need.",
            style="SidebarText.TLabel",
            justify="left",
        ).pack(anchor="w", pady=(8, 24))

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
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=6)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        cards = ttk.Frame(frame, style="Panel.TFrame", padding=6)
        cards.grid(row=0, column=0, sticky="nsew")
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.columnconfigure(2, weight=1)
        cards.rowconfigure(0, weight=1)

        renamer_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        renamer_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        renamer_card.columnconfigure(0, weight=1)
        renamer_card.rowconfigure(1, weight=1)
        ttk.Label(renamer_card, text="Batch File Renaming", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            renamer_card,
            text="Rename many files at once with a simple base name and instant preview.",
            style="CardText.TLabel",
            wraplength=250,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Button(renamer_card, text="Open Tool", style="Primary.TButton", command=self.show_renamer).pack(anchor="center")

        qr_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        qr_card.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)
        qr_card.columnconfigure(0, weight=1)
        qr_card.rowconfigure(1, weight=1)
        ttk.Label(qr_card, text="QR Code Generator", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            qr_card,
            text="Generate a QR code for a website, image link, or music link, then save it as a PNG.",
            style="CardText.TLabel",
            wraplength=260,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Button(qr_card, text="Open Tool", style="Primary.TButton", command=self.show_qr_generator).pack(anchor="center")

        pdf_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        pdf_card.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=0)
        pdf_card.columnconfigure(0, weight=1)
        pdf_card.rowconfigure(1, weight=1)
        ttk.Label(pdf_card, text="PDF Text Scanner", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            pdf_card,
            text="Extract readable text from every PDF page, keep page breaks, and save the result as a TXT file.",
            style="CardText.TLabel",
            wraplength=260,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(10, 18))
        ttk.Button(pdf_card, text="Open Tool", style="Primary.TButton", command=self.show_pdf_scanner).pack(anchor="center")

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
