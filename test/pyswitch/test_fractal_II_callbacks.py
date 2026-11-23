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
    from lib.pyswitch.clients.fractal_II.callbacks.preset_name import *
    from lib.pyswitch.clients.fractal_II.callbacks.scene_name import *
    from lib.pyswitch.clients.fractal_II.callbacks.tempo_bpm import *
    from lib.pyswitch.clients.fractal_II.callbacks.tuner_display import *
    from lib.pyswitch.ui.ui import DisplayElement
    from lib.pyswitch.ui.elements import TunerDisplay
    from lib.pyswitch.colors import Colors

    from .mocks_appl import MockController, MockPeriodCounter, MockAction
    from .mocks_ui import MockDisplayLabel
    from .mocks_fractal_II import *


class TestFractalIIPresetNameCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_name(self):
        cb = FractalIIPresetNameCallback(default_text = "-")
        appl = MockController(client = MockFractalIIClient())
        cb.init(appl)
        label = MockDisplayLabel()
        preset = FractalIIMappings.PRESET()
        name = FractalIIMappings.PRESET_NAME()

        # Only the preset is registered (polled)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [preset])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [preset])

        # Preset known: name requested
        preset.value = 4
        cb.update()
        self.assertEqual([c["mapping"] for c in appl.client.request_calls], [preset, preset, name])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        name.parse(name_answer("Clean"))
        cb.update_label(label)
        self.assertEqual(label.text, "Clean")

    def test_number(self):
        cb = FractalIIPresetNameCallback(show_name = False, show_number = True)
        appl = MockController(client = MockFractalIIClient(), config = { "fractalIIPresetDisplayOffset": 0 })
        cb.init(appl)
        label = MockDisplayLabel()

        FractalIIMappings.PRESET().value = 4
        cb.update()
        cb.update_label(label)
        self.assertEqual(label.text, "004")

        self.assertNotIn(FractalIIMappings.PRESET_NAME(), [c["mapping"] for c in appl.client.request_calls])

    def test_both(self):
        cb = FractalIIPresetNameCallback(show_number = True)
        appl = MockController(client = MockFractalIIClient())
        cb.init(appl)
        label = MockDisplayLabel()

        FractalIIMappings.PRESET().value = 4
        FractalIIMappings.PRESET_NAME().value = "Clean"
        cb.update_label(label)
        self.assertEqual(label.text, "005 Clean")


class TestFractalIISceneNameCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        cb = FractalIISceneNameCallback(default_text = "-")
        appl = MockController(client = MockFractalIIClient())
        cb.init(appl)
        label = MockDisplayLabel()
        scene = FractalIIMappings.SCENE()

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [scene])

        cb.update_label(label)
        self.assertEqual(label.text, "-")

        scene.value = 2
        cb.update_label(label)
        self.assertEqual(label.text, "Scene 3")


class TestFractalIICallback(unittest.TestCase):

    def test_push_release(self):
        cb = FractalIICallback(color = (1, 1, 1), text = None)
        cb.push()
        cb.release()


class TestFractalIITempoDisplayCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        cb = FractalIITempoDisplayCallback()
        appl = MockController(client = MockFractalIIClient(), config = { "fractalIIModel": MODEL_AXE_FX_II })
        cb.init(appl)
        label = MockDisplayLabel()
        bpm = FractalIIMappings.TEMPO_BPM()

        self.assertEqual(FRACTAL_II.model, MODEL_AXE_FX_II)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [bpm])

        bpm.value = 120
        cb.update_label(label)
        self.assertEqual(label.text, "120 bpm")

        bpm.value = None
        cb.update_label(label)


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


class TestFractalIITunerDisplayCallback(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

        self.period = MockPeriodCounter()
        mapping = FractalIIMappings.TUNER_STATE()
        mapping._FractalIITunerStateMapping__period = self.period
        mapping._FractalIITunerStateMapping__ignore = False

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        self._test(process_overridden_actions = False)
        self._test(process_overridden_actions = True)

    def _test(self, process_overridden_actions):
        element = DisplayElement()
        mapping = FractalIIMappings.TUNER_STATE()
        mapping.value = None

        cb = FractalIITunerDisplayCallback(
            splash_default = element,
            process_overridden_actions = process_overridden_actions,
            tuner_cc = 16,
            midi_channel = 2
        )

        action = MockAction()
        switch = _MockSwitch(actions = [action])
        other = object()

        appl = MockController(client = MockFractalIIClient(), inputs = [switch, other])
        appl.client.pending.append(mapping)
        cb.init(appl)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [mapping])
        self.assertIsInstance(cb._FractalIITunerDisplayCallback__splash_tuner, TunerDisplay)

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
        cb.parameter_changed(FractalIIMappings.TUNER_NOTE())
        self.assertEqual(switch.override_action, cb)

        # Release without push does nothing
        cb.release()
        self.assertEqual(appl.client.set_calls, [])

        # Push / release switches off (tuner CC)
        self.assertEqual(cb.push(), process_overridden_actions)
        self.assertEqual(cb.release(), process_overridden_actions)

        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalIIMappings.TUNER_ON_OFF(16, 1), "value": 0 }])
        self.assertEqual(mapping.value, 0)
        self.assertEqual(appl.client.notified, [mapping])

        # Off
        cb.parameter_changed(mapping)
        self.assertEqual(switch.override_action, None)
        self.assertEqual(action.num_reset_calls, 1)
        self.assertEqual(cb.get_root(), element)

    def test_timeout(self):
        cb = FractalIITunerDisplayCallback(splash_default = DisplayElement())
        appl = MockController(client = MockFractalIIClient())
        cb.init(appl)
        mapping = FractalIIMappings.TUNER_STATE()
        appl.client.pending.append(mapping)

        mapping.value = 1
        self.period.passed = 1501
        cb.update()

        self.assertEqual(mapping.value, 0)
        self.assertEqual(appl.client.notified, [mapping])

    def test_custom_splash(self):
        tuner = DisplayElement()
        cb = FractalIITunerDisplayCallback(splash_default = DisplayElement(), splash_tuner = tuner)

        FractalIIMappings.TUNER_STATE().value = 1
        self.assertEqual(cb.get_root(), tuner)

    def test_strobe(self):
        with patch.dict(sys.modules, {
            "lib.pyswitch.controller.strobe": _MockStrobe
        }):
            cb = FractalIITunerDisplayCallback(
                splash_default = DisplayElement(),
                strobe = True,
                strobe_reverse = False
            )

            strobe = cb._FractalIITunerDisplayCallback__strobe_controller
            self.assertIsInstance(strobe, _MockStrobe.StrobeController)
            self.assertEqual(strobe.mapping_state, FractalIIMappings.TUNER_STATE())
            self.assertEqual(strobe.mapping_deviance, FractalIIMappings.TUNER_DEVIANCE())
            self.assertEqual(strobe.reverse, False)

            appl = MockController(client = MockFractalIIClient())
            cb.init(appl)

            self.assertEqual(strobe.init_calls, [appl])
