from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class OneHP(BaseEffect):
    name = "1 HP"

    @classmethod
    async def start(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        HealthPointer = PointerAddress.PlayerHP(pm, BaseX)
        memory.write_float(pm.process_handle, HealthPointer, 1)
