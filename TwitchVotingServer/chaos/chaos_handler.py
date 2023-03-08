import asyncio
import logging
import os
import random

import psutil
from config_handler.config_handler import ConfigHandler
from pymem import Pymem, process
from pymem.exception import ProcessNotFound

from .dark_souls_remastered.game import DarkSoulsRemastered


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
        """
        Load the available effects for each game based on its configuration file.

        For each game listed in the "GAME_CONFIGS" section of the config file, this method loads the available effects by parsing
        its configuration file and filtering the options based on whether they are set to "True". The resulting dictionary of
        game effects is stored in the `available_effects` attribute, with the game name as the key and the effect dictionary as
        the value.
        """
        self.available_effects = {}

        for game_name, game_config_path in self.config_handler.get_section(
            "GAME_CONFIGS"
        ).items():
            game_effects = {}

            for section in ConfigHandler(
                config_path=os.path.join(
                    os.path.dirname(__file__), f"../config/{game_config_path}"
                )
            ).config.values():
                game_effects.update(
                    {
                        k: v if not isinstance(v, str) or v.lower() != "true" else True
                        for k, v in section.items()
                    }
                )

            self.available_effects[game_name] = game_effects

    def get_options(self):
        """
        Returns a list of randomly sampled effect options for the current game, based on the available game configurations.

        The filtered effect options are randomly sampled up to a maximum of 3 effects, or fewer if there are fewer than 3
        available options. The sampled effects are stored in the `sampled_options` attribute and returned as a list.

        Returns:
            A list of up to 3 randomly sampled effect options for the current game, based on the available game configurations.
        """
        if self.game is None:
            return []

        game_alias = self.game.config_alias.lower()

        if game_alias not in self.available_effects:
            effect_options = self.game.effects
        else:
            game_configs = self.available_effects[game_alias]

            effect_options = [
                effect
                for effect in self.game.effects
                if game_configs.get(effect.config_alias.lower(), False) == True
            ]

        num_effects_to_sample = min(3, len(effect_options))
        self.sampled_options = random.sample(effect_options, k=num_effects_to_sample)

        return self.sampled_options

    def get_existing_options(self):
        """
        Returns a list of existing effect options, either the previously sampled options or a new set of options.
        """
        return self.sampled_options or self.get_options()

    async def effect_controller(self):
        """
        An infinite loop that waits for the `effect` Event to be set, triggers the current effect, and stops it when it's done.

        If there's an error starting or stopping the effect, an error message is logged using the `debug_logger`, and the
        loop continues. If an error occurs during the stopping process, the loop is exited using `return`.
        """
        while True:
            await self.effect.wait()

            try:
                self.debug_logger.info(
                    f"ChaosHandler: Triggering the {self.current_effect.name} effect."
                )
                await self.current_effect.start()
            except Exception as e:
                self.debug_logger.error(
                    f"ChaosHandler: Error starting effect '{self.current_effect.name}': {e}"
                )
            finally:
                self.effect.clear()
                try:
                    self.debug_logger.info(
                        f"ChaosHandler: Stopping the {self.current_effect.name} effect."
                    )
                    await self.current_effect.stop()
                except Exception as e:
                    self.debug_logger.error(
                        f"ChaosHandler: Error stopping effect '{self.current_effect.name}': {e}"
                    )
                    return

    def trigger_effect(self, effect, seconds):
        """Triggers an effect with a given duration.

        Args:
            effect (Effect): The effect to be triggered.
            seconds (int): The duration of the effect in seconds.

        Returns:
            Effect: The currently triggered effect.

        """
        self.current_effect = effect(seconds=seconds, pm=self.pm, module=self.module)
        self.effect.set()
        return self.current_effect

    def hook(self):
        """
        Finds a running game process, loads the game configuration, and sets up the necessary objects for effect triggering.

        Raises:
            NoProcessFoundError: If a suitable game process is not found.

        """
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

    def __find_process(self):
        """Finds the process of the game being played.

        Returns:
            str: The name of the process of the game being played, if found. Otherwise None.

        """
        self.process_title = None
        for process in psutil.process_iter():
            if process.name() == DarkSoulsRemastered.process_title:
                self.game = DarkSoulsRemastered
                self.process_title = DarkSoulsRemastered.process_title
        return self.process_title
