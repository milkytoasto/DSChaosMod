import asyncio
import json


class VotingHandler:
    def __init__(self, configHandler, websocketHandler):
        self.running = False
        self.votes = {}
        self.websocketHandler = websocketHandler
        self.configHandler = configHandler
        self.load_config()

    def stop(self):
        self.running = False

    async def voting_controller(self, twitchBot):
        self.running = True

        while self.running:
            await asyncio.sleep(1)

            if self.remainingTime == 0:
                twitchBot.init_votes()
                self.acceptingVotes = not self.acceptingVotes
                self.remainingTime = (
                    self.votingDuration if self.acceptingVotes else self.effectDuration
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

        self.websocketHandler.broadcast(json.dumps(broadcast_message))

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
