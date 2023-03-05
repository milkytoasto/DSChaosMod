import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler
from ConfigHandler.ConfigHandler import ConfigHandler

from .components.checkbox_collection import (
    CheckboxCollectionStore,
    CheckboxSectionStore,
    CheckboxTreeStore,
)
from .components.widget_logger import WidgetLogger
from .styles.theme import ChaosTheme


class ServerGUI(ChaosTheme):
    def __init__(self, title, config_handler, voting_handler, websocket_server):
        super().__init__(title)
        self._config_handler = config_handler
        self._voting_handler = voting_handler
        self._effect_store = CheckboxCollectionStore()

        # Main buttons
        self._connect_button = None
        self._disconnect_button = None
        self._start_button = None
        self._pause_button = None
        self._stop_button = None
        self._integrate_button = None

        # Action groups tied to buttons
        self._connection_actions = None
        self._voting_actions = None
        self._pubsub_actions = None

        # Config tabs
        self._settings_tab = None
        self._effects_tab = None

        # Option store for the settings tab
        self._settings_field_values = None
        self._settings_fields = None

        # Window containing available effects
        self._effect_box = None

        self._init_frames()
        self._init_commands()

        async_handler(websocket_server)()

    def _connected(self):
        self._connect_button["state"] = "disabled"
        self._disconnect_button["state"] = "normal"
        self._start_button["state"] = "normal"

    def _disconnected(self):
        self._connect_button["state"] = "normal"
        self._disconnect_button["state"] = "disabled"
        self._start_button["state"] = "disabled"
        self._pause_button["state"] = "disabled"
        self._stop_button["state"] = "disabled"

    def _started(self):
        self._start_button["state"] = "disabled"
        self._pause_button["state"] = "normal"
        self._stop_button["state"] = "normal"

    def _paused(self):
        self._start_button["state"] = "normal"
        self._pause_button["state"] = "disabled"

    def _stopped(self):
        self._start_button["state"] = "normal"
        self._pause_button["state"] = "disabled"
        self._stop_button["state"] = "disabled"

    def _integrate(self):
        self._integrate_button["state"] = "disabled"
        self._disconnect_button["state"] = "disabled"

    def _http_server_closed(self):
        self._integrate_button["state"] = "normal"
        if str(self._connect_button["state"]) != "normal":
            self._disconnect_button["state"] = "normal"

    def _init_frames(self):
        tabs_frame = tk.Frame(self.root, pady=4, padx=4)
        self._connection_actions = ttk.LabelFrame(
            self.root, text="Connection", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self._voting_actions = ttk.LabelFrame(
            self.root, text="Voting", width=450, height=50, padding=[8, 0, 8, 8]
        )
        self._pubsub_actions = ttk.LabelFrame(
            self.root, text="PubSub", width=450, height=50, padding=[8, 0, 8, 8]
        )

        self._connection_actions.grid(row=0, pady=4, padx=4, sticky=tk.W)
        self._voting_actions.grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        self._pubsub_actions.grid(row=1, column=1, pady=4, padx=4, sticky=tk.W + tk.N)

        tabs_frame.grid(
            row=2, column=0, columnspan=20, sticky=tk.E + tk.W + tk.N + tk.S
        )

        tab_control = ttk.Notebook(tabs_frame)
        debug_tab = ttk.Frame(tab_control)
        chat_tab = ttk.Frame(tab_control)
        broadcast_tab = ttk.Frame(tab_control)

        self._settings_tab = ttk.Frame(tab_control)
        self._effects_tab = ttk.Frame(tab_control)

        tab_control.add(debug_tab, text="Debugging")
        tab_control.add(chat_tab, text="Chat")
        tab_control.add(broadcast_tab, text="Broadcast")
        tab_control.add(self._settings_tab, text="Settings")
        tab_control.add(self._effects_tab, text="Effects")
        tab_control.pack(expand=0, fill="both")

        self._init_logging_tab(debug_tab, "debug")
        self._init_logging_tab(chat_tab, "chat")
        self._init_logging_tab(broadcast_tab, "broadcast")

    def _init_logging_tab(self, tab, name=""):
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

    async def _quit(self, disconnect):
        await disconnect()
        self.root.destroy()

    def _init_commands(self):
        self._connect_button = ttk.Button(
            self._connection_actions,
            text="Connect to Twitch",
            command=lambda: [
                self._connected(),
                async_handler(self._voting_handler.connect)(self._disconnected),
            ],
        )
        self._disconnect_button = ttk.Button(
            self._connection_actions,
            text="Disconnect",
            command=lambda: [
                async_handler(self._voting_handler.disconnect)(),
                self._disconnected(),
            ],
        )
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: [async_handler(self._quit)(self._voting_handler.disconnect)],
        )
        self._start_button = ttk.Button(
            self._voting_actions,
            text="Start",
            command=lambda: [
                self._started(),
                self._voting_handler.start(self._stopped),
            ],
        )
        self._pause_button = ttk.Button(
            self._voting_actions,
            text="Pause",
            command=lambda: [self._voting_handler.pause(), self._paused()],
        )
        self._stop_button = ttk.Button(
            self._voting_actions,
            text="Stop",
            command=lambda: [self._voting_handler.stop(), self._stopped()],
        )
        self._integrate_button = ttk.Button(
            self._pubsub_actions,
            text="Integrate",
            command=lambda: [
                self._integrate(),
                async_handler(self._voting_handler.integrate)(self._http_server_closed),
            ],
        )

        self._connect_button.grid(row=0, column=0, padx=4)
        self._disconnect_button.grid(row=0, column=1, padx=4)
        self._start_button.grid(row=0, column=2, padx=4)
        self._pause_button.grid(row=0, column=3, padx=4)
        self._stop_button.grid(row=0, column=4, padx=4)
        self._integrate_button.grid(row=1, column=2, padx=4)
        self._disconnected()

    def init_settings_tab(
        self,
        tmi_token="",
        channel="",
        voting_duration=60,
        effect_duration=120,
    ):
        channel_var = tk.StringVar(self.root, value=channel)
        tmi_token_var = tk.StringVar(self.root, value=tmi_token)
        voting_duration_var = tk.StringVar(self.root, value=voting_duration)
        effect_duration_var = tk.StringVar(self.root, value=effect_duration)

        channel_label = ttk.Label(self._settings_tab, text="Channel")
        channel_field = ttk.Entry(self._settings_tab, textvariable=channel_var)
        tmi_token_label = ttk.Label(self._settings_tab, text="Oauth Token")
        tmi_token_field = ttk.Entry(
            self._settings_tab, show="*", textvariable=tmi_token_var
        )
        voting_duration_label = ttk.Label(self._settings_tab, text="Voting Duration")
        voting_duration_field = ttk.Entry(
            self._settings_tab, textvariable=voting_duration_var
        )
        effect_duration_label = ttk.Label(self._settings_tab, text="Effect Duration")
        effect_duration_field = ttk.Entry(
            self._settings_tab, textvariable=effect_duration_var
        )

        channel_label.grid(row=0, column=0, padx=8, pady=8, sticky="e")
        channel_field.grid(row=0, column=1, padx=8, pady=8)
        tmi_token_label.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        tmi_token_field.grid(row=1, column=1, padx=8, pady=8)
        voting_duration_label.grid(row=2, column=0, padx=8, pady=8, sticky="e")
        voting_duration_field.grid(row=2, column=1, padx=8, pady=8)
        effect_duration_label.grid(row=3, column=0, padx=8, pady=8, sticky="e")
        effect_duration_field.grid(row=3, column=1, padx=8, pady=8)

        # Give save row/column a non-zero weight to give extra
        # space to that row/column in the grid
        self._settings_tab.grid_columnconfigure(10, weight=1)
        self._settings_tab.grid_rowconfigure(10, weight=1)

        self._settings_fields = [
            channel_field,
            tmi_token_field,
            voting_duration_field,
            effect_duration_field,
        ]

        self._settings_field_values = {
            "TWITCH": {
                "CHANNEL": channel_var,
                "TMI_TOKEN": tmi_token_var,
            },
            "VOTING": {
                "VOTING_DURATION": voting_duration_var,
                "EFFECT_DURATION": effect_duration_var,
            },
        }

        self._save_settings = ttk.Button(
            self._settings_tab,
            text="Save Settings",
            command=self._save_settings,
        ).grid(row=10, column=10, padx=8, pady=8, sticky="se")

    def _save_settings(self):
        for field in self._settings_fields:
            field["state"] = "disabled"
        self._config_handler.save_config(self._settings_field_values)
        self._voting_handler.load_config()
        for field in self._settings_fields:
            field["state"] = "active"

    def init_effects_tab(self, saveHandler):
        left = ttk.Frame(self._effects_tab)
        right = ttk.Frame(self._effects_tab)

        vsb = ttk.Scrollbar(left, orient="vertical")
        effect_box = tk.Text(
            left, cursor="arrow", width=40, height=20, yscrollcommand=vsb.set
        )
        vsb.config(command=effect_box.yview)
        effect_box.pack(side="left", fill="y")
        vsb.pack(side="left", fill="y", anchor="w")

        games = [key for key in self._config_handler.config["GAME_CONFIGS"]]
        game_options = []

        for game_name in games:
            game_store = CheckboxTreeStore(game_name)
            config_path = os.path.join(
                os.path.dirname(__file__),
                f'../config/{self._config_handler.config["GAME_CONFIGS"][game_name]}',
            )
            game_config_handler = ConfigHandler(config_path=config_path)

            for section_name in game_config_handler.config.sections():
                section_store = CheckboxSectionStore(section_name)
                section = game_config_handler.get_section(section_name)

                for effect_name in section:
                    effect_value = game_config_handler.config[section_name].getboolean(
                        effect_name
                    )
                    new_var = tk.BooleanVar(self.root, value=effect_value)
                    section_store.option_vars[effect_name] = new_var
                section_store.create_section_var(self.root)
                game_store.add(section_name, section_store)
            self._effect_store.add(game_name, game_store)

        effect_box["state"] = "disabled"
        self._effect_box = effect_box
        self.selected_game = tk.StringVar()
        self._options_menu = ttk.Combobox(
            right,
            state="readonly",
            values=games,
            textvariable=self.selected_game,
            width=50,
        )
        self._options_menu.configure(cursor="target")
        self._options_menu.pack(
            side="top", anchor="n", fill="x", expand=True, padx=8, pady=8
        )
        self._options_menu.bind(
            "<<ComboboxSelected>>", lambda event: self._dropdown_select()
        )

        self._save_settings = ttk.Button(
            right,
            text="Save Effects",
            command=lambda: self._save_effects(saveHandler),
        ).pack(side="right", anchor="s", padx=8, pady=8)

        left.pack(side="left", fill="y")
        right.pack(side="right", anchor="e", fill="both")

        if len(game_options) > 0:
            self.selected_game.set(game_options[0])
            self._dropdown_select()

    def _save_effects(self, save_handler):
        game_configs = self._config_handler.config["GAME_CONFIGS"]
        effect_store = self._effect_store.to_dict()

        for game, config_file in game_configs.items():
            config_path = os.path.join(
                os.path.dirname(__file__), f"../config/{config_file}"
            )
            game_config_handler = ConfigHandler(config_path=config_path)
            game_config_handler.save_config(effect_store[game])

        save_handler()

    def _dropdown_select(self):
        game = self.selected_game.get()
        game_sections = self._effect_store.trees[game].sections
        section_keys = list(game_sections.keys())

        effect_objects = []
        self._effect_box.config(state="normal")
        self._effect_box.delete("1.0", "end")

        for effect in effect_objects:
            effect.destroy()

        for section_name in section_keys:
            section = game_sections[section_name]
            button = section.create_button(self._effect_box)

            self._effect_box.window_create("end", window=button)
            self._effect_box.insert("end", "\n  ")
            effect_objects.append(button)

            for effect_name in section.option_vars:
                option_var = section.option_vars[effect_name]
                button = ttk.Checkbutton(
                    self._effect_box,
                    cursor="hand2",
                    text=f"{effect_name.upper().replace('_', ' ')}",
                    variable=option_var,
                )
                self._effect_box.insert("end", "  ")
                self._effect_box.window_create("end", window=button)
                self._effect_box.insert("end", "\n  ")
                effect_objects.append(button)

            if section_name != section_keys[-1]:
                self._effect_box.insert("end", "\n")

        self._effect_box.config(state="disabled")
