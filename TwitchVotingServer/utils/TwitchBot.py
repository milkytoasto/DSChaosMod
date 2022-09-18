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
        self.voting = False
        self.messageHandler = messageHandler
        self.debug_logger = debug_logger
        self.chat_logger = chat_logger
        self.channel = channel
        self.optionKeys = [str(val + 1) for val in range(numOptions)]
        self.initVotes()

    def initVotes(self):
        self.votes = {key: set() for key in self.optionKeys}

    async def event_ready(self):
        self.debug_logger.info(f"TwitchBot: Logged onto Twitch WS as {self.nick}")
        self.debug_logger.info(f"TwitchBot: Listening in on {self.channel}'s chat")

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author
        content = message.content

        self.chat_logger.info(f"{author.name}: {content}")

        if message.content in self.votes.keys():
            self.votes[message.content].add(message.author.name)

            if self.messageHandler:
                self.messageHandler(self.votes)
