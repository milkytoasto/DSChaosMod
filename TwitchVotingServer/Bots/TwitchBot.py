import random

from twitchio.ext import commands


class TwitchBot(commands.Bot):
    def __init__(
        self,
        token,
        channel,
        debug_logger,
        chat_logger,
        messageHandler=False,
    ):
        super().__init__(token=token, prefix="?", initial_channels=[channel])
        self.acceptingVotes = False
        self.messageHandler = messageHandler
        self.debug_logger = debug_logger
        self.chat_logger = chat_logger
        self.channel = channel
        self.votes = {}

    async def start(self):
        try:
            await super().start()
        except:
            await self._http.session.close()

    def init_votes(self, acceptingVotes, effects):
        self.acceptingVotes = acceptingVotes

        self.votes = {
            str(index + 1): {"votes": set(), "name": effect.name, "effect": effect}
            for index, effect in enumerate(effects)
        }

    def get_effect(self):
        max_value = -1
        results = {}
        for (key, value) in self.votes.items():
            count = len(value["votes"])
            if count > max_value:
                results = {}
                max_value = count
            if count == max_value:
                results[key] = value
        result = results[random.choice(list(results.keys()))]
        return result["effect"]

    async def event_ready(self):
        self.debug_logger.info(f"TwitchBot: Logged onto Twitch WS as {self.nick}")
        self.debug_logger.info(f"TwitchBot: Listening in on {self.channel}'s chat")

    def format_votes(self):
        return {
            index: {
                "count": len(self.votes[index]["votes"]),
                "name": self.votes[index]["name"],
            }
            for index in self.votes.keys()
        }

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author
        content = message.content

        self.chat_logger.info(f"{author.name}: {content}")

        if self.acceptingVotes and content in self.votes.keys():
            self.votes[content]["votes"].add(message.author.name)
