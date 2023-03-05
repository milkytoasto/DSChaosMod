from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class Sliding(DSREffect):
    name = "Sliding"
    config_alias = "sliding"

    async def onStart(self, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        SlidePointer = Pointer.Slide(pm, BaseX)

        await self.tick(self.seconds, pm, SlidePointer)

    async def onTick(self, pm, SlidePointer):
        memory.write_bytes(pm.process_handle, SlidePointer, b"\x01", 1)
