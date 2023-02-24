import asyncio
import json
import logging

from Bots.TwitchBot import TwitchBot
from ChaosHandler.ChaosHandler import NoProcessFoundError


class VotingHandler:
    def __init__(
        self,
        config_handler,
        chaos_handler,
        websocket_handler,
    ):
        self.websocket_handler = websocket_handler
        self.chaos_handler = chaos_handler
        self.config_handler = config_handler

        self.debug_logger = logging.getLogger("debug")

        self.connected = False
        self.paused = False
        self.bot = None
        self.current_effect = None
        self.enabled = asyncio.Event()
        self.votes = {}

        self.load_config()

    async def connect(self, disconnect_gui):
        """Primary task handling logic, called when the GUI button
        for connect is pressed. Starts all tasks, with the voting/effect
        tasks set to wait until they are started.

        Args:
            disconnect_gui (method): Method to call when tasks finished.
        """
        if self.connected:
            self.debug_logger.error("Already connected.")
            return

        self.connected = True

        self.bot = TwitchBot(
            token=self.config_handler.get_option(
                "TWITCH", "TMI_TOKEN", "", type=str
            ),
            channel=self.config_handler.get_option(
                "TWITCH", "CHANNEL", "", type=str
            ),
            debug_logger=self.debug_logger,
            chat_logger=logging.getLogger("chat"),
            message_handler=self.broadcast_votes,
        )

        loop = asyncio.get_event_loop()
        twitch_task = loop.create_task(self.bot.start(), name="Twitch Task")
        voting_task = loop.create_task(
            self.voting_controller(), name="Voting Task"
        )
        effect_task = loop.create_task(
            self.chaos_handler.effect_controller(),
            name="Effects Task",
        )

        tasks = [twitch_task, effect_task, voting_task]
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED
        )

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
        disconnect_gui()
        self.debug_logger.info(
            f"Tasks cancelled. Connect to Twitch to re-run tasks"
        )

    async def disconnect(self):
        """Handles disconnect logic by closing the bot if it exists."""
        if self.bot is not None:
            await self.bot.close()

    def start(self, stop_gui):
        """Handle the logic for starting the voting process.
        Called by the GUI.

        Args:
            stopped (method): Method to call upon failure to start,
                sets the GUI state to stopped.
        """
        try:
            self.chaos_handler.hook()
        except NoProcessFoundError as e:
            self.debug_logger.error(f"{e}")
            stop_gui()
            return

        if not self.paused:
            self.bot.init_votes(
                self.accepting_votes,
                self.chaos_handler.get_options(),
            )
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
            self.accepting_votes,
            self.chaos_handler.get_existing_options(),
        )

        if self.current_effect is not None:
            self.current_effect.cancel()
            self.current_effect = None
            self.chaos_handler.effect.clear()

    async def voting_controller(self):
        """Voting task -- handles logic for getting and triggering effects,
        as well as getting / broadcasting the current voting state.
        """
        await self.enabled.wait()

        while self.connected:
            await self.enabled.wait()
            await asyncio.sleep(1)

            if self.remaining_time == 0:
                if self.accepting_votes:
                    effect_to_trigger = self.bot.get_effect()
                    self.current_effect = self.chaos_handler.trigger_effect(
                        effect_to_trigger,
                        self.effect_duration,
                    )

                self.accepting_votes = not self.accepting_votes
                self.remaining_time = (
                    self.voting_duration
                    if self.accepting_votes
                    else self.effect_duration
                )

                while (
                    self.enabled.is_set()
                    and self.current_effect.remaining_seconds
                    >= self.current_effect.seconds
                ):
                    self.broadcast_votes(self.bot.format_votes())
                    await asyncio.sleep(1)

                self.bot.init_votes(
                    self.accepting_votes,
                    self.chaos_handler.get_options(),
                )
            else:
                self.broadcast_votes(self.bot.format_votes())
                if (
                    self.current_effect is not None
                    and self.current_effect.running
                ):
                    self.remaining_time = self.current_effect.remaining_seconds
                else:
                    self.remaining_time -= 1

    def broadcast_votes(self, votes):
        """Formats current votes as well as stored voting state to be sent as
        a broadcasted message via the websocket connection.

        Args:
            votes (dict): Dictionary of voting options and current votes.
        """
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

    def load_config(self):
        """Loads and stores the state the necessary config settings."""
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
            self.voting_duration
            if self.accepting_votes
            else self.effect_duration
        )
