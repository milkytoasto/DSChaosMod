from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class Sliding(BaseEffect):
    name = "Sliding"
    config_alias = "sliding"

    async def onStart(self, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        SlidePointer = PointerAddress.Slide(pm, BaseX)

        await self.tick(self.seconds, pm, SlidePointer)

    async def onTick(self, pm, SlidePointer):
        memory.write_bytes(pm.process_handle, SlidePointer, b"\x01", 1)
