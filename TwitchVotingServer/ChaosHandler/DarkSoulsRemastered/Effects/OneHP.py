from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, PointerAddress
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class OneHP(BaseEffect):
    name = "1 HP"

    @classmethod
    async def onStart(cls, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        HealthPointer = PointerAddress.PlayerHP(pm, BaseX)
        memory.write_bytes(
            pm.process_handle, HealthPointer, (1).to_bytes(4, "little"), 4
        )
