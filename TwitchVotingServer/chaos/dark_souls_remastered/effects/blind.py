from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class Blind(DSREffect):
    name = "Blinded"
    config_alias = "blind"

    async def _on_start(self):
        BaseCAR = BaseAddress.BaseCAR(self.pm, self.module)
        draw_distance_pointer = Pointer.Settings.draw_distance(self.pm, BaseCAR)

        memory.write_float(self.pm.process_handle, draw_distance_pointer, 1)
        await self.tick(self.seconds)

    async def _on_stop(self):
        BaseCAR = BaseAddress.BaseCAR(self.pm, self.module)
        draw_distance_pointer = Pointer.Settings.draw_distance(self.pm, BaseCAR)

        memory.write_float(self.pm.process_handle, draw_distance_pointer, 3100)
