import configparser

from async_tkinter_loop import async_mainloop
from ChaosHandler.ChaosHandler import ChaosHandler
from ConfigHandler.ConfigHandler import ConfigHandler
from ServerGUI.ServerGUI import ServerGUI
from VotingHandler.VotingHandler import VotingHandler
from WebsocketHandler.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    chaos = ChaosHandler()
    ch = ConfigHandler(config)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(configHandler=ch, chaosHandler=chaos, websocketHandler=wsh)

    gui = ServerGUI("Dark Souls Chaos Server", websocket_server=wsh.websocket_server)
    gui.init_commands(
        connect=vh.connect,
        disconnect=vh.disconnect,
        start=vh.start,
        pause=vh.pause,
        stop=vh.stop,
    )
    gui.init_settings_tab(
        saveHandler=lambda fields: [ch.save_config(fields), vh.load_config()],
        channel=ch.get_channel(),
        tmiToken=ch.get_token(),
        votingDuration=vh.votingDuration,
        effectDuration=vh.effectDuration,
    )
    gui.init_effects_tab(
        saveHandler=lambda fields: [ch.save_config(fields), vh.load_config()],
        configHandler=ch,
    )

    async_mainloop(gui.root)
