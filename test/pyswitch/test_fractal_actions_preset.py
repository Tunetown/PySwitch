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
    from lib.pyswitch.clients.fractal.actions.preset import *
    from lib.pyswitch.clients.fractal.actions.bank import *
    from lib.pyswitch.controller.actions import Action
    from lib.pyswitch.colors import dim_color, Colors

    from .mocks_callback import MockEnabledCallback
    from .mocks_fractal import *


class TestFractalActionPresetSelect(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_properties(self):
        ecb = MockEnabledCallback(output = True)

        action = PRESET_SELECT(
            5,
            midi_channel = 3,
            id = 45,
            use_leds = False,
            enable_callback = ecb
        )

        self.assertIsInstance(action, Action)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, False)
        self.assertEqual(action._Action__enable_callback, ecb)

        appl, switch, label = setup_action(action)

        self.assertEqual(appl.client.register_calls[0]["mapping"], FractalMappings.PRESET())

        action.callback.update()
        self.assertEqual(appl.client.request_calls[0]["mapping"], FractalMappings.PRESET())

        FractalMappings.PRESET().value = 2
        action.push()

        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(2), "value": 5 }])

    def test_leds(self):
        action = PRESET_SELECT(5, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # No value
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_PRESET)
        self.assertEqual(label.back_color, dim_color(COLOR_PRESET, 0.2))
        self.assertEqual(label.text, "005")

        mapping.value = 3
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.back_color, dim_color(COLOR_PRESET, 0.2))

        mapping.value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.back_color, COLOR_PRESET)

    def test_config_brightness(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action, config = {
            "ledBrightnessOn": 0.5,
            "ledBrightnessOff": 0.1,
            "displayDimFactorOn": 0.8,
            "displayDimFactorOff": 0.3
        })
        mapping = FractalMappings.PRESET()

        mapping.value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], 0.5)
        self.assertEqual(label.back_color, dim_color(COLOR_PRESET, 0.8))

        mapping.value = 4
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], 0.1)
        self.assertEqual(label.back_color, dim_color(COLOR_PRESET, 0.3))

    def test_color_and_text(self):
        action = PRESET_SELECT(5, color = (3, 4, 5), text = "foo")
        appl, switch, label = setup_action(action)

        FractalMappings.PRESET().value = 5
        action.update_displays()

        self.assertEqual(switch.colors[0], (3, 4, 5))
        self.assertEqual(label.text, "foo")

    def test_push(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # Without value
        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(0), "value": 5 }])
        self.assertEqual(mapping.value, 5)

        # Local feedback: the next answer is skipped
        mapping.parse(preset_answer(2, "foo"))
        self.assertEqual(mapping.value, 5)

        FRACTAL.selected_bank = 7

        appl.client.set_calls = []
        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(0), "value": 5 }])
        self.assertEqual(FRACTAL.selected_bank, None)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_second_press_previous(self):
        action = PRESET_SELECT(5, second_press_previous = True)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # No previous yet
        mapping.value = 5
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 5)

        mapping.value = 3
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 5)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 3)
        self.assertEqual(mapping.value, 3)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 5)

    def test_name_label(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        cb = action.callback

        action.update_displays()
        self.assertEqual(label.text, "")

        cb.update()

        target_name = appl.client.request_calls[-1]["mapping"]
        self.assertEqual(target_name.target, 5)
        self.assertEqual(appl.client.request_calls[-1]["listener"], cb)
        self.assertEqual(FRACTAL.pending_names, [5])

        # Answer
        self.assertEqual(target_name.parse(preset_answer(5, "Five")), True)
        action.update_displays()
        self.assertEqual(label.text, "Five")

        # No more requests when the name is known
        appl.client.request_calls = []
        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.PRESET()])

    def test_name_request_terminated(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        cb = action.callback

        action.update_displays()
        cb.update()
        target_name = appl.client.request_calls[-1]["mapping"]
        self.assertEqual(FRACTAL.pending_names, [5])

        cb.request_terminated(target_name)
        self.assertEqual(FRACTAL.pending_names, [])

        cb.request_terminated(FractalMappings.PRESET())
        self.assertEqual(FractalMappings.PRESET().value, None)

    def test_p_num_label(self):
        action = PRESET_SELECT(7, label = FractalLabel.P_NUM)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "P3")

    def test_display_offset(self):
        action = PRESET_SELECT(7, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action, config = { "fractalPresetDisplayOffset": 1 })

        action.update_displays()
        self.assertEqual(label.text, "008")

    def test_current_labels(self):
        action = PRESET_SELECT(7, label = FractalLabel.CURRENT_NAME)
        appl, switch, label = setup_action(action)

        self.assertIn(FractalMappings.PRESET_NAME(), [c["mapping"] for c in appl.client.register_calls])

        action.update_displays()
        self.assertEqual(label.text, "")

        FractalMappings.PRESET_NAME().value = "Current"
        action.update_displays()
        self.assertEqual(label.text, "Current")

        action = PRESET_SELECT(7, label = FractalLabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "")

        FractalMappings.PRESET().value = 12
        action.update_displays()
        self.assertEqual(label.text, "012")


