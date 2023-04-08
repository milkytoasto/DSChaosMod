import asyncio


class BaseEffect:
    name = "Base Effect"
    config_alias = "base_effect"

    def __init__(self, seconds, pm=None, module=None):
        self.running = False
        self.seconds = int(seconds)
        self.remaining_seconds = int(seconds)
        self.pm = pm
        self.module = module

    def _is_loading(self):
        pass

    async def start(self, *args):
        if not self.running:
            self.running = True
            while self._is_loading() and self.running:
                await asyncio.sleep(1)
            await self._on_start(*args)

    async def _on_start(self, *args):
        pass

    def cancel(self):
        self.running = False

    async def tick(self, seconds=0, *args):
        if seconds is None:
            seconds = self.seconds

        self.remaining_seconds = int(seconds)
        while self.remaining_seconds > 0:
            if not self._is_loading():
                if self.running:
                    await self._on_tick(*args)
                    self.remaining_seconds = self.remaining_seconds - 1
                else:
                    await self._on_stop(*args)
            if not self.running:
                return
            await asyncio.sleep(1)

    async def _on_tick(self, *args):
        pass

    async def stop(self, *args):
        if self.running:
            while self._is_loading() and self.running:
                await asyncio.sleep(1)
            self.running = False
            await self._on_stop(*args)

    async def _on_stop(self, *args):
        pass
