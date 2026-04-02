from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf_logic import extract_pdf_text


class PDFTextScannerView(ttk.Frame):
    """UI for extracting readable text from every page of a PDF."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        self.selected_pdf_path: Path | None = None
        self.extracted_text = ""
        self.status_var = tk.StringVar(value="Choose a PDF to scan its text.")
        self.file_label_var = tk.StringVar(value="No PDF selected yet.")

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="PDF Text Scanner", style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Open a PDF, extract the full text page by page, and use OCR automatically when a page is scanned.",
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text="Back to Home", style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        controls_card = ttk.Frame(self, style="Card.TFrame", padding=22)
        controls_card.grid(row=1, column=0, sticky="ew", padx=6, pady=(0, 14))
        controls_card.columnconfigure(0, weight=1)

        ttk.Label(controls_card, text="Selected PDF", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            controls_card,
            textvariable=self.file_label_var,
            style="CardText.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        action_row = ttk.Frame(controls_card, style="Card.TFrame")
        action_row.grid(row=2, column=0, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text="Choose PDF", style="Primary.TButton", command=self.choose_pdf).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(action_row, text="Extract Text", style="Secondary.TButton", command=self.extract_text).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(action_row, text="Save TXT", style="Secondary.TButton", command=self.save_text).pack(side="left")

        status_box = ttk.Frame(controls_card, style="Card.TFrame", padding=0)
        status_box.grid(row=3, column=0, sticky="ew", pady=(18, 0))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(
            anchor="w", fill="x"
        )

        preview_card = ttk.Frame(self, style="Card.TFrame", padding=22)
        preview_card.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(1, weight=1)

        ttk.Label(preview_card, text="Extracted Text", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        text_frame = ttk.Frame(preview_card, style="Card.TFrame")
        text_frame.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            background="#fffdf9",
            foreground="#21303a",
            insertbackground="#21303a",
            selectbackground="#f1d7c2",
            padx=12,
            pady=12,
            undo=False,
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def choose_pdf(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title="Choose PDF",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not pdf_path:
            return

        self.selected_pdf_path = Path(pdf_path)
        self.file_label_var.set(self.selected_pdf_path.name)
        self.extract_text()

    def extract_text(self) -> None:
        if self.selected_pdf_path is None:
            messagebox.showerror("PDF Text Scanner", "Choose a PDF first.")
            return

        try:
            extracted_text = extract_pdf_text(self.selected_pdf_path)
        except Exception as exc:
            messagebox.showerror("PDF Text Scanner", f"Could not extract text:\n{exc}")
            return

        self.extracted_text = extracted_text
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", extracted_text)
        self.status_var.set(f"Extracted text from {self.selected_pdf_path.name}.")

    def save_text(self) -> None:
        if not self.extracted_text:
            messagebox.showerror("PDF Text Scanner", "Extract text from a PDF first.")
            return

        default_name = "pdf_text.txt"
        if self.selected_pdf_path is not None:
            default_name = f"{self.selected_pdf_path.stem}.txt"

        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Text",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile=default_name,
        )
        if not save_path:
            return

        Path(save_path).write_text(self.extracted_text, encoding="utf-8")
        self.status_var.set(f"Saved extracted text to {Path(save_path).name}.")
        messagebox.showinfo("PDF Text Scanner", f"Saved extracted text to:\n{save_path}")
