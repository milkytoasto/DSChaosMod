import asyncio
import logging

from .TwitchBot import TwitchBot


def load_twitch_config(ch):
    CHANNEL = ch.get_option("TWITCH", "CHANNEL", "", type=str)
    TOKEN = ch.get_option("TWITCH", "TMI_TOKEN", "", type=str)

    return CHANNEL, TOKEN


async def start(vh, ch):

    debug_logger = logging.getLogger("debug")
    chat_logger = logging.getLogger("chat")

    if vh.running:
        debug_logger.error("Already running.")
        return

    CHANNEL, TOKEN = load_twitch_config(ch)

    bot = TwitchBot(
        token=TOKEN,
        channel=CHANNEL,
        debug_logger=debug_logger,
        chat_logger=chat_logger,
        messageHandler=vh.broadcast_votes,
    )
    vh.set_bot(bot)

    loop = asyncio.get_event_loop()
    twitch_task = loop.create_task(bot.start())
    voting_task = loop.create_task(vh.voting_controller())

    tasks = [twitch_task, voting_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for p in pending:
        debug_logger.info(f"{len(done)} tasks exited. Cancelling {len(pending)} tasks ")
        p.cancel()

    debug_logger.info(f"Tasks cancelled. Connect to Twitch to re-run tasks")


def save_handler(fields, vh, config):

    for section in fields:
        for option in fields[section]:
            value = fields[section][option].get()
            if value:
                config.set(section, option, value)

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    vh.load_config()
