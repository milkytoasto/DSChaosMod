import os

from async_tkinter_loop import async_mainloop
from ChaosHandler.ChaosHandler import ChaosHandler
from ConfigHandler.ConfigHandler import ConfigHandler
from gui.server_gui import ServerGUI
from HTTPServer.UrlFragmentFetchServer import UrlFragmentFetchServer
from VotingHandler.VotingHandler import VotingHandler
from WebsocketHandler.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    http_server = UrlFragmentFetchServer()

    config_path = os.path.join(os.path.dirname(__file__), f"config/config.ini")
    ch = ConfigHandler(config_path=config_path)
    chaos = ChaosHandler(configHandler=ch)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(configHandler=ch, chaosHandler=chaos, websocketHandler=wsh)

    gui = ServerGUI(
        "Dark Souls Chaos Server",
        config_handler=ch,
        voting_handler=vh,
        websocket_server=wsh.websocket_server,
    )
    gui.init_settings_tab(
        tmi_token=ch.get_option("TWITCH", "TMI_TOKEN", "", type=str),
        channel=ch.get_option("TWITCH", "CHANNEL", "", type=str),
        voting_duration=vh.votingDuration,
        effect_duration=vh.effectDuration,
    )
    gui.init_effects_tab(
        saveHandler=lambda: [chaos.load_config()],
    )

    async_mainloop(gui.root)
