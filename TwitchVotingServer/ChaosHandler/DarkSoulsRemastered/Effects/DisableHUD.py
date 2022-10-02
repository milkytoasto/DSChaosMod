import asyncio

from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class DisableHUD(BaseEffect):
    name = "Disable HUD"

    @classmethod
    async def start(cls, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HUDPointer = PointerAddress.HUD(pm, BaseB)

        memory.write_bytes(pm.process_handle, HUDPointer, b"\x00", 1)
        await asyncio.sleep(cls.seconds)
        memory.write_bytes(pm.process_handle, HUDPointer, b"\x01", 1)
