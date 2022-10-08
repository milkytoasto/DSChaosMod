import logging
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler

from .Theming.ChaosTheme import ChaosTheme
from .utils.WidgetLogger import WidgetLogger


class ServerGUI(ChaosTheme):
    def __init__(self, title, websocket_server):
        super().__init__(title)
        self.__init_frames()
        self.__init_tabs()
        self.__init_logging_tab(self.debug_tab, "debug")
        self.__init_logging_tab(self.chat_tab, "chat")
        self.__init_logging_tab(self.broadcast_tab, "broadcast")
        async_handler(websocket_server)()

    def connected(self):
        self.connectButton["state"] = "disabled"
        self.disconnectButton["state"] = "normal"
        self.startButton["state"] = "normal"

    def disconnected(self):
        self.connectButton["state"] = "normal"
        self.disconnectButton["state"] = "disabled"
        self.startButton["state"] = "disabled"
        self.stopButton["state"] = "disabled"
        self.pauseButton["state"] = "disabled"

    def started(self):
        self.startButton["state"] = "disabled"
        self.stopButton["state"] = "normal"
        self.pauseButton["state"] = "normal"

    def paused(self):
        self.startButton["state"] = "normal"
        self.pauseButton["state"] = "disabled"

    def stopped(self):
        self.startButton["state"] = "normal"
        self.stopButton["state"] = "disabled"
        self.pauseButton["state"] = "disabled"

    def __init_frames(self):
        self.connection_actions = ttk.LabelFrame(
            self.root, text="Connection", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self.connection_actions.grid(row=0, pady=8, padx=8, sticky=tk.W)
        self.voting_actions = ttk.LabelFrame(
            self.root, text="Voting", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self.voting_actions.grid(row=0, column=1, pady=8, padx=8, sticky=tk.W)

        self.tabs_frame = tk.Frame(self.root, pady=8, padx=8)
        self.tabs_frame.grid(row=1, columnspan=20, sticky=tk.E + tk.W + tk.N + tk.S)

    def init_commands(self, connect, disconnect, start, pause, stop):
        self.connectButton = ttk.Button(
            self.connection_actions,
            text="Connect to Twitch",
            command=lambda: [async_handler(connect)(), self.connected()],
        )
        self.disconnectButton = ttk.Button(
            self.connection_actions,
            text="Disconnect",
            command=lambda: [async_handler(disconnect)(), self.disconnected()],
        )
        self.startButton = ttk.Button(
            self.voting_actions,
            text="Start",
            command=lambda: [start(), self.started()],
        )
        self.pauseButton = ttk.Button(
            self.voting_actions, text="Pause", command=lambda: [pause(), self.paused()]
        )
        self.stopButton = ttk.Button(
            self.voting_actions, text="Stop", command=lambda: [stop(), self.stopped()]
        )

        self.connectButton.grid(row=0, column=0, padx=4)
        self.disconnectButton.grid(row=0, column=1, padx=4)
        self.startButton.grid(row=0, column=2, padx=4)
        self.pauseButton.grid(row=0, column=3, padx=4)
        self.stopButton.grid(row=0, column=4, padx=4)
        self.disconnected()

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
