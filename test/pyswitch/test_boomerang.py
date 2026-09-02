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
    from lib.pyswitch.colors import Colors, dim_color
    from lib.pyswitch.ui.elements import DisplayLabel
    from lib.pyswitch.clients.boomerang.actions.boomerang import *
    from .mocks_callback import *
    from .mocks_appl import *

    from lib.pyswitch.controller.callbacks import Callback
    from lib.pyswitch.controller.actions import Action


class TestBoomerang(unittest.TestCase):

    def test(self):
        self._test_action(BOOMERANG_PLAY_STOP_ALL, 17, 25, "PlayStp", Colors.GREEN)
        self._test_action(BOOMERANG_SYNC_SERIAL, 43, 65, "SyncSerial", Colors.YELLOW)
        self._test_action(BOOMERANG_MUTE_THRU, 3, 8, "MuteThru", Colors.PURPLE)
        self._test_action(BOOMERANG_PANIC, 11, 40, "PANIC", Colors.RED)
        self._test_action(BOOMERANG_ERASE, 16, 61, "ERASE", Colors.RED)
        self._test_action(BOOMERANG_ERASE_ALL, 28, 35, "ERASEALL", Colors.RED)
        self._test_action(BOOMERANG_STACK, 15, 23, "Stack", Colors.YELLOW)
        self._test_action(BOOMERANG_COPY, 1, 4, "Copy", Colors.BLUE)
        self._test_action(BOOMERANG_FADE, 21, 32, "Fade", Colors.LIGHT_BLUE)
        self._test_action(BOOMERANG_OCTAVE, 2, 49, "Octave", Colors.WHITE)
        self._test_action(BOOMERANG_ONCE, 10, 18, "Once", Colors.LIGHT_GREEN)
        self._test_action(BOOMERANG_REVERSE, 47, 56, "Reverse", Colors.TURQUOISE)


    def _test_action(self, func, pc_1, pc_2, expText, expColor):
        self._test_action_defaults(func, expText, expColor)
        self._test_action_messages(func, pc_1, pc_2, expText, expColor)
        self._test_action_multi_leds(func, pc_1, pc_2, expText, expColor)


    def _test_action_defaults(self, func, expText, expColor):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = func(
            display = display, 
            id = 67,
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, Callback)
        self.assertIsInstance(action, Action)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        action.update_displays()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.3))
        self.assertEqual(switch.brightness, 1)


    def _test_action_messages(self, func, pc_1, pc_2, expText, expColor):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = func(
            display = display
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        action.update_displays()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.3))
        self.assertEqual(switch.brightness, 1)
        
        # Send first time
        action.push()
        action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.02))
        self.assertEqual(switch.brightness, 1)

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(appl.client.midi.messages_sent[0], tuple([207, pc_1]))

        # Send second time
        action.push()
        action.release()
        
        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.3))
        self.assertEqual(switch.brightness, 1)

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(appl.client.midi.messages_sent[1], tuple([207, pc_2]))

        # Send third time
        action.push()
        action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.02))
        self.assertEqual(switch.brightness, 1)

        self.assertEqual(len(appl.client.midi.messages_sent), 3)
        self.assertEqual(appl.client.midi.messages_sent[2], tuple([207, pc_1]))

        # Send fourth time
        action.push()
        action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.color, dim_color(expColor, 0.3))
        self.assertEqual(switch.brightness, 1)

        self.assertEqual(len(appl.client.midi.messages_sent), 4)
        self.assertEqual(appl.client.midi.messages_sent[3], tuple([207, pc_2]))


    def _test_action_multi_leds(self, func, pc_1, pc_2, expText, expColor):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        actions = func(
            display = display,
            num_leds = 3
        )
        self.assertEqual(len(actions), 3)

        appl = MockController()
        switch = MockFootswitch(actions = actions, pixels = [0, 1, 2])
        for action in actions:
            action.init(appl, switch)

        for action in actions:
            action.update_displays()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.colors, [
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.3)
        ])
        self.assertEqual(switch.brightnesses, [1, 1, 1])
        
        # Send first time
        for action in actions:
            action.push()
            action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.colors, [
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.3),
            dim_color(expColor, 0.02)
        ])
        self.assertEqual(switch.brightnesses, [1, 1, 1])

        self.assertEqual(len(appl.client.midi.messages_sent), 1)
        self.assertEqual(appl.client.midi.messages_sent[0], tuple([207, pc_1]))

        # Send second time
        for action in actions:
            action.push()
            action.release()
        
        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.colors, [
            dim_color(expColor, 0.3),
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.02)
        ])
        self.assertEqual(switch.brightnesses, [1, 1, 1])

        self.assertEqual(len(appl.client.midi.messages_sent), 2)
        self.assertEqual(appl.client.midi.messages_sent[1], tuple([207, pc_2]))

        # Send third time
        for action in actions:
            action.push()
            action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.colors, [
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.3)
        ])
        self.assertEqual(switch.brightnesses, [1, 1, 1])

        self.assertEqual(len(appl.client.midi.messages_sent), 3)
        self.assertEqual(appl.client.midi.messages_sent[2], tuple([207, pc_1]))

        # Send fourth time
        for action in actions:
            action.push()
            action.release()

        self.assertEqual(display.back_color, expColor)
        self.assertEqual(display.text, expText)

        self.assertEqual(switch.colors, [
            dim_color(expColor, 0.02),
            dim_color(expColor, 0.3),
            dim_color(expColor, 0.02)
        ])
        self.assertEqual(switch.brightnesses, [1, 1, 1])

        self.assertEqual(len(appl.client.midi.messages_sent), 4)
        self.assertEqual(appl.client.midi.messages_sent[3], tuple([207, pc_2]))


