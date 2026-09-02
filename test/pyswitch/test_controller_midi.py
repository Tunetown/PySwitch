import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from lib.pyswitch.controller.controller import Controller


class TestControllerMidi(unittest.TestCase):

    def test_clear_buffers(self):
        self._test_clear_buffers(False, 0)
        self._test_clear_buffers(False, 3)
        self._test_clear_buffers(False, 7)

        self._test_clear_buffers(True, 0)
        self._test_clear_buffers(True, 1)
        self._test_clear_buffers(True, 100)


    def _test_clear_buffers(self, do_it, num_msgs):
        midi = MockMidiController()

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = midi,
            config = {
                "clearBuffers": do_it
            },
            inputs = [
                {
                    "assignment": {
                        "model":  MockSwitch()
                    }
                }
            ]
        )

        for i in range(num_msgs):
            midi.next_receive_messages.append(
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x03, 0x04]
                # )
            )            

        appl.init()

        self.assertEqual(len(midi.next_receive_messages), 0 if do_it else num_msgs)



