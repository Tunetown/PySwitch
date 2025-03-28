import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC(),
    "usb_hid": MockUsbHid(),
    "adafruit_hid.keyboard": MockUsbHidKeyboard,
    "adafruit_hid.keycode": MockUsbHidKeycode,
}):
    from adafruit_hid.keycode import Keycode

    from lib.pyswitch.clients.local.actions.hid import *
    from lib.pyswitch.ui.elements import DisplayLabel
    from lib.pyswitch.misc import Updater
    
    from .mocks_appl import *


class MockController2(Updater):
    def __init__(self, inputs = []):
        super().__init__()
        self.inputs = inputs


class MockFootswitch:
    def __init__(self, pixels = [0, 1, 2], actions = []):
        self.pixels = pixels
        self.actions = actions

        self._colors = [(0, 0, 0) for i in pixels]
        self._brightnesses = [0 for i in pixels]

    @property
    def color(self):
        return self._colors[0]

    @property
    def colors(self):
        return self._colors
    
    @colors.setter
    def colors(self, colors):
        self._colors = colors

    @property
    def brightness(self):
        return self._brightnesses[0]

    @property
    def brightnesses(self):
        return self._brightnesses
    
    @brightnesses.setter
    def brightnesses(self, brightnesses):
        self._brightnesses = brightnesses


######################################################


class TestLocalHidActions(unittest.TestCase):

    def test_without_label(self):
        MockUsbHidKeyboard.reset()

        action = HID_KEYBOARD(
            keycodes = Keycode.A,
            color = (8, 9, 2),
            led_brightness = 0.5
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController2(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        # Trigger
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4, 4])


    def test_list_of_codes(self):
        MockUsbHidKeyboard.reset()

        action = HID_KEYBOARD(
            keycodes = [Keycode.A, Keycode.C, Keycode.B],
            color = (8, 9, 2),
            led_brightness = 0.5
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController2(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        # Trigger
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4, 6, 5])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4, 6, 5, 4, 6, 5])


    def test_tuple_of_codes(self):
        MockUsbHidKeyboard.reset()

        action = HID_KEYBOARD(
            keycodes = (Keycode.A, Keycode.C, Keycode.B),
            color = (8, 9, 2),
            led_brightness = 0.5
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController2(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        # Trigger
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4, 6, 5])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(keyboard.send_calls, [4, 6, 5, 4, 6, 5])


    def test_with_label(self):
        MockUsbHidKeyboard.reset()
        
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = HID_KEYBOARD(
            display = display,
            keycodes = Keycode.A,
            color = (8, 9, 2),
            text = "hey",
            led_brightness = 0.5
        )

        switch = MockFootswitch(
            actions = [
                action,
            ]
        )
        
        appl = MockController2(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.text, "hey")
        self.assertEqual(display.back_color, (8, 9, 2))


