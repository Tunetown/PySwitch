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
    from lib.pyswitch.clients.fractal.actions.tuner import *
    from lib.pyswitch.clients.fractal.actions.tap_tempo import *
    from lib.pyswitch.clients.fractal.actions.looper import *
    from lib.pyswitch.clients.fractal.actions.preset_select_encoder import *
    from lib.pyswitch.clients.fractal.actions.tempo_bpm import *
    from lib.pyswitch.clients.fractal.mappings.tempo import *
    from lib.pyswitch.clients.fractal.mappings.looper import *
    from lib.pyswitch.controller.actions import Action
    from lib.pyswitch.controller.actions.EncoderAction import EncoderAction
    from lib.pyswitch.colors import Colors

    from .mocks_appl import MockPeriodCounter, MockController
    from .mocks_fractal import *


class TestFractalActionTuner(unittest.TestCase):

    def setUp(self):
        reset_fractal()

        self.period = MockPeriodCounter()
        mapping = FractalMappings.TUNER_STATE()
        mapping._FractalTunerStateMapping__period = self.period
        mapping._FractalTunerStateMapping__ignore = False

    def test_tuner(self):
        action = TUNER(id = 5)
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.TUNER_STATE()

        self.assertIsInstance(action, Action)
        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [mapping])

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(switch.colors[0], COLOR_UTILITY)
        self.assertEqual(label.text, "Tuner")

        # On
        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.TUNER_ON_OFF(), "value": 1 }])
        self.assertEqual(mapping.value, 1)
        self.assertEqual(appl.client.notified, [mapping])
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        # Off
        action.push()
        self.assertEqual(appl.client.set_calls[-1], { "mapping": FractalMappings.TUNER_ON_OFF(), "value": 0 })
        self.assertEqual(mapping.value, 0)
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_timeout(self):
        action = TUNER()
        appl, switch, label = setup_action(action)
        mapping = FractalMappings.TUNER_STATE()

        mapping.value = 1
        self.period.passed = 2000

        action.callback.update()
        self.assertEqual(mapping.value, 0)
        self.assertEqual(appl.client.notified, [mapping])

    def test_text(self):
        action = TUNER(text = "Tune", color = (1, 2, 3))
        appl, switch, label = setup_action(action)

        action.update_displays()
        self.assertEqual(label.text, "Tune")
        self.assertEqual(switch.colors[0], (1, 2, 3))


###############################################################################################################


class TestFractalActionTapTempo(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_tap(self):
        action = TAP_TEMPO()
        appl, switch, label = setup_action(action)
        cb = action.callback

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [MAPPING_TEMPO_BEAT()])

        period = MockPeriodCounter()
        period.interval = 100
        cb._FractalTapTempoCallback__flash = period

        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_DIM)
        self.assertEqual(switch.colors[0], COLOR_UTILITY)
        self.assertEqual(label.text, "Tap Tempo")

        action.push()
        action.release()
        self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_TAP_TEMPO(), "value": 0 }])

        # Beat: flash
        MAPPING_TEMPO_BEAT().parse(push_message(0x10))
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)
        self.assertEqual(period.num_reset_calls, 1)

        # Same beat value: no new flash
        action.update_displays()
        self.assertEqual(period.num_reset_calls, 1)

        period.passed = 100
        cb.update()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        period.passed = 101
        cb.update()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

        # Not flashing: no update
        cb.update()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_bpm_label(self):
        action = TAP_TEMPO(label = FractalLabel.BPM)
        appl, switch, label = setup_action(action)

        self.assertEqual([c["mapping"] for c in appl.client.register_calls], [MAPPING_TEMPO_BEAT(), MAPPING_TEMPO_BPM()])

        action.update_displays()
        self.assertEqual(label.text, "")

        MAPPING_TEMPO_BPM().value = 133
        action.update_displays()
        self.assertEqual(label.text, "133 bpm")


###############################################################################################################


