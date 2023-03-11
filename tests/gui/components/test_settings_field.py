import unittest
import tkinter as tk
from TwitchVotingServer.gui.components.settings_tab import SettingsField 

class TestSettingsField(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    def test_get_default_value(self):
        sf = SettingsField(self.root, "Label")
        self.assertEqual(sf.get(), "")

    def test_get_custom_value(self):
        sf = SettingsField(self.root, "Label", "Value")
        self.assertEqual(sf.get(), "Value")

if __name__ == "__main__":
    unittest.main()