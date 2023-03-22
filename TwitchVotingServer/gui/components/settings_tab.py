import tkinter as tk
import tkinter.ttk as ttk


class SettingsTab(ttk.Frame):
    def __init__(
        self, parent, config_handler, voting_handler, toggle_theme, toggle_stay_on_top
    ):
        super().__init__(parent)
        self._voting_handler = voting_handler
        self._config_handler = config_handler
        self._toggle_theme = toggle_theme
        self._toggle_stay_on_top = toggle_stay_on_top

        self._settings_field_values = {}
        self._init_settings_tab()

    def _init_settings_tab(self):
        self.twitch_settings = TwitchSettings(self, self._config_handler)
        self.voting_settings = VotingSettings(self, self._config_handler)
        self.app_settings_frame = ttk.Frame(self)
        self.save_button_frame = ttk.Frame(self)
        self.save_button_frame.grid(row=1, column=1, sticky="se", padx=8, pady=8)

        self.save_button = ttk.Button(
            self.save_button_frame, text="Save Settings", command=self._save_settings
        )
        self.save_button.pack(side="right")

        self.unsaved_label = ttk.Label(
            self, text="You have unsaved changes.", foreground="red"
        )

        self.toggle_stay_on_top_button = ttk.Button(
            self.app_settings_frame,
            style="ToggleButton.On.TButton",
            text="Stay On Top",
            command=self.handle_stay_on_top,
        )
        self.toggle_stay_on_top_button.grid(row=0, column=0, sticky="e", padx=8, pady=8)

        self.toggle_theme_button = ttk.Button(
            self.app_settings_frame, text="Toggle Theme", command=self._toggle_theme
        )
        self.toggle_theme_button.grid(row=0, column=1, sticky="e", padx=8, pady=8)

        self.twitch_settings.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.voting_settings.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        self.app_settings_frame.grid(row=1, column=1, sticky="ne", padx=8, pady=8)
        self.save_button_frame.grid(row=2, column=1, sticky="se", padx=8, pady=8)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def handle_stay_on_top(self):
        self._toggle_stay_on_top()
        if self.toggle_stay_on_top_button["style"] == "ToggleButton.On.TButton":
            self.toggle_stay_on_top_button["style"] = "ToggleButton.Off.TButton"
        else:
            self.toggle_stay_on_top_button["style"] = "ToggleButton.On.TButton"

    def _field_changed(self):
        for settings_field in (
            self.twitch_settings.get_fields() + self.voting_settings.get_fields()
        ):
            if settings_field.is_changed():
                self.unsaved_label.place_configure(
                    relx=1.0,
                    rely=1.0,
                    x=-self.save_button.winfo_width()
                    - 16
                    - self.unsaved_label.winfo_reqwidth(),
                    y=-self.save_button_frame.winfo_height(),
                )
                return
        # Hide the label when settings are saved
        self.unsaved_label.place_forget()

    def _save_settings(self):
        self.save_button["state"] = "disabled"
        self.twitch_settings.save()
        self.voting_settings.save()
        self._voting_handler.load_config()
        self.save_button["state"] = "normal"
        self.unsaved_label.place_forget()  # Hide the label when settings are saved


class VotingSettings(ttk.Frame):
    def __init__(self, parent, config_handler):
        super().__init__(parent)
        self.parent = parent
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

    def get_fields(self):
        return [self.voting_duration_field, self.effect_duration_field]

    def _field_changed(self):
        self.parent._field_changed()

    def save(self):
        fields = {
            "VOTING": {
                "VOTING_DURATION": self.voting_duration_field,
                "EFFECT_DURATION": self.effect_duration_field,
            }
        }
        self.voting_duration_field.save()
        self.effect_duration_field.save()
        self.config_handler.save_config(fields)


class TwitchSettings(ttk.Frame):
    def __init__(self, parent, config_handler):
        super().__init__(parent)
        self.parent = parent
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
            show="*",
        )

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.channel_field.grid(row=0, column=0, padx=8, pady=8, sticky="ne")
        self.tmi_token_field.grid(row=1, column=0, padx=8, pady=8, sticky="ne")

    def get_fields(self):
        return [self.channel_field, self.tmi_token_field]

    def _field_changed(self):
        self.parent._field_changed()

    def save(self):
        fields = {
            "TWITCH": {"CHANNEL": self.channel_field, "TMI_TOKEN": self.tmi_token_field}
        }
        self.channel_field.save()
        self.tmi_token_field.save()
        self.config_handler.save_config(fields)


class SettingsField(ttk.Frame):
    def __init__(self, parent, label_text, value="", show=""):
        super().__init__(parent)
        self.parent = parent
        self.variable = tk.StringVar(self, value=value)
        self.label_text = label_text
        self.initial_value = value  # Store the initial value

        self.label = ttk.Label(self, text=label_text)
        self.field = ttk.Entry(self, textvariable=self.variable, show=show)
        self.field.bind("<KeyRelease>", self.on_key_release)

        self.label.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.field.grid(row=1, column=1, padx=8, pady=8)

    def is_changed(self):
        return self.variable.get() != self.initial_value

    def on_key_release(self, event):
        self.parent._field_changed()

    def save(self):
        self.initial_value = self.variable.get()

    def get(self):
        return self.variable.get()
