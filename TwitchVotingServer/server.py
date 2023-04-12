import os

from async_tkinter_loop import async_mainloop
from chaos.chaos_handler import ChaosHandler
from config_handler.config_handler import ConfigHandler
from gui.server_gui import ServerGUI
from voting.voting_handler import VotingHandler
from websocket.websocket_handler import WebsocketHandler

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), f"config/config.toml")
    ch = ConfigHandler(config_path=config_path)
    chaos = ChaosHandler(config_handler=ch)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(config_handler=ch, chaos_handler=chaos, websocket_handler=wsh)
    gui = ServerGUI(
        "Dark Souls Chaos Server",
        config_handler=ch,
        voting_handler=vh,
        websocket_server=wsh.websocket_server,
        chaos_handler=chaos,
    )
    async_mainloop(gui.root)
