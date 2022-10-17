from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class DisableHUD(BaseEffect):
    name = "Disable HUD"
    config_alias = "disable_hud"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HUDPointer = PointerAddress.HUD(pm, BaseB)

        memory.write_bytes(pm.process_handle, HUDPointer, b"\x00", 1)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HUDPointer = PointerAddress.HUD(pm, BaseB)

        memory.write_bytes(pm.process_handle, HUDPointer, b"\x01", 1)
