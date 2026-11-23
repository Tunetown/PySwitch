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
    from lib.pyswitch.clients.fractal_am4 import *
    from lib.pyswitch.clients.fractal_am4.actions.preset import *
    from lib.pyswitch.clients.fractal_am4.actions.scene import *
    from lib.pyswitch.clients.fractal_am4.actions.effect_bypass import *
    from lib.pyswitch.clients.fractal_am4.actions.mode import *
    from lib.pyswitch.clients.fractal_am4.callbacks.preset_name import *
    from lib.pyswitch.clients.fractal_am4.callbacks.scene_name import *
    from lib.pyswitch.controller.actions import Action

    from .mocks_fractal_am4 import *
    from .mocks_ui import MockDisplayLabel


SCENE_NAMES = ("Clean", "Crunch", "", "Lead")

# Name table value: (scene, preset name, scene names, slot blocks)
def table(scene = 0, name = "Gig", blocks = (FractalAM4Block.DRIVE, FractalAM4Block.AMP, 0, FractalAM4Block.REVERB)):
    return (scene, name, SCENE_NAMES, blocks)


class TestFractalAM4Preset(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_invalid(self):
        with self.assertRaises(Exception):
            PRESET_SELECT(-1)
        with self.assertRaises(Exception):
            PRESET_SELECT(104)
        with self.assertRaises(Exception):
            PRESET_SELECT_IN_BANK(0)
        with self.assertRaises(Exception):
            PRESET_SELECT_IN_BANK(5)

    def test_select_number(self):
        action = PRESET_SELECT(5, label = FractalAM4Label.NUMBER, id = 3)
        appl, switch, label = setup_action(action)
        preset = FractalAM4Mappings.PRESET()

        self.assertIsInstance(action, Action)
        self.assertEqual(action.id, 3)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [preset])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_PRESET)
        self.assertEqual(label.text, "B02")

        preset.value = 2
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalAM4Mappings.PRESET_SELECT(), "value": 5 }])
        self.assertEqual(preset.value, 5)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()

    def test_select_name(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        cb = action.callback
        preset = FractalAM4Mappings.PRESET()
        tab = FractalAM4Mappings.NAME_TABLE()
        name = FractalAM4Mappings.PRESET_NAME(5)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [preset, tab])

        # Name not known yet: location
        action.update_displays()
        self.assertEqual(label.text, "B02")

        # Other preset loaded: the name of location 5 is requested
        preset.value = 2
        action.update_displays()
        self.assertEqual(label.text, "B02")

        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": name, "listener": cb })

        name.value = "Lead"
        action.update_displays()
        self.assertEqual(label.text, "Lead")

        appl.client.request_calls = []
        cb.update()
        self.assertNotIn(name, [c["mapping"] for c in appl.client.request_calls])

        # Loaded: the name comes from the name table (location as long as the table is not received)
        preset.value = 5
        action.update_displays()
        self.assertEqual(label.text, "B02")

        tab.value = table(name = "Current")
        action.update_displays()
        self.assertEqual(label.text, "Current")

        # After the preset change, the name of location 5 is read again when another preset is loaded. The old name 
        # is shown until the answer arrives.
        preset.value = 3
        action.update_displays()
        self.assertEqual(label.text, "Lead")

        appl.client.request_calls = []
        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": name, "listener": cb })

        appl.client.request_calls = []
        cb.update()
        self.assertNotIn(name, [c["mapping"] for c in appl.client.request_calls])

    def test_in_bank(self):
        action = PRESET_SELECT_IN_BANK(3, label = FractalAM4Label.NUMBER)
        appl, switch, label = setup_action(action)
        preset = FractalAM4Mappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # Nothing loaded yet: no target
        action.push()
        self.assertEqual(appl.client.set_calls, [])

        preset.value = 5        # B02
        action.update_displays()
        self.assertEqual(label.text, "B03")
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 6)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_inc_dec(self):
        action = PRESET_INC_DEC(-1)
        appl, switch, label = setup_action(action)
        preset = FractalAM4Mappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "Preset -1")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        preset.value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Wrap
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 103)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # No wrap
        action2 = PRESET_INC_DEC(1, wrap = False)
        appl2, switch2, label2 = setup_action(action2)
        preset.value = 103
        action2.push()
        self.assertEqual(appl2.client.set_calls[-1]["value"], 103)

    def test_inc_dec_destination(self):
        action = PRESET_INC_DEC(1, label = FractalAM4Label.DESTINATION_NAME)
        appl, switch, label = setup_action(action)
        preset = FractalAM4Mappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "")

        preset.value = 9
        action.update_displays()
        self.assertEqual(label.text, "C03")

        FractalAM4Mappings.PRESET_NAME(10).value = "Next"
        action.update_displays()
        self.assertEqual(label.text, "Next")

        # Number label
        action2 = PRESET_INC_DEC(1, label = FractalAM4Label.NUMBER)
        appl2, switch2, label2 = setup_action(action2)
        action2.update_displays()
        self.assertEqual(label2.text, "C03")

    def test_bank(self):
        action = BANK_INC_DEC(1, color = (1, 2, 3))
        appl, switch, label = setup_action(action)
        preset = FractalAM4Mappings.PRESET()

        action.update_displays()
        self.assertEqual(label.text, "Bank +1")
        self.assertEqual(switch.colors[0], (1, 2, 3))

        preset.value = 6        # B03
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 8)    # C01

        # Same position, wrap
        action2 = BANK_INC_DEC(-1, preset_load = FractalAM4PresetLoad.SAME, label = FractalAM4Label.NUMBER)
        appl2, switch2, label2 = setup_action(action2)
        preset.value = 2        # A03
        action2.update_displays()
        self.assertEqual(label2.text, "Bank Z")
        self.assertEqual(switch2.colors[0], COLOR_BANK)

        action2.push()
        self.assertEqual(appl2.client.set_calls[-1]["value"], 102)  # Z03

    def test_custom_text(self):
        action = PRESET_SELECT(0, text = "Foo")
        appl, switch, label = setup_action(action)
        action.update_displays()
        self.assertEqual(label.text, "Foo")


