import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.local.actions.custom import *
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *

######################################################


class TestLocalCustomMessage(unittest.TestCase):

    def test(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = CUSTOM_MESSAGE(
            message = [1, 3, 5],
            message_release = [23, 5],
            color = (8, 9, 2),
            led_brightness = 0.5,
            text = "foo2",
            display = display
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (8, 9, 2))

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(list(appl.client.midi.messages_sent[0]), [1, 3, 5])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(list(appl.client.midi.messages_sent[1]), [23, 5])

    def test_minimal(self):
        action = CUSTOM_MESSAGE(
            message = [1, 3, 5]
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (255, 255, 255))
        self.assertEqual(switch.brightness, 0.15)

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(list(appl.client.midi.messages_sent[0]), [1, 3, 5])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)        

        