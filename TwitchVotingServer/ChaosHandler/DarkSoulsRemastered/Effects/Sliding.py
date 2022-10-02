import asyncio

from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class Sliding(BaseEffect):
    name = "Sliding"

    @classmethod
    async def start(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        SlidePointer = PointerAddress.Slide(pm, BaseX)

        seconds_passed = 0
        while seconds_passed < cls.seconds:
            seconds_passed = seconds_passed + 1
            memory.write_bytes(pm.process_handle, SlidePointer, b"\x01", 1)
            await asyncio.sleep(1)
