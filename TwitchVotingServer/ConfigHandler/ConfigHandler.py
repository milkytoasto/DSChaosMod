import configparser


class ConfigHandler:
    def __init__(self, config_path):
        self.config_path = config_path

        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.config = config

    def save_config(self, fields):
        for section in fields:
            for option in fields[section]:
                if (value := fields[section][option].get()) is not None:
                    self.config.set(section, option, str(value))

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def get_section(self, section):
        if section in self.config:
            return self.config[section]

    def get_option(self, section, option, default_value, type=str):
        """_summary_

        Args:
            section (string): The section header to pull the option from.
            option (string): The option key value string to pull the value from.
            default_value (any): Default value to return if the option is not found.
            type (_type_, optional): Type of the configuration setting. Defaults to str.

        Returns:
            _type_: _description_
        """
        if self.config.has_option(section, option):
            if type is str:
                return self.config[section][option]
            if type is bool:
                return self.config[section].getboolean(option)
            if type is int:
                return self.config[section].getint(option)
            if type is float:
                return self.config[section].getfloat(option)
        return default_value
