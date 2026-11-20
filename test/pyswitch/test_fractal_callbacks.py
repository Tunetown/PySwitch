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
    from lib.pyswitch.clients.fractal.callbacks.preset_name import *
    from lib.pyswitch.clients.fractal.callbacks.scene_name import *
    from lib.pyswitch.clients.fractal.callbacks.tempo_bpm import *
    from lib.pyswitch.clients.fractal.mappings.tempo import MAPPING_TEMPO_BPM
    from lib.pyswitch.clients.fractal.actions.preset import PRESET_SELECT
    from lib.pyswitch.ui.ui import DisplayElement
    from lib.pyswitch.ui.elements import TunerDisplay
    from lib.pyswitch.colors import Colors

    from .mocks_appl import MockController, MockPeriodCounter, MockAction
    from .mocks_ui import MockDisplayLabel
    from .mocks_fractal import *


class TestFractalPresetNameCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_name(self):
        cb = FractalPresetNameCallback(default_text = "-")
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.PRESET(), FractalMappings.PRESET_NAME()])

        # (PRESET_NAME has no request message, the client ignores the call)
        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.PRESET(), FractalMappings.PRESET_NAME()])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        # Number without name
        FractalMappings.PRESET().value = 3
        cb.update_label(label)
        self.assertEqual(label.text, "-")

        FractalMappings.PRESET_NAME().value = "Plexi"
        cb.update_label(label)
        self.assertEqual(label.text, "Plexi")

    def test_name_and_number(self):
        cb = FractalPresetNameCallback(show_number = True)
        appl = MockController(client = MockFractalClient(), config = { "fractalPresetDisplayOffset": 1 })
        cb.init(appl)
        label = MockDisplayLabel()

        cb.update_label(label)
        self.assertEqual(label.text, "")

        FractalMappings.PRESET().value = 3
        FractalMappings.PRESET_NAME().value = "Plexi"
        cb.update_label(label)
        self.assertEqual(label.text, "004 Plexi")

    def test_number(self):
        cb = FractalPresetNameCallback(show_name = False, show_number = True)
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.PRESET()])

        FractalMappings.PRESET().value = 42
        cb.update_label(label)
        self.assertEqual(label.text, "042")

    def test_tracks_preset(self):
        cb = FractalPresetNameCallback()
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        FractalMappings.PRESET().value = 3
        cb.update_label(label)

        FRACTAL.selected_bank = 5
        FractalMappings.PRESET().value = 4
        cb.update_label(label)

        self.assertEqual(FRACTAL.selected_bank, None)


###############################################################################################################


class TestFractalSceneNameCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_name(self):
        cb = FractalSceneNameCallback(default_text = "-")
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

        FractalMappings.SCENE().value = 2
        cb.update_label(label)
        self.assertEqual(label.text, "-")

        appl.client.request_calls = []
        cb.update()
        self.assertEqual(appl.client.request_calls[-1], { "mapping": FractalMappings.SCENE_NAME(2), "listener": cb })

        FractalMappings.SCENE_NAME(2).value = "Lead"
        cb.update_label(label)
        self.assertEqual(label.text, "Lead")

        appl.client.request_calls = []
        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

        # Preset change invalidates the name
        FractalMappings.PRESET().value = 1
        cb.update_label(label)
        FractalMappings.PRESET().value = 2
        cb.update_label(label)
        self.assertEqual(label.text, "-")

        # Scene lost
        FractalMappings.SCENE().value = None
        cb.update_label(label)
        self.assertEqual(label.text, "-")

        appl.client.request_calls = []
        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [FractalMappings.SCENE(), FractalMappings.PRESET()])

    def test_name_and_number(self):
        cb = FractalSceneNameCallback(show_number = True)
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        FractalMappings.SCENE().value = 0
        FractalMappings.SCENE_NAME(0).value = "Clean"
        cb.update_label(label)
        self.assertEqual(label.text, "1 Clean")

    def test_number(self):
        cb = FractalSceneNameCallback(show_name = False)
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [FractalMappings.SCENE()])

        FractalMappings.SCENE().value = 7
        cb.update_label(label)
        self.assertEqual(label.text, "Scene 8")


###############################################################################################################


class TestFractalTempoDisplayCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test(self):
        cb = FractalTempoDisplayCallback()
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        label = MockDisplayLabel()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [MAPPING_TEMPO_BPM()])

        cb.update_label(label)
        self.assertEqual(label.text, "")

        MAPPING_TEMPO_BPM().value = 120
        cb.update_label(label)
        self.assertEqual(label.text, "120 bpm")


###############################################################################################################


