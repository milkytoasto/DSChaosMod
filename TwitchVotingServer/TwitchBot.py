from twitchio.ext import commands


class TwitchBot(commands.Bot):
    def __init__(self, token, channel, debug_logger, chat_logger, messageHandler=False):
        super().__init__(token=token, prefix="?", initial_channels=[channel])
        self.voting = False
        self.messages = []
        self.messageHandler = messageHandler
        self.debug_logger = debug_logger
        self.chat_logger = chat_logger
        self.channel = channel

    async def event_ready(self):
        self.debug_logger.info(f"TwitchBot: Logged onto Twitch WS as {self.nick}")
        self.debug_logger.info(f"TwitchBot: Listening in on {self.channel}'s chat")

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author
        content = message.content

        self.chat_logger.info(f"{author.name}: {content}")

        self.messages.append(content)
        if self.messageHandler:
            self.messageHandler(message.content)
