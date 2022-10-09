import asyncio


class BaseEffect:
    name = "Base Effect"
    running = False
    seconds: int
    config_alias = "base_effect"

    @classmethod
    async def start(cls, *args):
        if not cls.running:
            cls.running = True
            await cls.onStart(*args)

    @classmethod
    async def onStart(cls, *args):
        pass

    @classmethod
    def cancel(cls):
        cls.running = False

    @classmethod
    async def tick(cls, seconds=None, *args):
        if seconds is None:
            seconds = cls.seconds

        i = 0
        while i < seconds:
            if cls.running:
                await cls.onTick(*args)
                await asyncio.sleep(1)
            else:
                await cls.onStop(*args)
                return
            i = i + 1

    @classmethod
    async def onTick(cls, *args):
        pass

    @classmethod
    async def stop(cls, *args):
        if cls.running:
            await cls.onStop(*args)
            cls.running = False

    @classmethod
    async def onStop(cls, *args):
        pass
