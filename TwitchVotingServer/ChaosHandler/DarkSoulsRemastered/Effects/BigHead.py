from ChaosHandler.DarkSoulsRemastered.DSREffect import DSREffect
from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from pymem import memory


class BigHead(DSREffect):
    name = "Big Head Mode"
    config_alias = "big_head"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = Pointer.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 20)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = Pointer.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 0)
