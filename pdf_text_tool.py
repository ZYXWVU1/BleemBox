from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from i18n import t
from scrollable_panel import ScrollablePanel
from pdf_logic import extract_pdf_text
from ui_fonts import ui_font


class PDFTextScannerView(ttk.Frame):
    """UI for extracting readable text from every page of a PDF."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        self.selected_pdf_path: Path | None = None
        self.extracted_text = ""
        self.status_var = tk.StringVar(value=t("pdf.status_initial"))
        self.file_label_var = tk.StringVar(value=t("pdf.no_file"))

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        scroll_panel = ScrollablePanel(self, canvas_background="#f6f6f7")
        scroll_panel.grid(row=0, column=0, sticky="nsew")
        surface = scroll_panel.content
        surface.columnconfigure(0, weight=1)

        header = ttk.Frame(surface, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text=t("pdf.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("pdf.subtitle"),
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        controls_card = ttk.Frame(surface, style="Card.TFrame", padding=24)
        controls_card.grid(row=1, column=0, sticky="ew", padx=6, pady=(0, 14))
        controls_card.columnconfigure(0, weight=1)

        ttk.Label(controls_card, text=t("pdf.selected_pdf"), style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            controls_card,
            textvariable=self.file_label_var,
            style="CardText.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        action_row = ttk.Frame(controls_card, style="Card.TFrame")
        action_row.grid(row=2, column=0, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text=t("pdf.choose_pdf"), style="Primary.TButton", command=self.choose_pdf).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(action_row, text=t("pdf.extract_text"), style="Secondary.TButton", command=self.extract_text).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(action_row, text=t("pdf.save_txt"), style="Secondary.TButton", command=self.save_text).pack(side="left")

        status_box = ttk.Frame(controls_card, style="Card.TFrame", padding=0)
        status_box.grid(row=3, column=0, sticky="ew", pady=(18, 0))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(
            anchor="w", fill="x"
        )

        preview_card = ttk.Frame(surface, style="Card.TFrame", padding=24)
        preview_card.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(1, weight=1)

        ttk.Label(preview_card, text=t("pdf.extracted_text"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        text_frame = ttk.Frame(preview_card, style="Card.TFrame")
        text_frame.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(
            text_frame,
            wrap="word",
            font=ui_font(10),
            relief="flat",
            borderwidth=0,
            background="#fafafb",
            foreground="#242629",
            insertbackground="#242629",
            selectbackground="#dedfe3",
            selectforeground="#242629",
            width=1,
            highlightthickness=1,
            highlightbackground="#dcdde0",
            highlightcolor="#62666d",
            padx=12,
            pady=12,
            undo=False,
            height=14,
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)

        scroll_panel.refresh_scroll_bindings()

    def choose_pdf(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title=t("pdf.choose_dialog"),
            filetypes=[(t("dialog.filetype_pdf"), "*.pdf")],
        )
        if not pdf_path:
            return

        self.selected_pdf_path = Path(pdf_path)
        self.file_label_var.set(self.selected_pdf_path.name)
        self.extract_text()

    def extract_text(self) -> None:
        if self.selected_pdf_path is None:
            messagebox.showerror(t("pdf.title"), t("pdf.choose_first"))
            return

        try:
            extracted_text = extract_pdf_text(self.selected_pdf_path)
        except Exception as exc:
            messagebox.showerror(t("pdf.title"), t("pdf.extract_failed", error=exc))
            return

        self.extracted_text = extracted_text
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", extracted_text)
        self.status_var.set(t("pdf.extracted_status", name=self.selected_pdf_path.name))

    def save_text(self) -> None:
        if not self.extracted_text:
            messagebox.showerror(t("pdf.title"), t("pdf.extract_first"))
            return

        default_name = "pdf_text.txt"
        if self.selected_pdf_path is not None:
            default_name = f"{self.selected_pdf_path.stem}.txt"

        save_path = filedialog.asksaveasfilename(
            title=t("pdf.save_dialog"),
            defaultextension=".txt",
            filetypes=[(t("dialog.filetype_text"), "*.txt")],
            initialfile=default_name,
        )
        if not save_path:
            return

        Path(save_path).write_text(self.extracted_text, encoding="utf-8")
        self.status_var.set(t("pdf.saved_status", name=Path(save_path).name))
        messagebox.showinfo(t("pdf.title"), t("pdf.saved_info", path=save_path))
