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

    from lib.pyswitch.clients.kemper.actions.amp import *
    from lib.pyswitch.clients.kemper.actions.effect_state import *
    from lib.pyswitch.clients.kemper.actions.tempo import *
    from lib.pyswitch.clients.kemper.actions.effect_button import *
    from lib.pyswitch.clients.kemper.actions.morph import *
    from lib.pyswitch.clients.kemper.actions.looper import *
    from lib.pyswitch.clients.kemper.actions.rig_volume_boost import *
    from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import *
    from lib.pyswitch.clients.kemper.actions.rig_transpose import *
    from lib.pyswitch.clients.kemper.actions.tempo_bpm import *

    from lib.pyswitch.clients.kemper.mappings.tempo_bpm import *
    from lib.pyswitch.clients.kemper.mappings.tempo import *
    from lib.pyswitch.clients.kemper.mappings.morph import *
    from lib.pyswitch.clients.kemper.mappings.looper import *

    from lib.pyswitch.clients.local.actions.encoder_button import *
    from lib.pyswitch.controller.actions.EncoderAction import EncoderAction
    

class TestKemperActionDefinitions(unittest.TestCase):


    def test_tap_tempo(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = TAP_TEMPO(
            display = display, 
            color = (4, 5, 6), 
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_TAP_TEMPO())
        self.assertEqual(cb._text, "Tap")
        self.assertEqual(cb._color, (4, 5, 6))

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


    def test_morph_button(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_BUTTON(
            display = display, 
            text = "foo",
            id = 67, 
            color = (3, 4, 5),
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_BUTTON())
        self.assertEqual(cb._text, "foo")
        #self.assertEqual(cb._color, (3, 4, 5))
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_morph_button_with_display(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_BUTTON(
            display = display, 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb,
            color = "kemper"
        )

        cb = action.callback
        self.assertIsInstance(cb, KemperMorphCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_BUTTON())
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_morph_display(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_DISPLAY(
            display = display, 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        action.init(appl, None)

        cb = action.callback
        self.assertIsInstance(cb, KemperMorphCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_PEDAL())
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._BinaryParameterCallback__comparison_mode, BinaryParameterCallback.NO_STATE_CHANGE)
        self.assertEqual(cb._led_brightness_off, 0.3)

        self.assertEqual(cb._BinaryParameterCallback__display_dim_factor_off, 1)
        self.assertEqual(cb._KemperMorphCallback__suppress_send, True)
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


    def test_rig_volume_boost(self):
        self._test_rig_volume_boost(False, 0.75, int(16383 * 0.75), int(16383 * 0.5))
        self._test_rig_volume_boost(True, 0.85, int(16383 * 0.85), "auto")

    def _test_rig_volume_boost(self, remember_off_value, boost_volume, exp_value_enable, exp_value_disable):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = RIG_VOLUME_BOOST(
            boost_volume = boost_volume, 
            mode = PushButtonAction.LATCH, 
            remember_off_value = remember_off_value, 
            display = display, 
            color = (4, 5, 6), 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_RIG_VOLUME())
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._value_enable, exp_value_enable)
        self.assertEqual(cb._value_disable, exp_value_disable)
        self.assertEqual(cb._color, (4, 5, 6))

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.LATCH)


    def test_rig_select_and_morph(self):
        display_select = DisplayLabel(layout = {
            "font": "foo"
        })
        display_morph = DisplayLabel(layout = {
            "font": "foo2"
        })

        ecb = MockEnabledCallback()

        action_select, action_morph = RIG_SELECT_AND_MORPH_STATE(
            rig = 1,
            rig_off = 2,
            display = display_select, 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb,     
            #color_callback
            color = (2, 4, 6),
            #text_callback,
            morph_display = display_morph,
            morph_use_leds = False,
            morph_id = 68,
            morph_only_when_enabled = False
        )

        appl = MockController()
        action_select.init(appl, None)
        action_morph.init(appl, None)

        cb_select = action_select.callback
        cb_morph = action_morph.callback

        self.assertIsInstance(cb_select, Callback)
        
        self.assertIsInstance(cb_morph, KemperMorphCallback)
        self.assertEqual(cb_morph.mapping, MAPPING_MORPH_PEDAL())
        self.assertEqual(cb_morph._BinaryParameterCallback__comparison_mode, BinaryParameterCallback.NO_STATE_CHANGE)
        self.assertEqual(cb_morph._led_brightness_off, 0.3)
        self.assertEqual(cb_morph._BinaryParameterCallback__display_dim_factor_off, 1)
        self.assertEqual(cb_morph._KemperMorphCallback__suppress_send, True)
        
        self.assertEqual(action_select.label, display_select)
        self.assertEqual(action_select.id, 67)
        self.assertEqual(action_select.uses_switch_leds, True)
        self.assertEqual(action_select._Action__enable_callback, ecb)

        self.assertEqual(action_morph.label, display_morph)
        self.assertEqual(action_morph.id, 68)
        self.assertEqual(action_morph.uses_switch_leds, False)
        self.assertNotEqual(action_morph._Action__enable_callback, ecb)


    # def test_rig_and_bank_select_and_morph(self):
    #     display_select = DisplayLabel(layout = {
    #         "font": "foo"
    #     })
    #     display_morph = DisplayLabel(layout = {
    #         "font": "foo2"
    #     })

    #     ecb = MockEnabledCallback()

    #     action_select, action_morph = RIG_AND_BANK_SELECT_AND_MORPH_STATE(
    #         rig = 1,
    #         bank = 5, 
    #         rig_off = 2,
    #         bank_off = 9,
    #         display = display_select, 
    #         text = "foo",
    #         id = 67, 
    #         use_leds = True, 
    #         enable_callback = ecb,     
    #         #color_callback
    #         color = (2, 4, 6),
    #         #text_callback,
    #         morph_display = display_morph,
    #         morph_use_leds = False,
    #         morph_id = 68,
    #         morph_only_when_enabled = False
    #     )

    #     appl = MockController()
    #     action_select.init(appl, None)
    #     action_morph.init(appl, None)

    #     cb_select = action_select.callback
    #     cb_morph = action_morph.callback

    #     self.assertIsInstance(cb_select, BinaryParameterCallback)
    #     self.assertEqual(cb_select.mapping, MAPPING_BANK_AND_RIG_SELECT(0))

    #     self.assertIsInstance(cb_morph, KemperMorphCallback)
    #     self.assertEqual(cb_morph.mapping, MAPPING_MORPH_PEDAL())
    #     self.assertEqual(cb_morph._BinaryParameterCallback__comparison_mode, BinaryParameterCallback.NO_STATE_CHANGE)
    #     self.assertEqual(cb_morph._led_brightness_off, 0.3)
    #     self.assertEqual(cb_morph._BinaryParameterCallback__display_dim_factor_off, 1)
    #     self.assertEqual(cb_morph._KemperMorphCallback__suppress_send, True)
        
    #     self.assertEqual(action_select.label, display_select)
    #     self.assertEqual(action_select.id, 67)
    #     self.assertEqual(action_select.uses_switch_leds, True)
    #     self.assertEqual(action_select._Action__enable_callback, ecb)

    #     self.assertEqual(action_morph.label, display_morph)
    #     self.assertEqual(action_morph.id, 68)
    #     self.assertEqual(action_morph.uses_switch_leds, False)
    #     self.assertNotEqual(action_morph._Action__enable_callback, ecb)


########################################################################################


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

    def test_tempo_bpm(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = ENCODER_BPM(
            step_width = 1,
            accept_action = accept,
            cancel_action = cancel,
            preview_display = display,
            preview_blink_color = (3, 4, 5),
            preview_timeout_millis = 345,
            id = 45, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_TEMPO_BPM())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 1)
        self.assertEqual(action._EncoderAction__preselect, True)
        self.assertEqual(action._EncoderAction__preview.label, display)

        appl = MockController()
        action.init(appl)

        switch = MockSwitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        action.process(0)
        action.process(131 * 64)
        action.update()

        self.assertEqual(display.text, "131 bpm")


    def test_rig_transpose(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = ENCODER_RIG_TRANSPOSE(
            accept_action = accept,
            cancel_action = cancel,
            preview_display = display,
            preview_blink_color = (3, 4, 5),
            preview_timeout_millis = 345,
            id = 45, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_RIG_TRANSPOSE())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 1)
        self.assertEqual(action._EncoderAction__preselect, True)
        self.assertEqual(action._EncoderAction__preview.label, display)
        
        appl = MockController()
        action.init(appl)

        switch = MockSwitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        action.process(0)
        action.process(28)
        action.update()

        self.assertEqual(display.text, "Transpose: -36")
        
        action.process(64)
        action.update()

        self.assertEqual(display.text, "Transpose: 0")

        action.process(63)
        action.update()

        self.assertEqual(display.text, "Transpose: -1")

        action.process(65)
        action.update()

        self.assertEqual(display.text, "Transpose: +1")

        action.process(100)
        action.update()

        self.assertEqual(display.text, "Transpose: +36")


    def test_amp_gain(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = AMP_GAIN(
            step_width = 1,
            accept_action = accept,
            cancel_action = cancel,
            preview_display = display,
            preview_blink_color = (3, 4, 5),
            preview_timeout_millis = 345,
            id = 45, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_AMP_GAIN())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 1)
        self.assertEqual(action._EncoderAction__preselect, True)
        self.assertEqual(action._EncoderAction__preview.label, display)
        # self.assertEqual(action._EncoderAction__preview._ValuePreview__blink_color, (3, 4, 5))
        # self.assertEqual(action._EncoderAction__preview._ValuePreview__period.interval, 345)

        appl = MockController()
        action.init(appl)

        switch = MockSwitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        action.process(0)
        action.process(8192)
        action.update()

        self.assertEqual(display.text, "Gain: 5.0")