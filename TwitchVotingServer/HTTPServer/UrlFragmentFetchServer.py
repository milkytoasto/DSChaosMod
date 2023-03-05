import asyncio
import logging
import os
import time
from urllib.parse import unquote, urlparse


class UrlFragmentFetchServer:
    # Based on https://github.com/noskillsben/python-url-fragment-extractor/blob/main/urlfragmentfetchserver.py

    def __init__(self, timeout=20, port=8080):
        self._port = port
        self._keep_running = True
        self._connected = False
        self._timeout_time = time.time() + timeout
        self._port = port
        self._server = None
        self.data = None
        self.debug_logger = logging.getLogger("debug")

    def start(self, callback=None):
        """Starts listening on localhost until it times out or until it returns Url fragments in a dict."""
        self.debug_logger.info(f"Starting HTTP Server on port {self._port}.")
        self._keep_running = True
        asyncio.ensure_future(self.__start_server(callback))
        return self.data

    async def __time_out_shutdown(self):
        """Simple function that ensures the server shuts down if there is no connection for a while"""
        while self._keep_running or self._connected:
            await asyncio.sleep(1)
            if time.time() >= self._timeout_time:
                self._keep_running = False

        self._server.close()
        await self._server.wait_closed()
        self.debug_logger.info(f"HTTP Server on port {self._port} closed.")

    async def __start_server(self, callback):
        """Asyncio "main" async coroutine starts the server in server_forever mode"""
        server = await asyncio.start_server(
            client_connected_cb=self.__handle_connection,
            host="localhost",
            port=self._port,
        )

        self._server = server
        asyncio.ensure_future(self.__time_out_shutdown())

        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass

        await callback(self.data)

    def __get_html_block(self):
        html_file = open(
            os.path.join(os.path.dirname(__file__), "./html_block.html"),
            "r",
            encoding="utf-8",
        )
        html_string = html_file.read()
        html_byte = html_string.encode()
        return html_byte

    async def __send_response(self, writer, response):
        headers = {
            "Content-Type": "text/html",
            "Content-Length": str(len(response)),
        }
        encoded_headers = b"".join(
            f"{key}: {value}\n".encode() for key, value in headers.items()
        )
        writer.write(b"HTTP/1.0 200 OK\n" + encoded_headers + b"\n" + response)
        await writer.drain()
        writer.close()

    async def __handle_connection(self, reader, writer):
        data = await reader.readline()
        msg = data.decode()

        self._connected = True

        if msg.startswith("GET"):
            await reader.readuntil(b"\r\n")
            response = self.__get_html_block()
            await self.__send_response(writer, response)

        elif msg.startswith("POST"):
            data = await reader.read(4096)

            try:
                returned_url = urlparse(data.split(b"\r\n\r\n")[-1])
                returned_fragments = returned_url.fragment.decode().split("&")

                final_data = {}
                for fragment in returned_fragments:
                    decoded_fragment = unquote(fragment)
                    fragment_pair = decoded_fragment.split("=")
                    final_data[fragment_pair[0]] = fragment_pair[1]

                self.data = final_data
                response_msg = (
                    b"Information has been retrieved. You can now close this page."
                )
            except:
                response_msg = b"Something went wrong. See application for detail\nYou can now close this page."

            await self.__send_response(writer, response_msg)
            self._keep_running = False

        self._connected = False
