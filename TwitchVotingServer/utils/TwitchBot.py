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
        numOptions=3,
    ):
        super().__init__(token=token, prefix="?", initial_channels=[channel])
        self.acceptingVotes = False
        self.messageHandler = messageHandler
        self.debug_logger = debug_logger
        self.chat_logger = chat_logger
        self.channel = channel

    def init_votes(self, acceptingVotes, options):
        self.acceptingVotes = acceptingVotes

        self.votes = {
            str(index + 1): {"votes": set(), "name": value}
            for index, value in enumerate(options)
        }

        if self.messageHandler:
            self.messageHandler(
                {
                    index: {
                        "count": len(self.votes[index]["votes"]),
                        "name": self.votes[index]["name"],
                    }
                    for index in self.votes.keys()
                }
            )

    async def event_ready(self):
        self.debug_logger.info(f"TwitchBot: Logged onto Twitch WS as {self.nick}")
        self.debug_logger.info(f"TwitchBot: Listening in on {self.channel}'s chat")

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author
        # content = str(random.randint(1, 3))
        content = message.content

        self.chat_logger.info(f"{author.name}: {content}")

        if self.acceptingVotes and content in self.votes.keys():
            self.votes[content]["votes"].add(message.author.name)

            if self.messageHandler:
                self.messageHandler(
                    {
                        index: {
                            "count": len(self.votes[index]["votes"]),
                            "name": self.votes[index]["name"],
                        }
                        for index in self.votes.keys()
                    }
                )
