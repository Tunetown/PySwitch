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
    "gc": MockGC(),
    "usb_hid": MockUsbHid(),
    "adafruit_hid.keyboard": MockUsbHidKeyboard,
    "adafruit_hid.keycode": MockUsbHidKeycode,
}):
    from adafruit_hid.keycode import Keycode

    from lib.pyswitch.clients.local.actions.hid import *
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *

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
        
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        # Trigger
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        self.assertEqual(keyboard.send_calls, [4])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 2)
        keyboard = MockUsbHidKeyboard.keyboards[1]

        self.assertEqual(keyboard.send_calls, [4])


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
        
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        # Trigger
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        self.assertEqual(keyboard.send_calls, [4, 6, 5])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 2)
        keyboard = MockUsbHidKeyboard.keyboards[1]

        self.assertEqual(keyboard.send_calls, [4, 6, 5])


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
        
        appl = MockController(
            inputs = [
                switch
            ]
        )
        
        action.init(appl, switch)
        action.update_displays()

        self.assertEqual(switch.color, (8, 9, 2))
        self.assertEqual(switch.brightness, 0.5)

        # Trigger
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 1)
        keyboard = MockUsbHidKeyboard.keyboards[0]

        self.assertEqual(keyboard.send_calls, [4, 6, 5])
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 2)
        keyboard = MockUsbHidKeyboard.keyboards[1]

        self.assertEqual(keyboard.send_calls, [4, 6, 5])


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
        
        appl = MockController(
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


    def test_os_error(self):
        MockUsbHidKeyboard.reset()
        MockUsbHidKeyboard.except_on_init = OSError

        action = HID_KEYBOARD(
            keycodes = Keycode.A
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

        # Trigger (must not throw)
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 0)
        
        # Trigger again
        action.push()
        action.release()

        self.assertEqual(len(MockUsbHidKeyboard.keyboards), 0)
        