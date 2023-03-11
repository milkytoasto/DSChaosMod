import asyncio
import unittest
from unittest import mock
from TwitchVotingServer.chaos.effect import BaseEffect


class TestBaseEffect(unittest.TestCase):
    def setUp(self):
        self.effect = BaseEffect(seconds=5, pm=None, module=None)

    def test_init(self):
        self.assertFalse(self.effect.running)
        self.assertEqual(self.effect.seconds, 5)
        self.assertEqual(self.effect.remaining_seconds, 5)
        self.assertIsNone(self.effect.pm)
        self.assertIsNone(self.effect.module)

    def test_cancel(self):
        self.effect.running = True
        self.effect.cancel()
        self.assertFalse(self.effect.running)

    @mock.patch.object(BaseEffect, "_is_loading")
    @mock.patch.object(BaseEffect, "_on_start")
    def test_start(self, mock_on_start, mock_is_loading):
        mock_is_loading.return_value = False
        asyncio.run(self.effect.start())
        self.assertTrue(self.effect.running)
        mock_on_start.assert_called_once()

    @mock.patch.object(BaseEffect, "_is_loading")
    @mock.patch.object(BaseEffect, "_on_tick")
    @mock.patch.object(BaseEffect, "_on_stop")
    def test_tick(self, mock_on_stop, mock_on_tick, mock_is_loading):
        mock_is_loading.return_value = False
        self.effect.running = True
        asyncio.run(self.effect.tick(1))
        mock_on_tick.assert_called_once()

    @mock.patch.object(BaseEffect, "_is_loading")
    @mock.patch.object(BaseEffect, "_on_stop")
    def test_stop(self, mock_on_stop, mock_is_loading):
        mock_is_loading.return_value = False
        self.effect.running = True
        asyncio.run(self.effect.stop())
        self.assertFalse(self.effect.running)
        mock_on_stop.assert_called_once()

if __name__ == "__main__":
    unittest.main()
