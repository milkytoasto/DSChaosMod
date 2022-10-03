class BaseEffect:
    name = "Base Effect"
    running = False
    seconds: int

    @classmethod
    async def start(cls, *args):
        if not cls.running:
            cls.running = True
            await cls.onStart(*args)

    @classmethod
    async def onStart(cls, *args):
        pass

    @classmethod
    async def stop(cls, *args):
        if cls.running:
            await cls.onStop(*args)
            cls.running = False

    @classmethod
    async def onStop(cls, *args):
        pass
