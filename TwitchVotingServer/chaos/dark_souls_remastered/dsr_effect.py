from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from chaos.effect import BaseEffect
from pymem import memory


class DSREffect(BaseEffect):
    name = "Dark Souls Remastered Base Effect"
    config_alias = "DSR Base Effect"

    def _is_loading(self):
        BaseA = BaseAddress.BaseA(self.pm, self.module)
        loading_pointer = Pointer.GameState.is_loading(self.pm, BaseA)
        is_loading = memory.read_bool(self.pm.process_handle, loading_pointer)
        return is_loading
