from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from i18n import t
from pdf_merge_logic import PDFMergeItem, load_pdf_merge_items, merge_pdf_items, merge_summary, update_removed_pages
from scrollable_panel import ScrollablePanel


class PDFMergeToolView(ttk.Frame):
    """UI for removing unwanted pages from PDFs, then merging them into one file."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        # This list stores the current merge order and page-removal plan for each PDF.
        self.pdf_items: list[PDFMergeItem] = []
        self.status_var = tk.StringVar(value=t("pdf_merge.status_initial"))
        self.selected_pdf_var = tk.StringVar(value=t("pdf_merge.no_selection"))
        self.remove_pages_var = tk.StringVar()
        self.summary_var = tk.StringVar(value=t("pdf_merge.summary_empty"))

        self._build_layout()

    def _build_layout(self) -> None:
        # This tool can get tall on smaller screens, so the whole view is scrollable.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        scroll_panel = ScrollablePanel(self, canvas_background="#f7f2eb")
        scroll_panel.grid(row=0, column=0, sticky="nsew")

        surface = scroll_panel.content
        surface.columnconfigure(0, weight=1)
        surface.rowconfigure(1, weight=1)

        header = ttk.Frame(surface, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text=t("pdf_merge.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("pdf_merge.subtitle"),
            style="SectionText.TLabel",
            wraplength=800,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text=t("common.back_home"), style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        content = ttk.Frame(surface, style="Panel.TFrame", padding=6)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=5)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)

        files_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        files_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        files_card.columnconfigure(0, weight=1)
        files_card.rowconfigure(3, weight=1)

        ttk.Label(files_card, text=t("pdf_merge.files_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            files_card,
            text=t("pdf_merge.files_help"),
            style="CardText.TLabel",
            wraplength=560,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        file_actions = ttk.Frame(files_card, style="Card.TFrame")
        file_actions.grid(row=2, column=0, sticky="w", pady=(18, 14))
        ttk.Button(file_actions, text=t("pdf_merge.choose_pdfs"), style="Primary.TButton", command=self.choose_pdfs).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(
            file_actions,
            text=t("pdf_merge.remove_selected"),
            style="Secondary.TButton",
            command=self.remove_selected_pdf,
        ).pack(side="left", padx=(0, 10))
        ttk.Button(file_actions, text=t("pdf_merge.move_up"), style="Secondary.TButton", command=self.move_selected_up).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(
            file_actions,
            text=t("pdf_merge.move_down"),
            style="Secondary.TButton",
            command=self.move_selected_down,
        ).pack(side="left")

        table_frame = ttk.Frame(files_card, style="Card.TFrame")
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("name", "pages", "removed", "kept")
        self.files_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Clean.Treeview")
        self.files_table.heading("name", text=t("pdf_merge.column_name"))
        self.files_table.heading("pages", text=t("pdf_merge.column_pages"))
        self.files_table.heading("removed", text=t("pdf_merge.column_removed"))
        self.files_table.heading("kept", text=t("pdf_merge.column_kept"))
        self.files_table.column("name", width=340, anchor="w")
        self.files_table.column("pages", width=90, anchor="center")
        self.files_table.column("removed", width=150, anchor="w")
        self.files_table.column("kept", width=90, anchor="center")
        self.files_table.grid(row=0, column=0, sticky="nsew")
        self.files_table.bind("<<TreeviewSelect>>", self._handle_selection_change)

        table_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.files_table.yview)
        table_scrollbar.grid(row=0, column=1, sticky="ns")
        self.files_table.configure(yscrollcommand=table_scrollbar.set)

        right_panel = ttk.Frame(content, style="Panel.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)

        pages_card = ttk.Frame(right_panel, style="Card.TFrame", padding=22)
        pages_card.grid(row=0, column=0, sticky="ew")
        pages_card.columnconfigure(0, weight=1)

        ttk.Label(pages_card, text=t("pdf_merge.remove_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            pages_card,
            text=t("pdf_merge.remove_help"),
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        ttk.Label(pages_card, text=t("pdf_merge.selected_pdf"), style="FieldLabel.TLabel").grid(row=2, column=0, sticky="w", pady=(18, 0))
        ttk.Label(
            pages_card,
            textvariable=self.selected_pdf_var,
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

        ttk.Label(pages_card, text=t("pdf_merge.pages_to_remove"), style="FieldLabel.TLabel").grid(
            row=4, column=0, sticky="w", pady=(18, 0)
        )
        ttk.Entry(pages_card, textvariable=self.remove_pages_var, style="Modern.TEntry").grid(
            row=5, column=0, sticky="ew", pady=(8, 0)
        )
        ttk.Label(
            pages_card,
            text=t("pdf_merge.range_help"),
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))

        page_actions = ttk.Frame(pages_card, style="Card.TFrame")
        page_actions.grid(row=7, column=0, sticky="w", pady=(18, 0))
        ttk.Button(
            page_actions,
            text=t("pdf_merge.apply_pages"),
            style="Primary.TButton",
            command=self.apply_page_changes,
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            page_actions,
            text=t("pdf_merge.clear_pages"),
            style="Secondary.TButton",
            command=self.clear_page_changes,
        ).pack(side="left")

        merge_card = ttk.Frame(right_panel, style="Card.TFrame", padding=22)
        merge_card.grid(row=1, column=0, sticky="nsew", pady=(14, 0))
        merge_card.columnconfigure(0, weight=1)

        ttk.Label(merge_card, text=t("pdf_merge.merge_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            merge_card,
            text=t("pdf_merge.original_files_safe"),
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 18))
        ttk.Label(
            merge_card,
            textvariable=self.summary_var,
            style="PreviewText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=2, column=0, sticky="w")

        merge_actions = ttk.Frame(merge_card, style="Card.TFrame")
        merge_actions.grid(row=3, column=0, sticky="w", pady=(18, 0))
        ttk.Button(merge_actions, text=t("pdf_merge.merge_button"), style="Primary.TButton", command=self.merge_pdfs).pack(side="left")

        status_box = ttk.Frame(surface, style="Card.TFrame", padding=0)
        status_box.grid(row=2, column=0, sticky="ew", padx=6, pady=(8, 6))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(anchor="w", fill="x")

        scroll_panel.refresh_scroll_bindings()

    def choose_pdfs(self) -> None:
        # Load the selected PDFs and reset the merge plan to match the new file list.
        pdf_paths = filedialog.askopenfilenames(
            title=t("pdf_merge.choose_dialog"),
            filetypes=[(t("dialog.filetype_pdf"), "*.pdf")],
        )
        if not pdf_paths:
            return

        try:
            self.pdf_items = load_pdf_merge_items(pdf_paths)
        except Exception as exc:
            messagebox.showerror(t("pdf_merge.title"), str(exc))
            return

        self.remove_pages_var.set("")
        self._refresh_table()
        self._select_row(0)
        self.status_var.set(t("pdf_merge.files_loaded", count=len(self.pdf_items)))

    def _refresh_table(self) -> None:
        # Rebuild the table so it always matches the current order and page settings.
        self.files_table.delete(*self.files_table.get_children())

        for index, item in enumerate(self.pdf_items):
            self.files_table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    item.path.name,
                    item.total_pages,
                    item.removed_pages_text or t("pdf_merge.none"),
                    item.kept_pages,
                ),
            )

        if not self.pdf_items:
            self.selected_pdf_var.set(t("pdf_merge.no_selection"))
            self.remove_pages_var.set("")

        self._refresh_summary()

    def _refresh_summary(self) -> None:
        pdf_count, kept_pages = merge_summary(self.pdf_items)
        if pdf_count == 0:
            self.summary_var.set(t("pdf_merge.summary_empty"))
            return

        self.summary_var.set(t("pdf_merge.summary_ready", files=pdf_count, pages=kept_pages))

    def _selected_index(self) -> int | None:
        selection = self.files_table.selection()
        if not selection:
            return None
        return int(selection[0])

    def _select_row(self, index: int) -> None:
        if not self.pdf_items or index < 0 or index >= len(self.pdf_items):
            return

        iid = str(index)
        self.files_table.selection_set(iid)
        self.files_table.focus(iid)
        self.files_table.see(iid)
        self._handle_selection_change()

    def _handle_selection_change(self, _event=None) -> None:
        index = self._selected_index()
        if index is None or index >= len(self.pdf_items):
            self.selected_pdf_var.set(t("pdf_merge.no_selection"))
            self.remove_pages_var.set("")
            return

        item = self.pdf_items[index]
        self.selected_pdf_var.set(f"{item.path.name} ({item.total_pages} {t('pdf_merge.pages_suffix')})")
        self.remove_pages_var.set(item.removed_pages_text)

    def apply_page_changes(self) -> None:
        # Page removal only affects the merge result, not the original PDFs on disk.
        index = self._selected_index()
        if index is None:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.select_pdf_first"))
            return

        try:
            updated_item = update_removed_pages(self.pdf_items[index], self.remove_pages_var.get())
        except ValueError as exc:
            messagebox.showerror(t("pdf_merge.title"), str(exc))
            return

        self.pdf_items[index] = updated_item
        self._refresh_table()
        self._select_row(index)
        self.status_var.set(t("pdf_merge.pages_updated", name=updated_item.path.name))

    def clear_page_changes(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.select_pdf_first"))
            return

        self.remove_pages_var.set("")
        self.apply_page_changes()

    def remove_selected_pdf(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.select_pdf_first"))
            return

        removed_item = self.pdf_items.pop(index)
        self._refresh_table()

        if self.pdf_items:
            self._select_row(min(index, len(self.pdf_items) - 1))
        else:
            self.status_var.set(t("pdf_merge.status_initial"))

        self.status_var.set(t("pdf_merge.file_removed", name=removed_item.path.name))

    def move_selected_up(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.select_pdf_first"))
            return
        if index == 0:
            return

        self.pdf_items[index - 1], self.pdf_items[index] = self.pdf_items[index], self.pdf_items[index - 1]
        self._refresh_table()
        self._select_row(index - 1)
        self.status_var.set(t("pdf_merge.order_updated"))

    def move_selected_down(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.select_pdf_first"))
            return
        if index >= len(self.pdf_items) - 1:
            return

        self.pdf_items[index], self.pdf_items[index + 1] = self.pdf_items[index + 1], self.pdf_items[index]
        self._refresh_table()
        self._select_row(index + 1)
        self.status_var.set(t("pdf_merge.order_updated"))

    def merge_pdfs(self) -> None:
        if not self.pdf_items:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.choose_first"))
            return

        default_name = "merged.pdf"
        if self.pdf_items:
            default_name = f"{self.pdf_items[0].path.stem}_merged.pdf"

        save_path = filedialog.asksaveasfilename(
            title=t("pdf_merge.save_dialog"),
            defaultextension=".pdf",
            filetypes=[(t("dialog.filetype_pdf"), "*.pdf")],
            initialfile=default_name,
        )
        if not save_path:
            return

        try:
            written_pages = merge_pdf_items(self.pdf_items, save_path)
        except Exception as exc:
            messagebox.showerror(t("pdf_merge.title"), t("pdf_merge.merge_failed", error=exc))
            return

        output_name = Path(save_path).name
        self.status_var.set(t("pdf_merge.saved_status", name=output_name, pages=written_pages))
        messagebox.showinfo(t("pdf_merge.title"), t("pdf_merge.saved_info", path=save_path))