###############################################################################################################


class TestFractalActionPresetSelectInBank(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_bank(self):
        action = PRESET_SELECT_IN_BANK(2, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # No value
        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(appl.client.set_calls, [])

        # Bank 2 (presets 5-9)
        mapping.value = 8
        action.update_displays()
        self.assertEqual(label.text, "006")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        mapping.value = 6
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        mapping.value = 8
        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(0), "value": 6 }])

    def test_bank_size(self):
        action = PRESET_SELECT_IN_BANK(2, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action, config = { "fractalBankSize": 3 })

        FractalMappings.PRESET().value = 8
        action.update_displays()
        self.assertEqual(label.text, "007")

    def test_selected_bank(self):
        action = PRESET_SELECT_IN_BANK(1, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 0
        action.update_displays()
        self.assertEqual(label.text, "000")
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Bank selected by a bank function: update() refreshes the display
        FRACTAL.selected_bank = 4
        action.callback.update()
        self.assertEqual(label.text, "020")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 20)
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_partial_bank(self):
        action = PRESET_SELECT_IN_BANK(3, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)

        # Last bank 102: presets 510, 511
        FractalMappings.PRESET().value = 511
        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls, [])

    def test_name_follows_bank(self):
        action = PRESET_SELECT_IN_BANK(1)
        appl, switch, label = setup_action(action)
        cb = action.callback

        FractalMappings.PRESET().value = 3
        action.update_displays()
        cb.update()

        target_name = appl.client.request_calls[-1]["mapping"]
        self.assertEqual(target_name.target, 0)

        target_name.parse(preset_answer(0, "Zero"))
        action.update_displays()
        self.assertEqual(label.text, "Zero")

        # Preset change to another bank
        FractalMappings.PRESET().value = 12
        action.update_displays()
        self.assertEqual(target_name.target, 10)
        self.assertEqual(label.text, "")

        cb.update()
        self.assertEqual(FRACTAL.pending_names, [10])


###############################################################################################################


class TestFractalActionPresetToggle(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_toggle(self):
        action = PRESET_TOGGLE(3, 10)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # Neither
        mapping.value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "P003/P010")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 3)

        # Primary
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "[P003] P010")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 10)

        # Secondary
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "P003 [P010]")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 3)

    def test_destination_labels(self):
        action = PRESET_TOGGLE(3, 10, label = FractalLabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)

        FractalMappings.PRESET().value = 3
        action.update_displays()
        self.assertEqual(label.text, "010")

        action = PRESET_TOGGLE(3, 10, label = FractalLabel.DESTINATION_NAME)
        appl, switch, label = setup_action(action)

        action.update_displays()
        action.callback.update()
        target_name = appl.client.request_calls[-1]["mapping"]
        self.assertEqual(target_name.target, 10)

    def test_toggle_in_bank(self):
        action = PRESET_TOGGLE_IN_BANK(1, 3)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "[P1] P3")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 7)
        self.assertEqual(label.text, "P1 [P3]")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action = PRESET_TOGGLE_IN_BANK(1, 3, label = FractalLabel.BOTH_NUM)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "P005 [P007]")

    def test_toggle_in_bank_partial(self):
        action = PRESET_TOGGLE_IN_BANK(1, 3)
        appl, switch, label = setup_action(action)

        FractalMappings.PRESET().value = 511
        action.update_displays()
        self.assertEqual(label.text, "")

    def test_toggle_in_bank_no_value(self):
        action = PRESET_TOGGLE_IN_BANK(1, 3)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(switch.brightnesses[0], LED_OFF)


