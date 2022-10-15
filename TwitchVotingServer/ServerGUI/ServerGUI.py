import logging
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler
from ConfigHandler.ConfigHandler import ConfigHandler

from .Theming.ChaosTheme import ChaosTheme
from .utils.WidgetLogger import WidgetLogger


class CheckboxCollectionStore:
    def __init__(self):
        self.trees = dict()

    def to_dict(self):
        result = dict()
        for tree in self.trees:
            result[tree] = self.trees[tree].to_dict()
        return result

    def add(self, tree_name, tree):
        tree.root = self
        self.trees[tree_name] = tree


class CheckboxTreeStore:
    def __init__(self, name):
        self.parent = None
        self.tree_name = name
        self.sections = dict()

    def to_dict(self):
        result = dict()
        for section in self.sections:
            result[section] = self.sections[section].option_vars
        return result

    def add(self, section_name, section):
        section.tree = self
        self.sections[section_name] = section


class CheckboxSectionStore:
    def __init__(self, name):
        self.tree = None
        self.section_name = name
        self.section_var = None
        self.option_vars = dict()

    def __checkbox_section_select(self):
        value = self.section_var.get()
        for option in self.option_vars:
            self.option_vars[option].set(value)

    def create_section_var(self, root):
        self.section_var = tk.BooleanVar(root, value=True)
        for option in self.option_vars.values():
            if option.get() == False:
                self.section_var.set(False)
                return self.section_var
        return self.section_var

    def create_button(self, root):
        self.button = ttk.Checkbutton(
            root,
            cursor="hand2",
            text=f"{self.section_name}",
            variable=self.section_var,
            command=self.__checkbox_section_select,
        )
        return self.button


