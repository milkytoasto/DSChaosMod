from ChaosHandler.DarkSoulsRemastered.DSREffect import DSREffect
from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from pymem import memory


class OneHP(DSREffect):
    name = "1 HP"
    config_alias = "one_hp"

    async def onStart(self, pm, module):
        BaseX = BaseAddress.BaseX(pm, module)
        HealthPointer = Pointer.PlayerHP(pm, BaseX)
        memory.write_bytes(
            pm.process_handle,
            HealthPointer,
            (1).to_bytes(4, "little"),
            4,
        )
