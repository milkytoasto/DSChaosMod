import asyncio
import logging
import random

import psutil
from ConfigHandler.ConfigHandler import ConfigHandler
from pymem import Pymem, process
from pymem.exception import ProcessNotFound

from .DarkSoulsRemastered.Game import DarkSoulsRemastered


class NoProcessFoundError(Exception):
    pass


class ChaosHandler:
    def __init__(self, config_handler):
        self.effect = asyncio.Event()
        self.game = None
        self.sampled_options = None
        self.config_handler = config_handler
        self.debug_logger = logging.getLogger("debug")

    def load_config(self):
        self.available_effects = dict()
        game_sections = self.config_handler.get_section("GAME_CONFIGS")

        for game_name in game_sections:
            game_config_handler = ConfigHandler(
                config_path="./config/"
                + self.config_handler.config["GAME_CONFIGS"][game_name]
            )
            self.available_effects[game_name] = dict()

            for section_name in game_config_handler.config.sections():
                section = game_config_handler.get_section(section_name)

                for effect_name in section:
                    effect_value = game_config_handler.config[
                        section_name
                    ].getboolean(effect_name)
                    self.available_effects[game_name][
                        effect_name
                    ] = effect_value

    def get_options(self):
        """Selects a random sample from the list of available effects
        for the current game, and returns the result.

        Only grabs effects that are enabled in the configuration settings.

        Returns:
            list: Random sample of available effects to pull from.
        """
        if self.game is None:
            return []

        effect_options = []
        game = self.game

        game_alias = game.config_alias.lower()
        if game_alias in self.available_effects:
            game_configs = self.available_effects[game_alias]

            for effect in game.effects:
                effect_alias = effect.config_alias.lower()
                if (
                    effect_alias in game_configs
                    and game_configs[effect_alias] == True
                ):
                    effect_options.append(effect)
        else:
            effect_options = game.effects

        self.sampled_options = random.sample(
            effect_options, k=min(3, len(effect_options))
        )
        return self.sampled_options

    def get_existing_options(self):
        """Returns the pre-existing sampled list of effects.

        Returns:
            list: Random sample of available effects instantiated by get_options
        """
        if self.sampled_options is not None:
            return self.sampled_options
        return self.get_options()

    async def effect_controller(self):
        """Task for handling effect logic."""
        while True:
            await self.effect.wait()
            try:
                self.debug_logger.info(
                    f"ChaosHandler: Triggering the {self.current_effect.name} effect."
                )
                await self.current_effect.start(self.pm, self.module)
            except:
                self.debug_logger.error(
                    f"ChaosHandler: Ran into an error while starting the {self.current_effect.name} effect."
                )
            finally:
                self.effect.clear()
                try:
                    self.debug_logger.info(
                        f"ChaosHandler: Stopping the {self.current_effect.name} effect."
                    )
                    await self.current_effect.stop(self.pm, self.module)
                except:
                    self.debug_logger.error(
                        f"ChaosHandler: Ran into an error while stopping the {self.current_effect.name} effect."
                    )
                    return

    def hook(self):
        """Hooks into a game using pymem."""
        self.__find_process()

        if self.process_title is None:
            raise NoProcessFoundError(f"No suitable process found.")

        self.load_config()

        try:
            pm = Pymem(self.process_title)
        except ProcessNotFound:
            raise NoProcessFoundError(
                f"Process {self.process_title} not found"
            )

        self.pm = pm
        self.module = process.module_from_name(
            self.pm.process_handle, self.process_title
        )

    def trigger_effect(self, effect, seconds):
        """Triggers the effect passed in for the given duration of seconds.

        Args:
            effect (Effect): Effect to trigger.
            seconds (int): Duration of the effect.

        Returns:
            effect: A reference to the instantiated effect
        """
        self.current_effect = effect(
            seconds=seconds, pm=self.pm, module=self.module
        )
        self.effect.set()
        return self.current_effect

    def __find_process(self):
        """Helper method for finding a currently running process from
        a list of processes.

        Returns:
            string: Title of the process discovered. None if not found.
        """
        self.process_title = None
        for process in psutil.process_iter():
            if process.name() == DarkSoulsRemastered.process_title:
                self.game = DarkSoulsRemastered
                self.process_title = DarkSoulsRemastered.process_title
                return self.process_title
        return self.process_title
