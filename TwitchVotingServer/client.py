import websockets
import asyncio

async def listen():
    url = "ws://localhost:7890"

    async with websockets.connect(url) as ws:
        await ws.send(f'Hello server!')
        while True:
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())