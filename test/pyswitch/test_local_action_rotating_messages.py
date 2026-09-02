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
    from lib.pyswitch.clients.local.actions.rotate import *
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *

######################################################


class TestLocalRotatingMessages(unittest.TestCase):

    def test_minimal(self):
        action = ROTATING_MESSAGES(
            messages = [
                [1, 3, 5]
            ]
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

        self.assertEqual(switch.color, (0, 0, 0))
        self.assertEqual(switch.brightness, 0)

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(list(appl.client.midi.messages_sent[0]), [1, 3, 5])

        action.release()

        self.assertEqual(switch.color, (0, 0, 0))
        self.assertEqual(switch.brightness, 0)

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(list(appl.client.midi.messages_sent[1]), [1, 3, 5])

        action.release()

        self.assertEqual(switch.color, (0, 0, 0))
        self.assertEqual(switch.brightness, 0)

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 3)
        self.assertEqual(list(appl.client.midi.messages_sent[2]), [1, 3, 5])

        action.release()

        self.assertEqual(switch.color, (0, 0, 0))
        self.assertEqual(switch.brightness, 0)
        
        
    def test_single(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = ROTATING_MESSAGES(
            messages = [
                [1, 3, 5],
                [2, 4, 6],
                [2, 4, 8]
            ],
            messages_release = [
                [23, 5],
                [233],
                [3, 4, 6, 7]
            ],
            led_colors = [
                (8, 9, 2),
                (4, 6, 9)
            ],
            led_brightness = 0.5,
            display_colors = [
                (3, 6, 8),
                (9, 8, 6),
                (3, 5, 7)
            ],            
            texts = [
                "foo2",
                "bar",
                "etc"
            ],
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
        self.assertEqual(display.back_color, (3, 6, 8))

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(list(appl.client.midi.messages_sent[0]), [1, 3, 5])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(list(appl.client.midi.messages_sent[1]), [23, 5])

        self.assertEqual(switch.color, (4, 6, 9))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "bar")
        self.assertEqual(display.back_color, (9, 8, 6))

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 3)
        self.assertEqual(list(appl.client.midi.messages_sent[2]), [2, 4, 6])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 4)
        self.assertEqual(list(appl.client.midi.messages_sent[3]), [233])

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "etc")
        self.assertEqual(display.back_color, (3, 5, 7))

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 5)
        self.assertEqual(list(appl.client.midi.messages_sent[4]), [2, 4, 8])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 6)
        self.assertEqual(list(appl.client.midi.messages_sent[5]), [3, 4, 6, 7])

        self.assertEqual(switch.color, (4, 6, 9))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))

        # Trigger
        action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 7)
        self.assertEqual(list(appl.client.midi.messages_sent[6]), [1, 3, 5])

        action.release()

        self.assertEqual(len(appl.client.midi.messages_sent), 8)
        self.assertEqual(list(appl.client.midi.messages_sent[7]), [23, 5])

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "bar")
        self.assertEqual(display.back_color, (9, 8, 6))


    def test_multiple_leds(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        actions = ROTATING_MESSAGES(
            messages = [
                [1, 3, 5]
            ],
            led_colors = [
                [
                    (8, 9, 2),
                    (4, 6, 9),
                    (2, 4, 6),
                ],
                [
                    (8, 9, 3),
                    (4, 6, 2),
                    (2, 4, 4),
                ],
                [
                    (8, 9, 6),
                    (4, 6, 1),
                    (2, 4, 2),
                ]
            ],
            led_brightness = 0.5,
            display_colors = [
                (3, 6, 8)
            ],            
            texts = [
                "foo2"
            ],
            display = display,
            num_leds = 3
        )

        switch = MockFootswitch(actions = actions)
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        for action in actions:
            action.init(appl, switch)
            action.update_displays()

        self.assertEqual(switch.colors, [(8, 9, 2), (8, 9, 3), (8, 9, 6)])
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))

        # Trigger
        for action in actions:
            action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(list(appl.client.midi.messages_sent[0]), [1, 3, 5])

        for action in actions:
            action.release()

        self.assertEqual(switch.colors, [(4, 6, 9), (4, 6, 2), (4, 6, 1)])
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))
        
        # Trigger
        for action in actions:
            action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(list(appl.client.midi.messages_sent[1]), [1, 3, 5])

        for action in actions:
            action.release()

        self.assertEqual(switch.colors, [(2, 4, 6), (2, 4, 4), (2, 4, 2)])
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))

        # Trigger
        for action in actions:
            action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 3)
        self.assertEqual(list(appl.client.midi.messages_sent[2]), [1, 3, 5])

        for action in actions:
            action.release()

        self.assertEqual(switch.colors, [(8, 9, 2), (8, 9, 3), (8, 9, 6)])
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))

        # Trigger
        for action in actions:
            action.push()

        self.assertEqual(len(appl.client.midi.messages_sent), 4)
        self.assertEqual(list(appl.client.midi.messages_sent[3]), [1, 3, 5])

        for action in actions:
            action.release()

        self.assertEqual(switch.colors, [(4, 6, 9), (4, 6, 2), (4, 6, 1)])
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "foo2")
        self.assertEqual(display.back_color, (3, 6, 8))