import asyncio
import logging

import websockets


class WebsocketHandler:
    def __init__(self, port):
        self.clients = set()
        self.port = port

    async def handler(self, websocket, path):
        debug_logger = logging.getLogger("debug")
        debug_logger.info(f"Websocket Handler: Client just connected.")
        self.clients.add(websocket)

        try:
            async for message in websocket:
                debug_logger.info(
                    f"Websocket Handler: Received message from client: {message}"
                )
                for connection in self.clients:
                    if connection != websocket:
                        await connection.send(
                            f"Websocket Handler: Someone said: {message}"
                        )
        except websockets.exceptions.ConnectionClosed as e:
            debug_logger.info(f"Websocket Handler: A client has lost connection.")
        finally:
            self.clients.remove(websocket)

    async def send(self, websocket, message):
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

    def broadcast(self, message):
        for websocket in self.clients:
            asyncio.create_task(self.send(websocket, message))

    async def websocket_server(self):
        logger = logging.getLogger("debug")
        logger.info(f"Websocket Server: Listening on port {self.port}")
        await websockets.serve(self.handler, "localhost", self.port)
