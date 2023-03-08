from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class DisableHUD(DSREffect):
    name = "Disable HUD"
    config_alias = "disable_hud"

    async def _on_start(self):
        BaseB = BaseAddress.BaseB(self.pm, self.module)
        hud_pointer = Pointer.Interface.hud(self.pm, BaseB)

        memory.write_bytes(self.pm.process_handle, hud_pointer, b"\x00", 1)
        await self.tick(self.seconds)

    async def _on_stop(self):
        BaseB = BaseAddress.BaseB(self.pm, self.module)
        hud_pointer = Pointer.Interface.hud(self.pm, BaseB)

        memory.write_bytes(self.pm.process_handle, hud_pointer, b"\x01", 1)
