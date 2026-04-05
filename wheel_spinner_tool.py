from __future__ import annotations

import math
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from i18n import t
from scrollable_panel import ScrollablePanel
from ui_fonts import ui_font
from wheel_logic import choose_winner_index, parse_wheel_items


class WheelSpinnerToolView(ttk.Frame):
    """UI for entering custom wheel items and spinning to get one result."""

    WHEEL_SIZE = 300
    POINTER_ANGLE = 90.0
    COLOR_PALETTE = (
        "#d97757",
        "#eab676",
        "#8eb486",
        "#78a6a8",
        "#7e95d1",
        "#b784c4",
        "#c98c8c",
        "#d6c17d",
    )

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        self.items: list[str] = []
        self.current_angle = 0.0
        self.is_spinning = False
        self._spin_job: str | None = None

        self.status_var = tk.StringVar(value=t("wheel.status_initial"))
        self.result_var = tk.StringVar(value=t("wheel.result_placeholder"))

        self._build_layout()
        self._set_default_items()

    def _build_layout(self) -> None:
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

        ttk.Label(header, text=t("wheel.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("wheel.subtitle"),
            style="SectionText.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text=t("common.back_home"), style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        content = ttk.Frame(surface, style="Panel.TFrame", padding=6)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        control_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        control_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        control_card.columnconfigure(0, weight=1)
        control_card.rowconfigure(3, weight=1)

        ttk.Label(control_card, text=t("wheel.entries_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            control_card,
            text=t("wheel.entries_help"),
            style="CardText.TLabel",
            wraplength=300,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 12))

        self.items_text = tk.Text(
            control_card,
            wrap="word",
            font=ui_font(10),
            relief="flat",
            borderwidth=0,
            background="#fffdf9",
            foreground="#21303a",
            insertbackground="#21303a",
            selectbackground="#f1d7c2",
            padx=12,
            pady=12,
            undo=False,
            height=14,
        )
        self.items_text.grid(row=2, column=0, sticky="nsew")
        self.items_text.bind("<KeyRelease>", self._handle_items_changed)

        text_scrollbar = ttk.Scrollbar(control_card, orient="vertical", command=self.items_text.yview)
        text_scrollbar.grid(row=2, column=1, sticky="ns")
        self.items_text.configure(yscrollcommand=text_scrollbar.set)

        action_row = ttk.Frame(control_card, style="Card.TFrame")
        action_row.grid(row=3, column=0, sticky="w", pady=(18, 0))
        ttk.Button(action_row, text=t("wheel.spin_button"), style="Primary.TButton", command=self.spin_wheel).pack(side="left")

        result_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        result_card.grid(row=1, column=0, sticky="nsew")
        result_card.columnconfigure(0, weight=1)
        result_card.rowconfigure(1, weight=1)

        ttk.Label(result_card, text=t("wheel.wheel_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        wheel_frame = ttk.Frame(result_card, style="Card.TFrame")
        wheel_frame.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
        wheel_frame.columnconfigure(0, weight=1)
        wheel_frame.rowconfigure(1, weight=1)

        ttk.Label(wheel_frame, text=t("wheel.pointer_label"), style="FieldLabel.TLabel").grid(row=0, column=0, sticky="n")

        self.wheel_canvas = tk.Canvas(
            wheel_frame,
            width=self.WHEEL_SIZE,
            height=self.WHEEL_SIZE + 32,
            background="#fffaf4",
            highlightthickness=0,
            borderwidth=0,
        )
        self.wheel_canvas.grid(row=1, column=0, sticky="n")

        status_box = ttk.Frame(result_card, style="Card.TFrame", padding=0)
        status_box.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(anchor="w", fill="x")

        result_box = ttk.Frame(result_card, style="Muted.TFrame", padding=16)
        result_box.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        ttk.Label(result_box, text=t("wheel.result_title"), style="MutedField.TLabel").pack(anchor="w")
        ttk.Label(
            result_box,
            textvariable=self.result_var,
            style="MutedTitle.TLabel",
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        scroll_panel.refresh_scroll_bindings()

    def _set_default_items(self) -> None:
        # Prefill the text box so the tool has something to show on first open.
        default_items = "\n".join(
            (
                t("wheel.default_item_1"),
                t("wheel.default_item_2"),
                t("wheel.default_item_3"),
                t("wheel.default_item_4"),
            )
        )
        self.items_text.delete("1.0", "end")
        self.items_text.insert("1.0", default_items)
        self.refresh_items()

    def _handle_items_changed(self, _event=None) -> None:
        if not self.is_spinning:
            self.refresh_items()

    def refresh_items(self) -> None:
        try:
            items = parse_wheel_items(self.items_text.get("1.0", "end"))
        except ValueError:
            self.items = []
            self.result_var.set(t("wheel.result_placeholder"))
            self.status_var.set(t("wheel.status_empty"))
            self._draw_wheel([])
            return

        self.items = items
        self.status_var.set(t("wheel.status_ready", count=len(items)))
        self._draw_wheel(items)

    def _draw_wheel(self, items: list[str]) -> None:
        self.wheel_canvas.delete("all")

        center_x = self.WHEEL_SIZE / 2
        center_y = self.WHEEL_SIZE / 2 + 20
        radius = self.WHEEL_SIZE / 2 - 18

        if not items:
            self.wheel_canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline="#d7c7b8",
                width=2,
                fill="#f7f2eb",
            )
            self.wheel_canvas.create_text(
                center_x,
                center_y,
                text=t("wheel.canvas_placeholder"),
                fill="#8a8179",
                font=ui_font(12, bold=True),
                width=220,
                justify="center",
            )
            self._draw_pointer(center_x, center_y, radius)
            return

        slice_angle = 360 / len(items)
        for index, item in enumerate(items):
            start_angle = self.current_angle + index * slice_angle
            fill_color = self.COLOR_PALETTE[index % len(self.COLOR_PALETTE)]
            self.wheel_canvas.create_arc(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                start=start_angle,
                extent=slice_angle,
                fill=fill_color,
                outline="#fffaf4",
                width=2,
            )

            label_angle = math.radians(start_angle + slice_angle / 2)
            label_radius = radius * 0.62
            label_x = center_x + math.cos(label_angle) * label_radius
            label_y = center_y - math.sin(label_angle) * label_radius
            self.wheel_canvas.create_text(
                label_x,
                label_y,
                text=self._shorten_label(item),
                fill="#1f2a33",
                font=ui_font(10, bold=True),
                width=max(60, int(radius * 0.45)),
                justify="center",
            )

        self.wheel_canvas.create_oval(
            center_x - 30,
            center_y - 30,
            center_x + 30,
            center_y + 30,
            fill="#fffaf4",
            outline="#d7c7b8",
            width=2,
        )
        self._draw_pointer(center_x, center_y, radius)

    def _draw_pointer(self, center_x: float, center_y: float, radius: float) -> None:
        tip_y = center_y - radius - 6
        self.wheel_canvas.create_polygon(
            center_x,
            tip_y,
            center_x - 16,
            tip_y - 26,
            center_x + 16,
            tip_y - 26,
            fill="#c76838",
            outline="",
        )

    def _shorten_label(self, value: str) -> str:
        if len(value) <= 18:
            return value
        return f"{value[:15]}..."

    def spin_wheel(self) -> None:
        if self.is_spinning:
            return

        try:
            self.items = parse_wheel_items(self.items_text.get("1.0", "end"))
        except ValueError as exc:
            messagebox.showerror(t("wheel.title"), str(exc))
            return

        winner_index = choose_winner_index(self.items)
        slice_angle = 360 / len(self.items)
        current_center = (self.current_angle + winner_index * slice_angle + slice_angle / 2) % 360
        offset_to_pointer = (self.POINTER_ANGLE - current_center) % 360
        extra_turns = 360 * random.randint(6, 10)
        target_angle = self.current_angle + extra_turns + offset_to_pointer

        self.is_spinning = True
        self.status_var.set(t("wheel.status_spinning"))
        self.result_var.set(t("wheel.result_spinning"))

        self._animate_spin(
            start_angle=self.current_angle,
            target_angle=target_angle,
            winner_text=self.items[winner_index],
            duration_ms=3200,
        )

    def _animate_spin(self, start_angle: float, target_angle: float, winner_text: str, duration_ms: int) -> None:
        begin = time.perf_counter()

        def step() -> None:
            elapsed_ms = (time.perf_counter() - begin) * 1000
            progress = min(1.0, elapsed_ms / duration_ms)
            eased_progress = 1 - (1 - progress) ** 4
            self.current_angle = start_angle + (target_angle - start_angle) * eased_progress
            self._draw_wheel(self.items)

            if progress < 1.0:
                self._spin_job = self.after(16, step)
                return

            self.current_angle = target_angle % 360
            self._draw_wheel(self.items)
            self.is_spinning = False
            self._spin_job = None
            self.result_var.set(winner_text)
            self.status_var.set(t("wheel.status_finished", result=winner_text))

        self._spin_job = self.after(16, step)
