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
    from lib.pyswitch.clients.fractal_II import *
    from lib.pyswitch.clients.fractal_II.actions.preset import *
    from lib.pyswitch.clients.fractal_II.actions.bank import *
    from lib.pyswitch.clients.fractal_II.actions.scene import *
    from lib.pyswitch.clients.fractal_II.actions.effect_bypass import *
    from lib.pyswitch.clients.fractal_II.actions.effect_channel import *
    from lib.pyswitch.clients.fractal_II.actions.tuner import *
    from lib.pyswitch.clients.fractal_II.actions.tap_tempo import *
    from lib.pyswitch.controller.actions import Action, PushButtonAction

    from .mocks_appl import MockPeriodCounter
    from .mocks_fractal_II import *


def set_calls(appl):
    return [(c["mapping"], c["value"]) for c in appl.client.set_calls]

def request_mappings(appl):
    return [c["mapping"] for c in appl.client.request_calls]


class TestFractalIIPreset(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_select_number(self):
        action = PRESET_SELECT(5, label = FractalIILabel.NUMBER, id = 3)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        self.assertIsInstance(action, Action)
        self.assertEqual(action.id, 3)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [preset])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_PRESET)
        self.assertEqual(label.text, "006")

        preset.value = 2
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Select (SysEx, same mapping)
        action.push()
        self.assertEqual(set_calls(appl), [(preset, 5)])
        self.assertEqual(preset.value, 5)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Answer to a request sent before is skipped
        preset.parse(preset_answer(2))
        self.assertEqual(preset.value, 5)

    def test_select_name(self):
        action = PRESET_SELECT(200)
        appl, switch, label = setup_action(action)
        cb = action.callback
        target = cb._FractalIIPresetCallback__target_name

        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(target.target, 200)

        # Target name requested until received
        action.callback.update()
        action.callback.update()
        self.assertEqual(request_mappings(appl).count(target), 2)

        target.parse(name_by_number_answer(200, "Lead"))
        action.update_displays()
        self.assertEqual(label.text, "Lead")

        action.callback.update()
        self.assertEqual(request_mappings(appl).count(target), 2)

    def test_select_p_num_and_previous(self):
        action = PRESET_SELECT(7, label = FractalIILabel.P_NUM, second_press_previous = True)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "P3")

        preset.value = 2
        action.push()
        self.assertEqual(preset.value, 7)

        # Second press: previous preset
        action.push()
        self.assertEqual(set_calls(appl)[-1], (preset, 2))

    def test_select_in_bank(self):
        action = PRESET_SELECT_IN_BANK(2, label = FractalIILabel.NUMBER)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        # No preset: no target
        action.update_displays()
        self.assertEqual(label.text, "")
        action.push()
        self.assertEqual(set_calls(appl), [])

        preset.value = 12
        action.update_displays()
        self.assertEqual(label.text, "012")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(set_calls(appl), [(preset, 11)])

        # Bank selected by a bank function
        FRACTAL_II.selected_bank = 4
        action.callback.update()
        self.assertEqual(label.text, "022")

        # Last (partial) bank: presets 765..767
        action = PRESET_SELECT_IN_BANK(4, label = FractalIILabel.NUMBER)
        appl, switch, label = setup_action(action)
        FRACTAL_II.selected_bank = 153
        action.update_displays()
        self.assertEqual(label.text, "")

    def test_toggle(self):
        action = PRESET_TOGGLE(3, 8)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        preset.value = 1
        action.update_displays()
        self.assertEqual(label.text, "P004/P009")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(label.text, "[P004] P009")
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(label.text, "P004 [P009]")
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(set_calls(appl), [(preset, 3), (preset, 8)])

    def test_toggle_in_bank(self):
        action = PRESET_TOGGLE_IN_BANK(1, 3)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "")

        preset.value = 7
        action.update_displays()
        self.assertEqual(label.text, "P1 [P3]")

        action = PRESET_TOGGLE_IN_BANK(1, 3, label = FractalIILabel.BOTH_NUM)
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "P006 [P008]")

    def test_current_name(self):
        action = PRESET_TOGGLE(3, 8, label = FractalIILabel.CURRENT_NAME)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()
        name = FractalIIMappings.PRESET_NAME()

        # The name is not registered (not polled)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [preset])

        action.callback.update()
        self.assertNotIn(name, request_mappings(appl))

        preset.value = 3
        action.callback.update()
        self.assertIn(name, request_mappings(appl))

        name.parse(name_answer("Clean"))
        action.update_displays()
        self.assertEqual(label.text, "Clean")

    def test_destination_and_current(self):
        preset = FractalIIMappings.PRESET()

        for (lbl, expected_none, expected) in (
            (FractalIILabel.DESTINATION_NUM, "004", "009"),
            (FractalIILabel.CURRENT_NUM, "", "004"),
            (FractalIILabel.ACTION, "Preset +1", "Preset +1")
        ):
            action = PRESET_TOGGLE(3, 8, label = lbl)
            appl, switch, label = setup_action(action)

            preset.value = None
            action.update_displays()
            self.assertEqual(label.text, expected_none)

            preset.value = 3
            action.update_displays()
            self.assertEqual(label.text, expected)

    def test_inc_dec(self):
        action = PRESET_INC_DEC(step = -1, label = FractalIILabel.DESTINATION_NAME)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()
        target = action.callback._FractalIIPresetCallback__target_name

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # No preset: nothing happens
        action.push()
        self.assertEqual(set_calls(appl), [])
        action.release()

        # Wrap to the last preset
        preset.value = 0
        action.update_displays()
        self.assertEqual(target.target, 767)
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(set_calls(appl), [(preset, 767)])

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_inc_dec_limits(self):
        action = PRESET_INC_DEC(step = 2, wrap = False, lower_limit = 10, upper_limit = 20, label = FractalIILabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        preset.value = 19
        action.update_displays()
        self.assertEqual(label.text, "021")

        preset.value = 2
        action.update_displays()
        self.assertEqual(label.text, "011")

    def test_custom(self):
        action = PRESET_SELECT(5, color = (1, 2, 3), text = "Foo")
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(switch.colors[0], (1, 2, 3))
        self.assertEqual(label.text, "Foo")

    def test_no_label(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        action.label = None

        FractalIIMappings.PRESET().value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_reset(self):
        action = PRESET_SELECT(5, label = FractalIILabel.NUMBER)
        appl, switch, label = setup_action(action)

        label.text = "x"
        action.reset()
        self.assertEqual(label.text, "006")



class TestFractalIIBank(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_select_none(self):
        action = BANK_SELECT(3)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_BANK)
        self.assertEqual(label.text, "Bank 3")

        preset.value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Preset load NONE: only the bank is selected
        action.push()
        self.assertEqual(set_calls(appl), [])
        self.assertEqual(FRACTAL_II.selected_bank, 2)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.callback.update()

        # Second press: previous bank
        action = BANK_SELECT(3, second_press_previous = True)
        appl, switch, label = setup_action(action)
        preset.value = 7
        action.update_displays()
        action.push()
        self.assertEqual(FRACTAL_II.selected_bank, 2)
        action.push()
        self.assertEqual(FRACTAL_II.selected_bank, None)

    def test_select_load(self):
        preset = FractalIIMappings.PRESET()

        action = BANK_SELECT(3, preset_load = FractalIIPresetLoad.FIRST)
        appl, switch, label = setup_action(action)
        preset.value = 1
        action.push()
        self.assertEqual(set_calls(appl), [(preset, 10)])

        action = BANK_SELECT(3, preset_load = FractalIIPresetLoad.CURRENT)
        appl, switch, label = setup_action(action)
        preset.value = 3
        action.push()
        self.assertEqual(set_calls(appl), [(preset, 13)])

        # Last bank is partial
        action = BANK_SELECT(154, preset_load = FractalIIPresetLoad.CURRENT)
        appl, switch, label = setup_action(action)
        preset.value = 4
        action.push()
        self.assertEqual(set_calls(appl), [(preset, 767)])

    def test_toggle(self):
        action = BANK_TOGGLE(1, 2)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        preset.value = 20
        action.update_displays()
        self.assertEqual(label.text, "B1/B2")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(label.text, "[B1] B2")
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(label.text, "B1 [B2]")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_inc_dec(self):
        action = BANK_INC_DEC(step = -1, label = FractalIILabel.NUMBER)
        appl, switch, label = setup_action(action)
        preset = FractalIIMappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "")
        action.push()
        action.release()

        preset.value = 2
        action.update_displays()
        self.assertEqual(label.text, "Bank 154")

        action.push()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action = BANK_INC_DEC(label = FractalIILabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "Bank 154")

        action = BANK_INC_DEC()
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "Bank +1")


