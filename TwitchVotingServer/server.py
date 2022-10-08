import configparser

from async_tkinter_loop import async_mainloop
from ChaosHandler.ChaosHandler import ChaosHandler
from utils.ConfigHandler import ConfigHandler
from utils.ServerGUI import ServerGUI
from utils.VotingHandler import VotingHandler
from utils.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    chaos = ChaosHandler()
    ch = ConfigHandler(config)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(configHandler=ch, chaosHandler=chaos, websocketHandler=wsh)

    gui = ServerGUI("Dark Souls Chaos Server", websocket_server=wsh.websocket_server)
    gui.init_commands(
        connect=lambda: vh.connect(gui.stopped),
        start=lambda: vh.start(gui.stopped),
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

    async_mainloop(gui.root)
