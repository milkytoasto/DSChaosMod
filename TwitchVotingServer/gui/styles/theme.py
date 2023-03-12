import tkinter as tk
import tkinter.ttk as ttk

from .colors import DarkColors, LightColors


class ChaosTheme:
    def __init__(self, title, theme="dark"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        width = 800
        height = 600

        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)

        self.root.option_add("*font", "segoe-ui 12 bold")

        self.s = ttk.Style()
        self.s.theme_use("clam")
        self.theme = theme
        self._set_colors()
        self._configure_style()

    def toggle_stay_on_top(self, value=True):
        self.root.attributes("-topmost", value)

    def _toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"

        self._set_colors()
        self._configure_style()

    def _set_colors(self):
        if self.theme == "dark":
            self.colors = DarkColors
        else:
            self.colors = LightColors

    def _configure_style(self):
        self.root.tk_setPalette(
            background=self.colors.BACKGROUND,
            foreground=self.colors.BACKGROUND_TEXT,
            highlightColor=self.colors.PRIMARY,
        )
        self.s.configure(
            ".",
            font=("Segoe Ui", 12, "bold"),
            background=self.colors.BACKGROUND,
            foreground=self.colors.BACKGROUND_TEXT,
            bordercolor=self.colors.BORDER,
            lightcolor=self.colors.BORDER,
            darkcolor=self.colors.BORDER,
            focuscolor="none",
            troughcolor=self.colors.BACKGROUND,
            selectbackground=self.colors.PRIMARY,
            selectforeground=self.colors.PRIMARY_TEXT,
            insertcolor=self.colors.BACKGROUND_TEXT,
            fieldbackground=self.colors.BACKGROUND,
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
        self._configure_toggle_button()

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
            selectbackground=[("!focus", self.colors.BACKGROUND)],
            selectforeground=[("!focus", self.colors.BACKGROUND_TEXT)],
        )

    def _configure_button(self):
        self.s.configure(
            "TButton",
            background=self.colors.PRIMARY,
            foreground=self.colors.PRIMARY_TEXT,
        )
        self.s.map(
            "TButton",
            background=[
                ("selected", self.colors.PRIMARY),
                ("active", self.colors.PRIMARY_DARK),
                ("disabled", self.colors.DISABLED),
            ],
        )

    def _configure_toggle_button(self):
        self.s.configure(
            "ToggleButton.On.TButton",
            foreground=self.colors.PRIMARY_TEXT,
            background=self.colors.PRIMARY,
            relief="raised",
        )
        self.s.map(
            "ToggleButton.On.TButton",
            background=[
                ("active", self.colors.PRIMARY_DARK),
            ],
        )
        self.s.configure(
            "ToggleButton.Off.TButton",
            foreground=self.colors.SURFACE_TEXT,
            background=self.colors.SURFACE,
            relief="sunken",
        )
        self.s.map(
            "ToggleButton.Off.TButton",
            background=[
                ("active", self.colors.DISABLED),
            ],
        )

    def _configure_combobox(self):
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground", self.colors.PRIMARY_DARK
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectForeground", self.colors.PRIMARY_TEXT
        )
        self.s.configure(
            "TCombobox",
            arrowsize=20,
            bordercolor=self.colors.PRIMARY,
            borderwidth=5,
        )
        self.s.map(
            "TCombobox",
            selectbackground=[("readonly", self.colors.BACKGROUND)],
            selectforeground=[("readonly", self.colors.BACKGROUND_TEXT)],
            fieldbackground=[("readonly", self.colors.BACKGROUND)],
            background=[
                ("readonly", self.colors.PRIMARY),
            ],
        )

    def _configure_checkbutton(self):
        self.s.configure(
            "TCheckbutton",
        )
        self.s.map(
            "TCheckbutton",
            background=[
                ("selected", self.colors.PRIMARY),
                ("active", self.colors.PRIMARY_DARK),
                ("disabled", self.colors.DISABLED),
            ],
        )

    def _configure_frame(self):
        self.s.configure(
            "TFrame",
            background=self.colors.SECONDARY,
            foreground=self.colors.SECONDARY_TEXT,
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
            "TLabel",
            background=self.colors.SECONDARY,
            foreground=self.colors.SECONDARY_TEXT,
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
        self.s.configure(
            "Vertical.TScrollbar", background=self.colors.PRIMARY, gripcount=0
        )
        self.s.map(
            "Vertical.TScrollbar",
            background=[
                ("active", self.colors.PRIMARY),
                ("disabled", self.colors.PRIMARY),
            ],
        )

    def _configure_notebook(self):
        self.s.configure(
            "TNotebook.Tab",
            background=self.colors.SECONDARY,
            foreground=self.colors.SECONDARY_TEXT,
            padding=[10, 2],
        )
        self.s.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.colors.PRIMARY),
                ("active", self.colors.PRIMARY_DARK),
                ("disabled", self.colors.DISABLED),
            ],
            foreground=[
                ("selected", self.colors.PRIMARY_TEXT),
                ("active", self.colors.PRIMARY_TEXT),
                ("disabled", self.colors.DISABLED_TEXT),
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
