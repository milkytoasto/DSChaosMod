from chaos.dark_souls_remastered.dsr_effect import DSREffect
from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from pymem import memory


class OneHP(DSREffect):
    name = "1 HP"
    config_alias = "one_hp"

    async def _on_start(self):
        BaseX = BaseAddress.BaseX(self.pm, self.module)
        player_hp_pointer = Pointer.Player.Stat.hp(self.pm, BaseX)
        memory.write_bytes(
            self.pm.process_handle, player_hp_pointer, (1).to_bytes(4, "little"), 4
        )
