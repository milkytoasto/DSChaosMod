import tkinter as tk
import tkinter.ttk as ttk


class SettingsTab(ttk.Frame):
    def __init__(self, parent, config_handler, voting_handler):
        super().__init__(parent)
        self._voting_handler = voting_handler
        self._config_handler = config_handler
        self._settings_field_values = {}
        self._init_settings_tab()

    def _init_settings_tab(self):
        self.twitch_settings = TwitchSettings(self, self._config_handler)
        self.voting_settings = VotingSettings(self, self._config_handler)

        self.save_button = ttk.Button(
            self, text="Save Settings", command=self._save_settings
        )

        self.twitch_settings.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.voting_settings.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        self.save_button.grid(row=1, column=1, sticky="se", padx=8, pady=8)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def _save_settings(self):
        self.save_button["state"] = "disabled"
        self.twitch_settings.save()
        self.voting_settings.save()
        self._voting_handler.load_config()
        self.save_button["state"] = "normal"


class VotingSettings(ttk.Frame):
    def __init__(self, parent, config_handler):
        super().__init__(parent)
        self.config_handler = config_handler
        self.voting_duration_field = SettingsField(
            self,
            "Voting Duration",
            self.config_handler.get_option("VOTING", "VOTING_DURATION", "60", type=str),
        )
        self.effect_duration_field = SettingsField(
            self,
            "Effect Duration",
            self.config_handler.get_option(
                "VOTING", "EFFECT_DURATION", "120", type=str
            ),
        )

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.voting_duration_field.grid(row=0, column=0, padx=8, pady=8, sticky="ne")
        self.effect_duration_field.grid(row=1, column=0, padx=8, pady=8, sticky="ne")

    def save(self):
        fields = {
            "VOTING": {
                "VOTING_DURATION": self.voting_duration_field,
                "EFFECT_DDURATION": self.effect_duration_field,
            }
        }
        self.config_handler.save_config(fields)


class TwitchSettings(ttk.Frame):
    def __init__(self, parent, config_handler):
        super().__init__(parent)
        self.config_handler = config_handler

        self.channel_field = SettingsField(
            self,
            "Channel",
            self.config_handler.get_option("TWITCH", "CHANNEL", "", type=str),
        )
        self.tmi_token_field = SettingsField(
            self,
            "Oauth Token",
            self.config_handler.get_option("TWITCH", "TMI_TOKEN", "", type=str),
        )

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.channel_field.grid(row=0, column=0, padx=8, pady=8, sticky="ne")
        self.tmi_token_field.grid(row=1, column=0, padx=8, pady=8, sticky="ne")

    def save(self):
        fields = {
            "TWITCH": {"CHANNEL": self.channel_field, "TMI_TOKEN": self.tmi_token_field}
        }
        self.config_handler.save_config(fields)


class SettingsField(ttk.Frame):
    def __init__(self, parent, label_text, value=""):
        super().__init__(parent)
        self.variable = tk.StringVar(self, value=value)
        self.label_text = label_text

        self.label = ttk.Label(self, text=label_text)
        self.field = ttk.Entry(self, textvariable=self.variable)

        self.label.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.field.grid(row=1, column=1, padx=8, pady=8)

    def get(self):
        return self.variable.get()
