import asyncio

from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class BigHead(BaseEffect):
    name = "Big Head Mode"

    @classmethod
    async def onStart(cls, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 20)
        await cls.tick(cls.seconds, pm, module)

    @classmethod
    async def onStop(cls, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 0)
