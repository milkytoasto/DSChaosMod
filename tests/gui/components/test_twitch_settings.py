import os
import unittest
import tempfile
import tkinter as tk
import configparser
from TwitchVotingServer.config_handler.config_handler import ConfigHandler
from TwitchVotingServer.gui.components.settings_tab import SettingsField, TwitchSettings

class TestTwitchSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.config_file = tempfile.NamedTemporaryFile(delete=False)
        self.config_path = self.config_file.name

        config = configparser.ConfigParser()
        config.add_section("TWITCH")
        config.set("TWITCH", "CHANNEL", "mychannel")
        config.set("TWITCH", "TMI_TOKEN", "mytoken")

        with open(self.config_path, "w") as f:
            config.write(f)

        self.config_handler = ConfigHandler(self.config_path)
        self.twitch_settings = TwitchSettings(self.root, self.config_handler)

    def tearDown(self):
        self.config_file.close()
        os.unlink(self.config_path)

    def test_init(self):
        self.assertIsInstance(self.twitch_settings.channel_field, SettingsField)
        self.assertIsInstance(self.twitch_settings.tmi_token_field, SettingsField)

    def test_channel_field(self):
        self.assertEqual(self.twitch_settings.channel_field.label_text, "Channel")
        self.assertEqual(self.twitch_settings.channel_field.get(), "mychannel")

    def test_tmi_token_field(self):
        self.assertEqual(self.twitch_settings.tmi_token_field.label_text, "Oauth Token")
        self.assertEqual(self.twitch_settings.tmi_token_field.get(), "mytoken")

    def test_channel_field_set_value(self):
        self.twitch_settings.channel_field.variable.set("newchannel")
        self.assertEqual(self.twitch_settings.channel_field.variable.get(), "newchannel")

    def test_tmi_token_field_set_value(self):
        self.twitch_settings.tmi_token_field.variable.set("newtoken")
        self.assertEqual(self.twitch_settings.tmi_token_field.variable.get(), "newtoken")

    def test_save(self):
        channel_var = tk.StringVar(value="newchannel")
        self.twitch_settings.channel_field.variable = channel_var

        tmi_token_var = tk.StringVar(value="newtoken")
        self.twitch_settings.tmi_token_field.variable = tmi_token_var

        self.twitch_settings.save()

        expected = configparser.ConfigParser()
        expected["TWITCH"] = {"CHANNEL": "newchannel", "TMI_TOKEN": "newtoken"}

        with open(self.config_path) as f:
            actual = configparser.ConfigParser()
            actual.read_file(f)

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()