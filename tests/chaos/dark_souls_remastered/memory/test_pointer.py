import unittest
from unittest.mock import MagicMock
from TwitchVotingServer.chaos.dark_souls_remastered.memory.pointer import _get_pointer


class TestGetPointer(unittest.TestCase):

    def test_no_offsets(self):
        # Test when no offsets are given
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(return_value=0x1234567890)
        result = _get_pointer(pm, 0xabcdef)
        self.assertEqual(result, 0x1234567890)

    def test_with_offsets(self):
        # Test when offsets are given
        """ Explanation of the math:
            pm.read_ulonglong(0xabcdef) returns 0x5555555555.
            pm.read_ulonglong(0x5555555565) returns 0x6666666666.
            pm.read_ulonglong(0x6666666686) returns 0x7777777777.
            The function returns 0x7777777777 + 0x30 = 0x77777777A7.
        """
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(side_effect=[0x5555555555, 0x6666666666, 0x7777777777])
        result = _get_pointer(pm, 0xabcdef, [0x10, 0x20, 0x30])
        self.assertEqual(result, 0x77777777A7)

    def test_invalid_input(self):
        # Test when invalid input values are given
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(side_effect=[Exception('Invalid pointer'), 0x5555555555])
        with self.assertRaises(Exception):
            _get_pointer(pm, 0xabcdef, [0x10, 0x20, 0x30])

    def test_empty_input(self):
        # Test when empty input values are given
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(return_value=0x1234567890)
        result = _get_pointer(pm, 0xabcdef, [])
        self.assertEqual(result, 0x1234567890)

    def test_one_offset(self):
        # Test when only one offset is given
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(return_value=0x5555555555)
        result = _get_pointer(pm, 0xabcdef, [0x10])
        self.assertEqual(result, 0x5555555565)

    def test_invalid_offset(self):
        # Test when an invalid offset value is given
        pm = MagicMock()
        pm.read_ulonglong = MagicMock(return_value=0x5555555555)
        with self.assertRaises(Exception):
            _get_pointer(pm, 0xabcdef, [0x10, 'invalid', 0x30])