class TestFractalAM4Scene(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_invalid(self):
        with self.assertRaises(Exception):
            SCENE_SELECT(0)
        with self.assertRaises(Exception):
            SCENE_SELECT(5)

    def test_select(self):
        action = SCENE_SELECT(2)
        appl, switch, label = setup_action(action)
        tab = FractalAM4Mappings.NAME_TABLE()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [tab])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_SCENE)
        self.assertEqual(label.text, "Scene 2")

        tab.value = table(scene = 0)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "Crunch")

        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalAM4Mappings.SCENE_SELECT(), "value": 1 }])
        self.assertEqual(tab.value[0], 1)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # The next answer is skipped (feedback)
        tab.parse(name_table_answer(0, "Gig", SCENE_NAMES, (0, 0, 0, 0)))
        self.assertEqual(tab.value[0], 1)

        action.release()

    def test_select_without_table(self):
        action = SCENE_SELECT(1)
        appl, switch, label = setup_action(action)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)
        self.assertEqual(FractalAM4Mappings.NAME_TABLE().value, None)

    def test_select_number_and_empty_name(self):
        action = SCENE_SELECT(3, label = FractalAM4Label.NUMBER)
        appl, switch, label = setup_action(action)
        FractalAM4Mappings.NAME_TABLE().value = table()
        action.update_displays()
        self.assertEqual(label.text, "Scene 3")

        action2 = SCENE_SELECT(3)
        appl2, switch2, label2 = setup_action(action2)
        action2.update_displays()
        self.assertEqual(label2.text, "Scene 3")      # Scene without name

    def test_inc_dec(self):
        action = SCENE_INC_DEC(1, label = FractalAM4Label.DESTINATION_NAME)
        appl, switch, label = setup_action(action)
        tab = FractalAM4Mappings.NAME_TABLE()

        action.update_displays()
        self.assertEqual(label.text, "")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # No scene known: nothing happens
        action.push()
        self.assertEqual(appl.client.set_calls, [])
        action.release()

        tab.value = table(scene = 3)
        action.update_displays()
        self.assertEqual(label.text, "Clean")         # Wrap to scene 1
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action2 = SCENE_INC_DEC(-1, wrap = False)
        appl2, switch2, label2 = setup_action(action2)
        tab.value = table(scene = 0)
        action2.update_displays()
        self.assertEqual(label2.text, "Scene -1")
        action2.push()
        self.assertEqual(appl2.client.set_calls[-1]["value"], 0)


