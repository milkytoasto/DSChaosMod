import asyncio
import logging

import websockets


class WebsocketHandler:
    def __init__(self, port):
        self.clients = set()
        self.port = port

    async def handler(self, websocket, path):
        debug_logger = logging.getLogger("debug")
        debug_logger.info(f"Client just connected.")
        self.clients.add(websocket)

        try:
            async for message in websocket:
                debug_logger.info(f"Received message from client: {message}")
                for connection in self.clients:
                    if connection != websocket:
                        await connection.send(f"Someone said: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            debug_logger.info(f"A client has lost connection.")
        finally:
            self.clients.remove(websocket)

    async def send(self, websocket, message):
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

    def broadcast(self, message):
        """Broadcasts messages to websocket clients via an async task.

        Args:
            message (string): The message to broadcast.
        """
        for websocket in self.clients:
            asyncio.create_task(self.send(websocket, message))

    async def websocket_server(self):
        logger = logging.getLogger("debug")
        logger.info(f"Listening on port {self.port}")
        await websockets.serve(self.handler, "localhost", self.port)
