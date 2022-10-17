from ChaosHandler.DarkSoulsRemastered.DSREffect import DSREffect
from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from pymem import memory


class Blind(DSREffect):
    name = "Blinded"
    config_alias = "blind"

    async def onStart(self, pm, module):
        BaseCAR = BaseAddress.BaseCAR(pm, module)
        DrawDistancePointer = Pointer.DrawDistance(pm, BaseCAR)

        memory.write_float(pm.process_handle, DrawDistancePointer, 1)
        await self.tick(self.seconds, pm, module)

    async def onStop(self, pm, module):
        BaseCAR = BaseAddress.BaseCAR(pm, module)
        DrawDistancePointer = Pointer.DrawDistance(pm, BaseCAR)

        memory.write_float(pm.process_handle, DrawDistancePointer, 3100)
