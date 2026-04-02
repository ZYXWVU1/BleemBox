from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from cursor_logic import (
    CursorPreset,
    apply_arrow_cursor,
    apply_cursor_skin_folder,
    ensure_cursor_template_files,
    is_windows_supported,
    reset_cursor_skin_to_default,
    starter_cursor_presets,
)
from i18n import t


class CursorSkinToolView(ttk.Frame):
    """UI for applying mouse cursor skins on Windows."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        self.selected_cursor_file: Path | None = None
        self.selected_skin_folder: Path | None = None
        self.template_dir = ensure_cursor_template_files()
        self.cursor_file_var = tk.StringVar(value=t("cursor.no_custom_file"))
        self.skin_folder_var = tk.StringVar(value=t("cursor.no_skin_folder"))
        self.status_var = tk.StringVar(value=t("cursor.status_initial"))
        self.presets = starter_cursor_presets()
        self.scroll_canvas: tk.Canvas | None = None
        self.scroll_content: ttk.Frame | None = None
        self.scroll_window_id: int | None = None
        self.preset_images: list[ImageTk.PhotoImage] = []

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        scroll_shell = ttk.Frame(self, style="Panel.TFrame")
        scroll_shell.grid(row=0, column=0, sticky="nsew")
        scroll_shell.columnconfigure(0, weight=1)
        scroll_shell.rowconfigure(0, weight=1)

        self.scroll_canvas = tk.Canvas(
            scroll_shell,
            background="#f7f2eb",
            borderwidth=0,
            highlightthickness=0,
        )
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(scroll_shell, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_content = ttk.Frame(self.scroll_canvas, style="Panel.TFrame", padding=0)
        self.scroll_window_id = self.scroll_canvas.create_window((0, 0), window=self.scroll_content, anchor="nw")
        self.scroll_content.bind("<Configure>", self._handle_content_configure)
        self.scroll_canvas.bind("<Configure>", self._handle_canvas_configure)

        surface = self.scroll_content
        surface.columnconfigure(0, weight=1)
        surface.rowconfigure(2, weight=1)

        header = ttk.Frame(surface, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text=t("cursor.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("cursor.subtitle"),
            style="SectionText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text=t("common.back_home"), style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        if not is_windows_supported():
            ttk.Label(
                surface,
                text=t("cursor.windows_only"),
                style="Status.TLabel",
                padding=(12, 9),
            ).grid(row=1, column=0, sticky="ew", padx=6, pady=(0, 6))
            return

        content = ttk.Frame(surface, style="Panel.TFrame", padding=6)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        custom_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        custom_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        custom_card.columnconfigure(0, weight=1)

        ttk.Label(custom_card, text=t("cursor.custom_skin"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            custom_card,
            text=t("cursor.custom_skin_help"),
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(10, 18))

        ttk.Label(custom_card, text=t("cursor.selected_cursor_file"), style="FieldLabel.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Label(
            custom_card,
            textvariable=self.cursor_file_var,
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

        file_actions = ttk.Frame(custom_card, style="Card.TFrame")
        file_actions.grid(row=4, column=0, sticky="w", pady=(14, 0))
        ttk.Button(file_actions, text=t("cursor.choose_cursor_file"), style="Primary.TButton", command=self.choose_cursor_file).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(file_actions, text=t("cursor.apply_file"), style="Secondary.TButton", command=self.apply_selected_cursor_file).pack(
            side="left"
        )

        ttk.Label(custom_card, text=t("cursor.selected_skin_folder"), style="FieldLabel.TLabel").grid(
            row=5, column=0, sticky="w", pady=(20, 0)
        )
        ttk.Label(
            custom_card,
            textvariable=self.skin_folder_var,
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))

        folder_actions = ttk.Frame(custom_card, style="Card.TFrame")
        folder_actions.grid(row=7, column=0, sticky="w", pady=(14, 0))
        ttk.Button(folder_actions, text=t("cursor.choose_skin_folder"), style="Primary.TButton", command=self.choose_skin_folder).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(
            folder_actions,
            text=t("cursor.apply_folder"),
            style="Secondary.TButton",
            command=self.apply_selected_skin_folder,
        ).pack(side="left")

        reset_row = ttk.Frame(custom_card, style="Card.TFrame")
        reset_row.grid(row=8, column=0, sticky="w", pady=(20, 0))
        ttk.Button(
            reset_row,
            text=t("cursor.reset_default"),
            style="Secondary.TButton",
            command=self.reset_to_default_skin,
        ).pack(side="left")

        starter_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        starter_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        starter_card.columnconfigure(0, weight=1)

        ttk.Label(starter_card, text=t("cursor.starter_presets"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            starter_card,
            text=t("cursor.starter_help"),
            style="CardText.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(10, 18))

        presets_frame = ttk.Frame(starter_card, style="Card.TFrame")
        presets_frame.grid(row=2, column=0, sticky="nsew")
        presets_frame.columnconfigure(0, weight=1)
        presets_frame.columnconfigure(1, weight=1)

        if self.presets:
            for row_index, preset in enumerate(self.presets):
                card = ttk.Frame(presets_frame, style="Muted.TFrame", padding=14)
                card.grid(row=row_index // 2, column=row_index % 2, sticky="nsew", padx=(0, 10) if row_index % 2 == 0 else 0, pady=(0, 10))
                card.columnconfigure(0, weight=1)
                preview_image = self._build_preset_preview(preset.cursor_path)
                image_button = tk.Button(
                    card,
                    image=preview_image,
                    command=lambda item=preset: self.apply_preset(item),
                    relief="flat",
                    borderwidth=0,
                    background="#efe5d7",
                    activebackground="#e7dac9",
                    cursor="hand2",
                )
                image_button.grid(row=0, column=0, sticky="w")
                ttk.Label(card, text=preset.name, style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 0))
                ttk.Label(
                    card,
                    text=preset.description,
                    style="CardText.TLabel",
                    wraplength=180,
                    justify="left",
                ).grid(row=2, column=0, sticky="w", pady=(6, 0))
        else:
            ttk.Label(
                presets_frame,
                text=t("cursor.no_presets"),
                style="CardText.TLabel",
            ).grid(row=0, column=0, sticky="w")

        status_box = ttk.Frame(surface, style="Card.TFrame", padding=0)
        status_box.grid(row=2, column=0, sticky="ew", padx=6, pady=(8, 12))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(
            anchor="w", fill="x"
        )

        self._install_scroll_bindings(self)

    def _build_preset_preview(self, cursor_path: Path) -> ImageTk.PhotoImage:
        tile_size = 112
        background = Image.new("RGBA", (tile_size, tile_size), "#efe5d7")

        try:
            cursor_image = Image.open(cursor_path).convert("RGBA")
        except Exception:
            cursor_image = Image.new("RGBA", (48, 48), (199, 104, 56, 255))

        cursor_image.thumbnail((72, 72), Image.Resampling.LANCZOS)
        offset_x = (tile_size - cursor_image.width) // 2
        offset_y = (tile_size - cursor_image.height) // 2
        background.alpha_composite(cursor_image, (offset_x, offset_y))

        preview = ImageTk.PhotoImage(background)
        self.preset_images.append(preview)
        return preview

    def _handle_content_configure(self, _event: tk.Event) -> None:
        if self.scroll_canvas is None or self.scroll_content is None:
            return
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _handle_canvas_configure(self, event: tk.Event) -> None:
        if self.scroll_canvas is None or self.scroll_content is None or self.scroll_window_id is None:
            return
        self.scroll_canvas.itemconfigure(self.scroll_window_id, width=event.width)

    def _bind_mousewheel(self, _event: tk.Event) -> None:
        self.bind_all("<MouseWheel>", self._handle_mousewheel)

    def _unbind_mousewheel(self, _event: tk.Event) -> None:
        self.unbind_all("<MouseWheel>")

    def _install_scroll_bindings(self, widget: tk.Misc) -> None:
        widget.bind("<Enter>", self._bind_mousewheel, add="+")
        widget.bind("<Leave>", self._unbind_mousewheel, add="+")
        for child in widget.winfo_children():
            self._install_scroll_bindings(child)

    def _handle_mousewheel(self, event: tk.Event) -> None:
        if self.scroll_canvas is None:
            return
        self.scroll_canvas.yview_scroll(int(-event.delta / 120), "units")

    def choose_cursor_file(self) -> None:
        cursor_path = filedialog.askopenfilename(
            title=t("cursor.choose_file_dialog"),
            filetypes=[(t("dialog.filetype_cursor"), "*.cur *.ani")],
        )
        if not cursor_path:
            return

        self.selected_cursor_file = Path(cursor_path)
        self.cursor_file_var.set(self.selected_cursor_file.name)
        self.status_var.set(t("cursor.file_selected_status"))

    def apply_selected_cursor_file(self) -> None:
        if self.selected_cursor_file is None:
            messagebox.showerror(t("cursor.title"), t("cursor.choose_file_first"))
            return

        confirm = messagebox.askyesno(
            t("cursor.title"),
            t("cursor.confirm_apply_file"),
        )
        if not confirm:
            return

        try:
            status = apply_arrow_cursor(self.selected_cursor_file)
        except Exception as exc:
            messagebox.showerror(t("cursor.title"), t("cursor.apply_file_failed", error=exc))
            return

        self.status_var.set(status)
        messagebox.showinfo(t("cursor.title"), status)

    def choose_skin_folder(self) -> None:
        folder_path = filedialog.askdirectory(title=t("cursor.choose_folder_dialog"))
        if not folder_path:
            return

        self.selected_skin_folder = Path(folder_path)
        self.skin_folder_var.set(self.selected_skin_folder.name)
        self.status_var.set(t("cursor.folder_selected_status"))

    def apply_selected_skin_folder(self) -> None:
        if self.selected_skin_folder is None:
            messagebox.showerror(t("cursor.title"), t("cursor.choose_folder_first"))
            return

        confirm = messagebox.askyesno(
            t("cursor.title"),
            t("cursor.confirm_apply_folder"),
        )
        if not confirm:
            return

        try:
            status = apply_cursor_skin_folder(self.selected_skin_folder)
        except Exception as exc:
            messagebox.showerror(t("cursor.title"), t("cursor.apply_folder_failed", error=exc))
            return

        self.status_var.set(status)
        messagebox.showinfo(t("cursor.title"), status)

    def apply_preset(self, preset: CursorPreset) -> None:
        confirm = messagebox.askyesno(
            t("cursor.title"),
            t("cursor.confirm_apply_preset", name=preset.name),
        )
        if not confirm:
            return

        try:
            status = apply_arrow_cursor(preset.cursor_path)
        except Exception as exc:
            messagebox.showerror(t("cursor.title"), t("cursor.apply_preset_failed", error=exc))
            return

        self.status_var.set(status)
        messagebox.showinfo(t("cursor.title"), status)

    def reset_to_default_skin(self) -> None:
        confirm = messagebox.askyesno(
            t("cursor.title"),
            t("cursor.confirm_reset_default"),
        )
        if not confirm:
            return

        try:
            status = reset_cursor_skin_to_default()
        except Exception as exc:
            messagebox.showerror(t("cursor.title"), t("cursor.reset_default_failed", error=exc))
            return

        self.selected_cursor_file = None
        self.selected_skin_folder = None
        self.cursor_file_var.set(t("cursor.no_custom_file"))
        self.skin_folder_var.set(t("cursor.no_skin_folder"))
        self.status_var.set(status)
        messagebox.showinfo(t("cursor.title"), status)
