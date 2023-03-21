import tkinter as tk

import toml


class ConfigHandler:
    def __init__(self, config_path):
        self.config_path = config_path

        with open(self.config_path) as f:
            self.config = toml.load(f)

    def save_config(self, fields):
        new_config = self.config.copy()
        for section_name, section_fields in fields.items():
            for field_name, field_value in section_fields.items():
                if isinstance(field_value, tk.BooleanVar):
                    new_config[section_name][field_name] = bool(field_value.get() == 1)
                else:
                    new_config[section_name][field_name] = field_value.get()

        with open(self.config_path, "w") as f:
            toml.dump(new_config, f)

    def get_section(self, section):
        return self.config[section] if section in self.config else None

    def get_option(self, section, option, default_value, type=str):
        if section in self.config and option in self.config[section]:
            return self.config[section][option]
        return default_value

    def get(self, option_name, default_value=None, type=str):
        option_parts = option_name.split(".")
        option_value = self.config
        for part in option_parts:
            if part in option_value:
                option_value = option_value[part]
            else:
                return default_value
        if option_value is None:
            return default_value
        if type == bool:
            return option_value.lower() == "true"
        else:
            return type(option_value)
