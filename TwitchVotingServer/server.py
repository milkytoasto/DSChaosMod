import configparser

from async_tkinter_loop import async_mainloop
from utils import load_twitch_config, save_handler, start
from utils.ConfigHandler import ConfigHandler
from utils.ServerGUI import ServerGUI
from utils.VotingHandler import VotingHandler
from utils.WebsocketHandler import WebsocketHandler

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    ch = ConfigHandler(config)
    wsh = WebsocketHandler(port=7890)
    vh = VotingHandler(configHandler=ch, websocketHandler=wsh)

    gui = ServerGUI("Dark Souls Chaos Server", websocket_server=wsh.websocket_server)
    gui.init_commands(start=lambda: start(vh, ch), pause=vh.pause, stop=vh.stop)

    CHANNEL, TOKEN = load_twitch_config(ch)

    gui.init_settings_tab(
        saveHandler=lambda fields: save_handler(fields=fields, vh=vh, config=config),
        channel=CHANNEL,
        tmiToken=TOKEN,
        votingDuration=vh.votingDuration,
        effectDuration=vh.effectDuration,
    )

    async_mainloop(gui.root)
