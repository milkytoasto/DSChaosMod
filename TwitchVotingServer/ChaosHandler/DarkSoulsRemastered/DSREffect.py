from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class DSREffect(BaseEffect):
    name = "Dark Souls Remastered Base Effect"
    config_alias = "DSR Base Effect"

    def isLoading(self):
        pass
        # return memory.read_bool(
        #     self.pm.process_handle, Pointer.Loading(self.pm, self.module)
        # )
