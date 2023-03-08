import asyncio
import json
import logging

from bots.twitch.bot import TwitchBot
from chaos.chaos_handler import NoProcessFoundError


class VotingHandler:
    def __init__(self, config_handler, chaos_handler, websocket_handler):
        self.bot = None
        self.current_effect = None
        self.enabled = asyncio.Event()
        self.connected = False
        self.paused = False
        self.votes = {}

        self.websocket_handler = websocket_handler
        self.chaos_handler = chaos_handler
        self.config_handler = config_handler

        self.debug_logger = logging.getLogger("debug")

        # Loaded from config
        self.accepting_votes = None
        self.voting_duration = None  # Accessed from GUI
        self.effect_duration = None  # Accessed from GUI
        self.remaining_time = None

        self.load_config()

    async def connect(self, gui_disconnected):
        if self.connected:
            self.debug_logger.error("Already connected.")
            return

        self.connected = True

        self.bot = TwitchBot(
            token=self.config_handler.get_option("TWITCH", "TMI_TOKEN", "", type=str),
            channel=self.config_handler.get_option("TWITCH", "CHANNEL", "", type=str),
            debug_logger=self.debug_logger,
            chat_logger=logging.getLogger("chat"),
            message_handler=self._broadcast_votes,
        )

        loop = asyncio.get_event_loop()
        twitch_task = loop.create_task(self.bot.start(), name="Twitch Task")
        voting_task = loop.create_task(self._voting_controller(), name="Voting Task")
        effect_task = loop.create_task(
            self.chaos_handler.effect_controller(), name="Effects Task"
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
        self.current_effect = None
        gui_disconnected()
        self.debug_logger.info(f"Tasks cancelled. Connect to Twitch to re-run tasks")

    async def disconnect(self):
        if self.bot is not None:
            await self.bot.close()

    def start(self, stopped):
        try:
            self.chaos_handler.hook()
        except NoProcessFoundError as e:
            self.debug_logger.error(f"EXCEPTION: {e}")
            stopped()
            return

        if not self.paused:
            self.bot.init_votes(self.accepting_votes, self.chaos_handler.get_options())
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
            self.accepting_votes, self.chaos_handler.get_existing_options()
        )

        if self.current_effect is not None:
            self.current_effect.cancel()
            self.current_effect = None
            self.chaos_handler.effect.clear()

    async def integrate(self, callback):
        try:
            if self.bot is not None:
                await self.bot.generate_access_token(callback)
        finally:
            callback()

    def load_config(self):
        self.accepting_votes = self.config_handler.get_option(
            "VOTING", "INITIAL_STATE", True, type=bool
        )
        self.voting_duration = self.config_handler.get_option(
            "VOTING", "VOTING_DURATION", 60, type=int
        )
        self.effect_duration = self.config_handler.get_option(
            "VOTING", "EFFECT_DURATION", 120, type=int
        )
        self.remaining_time = (
            self.voting_duration if self.accepting_votes else self.effect_duration
        )

    async def _voting_controller(self):
        await self.enabled.wait()

        while self.connected:
            await self.enabled.wait()

            if self.remaining_time == 0:
                if self.accepting_votes:
                    effect_to_trigger = self.bot.get_effect()
                    self.current_effect = self.chaos_handler.trigger_effect(
                        effect_to_trigger, self.effect_duration
                    )

                self.accepting_votes = not self.accepting_votes
                self.remaining_time = (
                    self.voting_duration
                    if self.accepting_votes
                    else self.effect_duration
                )

                while (
                    self.enabled.is_set()
                    and self.current_effect is not None
                    and self.current_effect.remaining_seconds
                    > self.current_effect.seconds
                ):
                    self._broadcast_votes(self.bot.format_votes())
                    await asyncio.sleep(1)

                self.bot.init_votes(
                    self.accepting_votes, self.chaos_handler.get_options()
                )
            else:
                self._broadcast_votes(self.bot.format_votes())
                await asyncio.sleep(1)

                if self.current_effect is not None and self.current_effect.running:
                    self.remaining_time = self.current_effect.remaining_seconds
                else:
                    self.remaining_time -= 1

    def _broadcast_votes(self, votes):
        self.votes = votes

        broadcast_message = {
            "ACCEPTING_VOTES": self.accepting_votes,
            "REMAINING_TIME": self.remaining_time,
            "DURATION": self.voting_duration
            if self.accepting_votes
            else self.effect_duration,
            "VOTES": self.votes,
        }
        broadcast_message = json.dumps(broadcast_message)

        logger = logging.getLogger("broadcast")
        logger.info(broadcast_message)

        self.websocket_handler.broadcast(broadcast_message)
