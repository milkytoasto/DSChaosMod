import asyncio
import configparser
import json
import logging

from async_tkinter_loop import async_mainloop
from utils.ConfigHandler import ConfigHandler
from utils.ServerGUI import ServerGUI
from utils.TwitchBot import TwitchBot
from utils.WebsocketHandler import WebsocketHandler

config = configparser.ConfigParser()
config.read("config.ini")

BOT = False
RUNNING = False
VOTES = {}


def load_config():
    global ACCEPTING_VOTES, VOTING_DURATION, EFFECT_DURATION, REMAINING_TIME, TOKEN, CHANNEL

    ACCEPTING_VOTES = ch.get_option("VOTING", "INITIAL_STATE", True, type=bool)
    VOTING_DURATION = ch.get_option("VOTING", "VOTING_DURATION", 60, type=int)
    EFFECT_DURATION = ch.get_option("VOTING", "EFFECT_DURATION", 60, type=int)
    REMAINING_TIME = VOTING_DURATION if ACCEPTING_VOTES else EFFECT_DURATION

    TOKEN = ch.get_option("TWITCH", "TMI_TOKEN", "", type=str)
    CHANNEL = ch.get_option("TWITCH", "CHANNEL", "", type=str)


def broadcast_votes(votes):
    global VOTES
    VOTES = votes

    broadcast_message = {
        "ACCEPTING_VOTES": ACCEPTING_VOTES,
        "REMAINING_TIME": REMAINING_TIME,
        "DURATION": VOTING_DURATION if ACCEPTING_VOTES else EFFECT_DURATION,
        "VOTES": votes,
    }

    wsh.broadcast(json.dumps(broadcast_message))


async def voting_controller(bot):
    global ACCEPTING_VOTES, REMAINING_TIME

    while RUNNING:
        await asyncio.sleep(1)

        if REMAINING_TIME == 0:
            bot.init_votes()
            ACCEPTING_VOTES = ~ACCEPTING_VOTES
            REMAINING_TIME = VOTING_DURATION if ACCEPTING_VOTES else EFFECT_DURATION
        else:
            broadcast_votes(VOTES)

        REMAINING_TIME -= 1


def stop():
    global RUNNING
    RUNNING = False


async def start(gui):
    global RUNNING
    gui.started()

    debug_logger = logging.getLogger("debug")
    chat_logger = logging.getLogger("chat")

    if RUNNING:
        debug_logger.error("Already running.")
        return

    RUNNING = True

    bot = TwitchBot(
        token=TOKEN,
        channel=CHANNEL,
        debug_logger=debug_logger,
        chat_logger=chat_logger,
        messageHandler=broadcast_votes,
    )

    loop = asyncio.get_event_loop()
    twitch_task = loop.create_task(bot.start())
    voting_task = loop.create_task(voting_controller(bot))

    tasks = [twitch_task, voting_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for p in pending:
        debug_logger.info(f"{len(done)} tasks exited. Cancelling {len(pending)} tasks ")
        p.cancel()
    debug_logger.info(f"Tasks cancelled. Connect to Twitch to re-run tasks")
    gui.stopped()


def save_handler(fields):

    for section in fields:
        for option in fields[section]:
            value = fields[section][option].get()
            if value:
                config.set(section, option, value)

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    load_config()


if __name__ == "__main__":
    ch = ConfigHandler(config)
    wsh = WebsocketHandler(port=7890)

    load_config()

    gui = ServerGUI("Dark Souls Chaos Server", websocket_server=wsh.websocket_server)
    gui.init_commands(start=start, stop=stop)
    gui.init_settings_tab(
        saveHandler=save_handler,
        channel=CHANNEL,
        tmiToken=TOKEN,
        votingDuration=VOTING_DURATION,
        effectDuration=EFFECT_DURATION,
    )

    async_mainloop(gui.root)