class ServerGUI(ChaosTheme):
    def __init__(self, title, configHandler, websocket_server):
        super().__init__(title)
        self.configHandler = configHandler
        self.effect_store = CheckboxCollectionStore()
        self.__init_frames()
        self.__init_tabs()
        self.__init_logging_tab(self.debug_tab, "debug")
        self.__init_logging_tab(self.chat_tab, "chat")
        self.__init_logging_tab(self.broadcast_tab, "broadcast")
        async_handler(websocket_server)()

    def __connected(self):
        self.connectButton["state"] = "disabled"
        self.disconnectButton["state"] = "normal"
        self.startButton["state"] = "normal"

    def __disconnected(self):
        self.connectButton["state"] = "normal"
        self.disconnectButton["state"] = "disabled"
        self.startButton["state"] = "disabled"
        self.pauseButton["state"] = "disabled"
        self.stopButton["state"] = "disabled"

    def __started(self):
        self.startButton["state"] = "disabled"
        self.pauseButton["state"] = "normal"
        self.stopButton["state"] = "normal"

    def __paused(self):
        self.startButton["state"] = "normal"
        self.pauseButton["state"] = "disabled"

    def __stopped(self):
        self.startButton["state"] = "normal"
        self.pauseButton["state"] = "disabled"
        self.stopButton["state"] = "disabled"

    def __init_frames(self):
        self.connection_actions = ttk.LabelFrame(
            self.root, text="Connection", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self.voting_actions = ttk.LabelFrame(
            self.root, text="Voting", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self.tabs_frame = tk.Frame(self.root, pady=8, padx=8)

        self.connection_actions.grid(row=0, pady=8, padx=8, sticky=tk.W)
        self.voting_actions.grid(row=0, column=1, pady=8, padx=8, sticky=tk.W)
        self.tabs_frame.grid(row=1, columnspan=20, sticky=tk.E + tk.W + tk.N + tk.S)

    def __init_tabs(self):
        self.tabControl = ttk.Notebook(self.tabs_frame)
        self.debug_tab = ttk.Frame(self.tabControl)
        self.chat_tab = ttk.Frame(self.tabControl)
        self.broadcast_tab = ttk.Frame(self.tabControl)
        self.settings_tab = ttk.Frame(self.tabControl)
        self.effects_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.debug_tab, text="Debugging")
        self.tabControl.add(self.chat_tab, text="Chat")
        self.tabControl.add(self.broadcast_tab, text="Broadcast")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.add(self.effects_tab, text="Effects")
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

    async def __quit(self, disconnect):
        await disconnect()
        self.root.destroy()

    def init_commands(self, connect, disconnect, start, pause, stop):
        self.connectButton = ttk.Button(
            self.connection_actions,
            text="Connect to Twitch",
            command=lambda: [
                self.__connected(),
                async_handler(connect)(self.__disconnected),
            ],
        )
        self.disconnectButton = ttk.Button(
            self.connection_actions,
            text="Disconnect",
            command=lambda: [async_handler(disconnect)(), self.__disconnected()],
        )
        self.root.protocol(
            "WM_DELETE_WINDOW", lambda: [async_handler(self.__quit)(disconnect)]
        )
        self.startButton = ttk.Button(
            self.voting_actions,
            text="Start",
            command=lambda: [self.__started(), start(self.__stopped)],
        )
        self.pauseButton = ttk.Button(
            self.voting_actions,
            text="Pause",
            command=lambda: [pause(), self.__paused()],
        )
        self.stopButton = ttk.Button(
            self.voting_actions, text="Stop", command=lambda: [stop(), self.__stopped()]
        )

        self.connectButton.grid(row=0, column=0, padx=4)
        self.disconnectButton.grid(row=0, column=1, padx=4)
        self.startButton.grid(row=0, column=2, padx=4)
        self.pauseButton.grid(row=0, column=3, padx=4)
        self.stopButton.grid(row=0, column=4, padx=4)
        self.__disconnected()

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

        self.channelLabel = ttk.Label(self.settings_tab, text="Channel")
        self.channelField = ttk.Entry(self.settings_tab, textvariable=self.channel)
        self.tmiTokenLabel = ttk.Label(self.settings_tab, text="Oauth Token")
        self.tmiTokenField = ttk.Entry(
            self.settings_tab, show="*", textvariable=self.tmiToken
        )
        self.votingDurationLabel = ttk.Label(self.settings_tab, text="Voting Durection")
        self.votingDurationField = ttk.Entry(
            self.settings_tab, textvariable=self.votingDuration
        )
        self.effectDurationLabel = ttk.Label(self.settings_tab, text="Voting Durection")
        self.effectDurationField = ttk.Entry(
            self.settings_tab, textvariable=self.effectDuration
        )

        self.channelLabel.grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.channelField.grid(row=0, column=1, padx=8, pady=8)
        self.tmiTokenLabel.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.tmiTokenField.grid(row=1, column=1, padx=8, pady=8)
        self.votingDurationLabel.grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.votingDurationField.grid(row=2, column=1, padx=8, pady=8)
        self.effectDurationLabel.grid(row=3, column=0, padx=8, pady=8, sticky="e")
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

    def __save_settings(self, saveHandler):
        for field in self.settingsFields:
            field["state"] = "disabled"
        self.configHandler.save_config(self.settingsFieldValues)
        saveHandler()
        for field in self.settingsFields:
            field["state"] = "active"

    def __save_effects(self, saveHandler):
        games = [key for key in self.configHandler.config["GAME_CONFIGS"]]
        store = self.effect_store.to_dict()

        for game in games:
            gameConfigHandler = ConfigHandler(
                config_path="./config/"
                + self.configHandler.config["GAME_CONFIGS"][game]
            )
            gameConfigHandler.save_config(store[game])
        saveHandler()

    def __dropdown_select(self):
        game = self.selected_game.get()
        game_sections = self.effect_store.trees[game].sections

        self.effectObjects = []
        self.effectBox.config(state="normal")
        self.effectBox.delete("1.0", "end")

        for effect in self.effectObjects:
            effect.destroy()

        for section_name in game_sections:
            section = game_sections[section_name]
            button = section.create_button(self.effectBox)

            self.effectBox.window_create("end", window=button)
            self.effectBox.insert("end", "\n")
            self.effectObjects.append(button)

            for effect_name in section.option_vars:
                option_var = section.option_vars[effect_name]
                button = ttk.Checkbutton(
                    self.effectBox,
                    cursor="hand2",
                    text=f"{effect_name}",
                    variable=option_var,
                )
                self.effectBox.insert("end", "  ")
                self.effectBox.window_create("end", window=button)
                self.effectBox.insert("end", "\n")
                self.effectObjects.append(button)

        self.effectBox.config(state="disabled")

    def init_effects_tab(self, saveHandler):
        self.effectObjects = []

        left = ttk.Frame(self.effects_tab)
        right = ttk.Frame(self.effects_tab)

        vsb = ttk.Scrollbar(left, orient="vertical")
        effectBox = tk.Text(left, width=40, height=20, yscrollcommand=vsb.set)
        vsb.config(command=effectBox.yview)
        effectBox.pack(side="left", fill="y")
        vsb.pack(side="left", fill="y", anchor="w")

        games = [key for key in self.configHandler.config["GAME_CONFIGS"]]
        game_options = []

        for game_name in games:
            game_store = CheckboxTreeStore(game_name)
            gameConfigHandler = ConfigHandler(
                config_path="./config/"
                + self.configHandler.config["GAME_CONFIGS"][game_name]
            )

            for section_name in gameConfigHandler.config.sections():
                section_store = CheckboxSectionStore(section_name)
                section = gameConfigHandler.get_section(section_name)

                for effect_name in section:
                    effect_value = gameConfigHandler.config[section_name].getboolean(
                        effect_name
                    )
                    new_var = tk.BooleanVar(self.root, value=effect_value)
                    section_store.option_vars[effect_name] = new_var
                section_store.create_section_var(self.root)
                game_store.add(section_name, section_store)
            self.effect_store.add(game_name, game_store)

        effectBox["state"] = "disabled"
        self.effectBox = effectBox
        self.selected_game = tk.StringVar()
        self.optionsMenu = ttk.Combobox(
            right,
            state="readonly",
            values=games,
            textvariable=self.selected_game,
            width=50,
        )
        self.optionsMenu.pack(
            side="top", anchor="n", fill="x", expand=True, padx=8, pady=8
        )
        self.optionsMenu.bind(
            "<<ComboboxSelected>>", lambda event: self.__dropdown_select()
        )

        self.saveSettings = ttk.Button(
            right,
            text="Save Effects",
            command=lambda: self.__save_effects(saveHandler),
        ).pack(side="right", anchor="s", padx=8, pady=8)

        left.pack(side="left", fill="y")
        right.pack(side="right", anchor="e", fill="both")

        if len(game_options) > 0:
            self.selected_game.set(game_options[0])
            self.__dropdown_select()