class TestFractalActionLooper(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def _create(self, factory, **kwargs):
        action = factory(**kwargs)
        appl, switch, label = setup_action(action)
        return action, appl, switch, label

    def _set(self, state, has_looper = True):
        MAPPING_LOOPER_STATE().value = state
        FractalMappings.STATUS_DUMP().value = dump([(LOOPER_BLOCK_ID, False, 0, 1)] if has_looper else [(58, False, 0, 4)])

    def test_buttons(self):
        def test(factory, button, color, text):
            action, appl, switch, label = self._create(factory)

            self.assertEqual([c["mapping"] for c in appl.client.register_calls], [MAPPING_LOOPER_STATE(), FractalMappings.STATUS_DUMP()])

            action.update_displays()
            self.assertEqual(switch.colors[0], color)
            self.assertEqual(label.text, text)

            action.push()
            self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_LOOPER_BUTTON(button), "value": 0 }])
            action.release()

        test(LOOPER_RECORD, LOOPER_BUTTON_RECORD, Colors.RED, "Record")
        test(LOOPER_PLAY_STOP, LOOPER_BUTTON_PLAY, Colors.GREEN, "Play")
        test(LOOPER_UNDO, LOOPER_BUTTON_UNDO, Colors.PURPLE, "Undo")
        test(LOOPER_ONCE, LOOPER_BUTTON_ONCE, Colors.BLUE, "Once")
        test(LOOPER_REVERSE, LOOPER_BUTTON_REVERSE, Colors.ORANGE, "Reverse")
        test(LOOPER_HALF_SPEED, LOOPER_BUTTON_HALF, Colors.PINK, "Half")

    def test_no_looper(self):
        action, appl, switch, label = self._create(LOOPER_PLAY_STOP)

        # No values
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        # State but no dump
        MAPPING_LOOPER_STATE().value = LOOPER_STATE_PLAY
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        self._set(LOOPER_STATE_PLAY, has_looper = False)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_OFF)

        self._set(LOOPER_STATE_PLAY)
        action.update_displays()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

    def test_states(self):
        def test(factory, state, led):
            action, appl, switch, label = self._create(factory)
            self._set(state)
            action.update_displays()
            self.assertEqual(switch.brightnesses[0], led)

        test(LOOPER_RECORD, 0, LED_DIM)
        test(LOOPER_RECORD, LOOPER_STATE_RECORD, LED_BRIGHT)
        test(LOOPER_RECORD, LOOPER_STATE_PLAY | LOOPER_STATE_OVERDUB, LED_BRIGHT)
        test(LOOPER_PLAY_STOP, LOOPER_STATE_RECORD, LED_DIM)
        test(LOOPER_PLAY_STOP, LOOPER_STATE_PLAY, LED_BRIGHT)
        test(LOOPER_UNDO, 0x3f, LED_DIM)
        test(LOOPER_ONCE, LOOPER_STATE_ONCE, LED_BRIGHT)
        test(LOOPER_ONCE, LOOPER_STATE_PLAY, LED_DIM)
        test(LOOPER_REVERSE, LOOPER_STATE_REVERSE, LED_BRIGHT)
        test(LOOPER_HALF_SPEED, LOOPER_STATE_HALF, LED_BRIGHT)
        test(LOOPER_HALF_SPEED, LOOPER_STATE_REVERSE, LED_DIM)

    def test_undo_pressed(self):
        action, appl, switch, label = self._create(LOOPER_UNDO)
        self._set(0)

        action.push()
        self.assertEqual(switch.brightnesses[0], LED_BRIGHT)

        action.release()
        self.assertEqual(switch.brightnesses[0], LED_DIM)

    def test_overdub(self):
        action, appl, switch, label = self._create(LOOPER_RECORD)
        self._set(LOOPER_STATE_PLAY | LOOPER_STATE_OVERDUB)

        action.update_displays()
        self.assertEqual(label.text, "Overdub")
        self.assertEqual(switch.colors[0], Colors.YELLOW)

        # Custom color is used for both
        action, appl, switch, label = self._create(LOOPER_RECORD, color = (1, 2, 3), text = "Rec")

        action.update_displays()
        self.assertEqual(label.text, "Rec")
        self.assertEqual(switch.colors[0], (1, 2, 3))

    def test_play_stop_label(self):
        action, appl, switch, label = self._create(LOOPER_PLAY_STOP)

        self._set(LOOPER_STATE_PLAY)
        action.update_displays()
        self.assertEqual(label.text, "Stop")

        self._set(0)
        action.update_displays()
        self.assertEqual(label.text, "Play")


###############################################################################################################


class TestFractalEncoders(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def tearDown(self):
        reset_fractal()

    def test_preset_select(self):
        action = ENCODER_PRESET_SELECT(midi_channel = 4, step_width = 1)
        self.assertIsInstance(action, EncoderAction)

        appl = MockController(client = MockFractalClient(), config = { "fractalModel": MODEL_AXE_FX_III })
        action.init(appl)

        self.assertEqual(action._EncoderAction__max_value, 1023)
        self.assertEqual(action._EncoderAction__min_value, 0)

        action.update()
        self.assertIn(FractalMappings.PRESET(), [c["mapping"] for c in appl.client.request_calls])

        FractalMappings.PRESET().value = 10
        FRACTAL.selected_bank = 4

        action.process(0)
        action.process(2)

        self.assertEqual(appl.client.set_calls, [{ "mapping": FractalMappings.PRESET_SELECT(3), "value": 12 }])
        self.assertEqual(FractalMappings.PRESET().value, 12)
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_preset_select_convert(self):
        action = ENCODER_PRESET_SELECT()
        self.assertEqual(action._EncoderAction__convert_value(7), "Preset 007")

    def test_bpm(self):
        action = ENCODER_BPM()
        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_TEMPO_BPM())
        self.assertEqual(action._EncoderAction__min_value, 24)
        self.assertEqual(action._EncoderAction__max_value, 250)
        self.assertEqual(action._EncoderAction__convert_value(120), "120 bpm")

        appl = MockController(client = MockFractalClient(), config = { "fractalBankSize": 7 })
        action.init(appl)
        self.assertEqual(FRACTAL.bank_size, 7)

        MAPPING_TEMPO_BPM().value = 120
        action.process(0)
        action.process(-1)

        self.assertEqual(appl.client.set_calls, [{ "mapping": MAPPING_TEMPO_BPM(), "value": 119 }])
