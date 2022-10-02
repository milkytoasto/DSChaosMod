import asyncio

from ChaosHandler.Effect import BaseEffect
from pymem import memory

from ..Memory import BaseAddress, get_pointer_address


class Sliding(BaseEffect):
    name = "Sliding"

    @classmethod
    async def start(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        slide_ptr = get_pointer_address(pm, BaseX, [0x68, 0x68, 0x48, 0x45C])

        seconds_passed = 0
        while seconds_passed < cls.seconds:
            seconds_passed = seconds_passed + 1
            memory.write_bytes(pm.process_handle, slide_ptr, b"\x01", 1)
            await asyncio.sleep(1)
