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
    from lib.pyswitch.clients.fractal.actions.scene import *
    from lib.pyswitch.controller.actions import Action

    from .mocks_fractal import *


class TestFractalActionScene(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_invalid(self):
        with self.assertRaises(Exception):
            SCENE_SELECT(0)

        with self.assertRaises(Exception):
            SCENE_SELECT(9)

        with self.assertRaises(Exception):
            SCENE_TOGGLE(1, 9)

    def test_select(self):
        action = SCENE_SELECT(3, label = FractalLabel.NUMBER, id = 4)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        self.assertIsInstance(action, Action)
        self.assertEqual(action.id, 4)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [mapping])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(switch.colors[0], COLOR_SCENE)
        self.assertEqual(label.text, "Scene 3")

        mapping.value = 0
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 2 }])
        self.assertEqual(mapping.value, 2)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # The next answer is skipped
        mapping.parse(sysex(0x0c, [0]))
        self.assertEqual(mapping.value, 2)

        action.release()

    def test_second_press_previous(self):
        action = SCENE_SELECT(3, second_press_previous = True)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        mapping.value = 5
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 2)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 5)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 2)

    def test_names(self):
        action = SCENE_SELECT(3)
        appl, switch, label = setup_action(action)
        cb = action.callback
        scene_name = FractalMappings.SCENE_NAME(2)

        # The preset is needed for invalidating the names
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

        action.update_displays()
        self.assertEqual(label.text, "")

        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": scene_name, "listener": cb })

        scene_name.parse(sysex(0x0e, [2] + name32("Lead")))
        action.update_displays()
        self.assertEqual(label.text, "Lead")

        appl.client.request_calls = []
        cb.update()
        self.assertNotIn(scene_name, [c["mapping"] for c in appl.client.request_calls])

        # Preset change invalidates the names
        FractalMappings.PRESET().value = 4
        action.update_displays()
        FractalMappings.PRESET().value = 5
        action.update_displays()
        self.assertEqual(label.text, "")

        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": scene_name, "listener": cb })

    def test_toggle(self):
        action = SCENE_TOGGLE(1, 3)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)
        self.assertEqual(label.text, "Scene 1/3")

        mapping.value = 4
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(label.text, "Scene [1] 3")

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 2)
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(label.text, "Scene 1 [3]")

    def test_toggle_labels(self):
        action = SCENE_TOGGLE(1, 3, label = FractalLabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        mapping.value = 0
        action.update_displays()
        self.assertEqual(label.text, "Scene 3")

        action = SCENE_TOGGLE(1, 3, label = FractalLabel.CURRENT_NUM)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "Scene 1")

        action = SCENE_TOGGLE(1, 3, label = FractalLabel.CURRENT_NAME)
        appl, switch, label = setup_action(action)

        FractalMappings.SCENE_NAME(0).value = "Clean"
        action.update_displays()
        self.assertEqual(label.text, "Clean")

        action = SCENE_TOGGLE(1, 3, label = FractalLabel.DESTINATION_NAME)
        appl, switch, label = setup_action(action)

        FractalMappings.SCENE_NAME(2).value = "Lead"
        action.update_displays()
        self.assertEqual(label.text, "Lead")

    def test_current_no_value(self):
        action = SCENE_TOGGLE(1, 3, label = FractalLabel.CURRENT_NAME)
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "")

        appl.client.request_calls = []
        action.callback.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

    def test_inc_dec(self):
        action = SCENE_INC_DEC()
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        action.update_displays()
        self.assertEqual(label.text, "Scene +1")
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [])

        mapping.value = 6
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 7)
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 0)

    def test_inc_dec_limits(self):
        action = SCENE_INC_DEC(step = -1, wrap = False, lower_limit = 2, upper_limit = 4, label = FractalLabel.DESTINATION_NUM)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.SCENE()

        mapping.value = 2
        action.update_displays()
        self.assertEqual(label.text, "Scene 2")

        mapping.value = 1
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 1)

        action = SCENE_INC_DEC(step = 1, wrap = True, lower_limit = 2, upper_limit = 4)
        appl, switch, label = setup_action(action)

        mapping.value = 3
        action.push()
        self.assertEqual(appl.client.set_calls[-1]["value"], 1)
        self.assertEqual(label.text, "Scene +1")
