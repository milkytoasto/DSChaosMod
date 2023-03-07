import tkinter as tk
import tkinter.ttk as ttk

from .colors import Colors


class ChaosTheme:
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        width = 800
        height = 600

        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)

        self.root.tk_setPalette(
            background=Colors.BACKGROUND,
            foreground=Colors.BACKGROUND_TEXT,
            highlightColor=Colors.PRIMARY,
        )
        self.root.option_add("*font", "segoe-ui 12 bold")
        self.s = ttk.Style()
        self.s.theme_use("clam")
        self.s.configure(
            ".",
            font=("Segoe Ui", 12, "bold"),
            background=Colors.BACKGROUND,
            foreground=Colors.BACKGROUND_TEXT,
            bordercolor=Colors.BORDER,
            lightcolor=Colors.BORDER,
            darkcolor=Colors.BORDER,
            focuscolor="none",
            troughcolor=Colors.BACKGROUND,
            selectbackground=Colors.PRIMARY,
            selectforeground="cyan",
            insertcolor=Colors.BACKGROUND_TEXT,
            fieldbackground=Colors.BACKGROUND,
            borderwidth=0,
        )

        self._configure_entry()
        self._configure_button()
        self._configure_combobox()
        self._configure_checkbutton()
        self._configure_frame()
        self._configure_labelframe()
        self._configure_label()
        self._configure_scrollbar()
        self._configure_notebook()

    def _configure_entry(self):
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
        self.s.map(
            "TEntry",
            selectbackground=[("!focus", Colors.BACKGROUND)],
            selectforeground=[("!focus", Colors.BACKGROUND_TEXT)],
        )

    def _configure_button(self):
        self.s.configure(
            "TButton",
            background=Colors.PRIMARY,
            foreground=Colors.PRIMARY_TEXT,
        )
        self.s.map(
            "TButton",
            background=[
                ("selected", Colors.PRIMARY),
                ("active", Colors.PRIMARY_HOVER),
                ("disabled", Colors.DISABLED),
            ],
        )

    def _configure_combobox(self):
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground", Colors.PRIMARY_HOVER
        )
        self.root.option_add("*TCombobox*Listbox.selectForeground", Colors.BACKGROUND)
        self.s.configure(
            "TCombobox",
            arrowsize=20,
            bordercolor=Colors.PRIMARY,
            borderwidth=5,
        )
        self.s.map(
            "TCombobox",
            selectbackground=[("readonly", Colors.BACKGROUND)],
            selectforeground=[("readonly", Colors.BACKGROUND_TEXT)],
            fieldbackground=[("readonly", Colors.BACKGROUND)],
            background=[
                ("readonly", Colors.PRIMARY),
            ],
        )

    def _configure_checkbutton(self):
        self.s.configure(
            "TCheckbutton",
        )
        self.s.map(
            "TCheckbutton",
            background=[
                ("selected", Colors.PRIMARY),
                ("active", Colors.PRIMARY_HOVER),
                ("disabled", Colors.DISABLED),
            ],
        )

    def _configure_frame(self):
        self.s.configure(
            "TFrame",
            background=Colors.SECONDARY,
            foreground=Colors.SECONDARY_TEXT,
        )

    def _configure_labelframe(self):
        self.s.configure(
            "TLabelframe",
            labeloutside=False,
        )
        self.s.configure(
            "TLabelframe.Label",
        )

    def _configure_label(self):
        self.s.configure(
            "TLabel", background=Colors.SECONDARY, foreground=Colors.SECONDARY_TEXT
        )

    def _configure_scrollbar(self):
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
        self.s.configure("Vertical.TScrollbar", background=Colors.PRIMARY, gripcount=0)
        self.s.map(
            "Vertical.TScrollbar",
            background=[("active", Colors.PRIMARY), ("disabled", Colors.PRIMARY)],
        )

    def _configure_notebook(self):
        self.s.configure(
            "TNotebook.Tab",
            background=Colors.SECONDARY,
            foreground=Colors.SECONDARY_TEXT,
            padding=[10, 2],
        )
        self.s.map(
            "TNotebook.Tab",
            background=[
                ("selected", Colors.PRIMARY),
                ("active", Colors.PRIMARY_HOVER),
                ("disabled", Colors.DISABLED),
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
