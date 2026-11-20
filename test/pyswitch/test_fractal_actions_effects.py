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
    from lib.pyswitch.clients.fractal import *
    from lib.pyswitch.clients.fractal.actions.effect_bypass import *
    from lib.pyswitch.clients.fractal.actions.effect_channel import *
    from lib.pyswitch.clients.fractal.mappings.effects import *
    from lib.pyswitch.controller.actions import Action, PushButtonAction

    from .mocks_fractal import *


DRIVE_1 = 118
AMP_1 = 58


class TestFractalActionEffectBypass(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_properties(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE, id = 3, use_leds = False)

        self.assertIsInstance(action, PushButtonAction)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.LATCH)
        self.assertEqual(action.id, 3)
        self.assertEqual(action.uses_switch_leds, False)

        action = EFFECT_BYPASS(FractalBlock.DRIVE, mode = PushButtonAction.MOMENTARY)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)

        appl, switch, label = setup_action(action)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.STATUS_DUMP()])

        action.callback.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.STATUS_DUMP()])

    def test_invalid_block(self):
        with self.assertRaises(Exception):
            EFFECT_BYPASS(40)

        with self.assertRaises(Exception):
            EFFECT_BYPASS(-1)

    def test_states(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()
        cb = action.callback

        # No dump
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_EFFECT)
        self.assertEqual(label.text, "Drive 1")
        self.assertEqual(action.state, False)
        self.assertEqual(cb.present, False)

        # Not in the preset
        mapping.value = dump([(AMP_1, False, 0, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "Drive 1")

        # Engaged
        mapping.value = dump([(AMP_1, False, 0, 4), (DRIVE_1, False, 2, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(action.state, True)
        self.assertEqual(cb.present, True)
        self.assertEqual(cb.engaged, True)
        self.assertEqual(cb.channel, 2)

        # Bypassed
        mapping.value = dump([(DRIVE_1, True, 1, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(action.state, False)
        self.assertEqual(cb.channel, 1)

    def test_push(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        mapping.value = dump([(DRIVE_1, False, 0, 4)])
        action.update_displays()

        # Bypass
        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_BLOCK_BYPASS(DRIVE_1), "value": 0 }])
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Local feedback: the next dump is skipped, the state is kept
        self.assertEqual(mapping.parse(sysex(0x13, dump([(DRIVE_1, False, 0, 4)]))), True)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Next dump is evaluated
        self.assertEqual(mapping.parse(sysex(0x13, dump([(DRIVE_1, True, 0, 4)]))), True)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Engage
        action.push()
        self.assertEqual(appl.client.set_calls[-1], { "mapping": MAPPING_BLOCK_BYPASS(DRIVE_1), "value": 1 })
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_push_absent(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE)
        appl, switch, label = setup_action(action)

        FractalMappings.STATUS_DUMP().value = dump([(AMP_1, False, 0, 4)])

        action.push()
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(action.state, False)
        self.assertEqual(switch.brightnesses[0], LED_OFF)

    def test_labels(self):
        def test(label_type, expected, block = FractalBlock.DRIVE, instance = 1):
            action = EFFECT_BYPASS(block, instance = instance, label = label_type)
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(label.text, expected)

        FractalMappings.STATUS_DUMP().value = dump([(DRIVE_1, False, 1, 4)])

        test(FractalLabel.LONG_NAME, "Drive 1")
        test(FractalLabel.SHORT_NAME, "DRV1")
        test(FractalLabel.SHORT_NAME_CHANNEL, "DRV1 B")
        test(FractalLabel.LONG_NAME_CHANNEL, "Drive 1 B")
        test(FractalLabel.CURRENT_CHANNEL, "DRV1 B")
        test(FractalLabel.LONG_NAME, "Delay 2", block = FractalBlock.DELAY, instance = 2)
        test(FractalLabel.SHORT_NAME_CHANNEL, "DLY2", block = FractalBlock.DELAY, instance = 2)
        test(FractalLabel.LONG_NAME_CHANNEL, "Delay 2", block = FractalBlock.DELAY, instance = 2)

    def test_push_callback(self):
        # The bypass function is triggered by the PushButtonAction state, not by push()
        action = EFFECT_BYPASS(FractalBlock.DRIVE)
        appl, switch, label = setup_action(action)

        FractalMappings.STATUS_DUMP().value = dump([(DRIVE_1, False, 0, 4)])
        action.callback.push()
        action.callback.release()
        self.assertEqual(appl.client.set_calls, [])

    def test_destination_label_bypass(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE, label = FractalLabel.DESTINATION_CHANNEL)
        appl, switch, label = setup_action(action)

        FractalMappings.STATUS_DUMP().value = dump([(DRIVE_1, False, 0, 4)])
        action.update_displays()
        self.assertEqual(label.text, "DRV1")

    def test_text_and_color(self):
        action = EFFECT_BYPASS(FractalBlock.DRIVE, color = (1, 2, 3), text = "Boost")
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "Boost")
        self.assertEqual(switch.colors[0], (1, 2, 3))

    def test_special_blocks(self):
        action = EFFECT_BYPASS(FractalBlock.MULTIPLEXER, instance = 2, label = FractalLabel.SHORT_NAME_CHANNEL)
        appl, switch, label = setup_action(action)

        FractalMappings.STATUS_DUMP().value = dump([(192, False, 5, 6)])
        action.update_displays()
        self.assertEqual(label.text, "MUX2 F")
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)


###############################################################################################################


class TestFractalActionEffectChannel(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_select(self):
        action = EFFECT_CHANNEL_SELECT(FractalBlock.AMP, FractalChannel.B)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        self.assertIsInstance(action, Action)

        # Absent (the label shows the switch's channel)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "AMP1 B")

        action.push()
        self.assertEqual(appl.client.set_calls, [])

        # Other channel
        mapping.value = dump([(AMP_1, False, 0, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "AMP1 B")

        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_BLOCK_CHANNEL(AMP_1), "value": 1 }])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "AMP1 B")

        # 2nd press without function
        action.push()
        self.assertEqual(len(appl.client.set_calls), 1)

        # Bypassed: off
        mapping.value = dump([(AMP_1, True, 1, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

    def test_select_labels(self):
        def test(label_type, expected):
            action = EFFECT_CHANNEL_SELECT(FractalBlock.AMP, FractalChannel.C, label = label_type)
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(label.text, expected)

        FractalMappings.STATUS_DUMP().value = dump([(AMP_1, False, 1, 4)])

        test(FractalLabel.SHORT_NAME_CHANNEL, "AMP1 C")
        test(FractalLabel.LONG_NAME_CHANNEL, "Amp 1 C")
        test(FractalLabel.CURRENT_CHANNEL, "AMP1 B")
        test(FractalLabel.DESTINATION_CHANNEL, "AMP1 C")

    def test_select_smart_bypass(self):
        action = EFFECT_CHANNEL_SELECT(FractalBlock.AMP, FractalChannel.B, second_press = FractalSecondPress.SMART_BYPASS)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        mapping.value = dump([(AMP_1, False, 1, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_BLOCK_BYPASS(AMP_1), "value": 0 }])
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1], { "mapping": MAPPING_BLOCK_BYPASS(AMP_1), "value": 1 })
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Other channel active
        mapping.value = dump([(AMP_1, False, 3, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_select_previous_channel(self):
        action = EFFECT_CHANNEL_SELECT(FractalBlock.AMP, FractalChannel.B, second_press = FractalSecondPress.PREVIOUS_CHANNEL)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        # No previous yet
        mapping.value = dump([(AMP_1, False, 1, 4)])
        action.push()
        self.assertEqual(appl.client.set_calls, [])

        mapping.value = dump([(AMP_1, False, 3, 4)])
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 1)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 3)
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_toggle(self):
        action = EFFECT_CHANNEL_TOGGLE(FractalBlock.DRIVE, FractalChannel.A, FractalChannel.C)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "DRV1 A/C")

        mapping.value = dump([(DRIVE_1, False, 1, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "DRV1 [A]C")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 2)
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "DRV1 A[C]")

    def test_toggle_destination(self):
        action = EFFECT_CHANNEL_TOGGLE(FractalBlock.DRIVE, FractalChannel.A, FractalChannel.C, label = FractalLabel.DESTINATION_CHANNEL)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "DRV1")

        FractalMappings.STATUS_DUMP().value = dump([(DRIVE_1, False, 0, 4)])
        action.update_displays()
        self.assertEqual(label.text, "DRV1 C")

    def test_inc_dec(self):
        action = EFFECT_CHANNEL_INC_DEC(FractalBlock.DRIVE)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "DRV1 +1")

        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [])

        mapping.value = dump([(DRIVE_1, False, 2, 4)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 3)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Wrap (4 channels from the dump)
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)

    def test_inc_dec_limits(self):
        action = EFFECT_CHANNEL_INC_DEC(FractalBlock.DRIVE, step = -1, wrap = False, lower_limit = FractalChannel.B, upper_limit = FractalChannel.C, label = FractalLabel.DESTINATION_CHANNEL)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.STATUS_DUMP()

        mapping.value = dump([(DRIVE_1, False, 2, 4)])
        action.update_displays()
        self.assertEqual(label.text, "DRV1 B")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 1)

        # Limit reached: no change
        action.push()
        self.assertEqual(len(appl.client.set_calls), 1)

        action = EFFECT_CHANNEL_INC_DEC(FractalBlock.DRIVE, step = -2)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "DRV1 -2")
