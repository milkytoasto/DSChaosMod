import logging
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler


class Colors:
    background = "#121212"
    backgroundText = "white"

    primary = "#1c54b2"
    primaryText = "white"

    secondary = "#212121"
    secondaryText = "white"

    disabled = "grey"
    disabledText = "white"

    border = "#2e2e2e"


class WidgetLogger(logging.Handler):
    """
    This implementation is based on the solutions
    provided at this stackoverflow question:

    https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget
    """

    def __init__(self, widget, level=logging.INFO):
        logging.Handler.__init__(self)
        self.setLevel(level)
        self.setFormatter(
            logging.Formatter("[%(asctime)s]: %(message)s", datefmt="%d-%b-%y %H:%M:%S")
        )
        self.widget = widget
        self.widget.config(state="disabled")
        self.widget.tag_config("INFO", foreground="white")
        self.widget.tag_config("DEBUG", foreground="white", background="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("ERROR", foreground="red")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)
        self.red = self.widget.tag_configure("red", foreground="red")

    def emit(self, record):
        self.widget.config(state="normal")
        # Append message (record) to the widget
        self.widget.insert(tk.END, self.format(record) + "\n", record.levelname)
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state="disabled")
        self.widget.update()  # Refresh the widget


class ServerGUI:
    def __init__(self, title, websocket_server):

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
        self.__init_frames()
        self.__init_tabs()
        self.__init_logging_tab(self.debug_tab, "debug")
        self.__init_logging_tab(self.chat_tab, "chat")
        self.__init_logging_tab(self.broadcast_tab, "broadcast")
        async_handler(websocket_server)()

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

    def connected(self):
        self.twButton["state"] = "normal"
        self.stButton["state"] = "disabled"
        self.psButton["state"] = "disabled"

    def stopped(self):
        self.twButton["state"] = "normal"
        self.stButton["state"] = "disabled"
        self.psButton["state"] = "disabled"

    def paused(self):
        self.twButton["state"] = "normal"
        self.stButton["state"] = "normal"
        self.psButton["state"] = "disabled"

    def started(self):
        self.twButton["state"] = "disabled"
        self.stButton["state"] = "normal"
        self.psButton["state"] = "normal"

    def __init_frames(self):
        self.actions_frame = ttk.LabelFrame(
            self.root, text="Actions", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self.actions_frame.grid(row=0, pady=8, padx=8, sticky=tk.W)

        self.tabs_frame = tk.Frame(self.root, pady=8, padx=8)
        self.tabs_frame.grid(row=1, sticky=tk.E + tk.W + tk.N + tk.S)

    def init_commands(self, connect, start, pause, stop):
        self.twButton = ttk.Button(
            self.actions_frame,
            text="Connect to Twitch",
            command=lambda: [async_handler(connect)(), self.connected()],
        )
        self.twButton.grid(row=0, column=0, padx=4)
        self.startButton = ttk.Button(
            self.actions_frame,
            text="Start",
            command=lambda: [start(), self.started()],
        )
        self.startButton.grid(row=0, column=1, padx=4)
        self.psButton = ttk.Button(
            self.actions_frame, text="Pause", command=lambda: [pause(), self.paused()]
        )
        self.psButton.grid(row=0, column=3, padx=4)

        self.stButton = ttk.Button(
            self.actions_frame, text="Stop", command=lambda: [stop(), self.stopped()]
        )
        self.stButton.grid(row=0, column=4)
        self.stopped()

    def __init_tabs(self):
        self.tabControl = ttk.Notebook(self.tabs_frame)
        self.debug_tab = ttk.Frame(self.tabControl)
        self.chat_tab = ttk.Frame(self.tabControl)
        self.broadcast_tab = ttk.Frame(self.tabControl)
        self.settings_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.debug_tab, text="Debugging")
        self.tabControl.add(self.chat_tab, text="Chat")
        self.tabControl.add(self.broadcast_tab, text="Broadcast")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.pack(expand=1, fill="both")

    def __init_logging_tab(self, tab, name=""):
        # Logging configuration
        logging.basicConfig(
            format="[%(asctime)s]: %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )

        scrollbar = ttk.Scrollbar(tab, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        text = tk.Text(
            tab, width=15, height=15, wrap="none", yscrollcommand=scrollbar.set
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand="true")

        logger = logging.getLogger(name)
        text_handler = WidgetLogger(text)
        logger.addHandler(text_handler)

    def __save_settings(self, saveHandler):
        for field in self.settingsFields:
            field["state"] = "disabled"
        saveHandler(self.settingsFieldValues)
        for field in self.settingsFields:
            field["state"] = "active"

    def init_settings_tab(
        self,
        saveHandler,
        channel="",
        votingDuration=60,
        effectDuration=120,
        tmiToken="",
    ):
        self.channel = tk.StringVar(self.root, value=channel)
        self.tmiToken = tk.StringVar(self.root, value=tmiToken)

        self.votingDuration = tk.StringVar(self.root, value=votingDuration)
        self.effectDuration = tk.StringVar(self.root, value=effectDuration)

        self.channelLabel = ttk.Label(self.settings_tab, text="Channel").grid(
            row=0, column=0, padx=8, pady=8, sticky="e"
        )
        self.channelField = ttk.Entry(self.settings_tab, textvariable=self.channel)
        self.channelField.grid(row=0, column=1, padx=8, pady=8)

        self.tmiTokenLabel = ttk.Label(self.settings_tab, text="Oauth Token").grid(
            row=1, column=0, padx=8, pady=8, sticky="e"
        )
        self.tmiTokenField = ttk.Entry(
            self.settings_tab, show="*", textvariable=self.tmiToken
        )
        self.tmiTokenField.grid(row=1, column=1, padx=8, pady=8)

        self.votingDurationLabel = ttk.Label(
            self.settings_tab, text="Voting Durection"
        ).grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.votingDurationField = ttk.Entry(
            self.settings_tab, textvariable=self.votingDuration
        )
        self.votingDurationField.grid(row=2, column=1, padx=8, pady=8)

        self.effectDurationLabel = ttk.Label(
            self.settings_tab, text="Voting Durection"
        ).grid(row=3, column=0, padx=8, pady=8, sticky="e")
        self.effectDurationField = ttk.Entry(
            self.settings_tab, textvariable=self.effectDuration
        )
        self.effectDurationField.grid(row=3, column=1, padx=8, pady=8)

        # Give save row/column a non-zero weight to give extra
        # space to that row/column in the grid
        self.settings_tab.grid_columnconfigure(10, weight=1)
        self.settings_tab.grid_rowconfigure(10, weight=1)

        self.settingsFields = [
            self.channelField,
            self.tmiTokenField,
            self.votingDurationField,
            self.effectDurationField,
        ]

        self.settingsFieldValues = {
            "TWITCH": {
                "CHANNEL": self.channel,
                "TMI_TOKEN": self.tmiToken,
            },
            "VOTING": {
                "VOTING_DURATION": self.votingDuration,
                "EFFECT_DURATION": self.effectDuration,
            },
        }

        self.saveSettings = ttk.Button(
            self.settings_tab,
            text="Save Settings",
            command=lambda: self.__save_settings(saveHandler),
        ).grid(row=10, column=10, padx=8, pady=8, sticky="se")
