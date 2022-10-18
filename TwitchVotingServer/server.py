import configparser

from async_tkinter_loop import async_mainloop
from ChaosHandler.ChaosHandler import ChaosHandler
from ConfigHandler.ConfigHandler import ConfigHandler
from ServerGUI.ServerGUI import ServerGUI
from VotingHandler.VotingHandler import VotingHandler
from WebsocketHandler.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    ch = ConfigHandler(config_path="./config/config.ini")
    chaos = ChaosHandler(config_handler=ch)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(
        config_handler=ch,
        chaos_handler=chaos,
        websocket_handler=wsh,
    )

    gui = ServerGUI(
        "Dark Souls Chaos Server",
        chaos_handler=chaos,
        config_handler=ch,
        voting_handler=vh,
        websocket_server=wsh.websocket_server,
    )

    async_mainloop(gui.root)
