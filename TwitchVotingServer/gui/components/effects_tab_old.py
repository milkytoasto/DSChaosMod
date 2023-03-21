import os
import tkinter as tk
import tkinter.ttk as ttk

from config_handler.config_handler import ConfigHandler

from .checkbox_collection import (
    CheckboxCollectionStore,
    CheckboxSectionStore,
    CheckboxTreeStore,
)


class EffectsTab(ttk.Frame):
    def __init__(
        self,
        parent,
        config_path,
        config_handler,
        voting_handler,
        save_handler,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        left = ttk.Frame(self)
        right = ttk.Frame(self)

        self._config_path = config_path
        self._config_handler = config_handler
        self._voting_handler = voting_handler
        self._games_store = GamesStore(parent=self, config_handler=config_handler)
        self.selected_game = tk.StringVar()

        self._options_menu = DropdownMenu(
            right,
            options=self._games_store.games,
            command=self._on_game_selected,
            width=50,
        )
        self._options_menu.configure(cursor="hand2")
        self._options_menu.pack(
            side="top", anchor="n", fill="x", expand=True, padx=8, pady=8
        )
        self._save_settings = ttk.Button(
            right,
            text="Save Effects",
            command=lambda: self._save_effects(save_handler),
        ).pack(side="right", anchor="s", padx=8, pady=8)

        left.pack(side="left", fill="y")
        right.pack(side="right", anchor="e", fill="both")

        self._effects_box = EffectsBox(left, self._games_store.effect_store)
        self._effects_box.pack(side="left", fill="y")

    def _on_game_selected(self, game_name):
        self._effects_box.populate_box(game_name)

    def _save_effects(self, save_handler):
        game_configs = self._config_handler.config["GAME_CONFIGS"]
        effect_store = self._games_store.effect_store.to_dict()

        for game, config_file in game_configs.items():
            config_path = os.path.join(self._config_path, f"{config_file}")
            game_config_handler = ConfigHandler(config_path=config_path)
            game_config_handler.save_config(effect_store[game])

        save_handler()


class GamesStore:
    def __init__(self, parent, config_handler):
        self._config_handler = config_handler
        self.effect_store = CheckboxCollectionStore()
        self.parent = parent
        self.games = self._create_games_store()

    def _create_games_store(self):
        games = [key for key in self._config_handler.config["GAME_CONFIGS"]]
        for game_name in games:
            game_store = self._create_game_store(game_name)
            self.effect_store.add(game_name, game_store)
        return games

    def _create_game_store(self, game_name):
        game_store = CheckboxTreeStore(game_name)
        config_path = os.path.join(
            os.path.dirname(self._config_handler.config_path),
            self._config_handler.config["GAME_CONFIGS"][game_name],
        )
        game_config_handler = ConfigHandler(config_path=config_path)

        for section_name in game_config_handler.config:
            section_store = CheckboxSectionStore(section_name)
            section = game_config_handler.get_section(section_name)

            for effect_name in section:
                effect_value = game_config_handler.get(
                    f"{section_name}.{effect_name}.enabled"
                )
                new_var = tk.BooleanVar(self.parent, value=effect_value == "true")
                section_store.option_vars[effect_name] = new_var
            section_store.create_section_var(self.parent)
            game_store.add(section_name, section_store)
        return game_store


class GamesStore:
    def __init__(self, parent, config_handler):
        self._config_handler = config_handler
        self.effect_store = CheckboxCollectionStore()
        self.parent = parent
        self.games = self._create_games_store()

    def _create_games_store(self):
        games = [key for key in self._config_handler.config["GAME_CONFIGS"]]
        for game_name in games:
            game_store = self._create_game_store(game_name)
            self.effect_store.add(game_name, game_store)
        return games

    def _create_game_store(self, game_name):
        game_store = CheckboxTreeStore(game_name)
        config_path = os.path.join(
            os.path.dirname(self._config_handler.config_path),
            self._config_handler.config["GAME_CONFIGS"][game_name],
        )
        game_config_handler = ConfigHandler(config_path=config_path)

        for section_name in game_config_handler.config:
            section_store = CheckboxSectionStore(section_name)
            section = game_config_handler.get_section(section_name)

            for effect_name in section:
                effect_value = game_config_handler.get(
                    f"{section_name}.{effect_name}.enabled"
                )
                new_var = tk.BooleanVar(self.parent, value=effect_value == "true")
                section_store.option_vars[effect_name] = new_var
            section_store.create_section_var(self.parent)
            game_store.add(section_name, section_store)
        return game_store


class EffectsBox(ttk.Frame):
    def __init__(self, parent, effect_store, **kwargs):
        super().__init__(parent, **kwargs)
        self._effect_store = effect_store
        self._effect_box = None

        vsb = ttk.Scrollbar(self, orient="vertical")
        effect_box = tk.Text(
            self, cursor="arrow", width=40, height=20, yscrollcommand=vsb.set
        )
        vsb.config(command=effect_box.yview)
        effect_box.pack(side="left", fill="y")
        vsb.pack(side="left", fill="y", anchor="w")

        effect_box["state"] = "disabled"
        self._effect_box = effect_box

    def populate_box(self, game_name):
        self._effect_box.config(state="normal")
        self._effect_box.delete("1.0", "end")

        game_sections = self._effect_store.trees[game_name].sections
        section_keys = list(game_sections.keys())

        for section_name in section_keys:
            section = game_sections[section_name]
            button = section.create_button(self._effect_box)
            self._effect_box.window_create("end", window=button)
            self._effect_box.insert("end", "\n  ")

            for effect_name, option_var in section.option_vars.items():
                button = ttk.Checkbutton(
                    self._effect_box,
                    cursor="hand2",
                    text=f"{effect_name.upper().replace('_', ' ')}",
                    variable=option_var,
                )
                self._effect_box.insert("end", "  ")
                self._effect_box.window_create("end", window=button)
                self._effect_box.insert("end", "\n  ")

            if section_name != section_keys[-1]:
                self._effect_box.insert("end", "\n")

        self._effect_box.config(state="disabled")


class DropdownMenu(ttk.Frame):
    def __init__(self, parent, options, command=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._selected_option = tk.StringVar()
        self._command = command

        self._options_menu = ttk.Combobox(
            self,
            state="readonly",
            values=options,
            textvariable=self._selected_option,
            width=50,
        )
        self._options_menu.configure(cursor="target")
        self._options_menu.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        self._options_menu.bind("<<ComboboxSelected>>", self._on_option_selected)

    def _on_option_selected(self, event):
        if self._command:
            self._command(self._selected_option.get())
