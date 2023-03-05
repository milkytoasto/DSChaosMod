from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class TinyHead(DSREffect):
    name = "Tiny Head Mode"
    config_alias = "tiny_head"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = Pointer.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, -10)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HeadPointer = Pointer.PlayerHeadSize(pm, BaseB)

        memory.write_float(pm.process_handle, HeadPointer, 0)
