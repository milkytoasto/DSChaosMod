import unittest
from TwitchVotingServer.chaos.dark_souls_remastered.memory.utils import packBytes, bytesToHexString


class TestUtils(unittest.TestCase):
    def test_packBytes(self):
        self.assertEqual(packBytes(0x00414243), b'CBA\x00\x00\x00\x00\x00')

    def test_bytesToHexString(self):
        self.assertEqual(
            bytesToHexString(b'CBA\x00\x00\x00\x00'),
            "\\x43\\x42\\x41\\x00\\x00\\x00\\x00"
        )

if __name__ == "__main__":
    unittest.main()
