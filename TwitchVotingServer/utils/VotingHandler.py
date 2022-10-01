import asyncio
import json
import logging

from .TwitchBot import TwitchBot


class VotingHandler:
    def __init__(self, configHandler, chaosHandler, websocketHandler):
        self.running = False
        self.votes = {}
        self.websocketHandler = websocketHandler
        self.chaosHandler = chaosHandler
        self.configHandler = configHandler
        self.load_config()

    def set_bot(self, bot):
        self.bot = bot

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.load_config()
        self.bot.init_votes(self.acceptingVotes, self.chaosHandler.get_options())

    async def start(self):

        debug_logger = logging.getLogger("debug")
        chat_logger = logging.getLogger("chat")

        if self.running:
            debug_logger.error("Already running.")
            return

        bot = TwitchBot(
            token=self.configHandler.get_token(),
            channel=self.configHandler.get_channel(),
            debug_logger=debug_logger,
            chat_logger=chat_logger,
            messageHandler=self.broadcast_votes,
        )
        self.set_bot(bot)

        loop = asyncio.get_event_loop()

        self.event = asyncio.Event()

        twitch_task = loop.create_task(bot.start())
        effect_task = asyncio.ensure_future(self.effect_controller())
        voting_task = loop.create_task(self.voting_controller())

        tasks = [twitch_task, effect_task, voting_task]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for p in pending:
            debug_logger.info(
                f"{len(done)} tasks exited. Cancelling {len(pending)} tasks "
            )
            p.cancel()

        debug_logger.info(f"Tasks cancelled. Connect to Twitch to re-run tasks")

    async def effect_controller(self):
        self.chaosHandler.hook()
        while True:
            await self.event.wait()
            print(f"Triggering {self.current_effect.name} effect")
            await self.chaosHandler.trigger_effect(
                effect=self.current_effect, seconds=self.effectDuration
            )
            self.event.clear()

    async def voting_controller(self):
        self.running = True
        self.bot.init_votes(self.acceptingVotes, self.chaosHandler.get_options())

        while self.running:
            await asyncio.sleep(1)

            if self.remainingTime == 0:
                if self.acceptingVotes:
                    self.current_effect = self.bot.get_effect()
                    self.event.set()

                self.acceptingVotes = not self.acceptingVotes
                self.remainingTime = (
                    self.votingDuration if self.acceptingVotes else self.effectDuration
                )
                self.bot.init_votes(
                    self.acceptingVotes, self.chaosHandler.get_options()
                )
            else:
                self.broadcast_votes(self.votes)

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
