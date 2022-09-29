import random

import psutil
from pymem import Pymem, process
from pymem.exception import ProcessNotFound

from .DarkSoulsRemastered.Effects import WarpToBonfire
from .utils.ProcessTitles import ProcessTitles


class NoProcessFoundError(Exception):
    pass


class Effects:
    WarpToBonfire: WarpToBonfire


class ChaosHandler:
    def __init_(self):
        pass

    def get_options(self):
        effect_options = {
            "Warp To Bonfire": WarpToBonfire,
            "Warp To Bonfire 2": WarpToBonfire,
            "Warp To Bonfire 3": WarpToBonfire,
            "Warp To Bonfire 4": WarpToBonfire,
        }
        self.sampled_options = {
            key: effect_options[key]
            for key in random.sample(effect_options.keys(), k=3)
        }
        print(self.sampled_options)
        return self.sampled_options

    def hook(self):
        self.__find_process()

        if self.process_title is None:
            raise NoProcessFoundError

        try:
            pm = Pymem(self.process_title)
        except ProcessNotFound:
            raise NoProcessFoundError(f"Process {self.process_title} not found")

        self.pm = pm
        self.module = process.module_from_name(
            self.pm.process_handle, self.process_title
        )

    async def trigger_effect(self, seconds=60, effect=WarpToBonfire):
        self.current_effect = effect
        effect.start(self.pm, self.module)
        self.current_effect.stop(self.pm, self.module)

    def __find_process(self):
        self.process_title = None
        for process in psutil.process_iter():
            if process.name() == ProcessTitles.DSR:
                self.process_title = ProcessTitles.DSR
        return self.process_title
