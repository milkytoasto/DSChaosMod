import asyncio
import random

import psutil
from pymem import Pymem, process
from pymem.exception import ProcessNotFound

from .DarkSoulsRemastered.Game import DarkSoulsRemastered


class NoProcessFoundError(Exception):
    pass


class ChaosHandler:
    def __init__(self):
        self.event = asyncio.Event()
        self.game = None

    def get_options(self):
        if self.game is None:
            return []

        effect_options = self.game.effects
        self.sampled_options = random.sample(effect_options, k=3)
        return self.sampled_options

    async def effect_controller(self):
        while True:
            await self.event.wait()
            try:
                await self.current_effect.start(self.pm, self.module)
            finally:
                await self.current_effect.stop(self.pm, self.module)
            self.event.clear()

    def hook(self):
        self.__find_process()

        if self.process_title is None:
            raise NoProcessFoundError(f"No suitable process found.")

        try:
            pm = Pymem(self.process_title)
        except ProcessNotFound:
            raise NoProcessFoundError(f"Process {self.process_title} not found")

        self.pm = pm
        self.module = process.module_from_name(
            self.pm.process_handle, self.process_title
        )

    def trigger_effect(self, effect):
        self.current_effect = effect
        self.event.set()

    def __find_process(self):
        self.process_title = None
        for process in psutil.process_iter():
            if process.name() == DarkSoulsRemastered.process_title:
                self.game = DarkSoulsRemastered
                self.process_title = DarkSoulsRemastered.process_title
        return self.process_title