class TestFractalAM4EffectBypass(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_invalid(self):
        with self.assertRaises(Exception):
            EFFECT_BYPASS(slot = None)
        with self.assertRaises(Exception):
            EFFECT_BYPASS(slot = 0)
        with self.assertRaises(Exception):
            EFFECT_BYPASS(slot = 5)

    def test_defaults(self):
        # Default: slot 1 (the emulator adds actions with their default parameters)
        cb = EFFECT_BYPASS().callback
        self.assertEqual(cb._FractalAM4BypassCallback__slot, 0)
        self.assertEqual(cb._FractalAM4BypassCallback__block, None)

        # Block set: the slot is ignored
        cb = EFFECT_BYPASS(slot = 3, block = FractalAM4Block.AMP).callback
        self.assertEqual(cb._FractalAM4BypassCallback__slot, None)
        self.assertEqual(cb._FractalAM4BypassCallback__block, FractalAM4Block.AMP)

    def test_slot(self):
        action = EFFECT_BYPASS(slot = 2)
        appl, switch, label = setup_action(action)
        cb = action.callback
        tab = FractalAM4Mappings.NAME_TABLE()
        amp = FractalAM4Mappings.BYPASS(FractalAM4Block.AMP)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [tab])

        # Unknown: off, no label, pressing does nothing
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_EFFECT)
        self.assertEqual(label.text, "")
        action.push()
        self.assertEqual(appl.client.set_calls, [])

        # Block known, bypass state not yet
        tab.value = table()
        action.update_displays()
        self.assertEqual(label.text, "Amp")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": amp, "listener": cb })

        action.push()
        self.assertEqual(appl.client.set_calls, [])

        # Engaged
        amp.value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.push()
        self.assertEqual(appl.client.set_calls[-1], { "mapping": amp, "value": 1 })
        self.assertEqual(amp.value, 1)
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1], { "mapping": amp, "value": 0 })

        # Slot empty
        tab.value = table(blocks = (0, 0, 0, 0))
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "")

        appl.client.request_calls = []
        cb.update()
        self.assertNotIn(amp, [c["mapping"] for c in appl.client.request_calls])

    def test_block(self):
        action = EFFECT_BYPASS(block = FractalAM4Block.DRIVE, label = FractalAM4Label.SHORT_NAME)
        appl, switch, label = setup_action(action)
        tab = FractalAM4Mappings.NAME_TABLE()
        drive = FractalAM4Mappings.BYPASS(FractalAM4Block.DRIVE)

        action.update_displays()
        self.assertEqual(label.text, "DRV")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        tab.value = table()
        drive.value = 1
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Not in the preset
        tab.value = table(blocks = (FractalAM4Block.AMP, 0, 0, 0))
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "DRV")


class TestFractalAM4Mode(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_mode(self):
        action = MODE_SELECT(FractalAM4Mode.TUNER)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "Tuner")
        self.assertEqual(switch.colors[0], COLOR_UTILITY)
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalAM4Mappings.MODE(), "value": FractalAM4Mode.TUNER }])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_base_callback(self):
        cb = FractalAM4Callback(color = (1, 2, 3), text = None)
        cb.push()
        cb.release()

    def test_reset(self):
        action = MODE_SELECT(FractalAM4Mode.SCENES)
        appl, switch, label = setup_action(action)

        label.text = ""
        action.callback.reset()
        self.assertEqual(label.text, "Scenes")


class TestFractalAM4Callbacks(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_preset_name(self):
        cb = FractalAM4PresetNameCallback(show_number = True, default_text = "-")
        appl = MockController(client = MockFractalAM4Client())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalAM4Mappings.PRESET(), FractalAM4Mappings.NAME_TABLE()])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        # Name table not received yet: location only
        FractalAM4Mappings.PRESET().value = 5
        cb.update_label(label)
        self.assertEqual(label.text, "B02")

        cb2 = FractalAM4PresetNameCallback(default_text = "-")
        cb2.init(appl)
        cb2.update_label(label)
        self.assertEqual(label.text, "-")

        FractalAM4Mappings.NAME_TABLE().value = table(name = "Plexi")
        cb.update_label(label)
        self.assertEqual(label.text, "B02 Plexi")

        cb2.update_label(label)
        self.assertEqual(label.text, "Plexi")

        # Empty name
        FractalAM4Mappings.NAME_TABLE().value = table(name = "")
        cb.update_label(label)
        self.assertEqual(label.text, "B02")

        FractalAM4Mappings.NAME_TABLE().value = table(name = "Plexi")

        cb3 = FractalAM4PresetNameCallback(show_name = False)
        cb3.init(appl)
        cb3.update_label(label)
        self.assertEqual(label.text, "B02")

    def test_scene_name(self):
        cb = FractalAM4SceneNameCallback(show_number = True, default_text = "-")
        appl = MockController(client = MockFractalAM4Client())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalAM4Mappings.NAME_TABLE()])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        tab = FractalAM4Mappings.NAME_TABLE()
        tab.value = table(scene = 1)
        cb.update_label(label)
        self.assertEqual(label.text, "2 Crunch")

        # Scene without name
        tab.value = table(scene = 2)
        cb.update_label(label)
        self.assertEqual(label.text, "Scene 3")

        cb2 = FractalAM4SceneNameCallback()
        cb2.init(appl)
        tab.value = table(scene = 3)
        cb2.update_label(label)
        self.assertEqual(label.text, "Lead")

        cb3 = FractalAM4SceneNameCallback(show_name = False)
        cb3.init(appl)
        cb3.update_label(label)
        self.assertEqual(label.text, "Scene 4")
