from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class Sliding(DSREffect):
    name = "Sliding"
    config_alias = "sliding"

    async def _on_start(self):
        BaseX = BaseAddress.BaseX(self.pm, self.module)
        slide_pointer = Pointer.Player.Animations.slide(self.pm, BaseX)
        await self.tick(self.seconds, slide_pointer)

    async def _on_tick(self, slide_pointer):
        memory.write_bytes(self.pm.process_handle, slide_pointer, b"\x01", 1)
