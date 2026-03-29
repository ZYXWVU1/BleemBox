from __future__ import annotations

import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from rename_logic import build_rename_preview, rename_files


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

        self.selected_files: list[str] = []
        self.base_name_var = tk.StringVar(value="file")
        self.start_number_var = tk.StringVar(value="1")
        self.keep_extension_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Choose files to start.")

        # Build the window once, then switch between the home screen and tools inside it.
        self._build_styles()
        self._build_layout()
        self._bind_live_preview()
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
            "ToolCard.TButton",
            background="#ffffff",
            foreground="#16324f",
            borderwidth=0,
            focuscolor="#ffffff",
            padding=(24, 20),
            font=("Segoe UI Semibold", 12),
        )
        style.map(
            "ToolCard.TButton",
            background=[("active", "#f1f6fa"), ("pressed", "#e7eff6")],
            foreground=[("active", "#16324f")],
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
        # The app uses a fixed sidebar plus a main content area that swaps views.
        shell = ttk.Frame(self, style="Shell.TFrame", padding=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(shell, style="Sidebar.TFrame", padding=22)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        ttk.Label(self.sidebar, text="Bleem Box", style="AppTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self.sidebar,
            text="Open one place,\nlaunch the tools you need.",
            style="SidebarText.TLabel",
            justify="left",
        ).pack(anchor="w", pady=(8, 24))

        ttk.Button(self.sidebar, text="Home", style="Nav.TButton", command=self.show_home).pack(fill="x", pady=(0, 8))
        ttk.Button(
            self.sidebar,
            text="Batch file renaming",
            style="Nav.TButton",
            command=self.show_renamer,
        ).pack(fill="x")

        self.content = ttk.Frame(shell, style="Panel.TFrame", padding=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.home_view = self._build_home_view(self.content)
        self.renamer_view = self._build_renamer_view(self.content)

    def _bind_live_preview(self) -> None:
        # Any change to these inputs should immediately refresh the rename preview.
        self.base_name_var.trace_add("write", self._handle_live_preview)
        self.start_number_var.trace_add("write", self._handle_live_preview)
        self.keep_extension_var.trace_add("write", self._handle_live_preview)

    def _handle_live_preview(self, *_args) -> None:
        if self.selected_files:
            self.refresh_preview()

    def _build_home_view(self, parent: ttk.Frame) -> ttk.Frame:
        # This is the first screen the user sees: a launcher for toolbox apps.
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=0)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        hero = ttk.Frame(frame, style="Hero.TFrame", padding=28)
        hero.grid(row=0, column=0, sticky="ew")
        hero.columnconfigure(0, weight=1)

        ttk.Label(hero, text="Simple tools, one clean desktop app.", style="HeroTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            hero,
            text="Start from the toolbox home screen, then open any tool when you need it.",
            style="HeroText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(10, 16))
        ttk.Button(hero, text="Open Batch File Renaming", style="Primary.TButton", command=self.show_renamer).grid(
            row=2, column=0, sticky="w"
        )

        intro = ttk.Frame(frame, style="Panel.TFrame", padding=(6, 24, 6, 12))
        intro.grid(row=1, column=0, sticky="ew")
        ttk.Label(intro, text="Available Tools", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(
            intro,
            text="The first tool is ready now. More tools can be added to this home page later.",
            style="SectionText.TLabel",
        ).pack(anchor="w", pady=(6, 0))

        cards = ttk.Frame(frame, style="Panel.TFrame", padding=6)
        cards.grid(row=2, column=0, sticky="nsew")
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)

        renamer_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        renamer_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        ttk.Label(renamer_card, text="Batch File Renaming", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            renamer_card,
            text="Rename many files at once with a simple base name and instant preview.",
            style="CardText.TLabel",
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(10, 18))
        ttk.Button(
            renamer_card,
            text="Launch Tool",
            style="Primary.TButton",
            command=self.show_renamer,
        ).pack(anchor="w")

        placeholder_card = ttk.Frame(cards, style="Card.TFrame", padding=22)
        placeholder_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        ttk.Label(placeholder_card, text="Next Tool Slot", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            placeholder_card,
            text="This space is ready for the next app you want inside the toolbox.",
            style="CardText.TLabel",
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(10, 18))
        ttk.Button(placeholder_card, text="Coming Soon", style="Secondary.TButton").pack(anchor="w")

        return frame

    def _build_renamer_view(self, parent: ttk.Frame) -> ttk.Frame:
        # The renamer tool lives in its own view, but still inside the same window.
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=0)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        header = ttk.Frame(frame, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Rename Multiple Files", style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Select files, preview the new names, then rename everything in one step.",
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Button(header, text="Back to Home", style="Secondary.TButton", command=self.show_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        controls_card = ttk.Frame(frame, style="Card.TFrame", padding=22)
        controls_card.grid(row=1, column=0, sticky="ew", padx=6, pady=(0, 14))
        controls_card.columnconfigure(1, weight=1)
        controls_card.columnconfigure(3, weight=1)

        ttk.Label(controls_card, text="Files", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(controls_card, text="Choose Files", style="Primary.TButton", command=self.choose_files).grid(
            row=1, column=0, sticky="w", padx=(0, 18), pady=(8, 0)
        )

        ttk.Label(controls_card, text="Base name", style="FieldLabel.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Entry(controls_card, textvariable=self.base_name_var).grid(row=1, column=1, sticky="ew", padx=(0, 18), pady=(8, 0))

        ttk.Label(controls_card, text="Start number", style="FieldLabel.TLabel").grid(row=0, column=2, sticky="w")
        ttk.Entry(controls_card, textvariable=self.start_number_var, width=10).grid(
            row=1, column=2, sticky="w", padx=(0, 18), pady=(8, 0)
        )

        options = ttk.Frame(controls_card, style="Card.TFrame")
        options.grid(row=1, column=3, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            options,
            text="Keep file extensions",
            variable=self.keep_extension_var,
        ).pack(anchor="w")

        action_row = ttk.Frame(controls_card, style="Card.TFrame")
        action_row.grid(row=2, column=0, columnspan=4, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text="Rename Files", style="Primary.TButton", command=self.perform_rename).pack(side="left")

        preview_card = ttk.Frame(frame, style="Card.TFrame", padding=22)
        preview_card.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(2, weight=1)

        ttk.Label(preview_card, text="Preview", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        status_box = ttk.Frame(preview_card, style="Card.TFrame", padding=0)
        status_box.grid(row=1, column=0, sticky="ew", pady=(10, 14))
        status_label = ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9))
        status_label.pack(anchor="w", fill="x")

        table_frame = ttk.Frame(preview_card, style="Card.TFrame")
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("original", "new")
        self.preview_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Clean.Treeview")
        self.preview_table.heading("original", text="Current Name")
        self.preview_table.heading("new", text="New Name")
        self.preview_table.column("original", width=360, anchor="w")
        self.preview_table.column("new", width=360, anchor="w")
        self.preview_table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.preview_table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.preview_table.configure(yscrollcommand=scrollbar.set)

        return frame

    def show_home(self) -> None:
        # Hide the tool view and bring the toolbox landing page back.
        self.renamer_view.grid_forget()
        self.home_view.grid(row=0, column=0, sticky="nsew")

    def show_renamer(self) -> None:
        # Hide the home screen and show the batch renaming tool.
        self.home_view.grid_forget()
        self.renamer_view.grid(row=0, column=0, sticky="nsew")

    def choose_files(self) -> None:
        paths = filedialog.askopenfilenames(title="Choose files to rename")
        if not paths:
            return
        # Store the selected file paths so the preview and rename step use the same list.
        self.selected_files = list(paths)
        self.status_var.set(f"{len(self.selected_files)} file(s) selected.")
        self.refresh_preview()

    def _parse_start_number(self) -> int:
        raw_value = self.start_number_var.get().strip()
        try:
            number = int(raw_value)
        except ValueError as exc:
            raise ValueError("Start number must be a whole number.") from exc

        if number < 1:
            raise ValueError("Start number must be 1 or higher.")
        return number

    def _get_preview(self):
        # Centralize preview creation so both the UI table and rename action stay in sync.
        start_number = self._parse_start_number()
        return build_rename_preview(
            self.selected_files,
            self.base_name_var.get(),
            start_number=start_number,
            keep_extension=self.keep_extension_var.get(),
        )

    def refresh_preview(self) -> None:
        # Rebuild the table from scratch to match the latest inputs.
        self.preview_table.delete(*self.preview_table.get_children())

        try:
            preview = self._get_preview()
        except ValueError as exc:
            if self.selected_files:
                self.status_var.set(str(exc))
            return

        for item in preview:
            self.preview_table.insert("", "end", values=(item.original_name, item.new_name))
        self.status_var.set(f"Preview ready for {len(preview)} file(s).")

    def perform_rename(self) -> None:
        try:
            preview = self._get_preview()
        except ValueError as exc:
            messagebox.showerror("Rename Files", str(exc))
            return

        # Ask for confirmation before changing anything on disk.
        confirm = messagebox.askyesno("Rename Files", f"Rename {len(preview)} file(s)?")
        if not confirm:
            return

        try:
            renamed_count = rename_files(preview)
        except Exception as exc:
            messagebox.showerror("Rename Files", f"Rename failed:\n{exc}")
            return

        # Update the stored paths so the app still points at the renamed files afterward.
        self.selected_files = [str(Path(item.path).with_name(item.new_name)) for item in preview]
        self.refresh_preview()
        self.status_var.set(f"Renamed {renamed_count} file(s) successfully.")
        messagebox.showinfo("Rename Files", f"Renamed {renamed_count} file(s).")


def run() -> None:
    enable_windows_dpi_awareness()
    app = ToolboxApp()
    app.mainloop()