class TestFractalCallbackBase(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_reset(self):
        action = PRESET_SELECT(5, label = FractalLabel.NUMBER)
        appl, switch, label = setup_action(action)

        label.text = "foo"
        action.callback.reset()
        self.assertEqual(label.text, "005")

    def test_push_release(self):
        cb = FractalCallback(color = (1, 2, 3), text = None)

        self.assertEqual(cb.push(), None)
        self.assertEqual(cb.release(), None)

    def test_no_label(self):
        action = PRESET_SELECT(5)
        appl, switch, label = setup_action(action)
        action.label = None

        FractalMappings.PRESET().value = 5
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)


###############################################################################################################


class _MockStrobe:
    class StrobeController:
        def __init__(self, mapping_state, mapping_deviance, dim_factor = 0, speed = 0, color = None, max_fps = 0, reverse = None):
            self.init_calls = []
            self.mapping_state = mapping_state
            self.mapping_deviance = mapping_deviance
            self.reverse = reverse

        def init(self, appl):
            self.init_calls.append(appl)


class _MockSwitch:
    def __init__(self, actions = []):
        self.override_action = None
        self.actions = actions
        self.pixels = [0]
        self.color = None
        self.brightness = None


class TestFractalTunerDisplayCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal()

        self.period = MockPeriodCounter()
        mapping = FractalMappings.TUNER_STATE()
        mapping._FractalTunerStateMapping__period = self.period
        mapping._FractalTunerStateMapping__ignore = False

    def test(self):
        self._test(process_overridden_actions = False)
        self._test(process_overridden_actions = True)

    def _test(self, process_overridden_actions):
        element = DisplayElement()
        mapping = FractalMappings.TUNER_STATE()
        mapping.value = None

        cb = TunerDisplayCallback(
            splash_default = element,
            process_overridden_actions = process_overridden_actions
        )

        action = MockAction()
        switch = _MockSwitch(actions = [action])
        other = object()

        appl = MockController(client = MockFractalClient(), inputs = [switch, other])
        cb.init(appl)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [mapping])
        self.assertIsInstance(cb._TunerDisplayCallback__splash_tuner, TunerDisplay)

        self.assertEqual(cb.get_root(), element)

        # On
        mapping.value = 1
        cb.parameter_changed(mapping)

        self.assertEqual(switch.override_action, cb)
        self.assertNotEqual(cb.get_root(), element)

        if not process_overridden_actions:
            self.assertEqual(switch.color, Colors.WHITE)
            self.assertEqual(switch.brightness, 0)
        else:
            self.assertEqual(switch.color, None)

        # Other mappings are ignored
        cb.parameter_changed(FractalMappings.TUNER_NOTE())
        self.assertEqual(switch.override_action, cb)

        # Release without push does nothing
        cb.release()
        self.assertEqual(appl.client.set_calls, [])

        # Push / release switches off
        self.assertEqual(cb.push(), process_overridden_actions)
        self.assertEqual(cb.release(), process_overridden_actions)

        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.TUNER_ON_OFF(), "value": 0 }])
        self.assertEqual(mapping.value, 0)
        self.assertEqual(appl.client.notified, [mapping])

        # Off
        cb.parameter_changed(mapping)
        self.assertEqual(switch.override_action, None)
        self.assertEqual(action.num_reset_calls, 1)
        self.assertEqual(cb.get_root(), element)

    def test_timeout(self):
        cb = TunerDisplayCallback(splash_default = DisplayElement())
        appl = MockController(client = MockFractalClient())
        cb.init(appl)
        mapping = FractalMappings.TUNER_STATE()

        mapping.value = 1
        self.period.passed = 1501
        cb.update()

        self.assertEqual(mapping.value, 0)
        self.assertEqual(appl.client.notified, [mapping])

    def test_custom_splash(self):
        tuner = DisplayElement()
        cb = TunerDisplayCallback(splash_default = DisplayElement(), splash_tuner = tuner)

        FractalMappings.TUNER_STATE().value = 1
        self.assertEqual(cb.get_root(), tuner)

    def test_strobe(self):
        with patch.dict(sys.modules, {
            "lib.pyswitch.controller.strobe": _MockStrobe
        }):
            cb = TunerDisplayCallback(
                splash_default = DisplayElement(),
                strobe = True,
                strobe_reverse = False
            )

            strobe = cb._TunerDisplayCallback__strobe_controller
            self.assertIsInstance(strobe, _MockStrobe.StrobeController)
            self.assertEqual(strobe.mapping_state, FractalMappings.TUNER_STATE())
            self.assertEqual(strobe.mapping_deviance, FractalMappings.TUNER_DEVIANCE())
            self.assertEqual(strobe.reverse, False)

            appl = MockController(client = MockFractalClient())
            cb.init(appl)

            self.assertEqual(strobe.init_calls, [appl])
