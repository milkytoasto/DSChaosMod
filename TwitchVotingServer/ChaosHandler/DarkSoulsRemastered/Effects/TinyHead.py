import asyncio

from ChaosHandler.Effect import BaseEffect
from pymem import memory

from ..Memory import BaseAddress, get_pointer_address


class TinyHead(BaseEffect):
    name = "Tiny Head Mode"

    @classmethod
    async def start(cls, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        head_ptr = get_pointer_address(pm, BaseB, [0x10, 0x388])

        memory.write_float(pm.process_handle, head_ptr, -10)
        await asyncio.sleep(cls.seconds)
        memory.write_bytes(pm.process_handle, head_ptr, 0)
