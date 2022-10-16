import asyncio
import random

import psutil
from ConfigHandler.ConfigHandler import ConfigHandler
from pymem import Pymem, process
from pymem.exception import ProcessNotFound

from .DarkSoulsRemastered.Game import DarkSoulsRemastered


class NoProcessFoundError(Exception):
    pass


class ChaosHandler:
    def __init__(self, configHandler):
        self.effect = asyncio.Event()
        self.game = None
        self.sampled_options = None
        self.configHandler = configHandler

    def load_config(self):
        self.available_effects = dict()
        game_sections = self.configHandler.get_section("GAME_CONFIGS")

        for game_name in game_sections:
            gameConfigHandler = ConfigHandler(
                config_path="./config/"
                + self.configHandler.config["GAME_CONFIGS"][game_name]
            )
            self.available_effects[game_name] = dict()

            for section_name in gameConfigHandler.config.sections():
                section = gameConfigHandler.get_section(section_name)

                for effect_name in section:
                    effect_value = gameConfigHandler.config[section_name].getboolean(
                        effect_name
                    )
                    self.available_effects[game_name][effect_name] = effect_value

    def get_options(self):
        if self.game is None:
            return []

        effect_options = []
        game = self.game

        game_alias = game.config_alias.lower()

        if game_alias in self.available_effects:
            game_configs = self.available_effects[game_alias]

            for effect in game.effects:
                effect_alias = effect.config_alias.lower()
                if effect_alias in game_configs and game_configs[effect_alias] == True:
                    effect_options.append(effect)
        else:
            effect_options = game.effects

        self.sampled_options = random.sample(
            effect_options, k=min(3, len(effect_options))
        )
        return self.sampled_options

    def get_existing_options(self):
        if self.sampled_options is not None:
            return self.sampled_options
        return self.get_options()

    async def effect_controller(self):
        while True:
            await self.effect.wait()
            try:
                await self.current_effect.start(self.pm, self.module)
            finally:
                await self.current_effect.stop(self.pm, self.module)
            self.effect.clear()

    def hook(self):
        self.__find_process()

        if self.process_title is None:
            raise NoProcessFoundError(f"No suitable process found.")

        self.load_config()

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
        self.effect.set()

    def __find_process(self):
        self.process_title = None
        for process in psutil.process_iter():
            if process.name() == DarkSoulsRemastered.process_title:
                self.game = DarkSoulsRemastered
                self.process_title = DarkSoulsRemastered.process_title
        return self.process_title
