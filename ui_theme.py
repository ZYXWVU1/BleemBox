"""Shared neutral palette and typography for the desktop workspace."""
from tkinter import ttk, font

from ui_fonts import ui_font, ui_font_family

PAGE = "#f6f6f7"
SURFACE = "#ffffff"
SIDEBAR = "#f0f0f2"
TEXT = "#242629"
MUTED = "#62666d"
BORDER = "#dcdde0"
SELECTED = "#dedfe3"


def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont"):
        font.nametofont(name).configure(family=ui_font_family(), size=10)
    root.option_add("*Listbox.background", SURFACE)
    root.option_add("*Listbox.foreground", TEXT)
    root.option_add("*Listbox.selectBackground", SELECTED)
    root.option_add("*Listbox.selectForeground", TEXT)
    style.configure(".", font=ui_font(10), background=PAGE, foreground=TEXT)
    for name, color in {"Shell": PAGE, "Panel": PAGE, "Sidebar": SIDEBAR,
                        "Card": SURFACE, "Muted": SIDEBAR}.items():
        style.configure(f"{name}.TFrame", background=color, relief="flat")
    labels = {
        "AppTitle": (SIDEBAR, TEXT, 18, True),
        "SidebarText": (SIDEBAR, MUTED, 9, False),
        "SidebarBadge": (SIDEBAR, MUTED, 9, True),
        "ToolbarLabel": (PAGE, MUTED, 10, False),
        "Eyebrow": (PAGE, MUTED, 9, True),
        "SectionTitle": (PAGE, TEXT, 23, True),
        "SectionText": (PAGE, MUTED, 10, False),
        "CardTitle": (SURFACE, TEXT, 14, True),
        "CardText": (SURFACE, MUTED, 10, False),
        "MutedField": (SIDEBAR, MUTED, 10, False),
        "MutedTitle": (SIDEBAR, TEXT, 14, True),
        "CardBadge": (SURFACE, MUTED, 10, True),
        "FieldLabel": (SURFACE, TEXT, 10, True),
        "Status": (SIDEBAR, MUTED, 10, False),
        "PreviewText": (SURFACE, MUTED, 10, False),
    }
    for name, (bg, fg, size, bold) in labels.items():
        style.configure(f"{name}.TLabel", background=bg, foreground=fg,
                        font=ui_font(size, bold=bold))
    for name, bg, fg, hover in (
        ("Primary", TEXT, SURFACE, "#404349"),
        ("Secondary", "#ececef", TEXT, "#e0e1e5"),
        ("Nav", SIDEBAR, MUTED, "#e6e6e9"),
        ("ActiveNav", SELECTED, TEXT, "#d4d5da"),
    ):
        style.configure(f"{name}.TButton", background=bg, foreground=fg,
                        borderwidth=0, relief="flat", padding=(14, 10),
                        anchor="w" if "Nav" in name else "center",
                        font=ui_font(10, bold=name in ("Primary", "ActiveNav")),
                        focuscolor=fg, focusthickness=1)
        style.map(f"{name}.TButton",
                  background=[("disabled", "#e8e8eb"), ("pressed", hover), ("active", hover)],
                  foreground=[("disabled", "#878a90")])
    for name in ("Modern.TEntry", "TCombobox", "TSpinbox"):
        style.configure(name, fieldbackground=SURFACE, foreground=TEXT,
                        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                        arrowcolor=MUTED, padding=(10, 8), relief="flat")
        style.map(name, bordercolor=[("focus", MUTED)],
                  lightcolor=[("focus", MUTED)], darkcolor=[("focus", MUTED)],
                  fieldbackground=[("readonly", SURFACE), ("disabled", SIDEBAR)],
                  foreground=[("readonly", TEXT), ("disabled", MUTED)],
                  selectbackground=[("!disabled", SELECTED)],
                  selectforeground=[("!disabled", TEXT)])
    style.configure("Modern.TCheckbutton", background=SURFACE, foreground=TEXT,
                    font=ui_font(10), indicatorbackground=SURFACE, indicatorforeground=TEXT)
    style.map("Modern.TCheckbutton", background=[("active", SURFACE)])
    style.configure("Clean.Treeview", background=SURFACE, fieldbackground=SURFACE,
                    foreground=TEXT, borderwidth=0, rowheight=36, font=ui_font(10))
    style.configure("Clean.Treeview.Heading", background=SIDEBAR, foreground=MUTED,
                    borderwidth=0, padding=(10, 10), font=ui_font(10, bold=True))
    style.map("Clean.Treeview", background=[("selected", SELECTED)],
              foreground=[("selected", TEXT)])
    style.map("Clean.Treeview.Heading", background=[("active", "#e6e6e9")])
    for orientation in ("Vertical", "Horizontal"):
        style.configure(f"{orientation}.TScrollbar", background="#d2d3d7",
                        troughcolor=PAGE, borderwidth=0, arrowsize=12,
                        bordercolor=PAGE, lightcolor=PAGE, darkcolor=PAGE,
                        arrowcolor=MUTED, relief="flat")
        style.layout(f"{orientation}.TScrollbar", [
            (f"{orientation}.Scrollbar.trough", {"sticky": "nswe", "children": [
                (f"{orientation}.Scrollbar.thumb", {"sticky": "nswe", "expand": "1"})
            ]})
        ])
    style.configure("TSeparator", background=BORDER)


def responsive_columns(container, left, right, *, threshold=900):
    """Stack two work areas when their shared viewport becomes narrow."""
    state = {"wide": None}

    def arrange(event):
        if event.widget is not container:
            return
        wide = event.width >= threshold
        if state["wide"] == wide:
            return
        state["wide"] = wide
        container.columnconfigure(0, weight=1, uniform="work" if wide else "")
        container.columnconfigure(1, weight=1 if wide else 0, uniform="work" if wide else "")
        left.grid_configure(row=0, column=0, padx=(0, 8) if wide else 0, pady=0)
        right.grid_configure(row=0 if wide else 1, column=1 if wide else 0,
                             padx=(8, 0) if wide else 0, pady=0 if wide else (16, 0))

    container.bind("<Configure>", arrange, add="+")


def fit_text(widget):
    """Wrap explanatory labels to their actual cell, including translated text."""
    for child in widget.winfo_children():
        if isinstance(child, ttk.Label) and str(child.cget("style")) in {
            "SectionText.TLabel", "CardText.TLabel", "Status.TLabel",
            "PreviewText.TLabel", "CardTitle.TLabel", "SectionTitle.TLabel", "MutedTitle.TLabel",
        }:
            child.configure(wraplength=240, justify="left")

            def wrap(event, label=child):
                if not label.winfo_exists():
                    return
                parent = label.master
                padding = [int(str(v)) for v in parent.cget("padding")]
                if len(padding) == 1:
                    horizontal = padding[0] * 2
                elif len(padding) >= 3:
                    horizontal = padding[0] + padding[2]
                elif padding:
                    horizontal = padding[0] * 2
                else:
                    horizontal = 0
                width = max(120, parent.winfo_width() - horizontal - 16)
                if int(label.cget("wraplength")) != width:
                    label.configure(wraplength=width)

            child.master.bind("<Configure>", wrap, add="+")
        fit_text(child)