###############################################################################################################


class TestFractalActionPresetIncDec(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_inc_dec(self):
        action = PRESET_INC_DEC()
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "Preset +1")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # No value: nothing sent
        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [])

        mapping.value = 10
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 11)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Wrap
        mapping.value = 511
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)

    def test_no_wrap_and_limits(self):
        action = PRESET_INC_DEC(step = -2, wrap = False, lower_limit = 5, upper_limit = 20, label = FractalLabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 10
        action.update_displays()
        self.assertEqual(label.text, "008")

        mapping.value = 6
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 5)

        action = PRESET_INC_DEC(step = -1, wrap = True, lower_limit = 5, upper_limit = 20, label = FractalLabel.ACTION)
        appl, switch, label = setup_action(action)

        mapping.value = 5
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 20)
        self.assertEqual(label.text, "Preset -1")

    def test_axe_fx_iii(self):
        action = PRESET_INC_DEC()
        appl, switch, label = setup_action(action, config = { "fractalModel": MODEL_AXE_FX_III })

        FractalMappings.PRESET().value = 511
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 512)

        reset_fractal()


###############################################################################################################


class TestFractalActionBank(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_select_no_load(self):
        action = BANK_SELECT(3)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        # No value
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "Bank 3")

        mapping.value = 4
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(switch.colors[0], COLOR_BANK)

        action.push()
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(FRACTAL.selected_bank, 2)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Selecting the bank of the current preset clears the selection
        mapping.value = 11
        action.push()
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_select_no_value(self):
        action = BANK_SELECT(3, preset_load = FractalPresetLoad.FIRST)
        appl, switch, label = setup_action(action)

        action.push()
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(FRACTAL.selected_bank, 2)

    def test_select_load_first(self):
        action = BANK_SELECT(3, preset_load = FractalPresetLoad.FIRST)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 4
        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(0), "value": 10 }])
        self.assertEqual(mapping.value, 10)
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_select_load_current(self):
        action = BANK_SELECT(3, preset_load = FractalPresetLoad.CURRENT, midi_channel = 2)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 3
        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(1), "value": 13 }])

        # Clamped in the last bank
        action = BANK_SELECT(103, preset_load = FractalPresetLoad.CURRENT)
        appl, switch, label = setup_action(action)

        mapping.value = 4
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 511)

    def test_select_second_press(self):
        action = BANK_SELECT(3, preset_load = FractalPresetLoad.FIRST, second_press_previous = True)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 4
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 10)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)

    def test_toggle(self):
        action = BANK_TOGGLE(1, 4)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 12
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "B1/B4")

        action.push()
        self.assertEqual(FRACTAL.selected_bank, 0)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "[B1] B4")

        action.push()
        self.assertEqual(FRACTAL.selected_bank, 3)
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "B1 [B4]")

    def test_inc_dec(self):
        action = BANK_INC_DEC(preset_load = FractalPresetLoad.CURRENT)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "Bank +1")

        # No value
        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [])

        mapping.value = 7
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 12)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Wrap
        mapping.value = 511
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 1)

    def test_inc_dec_limits(self):
        action = BANK_INC_DEC(step = -1, wrap = True, lower_limit = 2, upper_limit = 5, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 5
        action.update_displays()
        self.assertEqual(label.text, "Bank 5")

        action.push()
        self.assertEqual(FRACTAL.selected_bank, 4)

        action = BANK_INC_DEC(step = 1, wrap = False, label = FractalLabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)

        FRACTAL.selected_bank = None
        mapping.value = 510
        action.update_displays()
        self.assertEqual(label.text, "Bank 103")

        action.push()
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_selected_bank_update(self):
        action = BANK_SELECT(2)
        appl, switch, label = setup_action(action)

        FractalMappings.PRESET().value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        FRACTAL.selected_bank = 1
        action.callback.update()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_preset_change_resets_selection(self):
        action = BANK_SELECT(2)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.PRESET()

        mapping.value = 0
        action.update_displays()

        action.push()
        self.assertEqual(FRACTAL.selected_bank, 1)

        mapping.value = 30
        action.update_displays()
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_current_num_no_value(self):
        action = BANK_SELECT(2, label = FractalLabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "")
