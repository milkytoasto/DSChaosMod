import asyncio
import json
import logging

from Bots.TwitchBot import TwitchBot
from ChaosHandler.ChaosHandler import NoProcessFoundError


class VotingHandler:
    def __init__(self, configHandler, chaosHandler, websocketHandler):
        self.bot = None
        self.current_effect = None
        self.enabled = asyncio.Event()
        self.connected = False
        self.paused = False
        self.votes = {}
        self.websocketHandler = websocketHandler
        self.chaosHandler = chaosHandler
        self.configHandler = configHandler
        self.debug_logger = logging.getLogger("debug")
        self.load_config()

    async def connect(self, gui_disconnected):
        if self.connected:
            self.debug_logger.error("Already connected.")
            return

        self.connected = True

        self.bot = TwitchBot(
            token=self.configHandler.get_option("TWITCH", "TMI_TOKEN", "", type=str),
            channel=self.configHandler.get_option("TWITCH", "CHANNEL", "", type=str),
            debug_logger=self.debug_logger,
            chat_logger=logging.getLogger("chat"),
            messageHandler=self.broadcast_votes,
        )

        loop = asyncio.get_event_loop()
        twitch_task = loop.create_task(self.bot.start(), name="Twitch Task")
        voting_task = loop.create_task(self.voting_controller(), name="Voting Task")
        effect_task = loop.create_task(
            self.chaosHandler.effect_controller(), name="Effects Task"
        )

        tasks = [twitch_task, effect_task, voting_task]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        self.debug_logger.info(
            f"{len(done)} tasks exited. Cancelling {len(pending)} tasks "
        )

        for d in done:
            self.debug_logger.info(f"{d.get_name()} is done.")

        for p in pending:
            self.debug_logger.info(f"Cancelling {p.get_name()}.")
            p.cancel()

        self.bot = None
        self.connected = False
        self.enabled.clear()
        gui_disconnected()
        self.debug_logger.info(f"Tasks cancelled. Connect to Twitch to re-run tasks")

    async def disconnect(self):
        if self.bot is not None:
            await self.bot.close()

    def start(self, stopped):
        try:
            self.chaosHandler.hook()
        except NoProcessFoundError as e:
            self.debug_logger.error(f"EXCEPTION: {e}")
            stopped()
            return

        if not self.paused:
            self.bot.init_votes(self.acceptingVotes, self.chaosHandler.get_options())
        self.paused = False
        self.enabled.set()

    def pause(self):
        self.paused = True
        self.enabled.clear()

    def stop(self):
        self.paused = False
        self.enabled.clear()
        self.load_config()
        self.bot.init_votes(
            self.acceptingVotes, self.chaosHandler.get_existing_options()
        )

        if self.current_effect is not None:
            self.current_effect.cancel()

    async def voting_controller(self):
        await self.enabled.wait()

        while self.connected:
            await self.enabled.wait()
            await asyncio.sleep(1)

            if self.remainingTime == 0:
                if self.acceptingVotes:
                    self.current_effect = self.bot.get_effect()(self.effectDuration)
                    self.chaosHandler.trigger_effect(self.current_effect)

                self.acceptingVotes = not self.acceptingVotes
                self.remainingTime = (
                    self.votingDuration if self.acceptingVotes else self.effectDuration
                )
                self.bot.init_votes(
                    self.acceptingVotes, self.chaosHandler.get_options()
                )
            else:
                self.broadcast_votes(self.bot.format_votes())

            self.remainingTime -= 1

    def broadcast_votes(self, votes):
        self.votes = votes

        broadcast_message = {
            "ACCEPTING_VOTES": self.acceptingVotes,
            "REMAINING_TIME": self.remainingTime,
            "DURATION": self.votingDuration
            if self.acceptingVotes
            else self.effectDuration,
            "VOTES": self.votes,
        }
        broadcast_message = json.dumps(broadcast_message)

        logger = logging.getLogger("broadcast")
        logger.info(broadcast_message)

        self.websocketHandler.broadcast(broadcast_message)

    def load_config(self):
        self.acceptingVotes = self.configHandler.get_option(
            "VOTING", "INITIAL_STATE", True, type=bool
        )
        self.votingDuration = self.configHandler.get_option(
            "VOTING", "VOTING_DURATION", 60, type=int
        )
        self.effectDuration = self.configHandler.get_option(
            "VOTING", "EFFECT_DURATION", 120, type=int
        )
        self.remainingTime = (
            self.votingDuration if self.acceptingVotes else self.effectDuration
        )
