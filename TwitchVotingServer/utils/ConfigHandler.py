class ConfigHandler:
    def __init__(self, config):
        self.config = config

    def get_option(self, section, option, default_value, type=str):
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
