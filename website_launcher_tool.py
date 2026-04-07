from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from i18n import t
from scrollable_panel import ScrollablePanel
from ui_fonts import ui_font
from website_launcher_logic import (
    WebsiteButtonProfile,
    build_links_text,
    create_empty_profile,
    load_website_profiles,
    open_profile_links,
    save_website_profiles,
    update_profile,
)


class WebsiteLauncherToolView(ttk.Frame):
    """UI for creating buttons that open multiple websites at once."""

    def __init__(self, parent: ttk.Frame, on_back_home) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=0)
        self.on_back_home = on_back_home

        self.profiles: list[WebsiteButtonProfile] = load_website_profiles()
        self.selected_profile_id: str | None = self.profiles[0].id if self.profiles else None
        self.is_editing = False

        self.status_var = tk.StringVar(value=t("web_launcher.status_initial"))
        self.profile_name_var = tk.StringVar()
        self.selected_name_var = tk.StringVar(value=t("web_launcher.no_selection"))

        self.content_frame: ttk.Frame | None = None
        self.launcher_card: ttk.Frame | None = None
        self.editor_card: ttk.Frame | None = None
        self.launch_buttons_frame: ttk.Frame | None = None
        self.links_text: tk.Text | None = None
        self.scroll_panel: ScrollablePanel | None = None

        self._build_layout()
        self._load_selected_profile()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scroll_panel = ScrollablePanel(self, canvas_background="#f7f2eb")
        self.scroll_panel.grid(row=0, column=0, sticky="nsew")

        surface = self.scroll_panel.content
        surface.columnconfigure(0, weight=1)
        surface.rowconfigure(1, weight=1)

        header = ttk.Frame(surface, style="Panel.TFrame", padding=(6, 0, 6, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text=t("web_launcher.title"), style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=t("web_launcher.subtitle"),
            style="SectionText.TLabel",
            wraplength=800,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(header, text=t("common.back_home"), style="Secondary.TButton", command=self.on_back_home).grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        self.content_frame = ttk.Frame(surface, style="Panel.TFrame", padding=6)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        self.launcher_card = ttk.Frame(self.content_frame, style="Card.TFrame", padding=22)
        self.launcher_card.columnconfigure(0, weight=1)

        ttk.Label(self.launcher_card, text=t("web_launcher.buttons_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.launcher_card,
            text=t("web_launcher.buttons_help"),
            style="CardText.TLabel",
            wraplength=420,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 16))

        top_actions = ttk.Frame(self.launcher_card, style="Card.TFrame")
        top_actions.grid(row=2, column=0, sticky="w", pady=(0, 16))
        ttk.Button(top_actions, text=t("web_launcher.add_button"), style="Primary.TButton", command=self.add_profile).pack(
            side="left", padx=(0, 10)
        )

        self.launch_buttons_frame = ttk.Frame(self.launcher_card, style="Card.TFrame")
        self.launch_buttons_frame.grid(row=3, column=0, sticky="nsew")
        self.launch_buttons_frame.columnconfigure(0, weight=1)
        self.launch_buttons_frame.columnconfigure(1, weight=1)

        self.editor_card = ttk.Frame(self.content_frame, style="Card.TFrame", padding=22)
        self.editor_card.columnconfigure(0, weight=1)

        ttk.Label(self.editor_card, text=t("web_launcher.editor_title"), style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.editor_card,
            text=t("web_launcher.editor_help"),
            style="CardText.TLabel",
            wraplength=420,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 16))

        editor_top_actions = ttk.Frame(self.editor_card, style="Card.TFrame")
        editor_top_actions.grid(row=2, column=0, sticky="w", pady=(0, 18))
        ttk.Button(
            editor_top_actions,
            text=t("web_launcher.close_editor"),
            style="Secondary.TButton",
            command=self.close_editor,
        ).pack(side="left")

        ttk.Label(self.editor_card, text=t("web_launcher.selected_button"), style="FieldLabel.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(
            self.editor_card,
            textvariable=self.selected_name_var,
            style="CardText.TLabel",
            wraplength=420,
            justify="left",
        ).grid(row=4, column=0, sticky="w", pady=(8, 0))

        ttk.Label(self.editor_card, text=t("web_launcher.button_text"), style="FieldLabel.TLabel").grid(
            row=5, column=0, sticky="w", pady=(18, 0)
        )
        ttk.Entry(self.editor_card, textvariable=self.profile_name_var, style="Modern.TEntry").grid(
            row=6, column=0, sticky="ew", pady=(8, 0)
        )

        ttk.Label(self.editor_card, text=t("web_launcher.links_label"), style="FieldLabel.TLabel").grid(
            row=7, column=0, sticky="w", pady=(18, 0)
        )
        ttk.Label(
            self.editor_card,
            text=t("web_launcher.links_help"),
            style="CardText.TLabel",
            wraplength=420,
            justify="left",
        ).grid(row=8, column=0, sticky="w", pady=(8, 12))

        links_frame = ttk.Frame(self.editor_card, style="Card.TFrame")
        links_frame.grid(row=9, column=0, sticky="nsew")
        links_frame.columnconfigure(0, weight=1)
        links_frame.rowconfigure(0, weight=1)

        self.links_text = tk.Text(
            links_frame,
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
            height=12,
        )
        self.links_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(links_frame, orient="vertical", command=self.links_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.links_text.configure(yscrollcommand=scrollbar.set)

        editor_actions = ttk.Frame(self.editor_card, style="Card.TFrame")
        editor_actions.grid(row=10, column=0, sticky="w", pady=(18, 0))
        ttk.Button(
            editor_actions,
            text=t("web_launcher.save_changes"),
            style="Primary.TButton",
            command=self.save_selected_profile,
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            editor_actions,
            text=t("web_launcher.delete_button"),
            style="Secondary.TButton",
            command=self.delete_selected_profile,
        ).pack(side="left")

        status_box = ttk.Frame(surface, style="Card.TFrame", padding=0)
        status_box.grid(row=2, column=0, sticky="ew", padx=6, pady=(8, 6))
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(12, 9)).pack(anchor="w", fill="x")

        self._layout_editor_state()
        self._refresh_profile_buttons()
        self.scroll_panel.refresh_scroll_bindings()

    def _layout_editor_state(self) -> None:
        if self.content_frame is None or self.launcher_card is None or self.editor_card is None:
            return

        self.launcher_card.grid_forget()
        self.editor_card.grid_forget()

        if self.is_editing:
            self.launcher_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            self.editor_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        else:
            self.launcher_card.grid(row=0, column=0, columnspan=2, sticky="nsew")

        if self.scroll_panel is not None:
            self.scroll_panel.refresh_scroll_bindings()

    def _refresh_profile_buttons(self) -> None:
        if self.launch_buttons_frame is None:
            return

        for child in self.launch_buttons_frame.winfo_children():
            child.destroy()

        if not self.profiles:
            ttk.Label(
                self.launch_buttons_frame,
                text=t("web_launcher.no_buttons"),
                style="CardText.TLabel",
            ).grid(row=0, column=0, sticky="w")
            if self.scroll_panel is not None:
                self.scroll_panel.refresh_scroll_bindings()
            return

        for index, profile in enumerate(self.profiles):
            card = ttk.Frame(self.launch_buttons_frame, style="Muted.TFrame", padding=16)
            card.grid(
                row=index // 2,
                column=index % 2,
                sticky="nsew",
                padx=(0, 10) if index % 2 == 0 else 0,
                pady=(0, 10),
            )
            card.columnconfigure(0, weight=1)

            ttk.Label(card, text=profile.label, style="MutedTitle.TLabel").grid(row=0, column=0, sticky="w")

            button_row = ttk.Frame(card, style="Muted.TFrame")
            button_row.grid(row=1, column=0, sticky="w", pady=(10, 0))
            ttk.Button(
                button_row,
                text=t("web_launcher.open_now"),
                style="Primary.TButton",
                command=lambda item=profile: self.open_profile(item),
            ).pack(side="left", padx=(0, 10))
            ttk.Button(
                button_row,
                text=t("web_launcher.edit_button"),
                style="Secondary.TButton",
                command=lambda item=profile: self.select_profile(item.id),
            ).pack(side="left")

        if self.scroll_panel is not None:
            self.scroll_panel.refresh_scroll_bindings()

    def _selected_profile(self) -> WebsiteButtonProfile | None:
        if self.selected_profile_id is None:
            return None
        for profile in self.profiles:
            if profile.id == self.selected_profile_id:
                return profile
        return None

    def _load_selected_profile(self) -> None:
        profile = self._selected_profile()
        if profile is None:
            self.selected_name_var.set(t("web_launcher.no_selection"))
            self.profile_name_var.set("")
            if self.links_text is not None:
                self.links_text.delete("1.0", "end")
            return

        self.selected_name_var.set(profile.label)
        self.profile_name_var.set(profile.label)
        if self.links_text is not None:
            self.links_text.delete("1.0", "end")
            self.links_text.insert("1.0", build_links_text(profile.links))

    def select_profile(self, profile_id: str) -> None:
        self.selected_profile_id = profile_id
        self.is_editing = True
        self._layout_editor_state()
        self._load_selected_profile()
        profile = self._selected_profile()
        if profile is not None:
            self.status_var.set(t("web_launcher.selected_status", name=profile.label))

    def add_profile(self) -> None:
        new_profile = create_empty_profile()
        self.profiles.append(new_profile)
        self.selected_profile_id = new_profile.id
        self.is_editing = True
        save_website_profiles(self.profiles)
        self._layout_editor_state()
        self._refresh_profile_buttons()
        self._load_selected_profile()
        self.status_var.set(t("web_launcher.added_status", name=new_profile.label))

    def save_selected_profile(self) -> None:
        profile = self._selected_profile()
        if profile is None or self.links_text is None:
            messagebox.showerror(t("web_launcher.title"), t("web_launcher.select_button_first"))
            return

        try:
            updated_profile = update_profile(profile, self.profile_name_var.get(), self.links_text.get("1.0", "end"))
        except ValueError as exc:
            messagebox.showerror(t("web_launcher.title"), str(exc))
            return

        for index, item in enumerate(self.profiles):
            if item.id == updated_profile.id:
                self.profiles[index] = updated_profile
                break

        save_website_profiles(self.profiles)
        self._refresh_profile_buttons()
        self._load_selected_profile()
        self.status_var.set(t("web_launcher.saved_status", name=updated_profile.label))

    def delete_selected_profile(self) -> None:
        profile = self._selected_profile()
        if profile is None:
            messagebox.showerror(t("web_launcher.title"), t("web_launcher.select_button_first"))
            return

        if not messagebox.askyesno(t("web_launcher.title"), t("web_launcher.confirm_delete", name=profile.label)):
            return

        self.profiles = [item for item in self.profiles if item.id != profile.id]
        if not self.profiles:
            replacement = create_empty_profile()
            self.profiles.append(replacement)
            self.selected_profile_id = replacement.id
        else:
            self.selected_profile_id = self.profiles[0].id

        save_website_profiles(self.profiles)
        self.is_editing = False
        self._layout_editor_state()
        self._refresh_profile_buttons()
        self._load_selected_profile()
        self.status_var.set(t("web_launcher.deleted_status", name=profile.label))

    def open_profile(self, profile: WebsiteButtonProfile) -> None:
        try:
            opened_count = open_profile_links(profile)
        except ValueError as exc:
            messagebox.showerror(t("web_launcher.title"), str(exc))
            return

        self.selected_profile_id = profile.id
        self._load_selected_profile()
        self.status_var.set(t("web_launcher.opened_status", name=profile.label, count=opened_count))

    def close_editor(self) -> None:
        self.is_editing = False
        self._layout_editor_state()
        profile = self._selected_profile()
        if profile is not None:
            self.status_var.set(t("web_launcher.editor_closed", name=profile.label))
