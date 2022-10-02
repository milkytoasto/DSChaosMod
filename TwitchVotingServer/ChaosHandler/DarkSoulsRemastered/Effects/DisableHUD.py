import asyncio

from ChaosHandler.Effect import BaseEffect
from pymem import memory

from ..Memory import BaseAddress, get_pointer_address


class DisableHUD(BaseEffect):
    name = "Disable HUD"

    @classmethod
    async def start(cls, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        hud_ptr = get_pointer_address(pm, BaseB, [0x58, 0x11])

        memory.write_bytes(pm.process_handle, hud_ptr, b"\x00", 1)
        await asyncio.sleep(cls.seconds)
        memory.write_bytes(pm.process_handle, hud_ptr, b"\x01", 1)
