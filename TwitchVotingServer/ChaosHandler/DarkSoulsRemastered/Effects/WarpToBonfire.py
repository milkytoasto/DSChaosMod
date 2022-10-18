from ChaosHandler.DarkSoulsRemastered.DSREffect import DSREffect
from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Shellcode
from pymem import memory


class WarpToBonfire(DSREffect):
    name = "Warp to Bonfire"
    config_alias = "warp_to_bonfire"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HomewardCall = BaseAddress.HomewardCall(pm, module)

        shellcode = Shellcode.warp(BaseB, HomewardCall)

        BonFireTP = pm.allocate(128)
        memory.write_bytes(
            pm.process_handle,
            BonFireTP,
            bytes(shellcode),
            len(shellcode),
        )
        pm.start_thread(BonFireTP)
        pm.free(BonFireTP)
