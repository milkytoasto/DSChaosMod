import logging
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler
from ConfigHandler.ConfigHandler import ConfigHandler

from .Theming.ChaosTheme import ChaosTheme
from .utils.CheckboxCollectionStore import (
    CheckboxCollectionStore,
    CheckboxSectionStore,
    CheckboxTreeStore,
)
from .utils.WidgetLogger import WidgetLogger


class ServerGUI(ChaosTheme):
    def __init__(
        self,
        title,
        chaos_handler,
        config_handler,
        voting_handler,
        websocket_server,
    ):
        super().__init__(title)
        self.chaos_handler = chaos_handler
        self.config_handler = config_handler
        self.voting_handler = voting_handler
        self.effect_store = CheckboxCollectionStore()
        self.__init_frames()
        self.__init_tabs()
        self.__init_logging_tab(self.debug_tab, "debug")
        self.__init_logging_tab(self.chat_tab, "chat")
        self.__init_logging_tab(self.broadcast_tab, "broadcast")
        self.__init_commands()
        self.__init_settings_tab()
        self.__init_effects_tab()
        async_handler(websocket_server)()

    def __connected(self):
        self.connect_button["state"] = "disabled"
        self.disconnect_button["state"] = "normal"
        self.start_button["state"] = "normal"

    def __disconnected(self):
        self.connect_button["state"] = "normal"
        self.disconnect_button["state"] = "disabled"
        self.start_button["state"] = "disabled"
        self.pause_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"

    def __started(self):
        self.start_button["state"] = "disabled"
        self.pause_button["state"] = "normal"
        self.stop_button["state"] = "normal"

    def __paused(self):
        self.start_button["state"] = "normal"
        self.pause_button["state"] = "disabled"

    def __stopped(self):
        self.start_button["state"] = "normal"
        self.pause_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"

    def __init_frames(self):
        self.connection_actions = ttk.LabelFrame(
            self.root,
            text="Connection",
            width=450,
            height=50,
            padding=[8, 0, 8, 8],
        )
        self.voting_actions = ttk.LabelFrame(
            self.root,
            text="Voting",
            width=450,
            height=50,
            padding=[8, 0, 8, 8],
        )
        self.tabs_frame = tk.Frame(self.root, pady=8, padx=8)

        self.connection_actions.grid(row=0, pady=8, padx=8, sticky=tk.W)
        self.voting_actions.grid(row=0, column=1, pady=8, padx=8, sticky=tk.W)
        self.tabs_frame.grid(
            row=1,
            columnspan=20,
            sticky=tk.E + tk.W + tk.N + tk.S,
        )

    def __init_tabs(self):
        self.tab_control = ttk.Notebook(self.tabs_frame)
        self.debug_tab = ttk.Frame(self.tab_control)
        self.chat_tab = ttk.Frame(self.tab_control)
        self.broadcast_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.effects_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.debug_tab, text="Debugging")
        self.tab_control.add(self.chat_tab, text="Chat")
        self.tab_control.add(self.broadcast_tab, text="Broadcast")
        self.tab_control.add(self.settings_tab, text="Settings")
        self.tab_control.add(self.effects_tab, text="Effects")
        self.tab_control.pack(expand=1, fill="both")

    def __init_logging_tab(self, tab, name=""):
        """Initializes logging configuration for a tab.

        Args:
            tab (ttk.Notebook): The tkinter tab element to attach to
            name (str, optional): Name of the tab to use for the label. Defaults to "".
        """
        logging.basicConfig(
            format="[%(asctime)s]: %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )

        scrollbar = ttk.Scrollbar(tab, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        text = tk.Text(
            tab,
            width=15,
            height=15,
            wrap="none",
            yscrollcommand=scrollbar.set,
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand="true")

        logger = logging.getLogger(name)
        text_handler = WidgetLogger(text)
        logger.addHandler(text_handler)

    async def __quit(self, disconnect):
        await disconnect()
        self.root.destroy()

    def __init_commands(self):
        self.connect_button = ttk.Button(
            self.connection_actions,
            text="Connect to Twitch",
            command=lambda: [
                self.__connected(),
                async_handler(self.voting_handler.connect)(
                    self.__disconnected
                ),
            ],
        )
        self.disconnect_button = ttk.Button(
            self.connection_actions,
            text="Disconnect",
            command=lambda: [
                async_handler(self.voting_handler.disconnect)(),
                self.__disconnected(),
            ],
        )
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: [
                async_handler(self.__quit)(self.voting_handler.disconnect)
            ],
        )
        self.start_button = ttk.Button(
            self.voting_actions,
            text="Start",
            command=lambda: [
                self.__started(),
                self.voting_handler.start(stop_gui=self.__stopped),
            ],
        )
        self.pause_button = ttk.Button(
            self.voting_actions,
            text="Pause",
            command=lambda: [
                self.voting_handler.pause(),
                self.__paused(),
            ],
        )
        self.stop_button = ttk.Button(
            self.voting_actions,
            text="Stop",
            command=lambda: [
                self.voting_handler.stop(),
                self.__stopped(),
            ],
        )

        self.connect_button.grid(row=0, column=0, padx=4)
        self.disconnect_button.grid(row=0, column=1, padx=4)
        self.start_button.grid(row=0, column=2, padx=4)
        self.pause_button.grid(row=0, column=3, padx=4)
        self.stop_button.grid(row=0, column=4, padx=4)
        self.__disconnected()

    def __init_settings_tab(
        self,
    ):
        self.channel = tk.StringVar(
            self.root,
            value=self.config_handler.get_option(
                "TWITCH", "CHANNEL", "", type=str
            ),
        )
        self.tmi_token = tk.StringVar(
            self.root,
            value=self.config_handler.get_option(
                "TWITCH", "TMI_TOKEN", "", type=str
            ),
        )
        self.voting_duration = tk.StringVar(
            self.root,
            value=self.voting_handler.voting_duration,
        )
        self.effect_duration = tk.StringVar(
            self.root,
            value=self.voting_handler.effect_duration,
        )

        self.channel_label = ttk.Label(self.settings_tab, text="Channel")
        self.channel_field = ttk.Entry(
            self.settings_tab, textvariable=self.channel
        )
        self.tmi_token_label = ttk.Label(self.settings_tab, text="Oauth Token")
        self.tmi_token_field = ttk.Entry(
            self.settings_tab,
            show="*",
            textvariable=self.tmi_token,
        )
        self.voting_duration_label = ttk.Label(
            self.settings_tab, text="Voting Durection"
        )
        self.voting_duration_field = ttk.Entry(
            self.settings_tab,
            textvariable=self.voting_duration,
        )
        self.effect_durationLabel = ttk.Label(
            self.settings_tab, text="Voting Durection"
        )
        self.effect_durationField = ttk.Entry(
            self.settings_tab,
            textvariable=self.effect_duration,
        )

        self.channel_label.grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.channel_field.grid(row=0, column=1, padx=8, pady=8)
        self.tmi_token_label.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.tmi_token_field.grid(row=1, column=1, padx=8, pady=8)
        self.voting_duration_label.grid(
            row=2, column=0, padx=8, pady=8, sticky="e"
        )
        self.voting_duration_field.grid(row=2, column=1, padx=8, pady=8)
        self.effect_durationLabel.grid(
            row=3, column=0, padx=8, pady=8, sticky="e"
        )
        self.effect_durationField.grid(row=3, column=1, padx=8, pady=8)

        # Give save row/column a non-zero weight to give extra
        # space to that row/column in the grid
        self.settings_tab.grid_columnconfigure(10, weight=1)
        self.settings_tab.grid_rowconfigure(10, weight=1)

        self.settings_fields = [
            self.channel_field,
            self.tmi_token_field,
            self.voting_duration_field,
            self.effect_durationField,
        ]

        self.settings_field_values = {
            "TWITCH": {
                "CHANNEL": self.channel,
                "TMI_TOKEN": self.tmi_token,
            },
            "VOTING": {
                "VOTING_DURATION": self.voting_duration,
                "EFFECT_DURATION": self.effect_duration,
            },
        }

        self.save_settings = ttk.Button(
            self.settings_tab,
            text="Save Settings",
            command=lambda: self.__save_settings(
                lambda: [self.voting_handler.load_config()]
            ),
        ).grid(row=10, column=10, padx=8, pady=8, sticky="se")

    def __save_settings(self, save_handler):
        """Handles the logic for saving settings fields. Setting fields are disabled for the duration.

        Args:
            save_handler (method): Method to call after saving the config settings.
        """
        for field in self.settings_fields:
            field["state"] = "disabled"
        self.config_handler.save_config(self.settings_field_values)
        save_handler()
        for field in self.settings_fields:
            field["state"] = "active"

    def __save_effects(self, save_handler):
        """Handles the logic for saving effects fields. Effect fields are disabled for the duration.

        Args:
            save_handler (method): Method to call after saving the config settings.
        """
        games = [key for key in self.config_handler.config["GAME_CONFIGS"]]
        store = self.effect_store.to_dict()

        for game in games:
            game_config_handler = ConfigHandler(
                config_path="./config/"
                + self.config_handler.config["GAME_CONFIGS"][game]
            )
            game_config_handler.save_config(store[game])
        save_handler()

    def __dropdown_select(self):
        game = self.selected_game.get()
        game_sections = self.effect_store.trees[game].sections
        section_keys = list(game_sections.keys())

        self.effect_objects = []
        self.effect_box.config(state="normal")
        self.effect_box.delete("1.0", "end")

        for effect in self.effect_objects:
            effect.destroy()

        for section_name in section_keys:
            section = game_sections[section_name]
            button = section.create_button(self.effect_box)

            self.effect_box.window_create("end", window=button)
            self.effect_box.insert("end", "\n  ")
            self.effect_objects.append(button)

            for effect_name in section.option_vars:
                option_var = section.option_vars[effect_name]
                button = ttk.Checkbutton(
                    self.effect_box,
                    cursor="hand2",
                    text=f"{effect_name.upper().replace('_', ' ')}",
                    variable=option_var,
                )
                self.effect_box.insert("end", "  ")
                self.effect_box.window_create("end", window=button)
                self.effect_box.insert("end", "\n  ")
                self.effect_objects.append(button)

            if section_name != section_keys[-1]:
                self.effect_box.insert("end", "\n")

        self.effect_box.config(state="disabled")

    def __init_effects_tab(self):
        self.effect_objects = []

        left = ttk.Frame(self.effects_tab)
        right = ttk.Frame(self.effects_tab)

        vsb = ttk.Scrollbar(left, orient="vertical")
        effect_box = tk.Text(
            left,
            cursor="arrow",
            width=40,
            height=20,
            yscrollcommand=vsb.set,
        )
        vsb.config(command=effect_box.yview)
        effect_box.pack(side="left", fill="y")
        vsb.pack(side="left", fill="y", anchor="w")

        games = [key for key in self.config_handler.config["GAME_CONFIGS"]]
        game_options = []

        for game_name in games:
            game_store = CheckboxTreeStore(game_name)
            game_config_handler = ConfigHandler(
                config_path="./config/"
                + self.config_handler.config["GAME_CONFIGS"][game_name]
            )

            for section_name in game_config_handler.config.sections():
                section_store = CheckboxSectionStore(section_name)
                section = game_config_handler.get_section(section_name)

                for effect_name in section:
                    effect_value = game_config_handler.config[
                        section_name
                    ].getboolean(effect_name)
                    new_var = tk.BooleanVar(self.root, value=effect_value)
                    section_store.option_vars[effect_name] = new_var
                section_store.create_section_var(self.root)
                game_store.add(section_name, section_store)
            self.effect_store.add(game_name, game_store)

        effect_box["state"] = "disabled"
        self.effect_box = effect_box
        self.selected_game = tk.StringVar()
        self.options_menu = ttk.Combobox(
            right,
            state="readonly",
            values=games,
            textvariable=self.selected_game,
            width=50,
        )
        self.options_menu.configure(cursor="target")
        self.options_menu.pack(
            side="top",
            anchor="n",
            fill="x",
            expand=True,
            padx=8,
            pady=8,
        )
        self.options_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.__dropdown_select(),
        )

        self.save_settings = ttk.Button(
            right,
            text="Save Effects",
            command=lambda: self.__save_effects(
                lambda: [self.chaos_handler.load_config()]
            ),
        ).pack(side="right", anchor="s", padx=8, pady=8)

        left.pack(side="left", fill="y")
        right.pack(side="right", anchor="e", fill="both")

        if len(game_options) > 0:
            self.selected_game.set(game_options[0])
            self.__dropdown_select()
