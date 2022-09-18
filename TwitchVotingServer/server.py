import asyncio
import configparser
import logging

import websockets
from async_tkinter_loop import async_mainloop
from utils.ServerGUI import ServerGUI
from utils.TwitchBot import TwitchBot

config = configparser.ConfigParser()
config.read("config.ini")

BOT = False
RUNNING = False
PORT = config["WEBSOCKET"]["PORT"]
VOTING_ENABLED = config["VOTING"].getboolean("INITIAL_STATE")
VOTING_ENABLED_PERIOD = config["VOTING"].getint("VOTING_PERIOD")
VOTING_DISABLED_PERIOD = config["VOTING"].getint("VOTING_INTERVAL")
VOTING_PERIOD = VOTING_ENABLED_PERIOD if VOTING_ENABLED else VOTING_DISABLED_PERIOD
COUNTDOWN = VOTING_PERIOD
TOKEN = config["TWITCH"]["TMI_TOKEN"]
CHANNEL = config["TWITCH"]["CHANNEL"]
CLIENTS = set()


async def handler(websocket, path):
    debug_logger = logging.getLogger("debug")
    debug_logger.info(f"Websocket Handler: Client just connected.")
    CLIENTS.add(websocket)

    try:
        async for message in websocket:
            debug_logger.info(
                f"Websocket Handler: Received message from client: {message} {path}"
            )
            for connection in CLIENTS:
                if connection != websocket:
                    await connection.send(f"Websocket Handler: Someone said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        debug_logger.info(f"Websocket Handler: A client has lost connection.")
    finally:
        CLIENTS.remove(websocket)


async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass


def broadcast(message):
    for websocket in CLIENTS:
        asyncio.create_task(send(websocket, message))


async def voting_controller():
    global VOTING_ENABLED, VOTING_PERIOD, COUNTDOWN

    while RUNNING:
        broadcast(f"{VOTING_ENABLED} Time remaining {COUNTDOWN}")
        await asyncio.sleep(1)
        if COUNTDOWN == 0:
            VOTING_ENABLED = ~VOTING_ENABLED
            VOTING_PERIOD = (
                VOTING_ENABLED_PERIOD if VOTING_ENABLED else VOTING_DISABLED_PERIOD
            )
            COUNTDOWN = VOTING_PERIOD
        COUNTDOWN -= 1


def stop():
    global RUNNING
    RUNNING = False


async def start():
    global RUNNING
    debug_logger = logging.getLogger("debug")
    chat_logger = logging.getLogger("chat")

    if RUNNING:
        debug_logger.error("Already running, dumbass.")
        return

    RUNNING = True

    bot = TwitchBot(
        token=TOKEN,
        channel=CHANNEL,
        debug_logger=debug_logger,
        chat_logger=chat_logger,
        messageHandler=broadcast,
    )

    loop = asyncio.get_event_loop()
    twitch_task = loop.create_task(bot.start())
    voting_task = loop.create_task(voting_controller())

    tasks = [twitch_task, voting_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for p in pending:
        debug_logger.info(f"{len(done)} tasks exited. Cancelling {len(pending)} tasks ")
        p.cancel()


async def websocket_server():
    logger = logging.getLogger("debug")
    logger.info(f"Websocket Server: Listening on port {PORT}")
    await websockets.serve(handler, "localhost", PORT)


if __name__ == "__main__":
    gui = ServerGUI("Dark Souls Chaos Server")
    gui.initCommands(websocket_server=websocket_server, start=start, stop=stop)
    gui.initSettingsTab(channel=CHANNEL, votingDuration=VOTING_ENABLED_PERIOD)
    async_mainloop(gui.root)
