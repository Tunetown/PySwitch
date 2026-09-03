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
    from lib.pyswitch.ui.elements import DisplayLabel
    from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.looper import *
    from lib.pyswitch.clients.kemper.mappings.looper import *


class TestKemperActionsLooper(unittest.TestCase):

    def test_looper_rec_play_overdub(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_REC_PLAY_OVERDUB(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_REC_PLAY_OVERDUB())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_looper_stop(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_STOP(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_STOP())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_looper_erase(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_ERASE(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_ERASE())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

        

    def test_looper_cancel(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_CANCEL(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_CANCEL())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

        

    def test_looper_reverse(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_REVERSE(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_REVERSE())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

        

    def test_looper_trigger(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_TRIGGER(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_TRIGGER())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

        

    def test_looper_half_speed(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = LOOPER_HALF_SPEED(
            display = display, 
            text = "foo", 
            color = (2, 3, 4), 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_LOOPER_HALF_SPEED())
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._color, (2, 3, 4))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

