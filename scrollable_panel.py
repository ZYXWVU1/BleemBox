from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ScrollablePanel(ttk.Frame):
    """A simple canvas-based container for vertically scrollable views."""

    def __init__(self, parent: tk.Misc, *, canvas_background: str, style: str = "Panel.TFrame") -> None:
        super().__init__(parent, style=style, padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self,
            background=canvas_background,
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.content = ttk.Frame(self.canvas, style=style, padding=0)
        self._window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", self._handle_content_configure)
        self.canvas.bind("<Configure>", self._handle_canvas_configure)
        self.refresh_scroll_bindings()

    def _handle_content_configure(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _handle_canvas_configure(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self._window_id, width=event.width)

    def _install_scroll_bindings(self, widget: tk.Misc) -> None:
        # Bind scrolling directly on every child so wheel movement feels instant.
        widget.bind("<MouseWheel>", self._handle_mousewheel, add="+")
        widget.bind("<Button-4>", self._handle_mousewheel_linux_up, add="+")
        widget.bind("<Button-5>", self._handle_mousewheel_linux_down, add="+")
        for child in widget.winfo_children():
            self._install_scroll_bindings(child)

    def refresh_scroll_bindings(self) -> None:
        self._install_scroll_bindings(self)

    def _handle_mousewheel(self, event: tk.Event) -> str:
        delta = getattr(event, "delta", 0)
        if delta == 0:
            return "break"

        steps = max(1, abs(int(delta)) // 120)
        direction = -1 if delta > 0 else 1
        self.canvas.yview_scroll(direction * steps, "units")
        return "break"

    def _handle_mousewheel_linux_up(self, _event: tk.Event) -> str:
        self.canvas.yview_scroll(-1, "units")
        return "break"

    def _handle_mousewheel_linux_down(self, _event: tk.Event) -> str:
        self.canvas.yview_scroll(1, "units")
        return "break"
