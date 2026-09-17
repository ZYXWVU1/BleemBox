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

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._handle_scrollbar)
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
        # Preserve native scrolling in editors/tables and avoid duplicate bindings.
        if isinstance(widget, (tk.Text, tk.Listbox, ttk.Treeview, ttk.Combobox)):
            return
        if not getattr(widget, "_panel_scroll_bound", False):
            widget.bind("<MouseWheel>", self._handle_mousewheel, add="+")
            widget.bind("<Button-4>", self._handle_mousewheel_linux_up, add="+")
            widget.bind("<Button-5>", self._handle_mousewheel_linux_down, add="+")
            widget._panel_scroll_bound = True
        for child in widget.winfo_children():
            self._install_scroll_bindings(child)

    def refresh_scroll_bindings(self) -> None:
        self._install_scroll_bindings(self)

    def _scrollable_height(self) -> float:
        try:
            values = [float(value) for value in str(self.canvas.cget("scrollregion")).split()]
            region_height = values[3] - values[1]
        except (ValueError, IndexError, TypeError, tk.TclError):
            return 0.0

        return max(0.0, region_height - float(self.canvas.winfo_height()))

    def _scroll_to_fraction(self, fraction: float) -> None:
        # Moving to a bounded fraction prevents an embedded frame from bleeding
        # outside the canvas viewport during fast wheel or scrollbar updates.
        self.canvas.yview_moveto(max(0.0, min(1.0, fraction)))

    def _scroll_by_pixels(self, pixels: float) -> None:
        scrollable_height = self._scrollable_height()
        if scrollable_height <= 0:
            return

        first, _last = self.canvas.yview()
        self._scroll_to_fraction(first + pixels / scrollable_height)

    def _scroll_by_wheel(self, delta: int) -> None:
        if not delta or self._scrollable_height() <= 0:
            return

        steps = max(1, abs(int(delta)) // 120)
        direction = -1 if delta > 0 else 1
        self._scroll_by_pixels(direction * steps * 64)

    def _handle_scrollbar(self, *args: str) -> None:
        if not args:
            return

        if args[0] == "moveto" and len(args) > 1:
            self._scroll_to_fraction(float(args[1]))
            return

        if args[0] != "scroll" or len(args) < 3:
            return

        amount = float(args[1])
        unit = args[2]
        if unit == "pages":
            pixels = amount * max(1, self.canvas.winfo_height() - 32)
        else:
            pixels = amount * 64
        self._scroll_by_pixels(pixels)

    def _handle_mousewheel(self, event: tk.Event) -> str:
        delta = getattr(event, "delta", 0)
        self._scroll_by_wheel(delta)
        return "break"

    def _handle_mousewheel_linux_up(self, _event: tk.Event) -> str:
        self._scroll_by_wheel(120)
        return "break"

    def _handle_mousewheel_linux_down(self, _event: tk.Event) -> str:
        self._scroll_by_wheel(-120)
        return "break"
