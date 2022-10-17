from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, ShellCode
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class WarpToBonfire(BaseEffect):
    name = "Warp to Bonfire"
    config_alias = "warp_to_bonfire"

    async def onStart(self, pm, module):
        BaseB = BaseAddress.BaseB(pm, module)
        HomewardCall = BaseAddress.HomewardCall(pm, module)

        shellcode = ShellCode.WarpShellcode(BaseB, HomewardCall)

        BonFireTP = pm.allocate(128)
        memory.write_bytes(
            pm.process_handle, BonFireTP, bytes(shellcode), len(shellcode)
        )
        pm.start_thread(BonFireTP)
        pm.free(BonFireTP)
