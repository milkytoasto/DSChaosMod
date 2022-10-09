from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class Sliding(BaseEffect):
    name = "Sliding"

    @classmethod
    async def onStart(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        SlidePointer = PointerAddress.Slide(pm, BaseX)

        await cls.tick(cls.seconds, pm, SlidePointer)

    @classmethod
    async def onTick(cls, pm, SlidePointer):
        memory.write_bytes(pm.process_handle, SlidePointer, b"\x01", 1)
