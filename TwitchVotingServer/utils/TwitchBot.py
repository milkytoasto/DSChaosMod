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
        self.optionKeys = [str(val + 1) for val in range(numOptions)]

    def init_votes(self, acceptingVotes):
        self.acceptingVotes = acceptingVotes

        self.votes = {key: set() for key in self.optionKeys}

        if self.messageHandler:
            self.messageHandler({key: len(self.votes[key]) for key in self.optionKeys})

    async def event_ready(self):
        self.debug_logger.info(f"TwitchBot: Logged onto Twitch WS as {self.nick}")
        self.debug_logger.info(f"TwitchBot: Listening in on {self.channel}'s chat")

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author
        content = message.content

        self.chat_logger.info(f"{author.name}: {content}")

        if not self.acceptingVotes:
            return

        if content in self.votes.keys():
            self.votes[content].add(message.author.name)

            if self.messageHandler:
                self.messageHandler(
                    {key: len(self.votes[key]) for key in self.optionKeys}
                )
