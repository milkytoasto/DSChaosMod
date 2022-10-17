from ChaosHandler.DarkSoulsRemastered.DSREffect import DSREffect
from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from pymem import memory


class DisableHUD(DSREffect):
    name = "Disable HUD"
    config_alias = "disable_hud"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HUDPointer = Pointer.HUD(pm, BaseB)

        memory.write_bytes(pm.process_handle, HUDPointer, b"\x00", 1)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HUDPointer = Pointer.HUD(pm, BaseB)

        memory.write_bytes(pm.process_handle, HUDPointer, b"\x01", 1)
