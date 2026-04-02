from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from i18n import t
from rename_logic import build_rename_preview, rename_files


class BatchRenamerView(ttk.Frame):
    """UI for the batch file renaming tool."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        # These variables store the current form values for the renamer tool.
        self.selected_files: list[str] = []
        self.base_name_var = tk.StringVar(value=t("renamer.default_base_name"))
        self.start_number_var = tk.StringVar(value="1")
        self.keep_extension_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value=t("renamer.status_initial"))

        self._build_layout()
        self._bind_live_preview()

    def _build_layout(self) -> None:
        # This frame contains the renamer header, controls, and preview table.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text=t("renamer.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("renamer.subtitle"),
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text=t("common.back_home"), style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        controls_card = ttk.Frame(self, style="Card.TFrame", padding=22)
        controls_card.grid(row=1, column=0, sticky="ew", padx=6, pady=(0, 14))
        controls_card.columnconfigure(1, weight=1)
        controls_card.columnconfigure(3, weight=1)

        ttk.Label(controls_card, text=t("renamer.label_files"), style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(controls_card, text=t("renamer.choose_files"), style="Primary.TButton", command=self.choose_files).grid(
            row=1, column=0, sticky="w", padx=(0, 18), pady=(8, 0)
        )

        ttk.Label(controls_card, text=t("renamer.label_base_name"), style="FieldLabel.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Entry(controls_card, textvariable=self.base_name_var, style="Modern.TEntry").grid(
            row=1, column=1, sticky="ew", padx=(0, 18), pady=(8, 0)
        )

        ttk.Label(controls_card, text=t("renamer.label_start_number"), style="FieldLabel.TLabel").grid(row=0, column=2, sticky="w")
        ttk.Entry(controls_card, textvariable=self.start_number_var, width=10, style="Modern.TEntry").grid(
            row=1, column=2, sticky="w", padx=(0, 18), pady=(8, 0)
        )

        options = ttk.Frame(controls_card, style="Card.TFrame")
        options.grid(row=1, column=3, sticky="w", pady=(8, 0))
        ttk.Checkbutton(options, text=t("renamer.keep_extensions"), variable=self.keep_extension_var, style="Modern.TCheckbutton").pack(
            anchor="w"
        )

        action_row = ttk.Frame(controls_card, style="Card.TFrame")
        action_row.grid(row=2, column=0, columnspan=4, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text=t("renamer.rename_files"), style="Primary.TButton", command=self.perform_rename).pack(side="left")

        preview_card = ttk.Frame(self, style="Card.TFrame", padding=22)
        preview_card.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(2, weight=1)

        ttk.Label(preview_card, text=t("renamer.preview"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        status_box = ttk.Frame(preview_card, style="Card.TFrame", padding=0)
        status_box.grid(row=1, column=0, sticky="ew", pady=(10, 14))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(
            anchor="w", fill="x"
        )

        table_frame = ttk.Frame(preview_card, style="Card.TFrame")
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("original", "new")
        self.preview_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Clean.Treeview")
        self.preview_table.heading("original", text=t("renamer.current_name"))
        self.preview_table.heading("new", text=t("renamer.new_name"))
        self.preview_table.column("original", width=360, anchor="w")
        self.preview_table.column("new", width=360, anchor="w")
        self.preview_table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.preview_table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.preview_table.configure(yscrollcommand=scrollbar.set)

    def _bind_live_preview(self) -> None:
        # Whenever the form changes, rebuild the rename preview automatically.
        self.base_name_var.trace_add("write", self._handle_live_preview)
        self.start_number_var.trace_add("write", self._handle_live_preview)
        self.keep_extension_var.trace_add("write", self._handle_live_preview)

    def _handle_live_preview(self, *_args) -> None:
        if self.selected_files:
            self.refresh_preview()

    def choose_files(self) -> None:
        # The selected paths are reused for previewing and the final rename action.
        paths = filedialog.askopenfilenames(title=t("renamer.choose_files_dialog"))
        if not paths:
            return

        self.selected_files = list(paths)
        self.status_var.set(t("renamer.selected_count", count=len(self.selected_files)))
        self.refresh_preview()

    def _parse_start_number(self) -> int:
        raw_value = self.start_number_var.get().strip()
        try:
            number = int(raw_value)
        except ValueError as exc:
            raise ValueError(t("renamer.start_number_whole")) from exc

        if number < 1:
            raise ValueError(t("renamer.start_number_positive"))
        return number

    def _get_preview(self):
        # The preview is built from the current UI state so the table and rename action match.
        return build_rename_preview(
            self.selected_files,
            self.base_name_var.get(),
            start_number=self._parse_start_number(),
            keep_extension=self.keep_extension_var.get(),
        )

    def refresh_preview(self) -> None:
        # Redraw the entire preview table so it always reflects the latest values.
        self.preview_table.delete(*self.preview_table.get_children())

        try:
            preview = self._get_preview()
        except ValueError as exc:
            if self.selected_files:
                self.status_var.set(str(exc))
            return

        for item in preview:
            self.preview_table.insert("", "end", values=(item.original_name, item.new_name))
        self.status_var.set(t("renamer.preview_ready", count=len(preview)))

    def perform_rename(self) -> None:
        try:
            preview = self._get_preview()
        except ValueError as exc:
            messagebox.showerror(t("renamer.rename_files"), str(exc))
            return

        # Ask before renaming because this tool changes files on disk.
        confirm = messagebox.askyesno(t("renamer.rename_files"), t("renamer.confirm_rename", count=len(preview)))
        if not confirm:
            return

        try:
            renamed_count = rename_files(preview)
        except Exception as exc:
            messagebox.showerror(t("renamer.rename_files"), t("renamer.rename_failed", error=exc))
            return

        # Replace the stored paths with the new names so the tool can keep working afterward.
        self.selected_files = [str(Path(item.path).with_name(item.new_name)) for item in preview]
        self.refresh_preview()
        self.status_var.set(t("renamer.renamed_success", count=renamed_count))
        messagebox.showinfo(t("renamer.rename_files"), t("renamer.renamed_info", count=renamed_count))
