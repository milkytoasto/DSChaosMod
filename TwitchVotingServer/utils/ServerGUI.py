import logging
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler


class WidgetLogger(logging.Handler):
    """
    This implementation is based on:
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
    def __init__(self, title):

        root = tk.Tk()
        root.title(title)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        width = 600
        height = 350

        root.geometry(f"{width}x{height}")
        root.minsize(width, height)

        self.bgcolor = "#%02x%02x%02x" % (25, 25, 25)
        self.buttoncolor = "#%02x%02x%02x" % (53, 53, 53)

        root.tk_setPalette(self.bgcolor)

        self.root = root

        self.__configure_style()
        self.__init_frames()
        self.__init_tabs()
        self.__init_logging_tab(self.debug_tab, "debug")
        self.__init_logging_tab(self.chat_tab, "chat")

    def __configure_style(self):
        self.s = ttk.Style()
        self.s.theme_use("clam")
        self.s.configure(
            "TButton",
            background=self.buttoncolor,
            foreground="white",
            borderwidth=1,
            focusthickness=3,
            focuscolor="none",
        )
        self.s.configure(
            "TFrame",
            background=self.buttoncolor,
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        self.s.configure(
            "TNotebook",
            background=self.bgcolor,
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        self.s.configure(
            "TNotebook.Tab",
            background=self.buttoncolor,
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        self.s.configure("TLabel", background=self.buttoncolor, foreground="white")
        self.s.map(
            "TButton", background=[("active", self.bgcolor), ("disabled", "gray")]
        )
        self.s.map(
            "TNotebook.Tab", background=[("active", self.bgcolor), ("disabled", "gray")]
        )

    def __ws_button_press(self):
        self.wsButton["state"] = "disabled"

    def __init_frames(self):
        self.top_frame = tk.Frame(self.root, width=450, height=50, pady=8, padx=8)
        self.top_frame.grid(row=0, sticky=tk.W)

        self.bottom_frame = tk.Frame(self.root, pady=8, padx=8)
        self.bottom_frame.grid(row=1, sticky=tk.E + tk.W + tk.N + tk.S)

    def init_commands(self, websocket_server, start, stop):
        self.wsButton = ttk.Button(
            self.top_frame,
            text="Initiate Websocket Server",
            command=lambda: [
                self.__ws_button_press(),
                async_handler(websocket_server)(),
            ],
        )
        self.wsButton.grid(row=0, column=0)
        self.twButton = ttk.Button(
            self.top_frame, text="Connect to Twitch", command=async_handler(start)
        ).grid(row=0, column=1, padx=8)
        self.stButton = ttk.Button(self.top_frame, text="Stop", command=stop).grid(
            row=0, column=2
        )

    def __init_tabs(self):
        self.tabControl = ttk.Notebook(self.bottom_frame)
        self.debug_tab = ttk.Frame(self.tabControl)
        self.chat_tab = ttk.Frame(self.tabControl)
        self.settings_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.debug_tab, text="Debugging")
        self.tabControl.add(self.chat_tab, text="Chat")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.pack(expand=1, fill="both")

    def __init_logging_tab(self, tab, name=""):
        # Logging configuration
        logging.basicConfig(
            format="[%(asctime)s]: %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )

        text = st.ScrolledText(tab, height=15)
        text.configure(state="disabled")
        text.pack(fill="both", expand="true")

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
