class ConfigHandler:
    def __init__(self, config):
        self.config = config

    def save_config(self, fields):
        for section in fields:
            for option in fields[section]:
                value = fields[section][option].get()
                if value:
                    self.config.set(section, option, value)

        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

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

    def get_channel(self):
        return self.get_option("TWITCH", "CHANNEL", "", type=str)

    def get_token(self):
        return self.get_option("TWITCH", "TMI_TOKEN", "", type=str)
