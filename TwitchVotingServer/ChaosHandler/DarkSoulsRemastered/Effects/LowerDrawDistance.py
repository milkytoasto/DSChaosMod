import asyncio

from ChaosHandler.Effect import BaseEffect
from pymem import memory

from ..Memory import BaseAddress, get_pointer_address


class LowerDrawDistance(BaseEffect):
    name = "Lower Draw Distance"

    @classmethod
    async def start(cls, pm, module):
        BaseCAR = BaseAddress.BaseCAR(pm, module)
        drawdistance_ptr = get_pointer_address(pm, BaseCAR, [0x60, 0x60, 0x5C])

        memory.write_float(pm.process_handle, drawdistance_ptr, 10)
        await asyncio.sleep(cls.seconds)
        memory.write_float(pm.process_handle, drawdistance_ptr, 3100)
