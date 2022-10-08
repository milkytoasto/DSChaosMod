import tkinter as tk
import tkinter.ttk as ttk

from .Colors import Colors


class ChaosTheme:
    def __init__(self, title):
        root = tk.Tk()
        root.title(title)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        width = 600
        height = 350

        root.geometry(f"{width}x{height}")
        root.minsize(width, height)

        root.tk_setPalette(
            background=Colors.background,
            foreground=Colors.backgroundText,
            highlightColor=Colors.primary,
        )

        self.root = root

        self.__configure_style()

    def __configure_style(self):
        self.root.option_add("*font", "segoe-ui 10 bold")

        self.s = ttk.Style()
        self.s.theme_use("clam")
        self.s.configure(
            ".",
            font=("Segoe Ui", 10, "bold"),
            background=Colors.background,
            foreground=Colors.backgroundText,
            bordercolor=Colors.border,
            lightcolor=Colors.border,
            darkcolor=Colors.border,
            focuscolor="none",
            troughcolor=Colors.background,
            selectbackground=Colors.primary,
            selectforeground="cyan",
            insertcolor=Colors.backgroundText,
            fieldbackground=Colors.background,
            borderwidth=1,
            relief="flat",
        )

        self.s.layout(
            "TEntry",
            [
                (
                    "Entry.plain.field",
                    {
                        "children": [
                            (
                                "Entry.background",
                                {
                                    "children": [
                                        (
                                            "Entry.padding",
                                            {
                                                "children": [
                                                    (
                                                        "Entry.textarea",
                                                        {"sticky": "nswe"},
                                                    )
                                                ],
                                                "sticky": "nswe",
                                            },
                                        )
                                    ],
                                    "sticky": "nswe",
                                },
                            )
                        ],
                        "border": "2",
                        "sticky": "nswe",
                    },
                )
            ],
        )

        self.s.configure(
            "TButton",
            background=Colors.secondary,
            foreground=Colors.secondaryText,
        )
        self.s.map(
            "TButton",
            background=[
                ("selected", Colors.primary),
                ("active", Colors.primary),
                ("disabled", Colors.disabled),
            ],
        )

        self.s.configure(
            "TFrame",
            background=Colors.secondary,
            foreground=Colors.secondaryText,
        )

        self.s.configure(
            "TLabelframe",
            labeloutside=False,
        )
        self.s.configure(
            "TLabelframe.Label",
        )

        self.s.configure(
            "TLabel", background=Colors.secondary, foreground=Colors.secondaryText
        )

        self.s.layout(
            "Vertical.TScrollbar",
            [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "children": [("Vertical.Scrollbar.thumb", {"expand": "1"})],
                        "sticky": "ns",
                    },
                )
            ],
        )
        self.s.configure("Vertical.TScrollbar", background=Colors.primary, gripcount=0)
        self.s.map(
            "Vertical.TScrollbar",
            background=[("active", Colors.primary), ("disabled", Colors.primary)],
        )

        self.s.configure("TNotebook", tabmargins=[2, 5, 0, 0])

        self.s.configure(
            "TNotebook.Tab",
            background=Colors.secondary,
            foreground=Colors.secondaryText,
            padding=[10, 2],
        )
        self.s.map(
            "TNotebook.Tab",
            background=[
                ("selected", Colors.primary),
                ("active", Colors.primary),
                ("disabled", Colors.disabled),
            ],
            lightcolor=[],  # Overriding clam lightcolor list
            expand=[("selected", [1, 1, 1, 0])],
        )
        self.s.layout(
            "TNotebook.Tab",
            [
                (
                    "Notebook.tab",
                    {
                        "children": [
                            (
                                "Notebook.padding",
                                {
                                    "side": "top",
                                    "children": [
                                        (
                                            "Notebook.label",
                                            {
                                                "side": "top",
                                            },
                                        )
                                    ],
                                },
                            )
                        ]
                    },
                )
            ],
        )