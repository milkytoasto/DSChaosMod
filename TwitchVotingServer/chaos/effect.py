import asyncio


class BaseEffect:
    name = "Base Effect"
    config_alias = "base_effect"

    def __init__(self, seconds, pm=None, module=None):
        self.running = False
        self.seconds = seconds
        self.remaining_seconds = seconds
        self.pm = pm
        self.module = module

    def isLoading(self):
        pass

    async def start(self, *args):
        if not self.running:
            self.running = True
            while self.isLoading() and self.running:
                await asyncio.sleep(1)
            await self.onStart(*args)

    async def onStart(self, *args):
        pass

    def cancel(self):
        self.running = False

    async def tick(self, seconds=0, *args):
        if seconds is None:
            seconds = self.seconds

        self.remaining_seconds = seconds
        while self.remaining_seconds > 0:
            if not self.isLoading():
                if self.running:
                    await self.onTick(*args)
                    self.remaining_seconds = self.remaining_seconds - 1
                else:
                    await self.onStop(*args)
            if not self.running:
                return
            await asyncio.sleep(1)

    async def onTick(self, *args):
        pass

    async def stop(self, *args):
        if self.running:
            while self.isLoading() and self.running:
                await asyncio.sleep(1)
            self.running = False
            await self.onStop(*args)

    async def onStop(self, *args):
        pass
