import configparser

from async_tkinter_loop import async_mainloop
from ChaosHandler.ChaosHandler import ChaosHandler
from ConfigHandler.ConfigHandler import ConfigHandler
from ServerGUI.ServerGUI import ServerGUI
from VotingHandler.VotingHandler import VotingHandler
from WebsocketHandler.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    ch = ConfigHandler(config_path="./config/config.ini")
    chaos = ChaosHandler(configHandler=ch)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(configHandler=ch, chaosHandler=chaos, websocketHandler=wsh)

    gui = ServerGUI(
        "Dark Souls Chaos Server",
        configHandler=ch,
        websocket_server=wsh.websocket_server,
    )
    gui.init_commands(
        connect=vh.connect,
        disconnect=vh.disconnect,
        start=vh.start,
        pause=vh.pause,
        stop=vh.stop,
    )
    gui.init_settings_tab(
        saveHandler=lambda: [vh.load_config()],
        channel=ch.get_option("TWITCH", "CHANNEL", "", type=str),
        tmiToken=ch.get_option("TWITCH", "TMI_TOKEN", "", type=str),
        votingDuration=vh.votingDuration,
        effectDuration=vh.effectDuration,
    )
    gui.init_effects_tab(
        saveHandler=lambda: [chaos.load_config()],
    )

    async_mainloop(gui.root)
