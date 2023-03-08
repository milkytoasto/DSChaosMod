from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, ShellCode
from pymem import memory


class WarpToBonfire(DSREffect):
    name = "Warp to Bonfire"
    config_alias = "warp_to_bonfire"

    async def _on_start(self):
        BaseB = BaseAddress.BaseB(self.pm, self.module)
        HomewardCall = BaseAddress.HomewardCall(self.pm, self.module)

        shellcode = ShellCode.WarpShellcode(BaseB, HomewardCall)

        BonFireTP = self.pm.allocate(128)
        memory.write_bytes(
            self.pm.process_handle, BonFireTP, bytes(shellcode), len(shellcode)
        )
        self.pm.start_thread(BonFireTP)
        self.pm.free(BonFireTP)
