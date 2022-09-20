import asyncio
import json
import logging


class VotingHandler:
    def __init__(self, configHandler, websocketHandler):
        self.running = False
        self.votes = {}
        self.websocketHandler = websocketHandler
        self.configHandler = configHandler
        self.load_config()

    def set_bot(self, bot):
        self.bot = bot

    def __init_votes(self):
        self.bot.init_votes(self.acceptingVotes)

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.__init_votes()

    async def voting_controller(self):
        self.running = True
        self.__init_votes()

        while self.running:
            await asyncio.sleep(1)

            if self.remainingTime == 0:
                self.acceptingVotes = not self.acceptingVotes
                self.remainingTime = (
                    self.votingDuration if self.acceptingVotes else self.effectDuration
                )
                self.__init_votes()
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
