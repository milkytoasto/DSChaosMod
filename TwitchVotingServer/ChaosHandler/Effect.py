import asyncio


class BaseEffect:
    name = "Base Effect"
    config_alias = "base_effect"

    def __init__(self, seconds, pm=None, module=None):
        self.running = False
        self.seconds = seconds
        self.pm = pm
        self.module = module

    def isLoading(self):
        pass

    async def start(self, *args):
        if not self.running:
            self.running = True
            if not self.isLoading():
                await self.onStart(*args)

    async def onStart(self, *args):
        pass

    def cancel(self):
        self.running = False

    async def tick(self, seconds=None, *args):
        if seconds is None:
            seconds = self.seconds

        i = 0
        while i < seconds:
            if not self.isLoading():
                if self.running:
                    await self.onTick(*args)
                    await asyncio.sleep(1)
                else:
                    await self.onStop(*args)
            if not self.running:
                return
            i = i + 1

    async def onTick(self, *args):
        pass

    async def stop(self, *args):
        if self.running:
            self.running = False

            if not self.isLoading():
                await self.onStop(*args)

    async def onStop(self, *args):
        pass
