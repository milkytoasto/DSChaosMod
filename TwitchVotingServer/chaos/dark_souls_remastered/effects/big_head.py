from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class BigHead(DSREffect):
    name = "Big Head Mode"
    config_alias = "big_head"

    async def _set_head_size(self, size):
        BaseB = BaseAddress.BaseB(self.pm, self.module)
        head_pointer = Pointer.Player.Body.head_size(self.pm, BaseB)
        memory.write_float(self.pm.process_handle, head_pointer, size)

    async def _on_start(self):
        await self._set_head_size(20)
        await self.tick(self.seconds)

    async def _on_stop(self):
        await self._set_head_size(0)
