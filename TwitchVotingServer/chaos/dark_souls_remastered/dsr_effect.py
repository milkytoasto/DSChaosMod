from chaos.dark_souls_remastered.memory import BaseAddress, Pointer
from chaos.effect import BaseEffect
from pymem import memory


class DSREffect(BaseEffect):
    name = "Dark Souls Remastered Base Effect"
    config_alias = "DSR Base Effect"

    def isLoading(self):
        pass
        # return memory.read_bool(
        #     self.pm.process_handle, Pointer.Loading(self.pm, self.module)
        # )
