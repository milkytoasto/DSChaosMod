import random
import webbrowser

import requests
from bots.twitch import scopes
from HTTPServer.UrlFragmentFetchServer import UrlFragmentFetchServer
from twitchio.ext import commands, pubsub


class TwitchBot(commands.Bot):
    def __init__(
        self,
        token,
        channel,
        debug_logger,
        chat_logger,
        message_handler=False,
    ):
        super().__init__(token=token, prefix="?", initial_channels=[channel])
        self.channel = channel
        self.accepting_votes = False
        self.message_handler = message_handler
        self.debug_logger = debug_logger
        self.chat_logger = chat_logger
        self.votes = {}
        self._fragment_fetch_server = UrlFragmentFetchServer()

    async def subscribe(self, token):
        self.pubsub = pubsub.PubSubPool(self)
        channel = self.get_channel(self.channel)
        user = await channel.user()
        userId = user.id

        topics = [
            pubsub.channel_points(token)[userId],
        ]

        await self.pubsub.subscribe_topics(topics)

    async def handle_access_token(self, callback, data):
        access_token = data.get("access_token")

        if access_token:
            await self.subscribe(access_token)

        callback()

    async def generate_access_token(self, callback):
        self._fragment_fetch_server.start(
            lambda data: self.handle_access_token(callback, data)
        )

        server = "localhost"
        port = 8080
        redirect_uri = f"http://{server}:{port}"

        params = {
            "response_type": "token",
            "client_id": "zbdsd2e5665sahh5ijoqjjxhg9e2x1",
            "redirect_uri": redirect_uri,
            "scope": scopes.Channel.Read.REDEMPTIONS,
            "state": "c3ab8aa609ea11e793ae92361f002671",
        }

        url = "https://id.twitch.tv/oauth2/authorize"
        request = requests.Request("GET", url, params).prepare()
        request.prepare_url(url, params)
        webbrowser.open(request.url, 2, True)

    async def event_pubsub_channel_points(
        self, event: pubsub.PubSubChannelPointsMessage
    ):
        print("Got Channel Points")
        pass

    async def start(self):
        try:
            await super().start()
        except:
            await self._http.session.close()

    def init_votes(self, accepting_votes, effects):
        self.accepting_votes = accepting_votes

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

        if self.accepting_votes and content in self.votes.keys():
            self.votes[content]["votes"].add(message.author.name)
