from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import ImageTk

from qr_logic import build_qr_image


class QRCodeGeneratorView(ttk.Frame):
    """UI for generating and saving QR codes."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        # These values hold the current link and the last QR image that was generated.
        self.qr_input_var = tk.StringVar()
        self.qr_status_var = tk.StringVar(value="Paste a link to generate a QR code.")
        self.qr_image = None
        self.qr_photo: ImageTk.PhotoImage | None = None

        self._build_layout()

    def _build_layout(self) -> None:
        # This frame contains the QR form on the left and the image preview on the right.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="QR Code Generator", style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Paste a link to a website page, then generate a QR code to share and scan.",
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Button(header, text="Back to Home", style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        content = ttk.Frame(self, style="Panel.TFrame", padding=6)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        controls_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        controls_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        controls_card.columnconfigure(0, weight=1)

        ttk.Label(controls_card, text="Link", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            controls_card,
            text="Use any link that opens a website, image, playlist, song, or video.",
            style="CardText.TLabel",
            wraplength=340,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(6, 12))

        ttk.Entry(controls_card, textvariable=self.qr_input_var).grid(row=2, column=0, sticky="ew")

        quick_links = ttk.Frame(controls_card, style="Card.TFrame")
        quick_links.grid(row=3, column=0, sticky="w", pady=(14, 0))
        ttk.Button(
            quick_links,
            text="Website Example",
            style="Secondary.TButton",
            command=lambda: self._set_qr_link("https://www.wikipedia.org/"),
        ).pack(side="left", padx=(0, 10))

        action_row = ttk.Frame(controls_card, style="Card.TFrame")
        action_row.grid(row=4, column=0, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text="Generate QR Code", style="Primary.TButton", command=self.generate_qr_code).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(action_row, text="Save PNG", style="Secondary.TButton", command=self.save_qr_code).pack(side="left")

        status_box = ttk.Frame(controls_card, style="Card.TFrame", padding=0)
        status_box.grid(row=5, column=0, sticky="ew", pady=(18, 0))
        ttk.Label(status_box, textvariable=self.qr_status_var, style="Status.TLabel", padding=(12, 9)).pack(
            anchor="w", fill="x"
        )

        preview_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        preview_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(1, weight=1)

        ttk.Label(preview_card, text="QR Preview", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.qr_preview_label = ttk.Label(
            preview_card,
            text="Your QR code will appear here.",
            style="CardText.TLabel",
            anchor="center",
            justify="center",
        )
        self.qr_preview_label.grid(row=1, column=0, sticky="nsew", pady=(18, 0))

    def _set_qr_link(self, link: str) -> None:
        # This helper fills the entry box with a sample link.
        self.qr_input_var.set(link)

    def generate_qr_code(self) -> None:
        # Generate the full-size QR image, then scale a copy for the preview area.
        try:
            qr_image = build_qr_image(self.qr_input_var.get())
        except ValueError as exc:
            messagebox.showerror("QR Code Generator", str(exc))
            return

        preview_image = qr_image.copy()
        preview_image.thumbnail((360, 360))

        self.qr_image = qr_image
        self.qr_photo = ImageTk.PhotoImage(preview_image)
        self.qr_preview_label.configure(image=self.qr_photo, text="")
        self.qr_status_var.set("QR code ready. Save it as a PNG or scan it now.")

    def save_qr_code(self) -> None:
        # Save the full-size QR image as a PNG file.
        if self.qr_image is None:
            messagebox.showerror("QR Code Generator", "Generate a QR code first.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save QR Code",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qr_code.png",
        )
        if not save_path:
            return

        self.qr_image.save(save_path, format="PNG")
        self.qr_status_var.set(f"Saved QR code to {Path(save_path).name}.")
        messagebox.showinfo("QR Code Generator", f"Saved QR code to:\n{save_path}")
