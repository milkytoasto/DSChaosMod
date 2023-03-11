import os
import unittest
import tempfile
import tkinter as tk
import configparser
from TwitchVotingServer.config_handler.config_handler import ConfigHandler
from TwitchVotingServer.gui.components.settings_tab import SettingsField, VotingSettings

class TestVotingSettings(unittest.TestCase):
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
        config.add_section("VOTING")
        config.set("VOTING", "VOTING_DURATION", "60")
        config.set("VOTING", "EFFECT_DURATION", "120")

        with open(self.config_path, "w") as f:
            config.write(f)

        self.config_handler = ConfigHandler(self.config_path)
        self.voting_settings = VotingSettings(self.root, self.config_handler)

    def tearDown(self):
        self.config_file.close()
        os.unlink(self.config_path)

    def test_init(self):
        self.assertIsInstance(self.voting_settings.voting_duration_field, SettingsField)
        self.assertIsInstance(self.voting_settings.effect_duration_field, SettingsField)

    def test_voting_duration_field(self):
        self.assertEqual(
            self.voting_settings.voting_duration_field.label_text, "Voting Duration"
        )
        self.assertEqual(self.voting_settings.voting_duration_field.get(), "60")

    def test_effect_duration_field(self):
        self.assertEqual(
            self.voting_settings.effect_duration_field.label_text, "Effect Duration"
        )
        self.assertEqual(self.voting_settings.effect_duration_field.get(), "120")

    def test_voting_duration_field_set_value(self):
        self.voting_settings.voting_duration_field.variable.set("30")
        self.assertEqual(self.voting_settings.voting_duration_field.variable.get(), "30")

    def test_effect_duration_field_set_value(self):
        self.voting_settings.effect_duration_field.variable.set("60")
        self.assertEqual(self.voting_settings.effect_duration_field.variable.get(), "60")

    def test_save(self):
        voting_duration_var = tk.StringVar(value="30")
        self.voting_settings.voting_duration_field.variable = voting_duration_var

        effect_duration_var = tk.StringVar(value="60")
        self.voting_settings.effect_duration_field.variable = effect_duration_var

        self.voting_settings.save()

        expected = configparser.ConfigParser()
        expected["VOTING"] = {"VOTING_DURATION": 30, "EFFECT_DURATION": 60}

        with open(self.config_path) as f:
            actual = configparser.ConfigParser()
            actual.read_file(f)

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