class TestFractalIIScene(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_invalid(self):
        with self.assertRaises(Exception):
            SCENE_SELECT(0)
        with self.assertRaises(Exception):
            SCENE_SELECT(9)
        with self.assertRaises(Exception):
            SCENE_TOGGLE(1, 9)

    def test_select(self):
        action = SCENE_SELECT(3, second_press_previous = True)
        appl, switch, label = setup_action(action)
        scene = FractalIIMappings.SCENE()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [scene])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_SCENE)
        self.assertEqual(label.text, "Scene 3")

        scene.value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(set_calls(appl), [(scene, 2)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Second press: previous scene
        action.push()
        self.assertEqual(set_calls(appl)[-1], (scene, 0))

        action.release()

    def test_toggle(self):
        action = SCENE_TOGGLE(1, 2)
        appl, switch, label = setup_action(action)
        scene = FractalIIMappings.SCENE()

        scene.value = 5
        action.update_displays()
        self.assertEqual(label.text, "Scene 1/2")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(label.text, "Scene [1] 2")
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(label.text, "Scene 1 [2]")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action = SCENE_TOGGLE(1, 2, label = FractalIILabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "Scene 2")

    def test_inc_dec(self):
        action = SCENE_INC_DEC(step = 1, label = FractalIILabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)
        scene = FractalIIMappings.SCENE()

        action.update_displays()
        self.assertEqual(label.text, "")
        action.push()
        self.assertEqual(set_calls(appl), [])
        action.release()

        scene.value = 7
        action.update_displays()
        self.assertEqual(label.text, "Scene 1")

        action.push()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(set_calls(appl), [(scene, 0)])

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action = SCENE_INC_DEC(step = -1, wrap = False, lower_limit = 2, upper_limit = 4)
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "Scene -1")

        scene.value = 1
        action.push()
        self.assertEqual(set_calls(appl), [(scene, 1)])


class TestFractalIIEffects(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_invalid(self):
        with self.assertRaises(Exception):
            EFFECT_BYPASS(139)
        with self.assertRaises(Exception):
            EFFECT_CHANNEL_SELECT(None)

    def test_defaults(self):
        for action in (EFFECT_BYPASS(), EFFECT_CHANNEL_SELECT(), EFFECT_CHANNEL_TOGGLE()):
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(switch.colors[0], COLOR_EFFECT)

    def test_bypass(self):
        action = EFFECT_BYPASS(FractalIIBlock.DRIVE_1)
        appl, switch, label = setup_action(action)
        states = FractalIIMappings.BLOCK_STATES()
        bypass = FractalIIMappings.BYPASS(FractalIIBlock.DRIVE_1)

        self.assertIsInstance(action, PushButtonAction)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [states])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "Drive 1")

        # Not in the preset: nothing is sent
        states.value = block_states([(FractalIIBlock.AMP_1, True, True)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(set_calls(appl), [])
        self.assertEqual(action.state, False)
        action.release()

        # Bypassed
        states.value = block_states([(FractalIIBlock.AMP_1, True, True), (FractalIIBlock.DRIVE_1, False, True)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(action.state, False)

        # Engage
        action.push()
        self.assertEqual(set_calls(appl), [(bypass, 1)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        action.release()

        # The next answer is skipped (local state shown)
        states.parse(block_states_answer([(FractalIIBlock.DRIVE_1, False, True)]))
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        states.parse(block_states_answer([(FractalIIBlock.DRIVE_1, True, False)]))
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(action.state, True)

        # Bypass
        action.push()
        self.assertEqual(set_calls(appl)[-1], (bypass, 0))
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Push of the callback is not used by the bypass function
        action.callback.push()
        self.assertEqual(len(set_calls(appl)), 2)

        # Offline
        states.value = None
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

    def test_labels(self):
        states = FractalIIMappings.BLOCK_STATES()
        states.value = block_states([(FractalIIBlock.AMP_2, True, False)])

        for (lbl, expected_select, expected_toggle) in (
            (FractalIILabel.LONG_NAME, "Amp 2", "Amp 2"),
            (FractalIILabel.SHORT_NAME, "AMP2", "AMP2"),
            (FractalIILabel.LONG_NAME_CHANNEL, "Amp 2 X", "Amp 2 Y"),
            (FractalIILabel.SHORT_NAME_CHANNEL, "AMP2 X", "AMP2 Y"),
            (FractalIILabel.CURRENT_CHANNEL, "AMP2 Y", "AMP2 Y"),
            (FractalIILabel.BOTH_CHANNELS, "AMP2 X[Y]", "AMP2 X[Y]"),
            (FractalIILabel.DESTINATION_CHANNEL, "AMP2 X", "AMP2 X"),
        ):
            action = EFFECT_CHANNEL_SELECT(FractalIIBlock.AMP_2, FractalIIChannel.X, label = lbl)
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(label.text, expected_select, lbl)

            action = EFFECT_CHANNEL_TOGGLE(FractalIIBlock.AMP_2, label = lbl)
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(label.text, expected_toggle, lbl)

        # Not in the preset
        states.value = b""
        for (lbl, expected) in (
            (FractalIILabel.LONG_NAME_CHANNEL, "Amp 2"),
            (FractalIILabel.SHORT_NAME_CHANNEL, "AMP2"),
            (FractalIILabel.CURRENT_CHANNEL, "AMP2"),
            (FractalIILabel.BOTH_CHANNELS, "AMP2 X/Y"),
            (FractalIILabel.DESTINATION_CHANNEL, "AMP2"),
        ):
            action = EFFECT_CHANNEL_TOGGLE(FractalIIBlock.AMP_2, label = lbl)
            appl, switch, label = setup_action(action)
            action.update_displays()
            self.assertEqual(label.text, expected, lbl)

        action = EFFECT_BYPASS(FractalIIBlock.AMP_2, label = FractalIILabel.SHORT_NAME)
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "AMP2")

    def test_channel_select(self):
        action = EFFECT_CHANNEL_SELECT(FractalIIBlock.AMP_1, FractalIIChannel.Y)
        appl, switch, label = setup_action(action)
        states = FractalIIMappings.BLOCK_STATES()
        channel = FractalIIMappings.CHANNEL(FractalIIBlock.AMP_1)

        # Not present
        action.push()
        self.assertEqual(set_calls(appl), [])
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # Engaged on X
        states.value = block_states([(FractalIIBlock.AMP_1, True, True)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "AMP1 Y")

        action.push()
        self.assertEqual(set_calls(appl), [(channel, 1)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(action.callback.channel, FractalIIChannel.Y)

        # Second press without function
        action.push()
        self.assertEqual(len(set_calls(appl)), 1)

        # Bypassed: LED off
        states.value = block_states([(FractalIIBlock.AMP_1, False, False)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(action.callback.present, True)
        self.assertEqual(action.callback.engaged, False)

    def test_channel_select_smart_bypass(self):
        action = EFFECT_CHANNEL_SELECT(FractalIIBlock.AMP_1, FractalIIChannel.X, second_press = FractalIISecondPress.SMART_BYPASS)
        appl, switch, label = setup_action(action)
        states = FractalIIMappings.BLOCK_STATES()
        bypass = FractalIIMappings.BYPASS(FractalIIBlock.AMP_1)

        states.value = block_states([(FractalIIBlock.AMP_1, True, True)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Second press: bypass
        action.push()
        self.assertEqual(set_calls(appl), [(bypass, 0)])
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(set_calls(appl), [(bypass, 0), (bypass, 1)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_channel_select_previous(self):
        action = EFFECT_CHANNEL_SELECT(FractalIIBlock.AMP_1, FractalIIChannel.X, second_press = FractalIISecondPress.PREVIOUS_CHANNEL)
        appl, switch, label = setup_action(action)
        states = FractalIIMappings.BLOCK_STATES()
        channel = FractalIIMappings.CHANNEL(FractalIIBlock.AMP_1)

        states.value = block_states([(FractalIIBlock.AMP_1, True, True)])
        action.push()
        self.assertEqual(set_calls(appl), [(channel, 1)])
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(set_calls(appl), [(channel, 1), (channel, 0)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_channel_toggle(self):
        action = EFFECT_CHANNEL_TOGGLE(FractalIIBlock.REVERB_1)
        appl, switch, label = setup_action(action)
        states = FractalIIMappings.BLOCK_STATES()
        channel = FractalIIMappings.CHANNEL(FractalIIBlock.REVERB_1)

        states.value = block_states([(FractalIIBlock.REVERB_1, False, True)])
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "REV1 [X]Y")

        action.push()
        self.assertEqual(set_calls(appl), [(channel, 1)])
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "REV1 X[Y]")

        action.release()

        action.push()
        self.assertEqual(set_calls(appl), [(channel, 1), (channel, 0)])


class TestFractalIITuner(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

        self.period = MockPeriodCounter()
        mapping = FractalIIMappings.TUNER_STATE()
        mapping._FractalIITunerStateMapping__period = self.period
        mapping._FractalIITunerStateMapping__ignore = False

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        action = TUNER()
        appl, switch, label = setup_action(action)
        state = FractalIIMappings.TUNER_STATE()
        cc = FractalIIMappings.TUNER_ON_OFF(15, 0)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [state])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(switch.colors[0], COLOR_UTILITY)
        self.assertEqual(label.text, "Tuner")

        action.push()
        self.assertEqual(set_calls(appl), [(cc, 127)])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(set_calls(appl), [(cc, 127), (cc, 0)])
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Timeout check in update()
        state.value = 1
        self.period.passed = 2000
        action.callback.update()
        self.assertEqual(state.value, 0)

    def test_cc(self):
        action = TUNER(cc = 20, midi_channel = 3)
        appl, switch, label = setup_action(action)

        action.push()
        self.assertEqual(set_calls(appl), [(FractalIIMappings.TUNER_ON_OFF(20, 2), 127)])


class TestFractalIITapTempo(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        action = TAP_TEMPO()
        appl, switch, label = setup_action(action)
        beat = FractalIIMappings.TEMPO_BEAT()

        period = MockPeriodCounter()
        period.interval = 100
        action.callback._FractalIITapTempoCallback__flash = period

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [beat])

        action.update_displays()
        self.assertEqual(label.text, "Tap Tempo")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(set_calls(appl), [(FractalIIMappings.TAP_TEMPO(14, 0), 127)])

        # Beat: flash
        beat.value = 1
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(period.num_reset_calls, 1)

        action.update_displays()
        self.assertEqual(period.num_reset_calls, 1)

        period.passed = 100
        action.callback.update()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        period.passed = 101
        action.callback.update()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_bpm(self):
        action = TAP_TEMPO(label = FractalIILabel.BPM, cc = 30, midi_channel = 2)
        appl, switch, label = setup_action(action)
        bpm = FractalIIMappings.TEMPO_BPM()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalIIMappings.TEMPO_BEAT(), bpm])

        action.update_displays()
        self.assertEqual(label.text, "")

        bpm.value = 120
        action.update_displays()
        self.assertEqual(label.text, "120 bpm")

        action.push()
        self.assertEqual(set_calls(appl), [(FractalIIMappings.TAP_TEMPO(30, 1), 127)])
