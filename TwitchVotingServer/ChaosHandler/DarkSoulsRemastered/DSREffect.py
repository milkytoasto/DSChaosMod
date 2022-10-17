from ChaosHandler.DarkSoulsRemastered.Memory import BaseAddress, Pointer
from ChaosHandler.Effect import BaseEffect
from pymem import memory


class DSREffect(BaseEffect):
    name = "Dark Souls Remastered Base Effect"
    config_alias = "DSR Base Effect"

    def isLoading(self):
        return memory.read_bool(
            self.pm.process_handle, Pointer.Loading(self.pm, self.module)
        )

    async def start(self, *args):
        print(self.isLoading())
        await super().start(*args)

    async def tick(self, seconds=None, *args):
        print(self.isLoading())
        await super().tick(seconds, *args)

    async def stop(self, *args):
        print(self.isLoading())
        await super().stop(*args)
