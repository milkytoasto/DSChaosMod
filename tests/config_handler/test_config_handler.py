import unittest
import tempfile
import os
from TwitchVotingServer.config_handler.config_handler import ConfigHandler
import tkinter as tk
import configparser

class TestConfigHandler(unittest.TestCase):
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
        config.set("TWITCH", "CHANNEL", "")
        config.set("TWITCH", "TMI_TOKEN", "")

        with open(self.config_path, "w") as f:
            config.write(f)

        self.config_handler = ConfigHandler(self.config_path)

    def tearDown(self):
        self.config_file.close()
        os.unlink(self.config_path)

    def test_save_config(self):
        channel_var = tk.StringVar(value="mychannel")
        tmi_token_var = tk.StringVar(value="mytoken")

        fields = {
            "TWITCH": {
                "CHANNEL": channel_var,
                "TMI_TOKEN": tmi_token_var,
            },
        }

        self.config_handler.save_config(fields)

        expected = configparser.ConfigParser()
        expected["TWITCH"] = {"CHANNEL": "mychannel", "TMI_TOKEN": "mytoken"}

        with open(self.config_path) as f:
            actual = configparser.ConfigParser()
            actual.read_file(f)

        self.assertEqual(actual, expected)

    def test_get_section(self):
        section = self.config_handler.get_section("TWITCH")
        self.assertEqual(dict(section), {"channel": "", "tmi_token": ""})

        section = self.config_handler.get_section("INVALID")
        self.assertIsNone(section)

    def test_get_option(self):
        value = self.config_handler.get_option("TWITCH", "CHANNEL", "default")
        self.assertEqual(value, "")

        value = self.config_handler.get_option("TWITCH", "INVALID", "default")
        self.assertEqual(value, "default")

if __name__ == "__main__":
    unittest.main()