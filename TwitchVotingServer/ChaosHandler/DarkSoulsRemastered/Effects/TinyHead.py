from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class TinyHead(BaseEffect):
    name = "Tiny Head Mode"
    config_alias = "tiny_head"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, -10)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = PointerAddress.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 0)
