import asyncio

from ChaosHandler.Effect import BaseEffect
from pymem import memory, pattern

from ..Memory import AOBS, get_pointer_address


class Blind(BaseEffect):
    name = "Blinded"

    @classmethod
    async def start(cls, pm, module):
        GetCAR = pattern.pattern_scan_module(pm.process_handle, module, AOBS.BaseCAR)
        BaseCAR = GetCAR + pm.read_int(GetCAR + 3) + 7

        drawdistance_ptr = get_pointer_address(pm, BaseCAR, [0x60, 0x60, 0x5C])

        memory.write_float(pm.process_handle, drawdistance_ptr, 1)
        await asyncio.sleep(cls.seconds)
        memory.write_float(pm.process_handle, drawdistance_ptr, 3100)
