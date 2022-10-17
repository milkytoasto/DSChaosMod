from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class BigHead(BaseEffect):
    name = "Big Head Mode"
    config_alias = "big_head"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 20)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 0)
