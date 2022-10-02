from ChaosHandler.Effect import BaseEffect
from pymem import memory

from ..Memory import BaseAddress, get_pointer_address


class OneHP(BaseEffect):
    name = "1 HP"

    @classmethod
    async def start(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        head_ptr = get_pointer_address(pm, BaseX, [0x10, 0x388])
        memory.write_float(pm.process_handle, head_ptr, 1)
