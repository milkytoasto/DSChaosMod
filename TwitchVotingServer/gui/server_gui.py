import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

from async_tkinter_loop import async_handler

from .components.effects_tab import EffectsTab
from .components.settings_tab import SettingsTab
from .components.widget_logger import WidgetLogger
from .styles.theme import ChaosTheme


class ServerGUI(ChaosTheme):
    def __init__(
        self, title, config_handler, voting_handler, websocket_server, chaos_handler
    ):
        super().__init__(title)
        self._config_path = os.path.join(os.path.dirname(__file__), f"../config/")
        self._chaos_handler = chaos_handler
        self._config_handler = config_handler
        self._voting_handler = voting_handler

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

        self._init_frames()
        self._init_commands()

        async_handler(websocket_server)()

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

        self._settings_tab = SettingsTab(
            tab_control,
            config_handler=self._config_handler,
            voting_handler=self._voting_handler,
        )
        self._effects_tab = EffectsTab(
            tab_control,
            config_path=self._config_path,
            config_handler=self._config_handler,
            voting_handler=self._voting_handler,
            save_handler=lambda: [self._chaos_handler.load_config()],
        )

        tab_control.add(debug_tab, text="Debugging")
        tab_control.add(chat_tab, text="Chat")
        tab_control.add(broadcast_tab, text="Broadcast")
        tab_control.add(self._settings_tab, text="Settings")
        tab_control.add(self._effects_tab, text="Effects")
        tab_control.pack(expand=0, fill="both")

        self.debug_logger = WidgetLogger(debug_tab, "debug")
        self.chat_logger = WidgetLogger(chat_tab, "chat")
        self.broadcast_logger = WidgetLogger(broadcast_tab, "broadcast")

    def _toggle_theme(self):
        super()._toggle_theme()
        self.debug_logger.toggle_theme()
        self.chat_logger.toggle_theme()
        self.broadcast_logger.toggle_theme()

    async def _quit(self, disconnect):
        await disconnect()
        self.root.destroy()

    def _init_commands(self):
        self._connect_button = ttk.Button(
            self._connection_actions,
            text="Connect to Twitch",
            command=self._connect_button_clicked,
        )
        self._disconnect_button = ttk.Button(
            self._connection_actions,
            text="Disconnect",
            command=self._disconnect_button_clicked,
        )
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self._start_button = ttk.Button(
            self._voting_actions,
            text="Start",
            command=self._start_button_clicked,
        )
        self._pause_button = ttk.Button(
            self._voting_actions,
            text="Pause",
            command=self._pause_button_clicked,
        )
        self._stop_button = ttk.Button(
            self._voting_actions,
            text="Stop",
            command=self._stop_button_clicked,
        )
        self._integrate_button = ttk.Button(
            self._pubsub_actions,
            text="Integrate",
            command=self._integrate_button_clicked,
        )

        self._connect_button.grid(row=0, column=0, padx=4)
        self._disconnect_button.grid(row=0, column=1, padx=4)
        self._start_button.grid(row=0, column=2, padx=4)
        self._pause_button.grid(row=0, column=3, padx=4)
        self._stop_button.grid(row=0, column=4, padx=4)
        self._integrate_button.grid(row=1, column=2, padx=4)
        self._disconnected()

    # = = = = = = = = = = = = = = = = = = = #
    #             BUTTON ACTIONS            #
    # = = = = = = = = = = = = = = = = = = = #
    def _connect_button_clicked(self):
        self._connected()
        async_handler(self._voting_handler.connect)(self._disconnected)

    def _disconnect_button_clicked(self):
        async_handler(self._voting_handler.disconnect)()
        self._disconnected()

    def _on_window_close(self):
        async_handler(self._quit)(self._voting_handler.disconnect)

    def _start_button_clicked(self):
        self._started()
        self._voting_handler.start(self._stopped)

    def _pause_button_clicked(self):
        self._voting_handler.pause()
        self._paused()

    def _stop_button_clicked(self):
        self._voting_handler.stop()
        self._stopped()

    def _integrate_button_clicked(self):
        self._integrate()
        async_handler(self._voting_handler.integrate)(self._http_server_closed)

    # = = = = = = = = = = = = = = = = = = = #
    #             BUTTON STATES             #
    # = = = = = = = = = = = = = = = = = = = #
    def _connected(self):
        self._connect_button["state"] = "disabled"
        self._disconnect_button["state"] = "normal"
        self._start_button["state"] = "normal"
        self._integrate_button["state"] = "normal"

    def _disconnected(self):
        self._connect_button["state"] = "normal"
        self._disconnect_button["state"] = "disabled"
        self._start_button["state"] = "disabled"
        self._pause_button["state"] = "disabled"
        self._stop_button["state"] = "disabled"
        self._integrate_button["state"] = "disabled"

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
