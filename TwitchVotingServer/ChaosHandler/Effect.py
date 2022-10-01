class BaseEffect:
    name = "Base Effect"
    seconds: int

    @classmethod
    async def start(cls, *args):
        pass

    @classmethod
    async def stop(cls, *args):
        pass
