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
    from lib.pyswitch.clients.fractal_II import _decode_blocks, _FractalIITunerStateMapping
    from lib.pyswitch.controller.client import ClientParameterMapping

    from .mocks_appl import MockPeriodCounter
    from .mocks_fractal_II import *


# Messages for model 0x03 (Axe-Fx II Mark I/II), see protocol.md 4
class TestFractalIIMessages(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()
        FRACTAL_II.init({ "fractalIIModel": MODEL_AXE_FX_II })

    def tearDown(self):
        reset_fractal_II()

    def test_requests(self):
        self.assertEqual(bytes(FractalIIMappings.PRESET().request), hex_message("F0 00 01 74 03 14 12 F7"))
        self.assertEqual(bytes(FractalIIMappings.PRESET_NAME().request), hex_message("F0 00 01 74 03 0F 09 F7"))
        self.assertEqual(bytes(FractalIIMappings.SCENE().request), hex_message("F0 00 01 74 03 29 7F 50 F7"))
        self.assertEqual(bytes(FractalIIMappings.BLOCK_STATES().request), hex_message("F0 00 01 74 03 0E 08 F7"))
        self.assertEqual(bytes(FractalIIMappings.TEMPO_BPM().request), hex_message("F0 00 01 74 03 2F 29 F7"))

    def test_preset_select(self):
        mapping = FractalIIMappings.PRESET()

        mapping.set_value(699)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 3C 05 3B 04 F7"))

        mapping.set_value(0)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 3C 00 00 3A F7"))

    def test_scene_select(self):
        mapping = FractalIIMappings.SCENE()
        mapping.set_value(3)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 29 03 2C F7"))

    def test_bypass(self):
        mapping = FractalIIMappings.BYPASS(FractalIIBlock.AMP_1)

        mapping.set_value(1)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 02 6A 00 7F 01 00 00 00 01 11 F7"))

        mapping.set_value(0)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 02 6A 00 7F 01 01 00 00 01 10 F7"))

    def test_channel(self):
        mapping = FractalIIMappings.CHANNEL(FractalIIBlock.AMP_1)
        mapping.set_value(1)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 11 6A 00 01 01 7D F7"))

        # Example of the Fractal spec (Reverb 1 Y)
        mapping = FractalIIMappings.CHANNEL(FractalIIBlock.REVERB_1)
        mapping.set_value(1)
        self.assertEqual(bytes(mapping.set), hex_message("F0 00 01 74 03 11 6E 00 01 01 79 F7"))

    def test_preset_name_by_number(self):
        mapping = FractalIIPresetTargetNameMapping()
        mapping.set_target(699)
        self.assertEqual(bytes(mapping.request), bytes(sysex(0x15, [0x05, 0x3b], 0x03)))

    def test_cc(self):
        mapping = FractalIIMappings.TUNER_ON_OFF(15, 0)
        mapping.set_value(127)
        self.assertEqual(list(mapping.set), [0xb0, 15, 127])

        mapping = FractalIIMappings.TAP_TEMPO(14, 2)
        mapping.set_value(127)
        self.assertEqual(list(mapping.set), [0xb2, 14, 127])


class TestFractalIIState(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_defaults(self):
        FRACTAL_II.init({})

        self.assertEqual(FRACTAL_II.model, MODEL_AXE_FX_II_XL_PLUS)
        self.assertEqual(FRACTAL_II.bank_size, 5)
        self.assertEqual(FRACTAL_II.display_offset, 1)
        self.assertEqual(FRACTAL_II.num_presets, 768)
        self.assertEqual(FRACTAL_II.num_banks, 154)
        self.assertEqual(FRACTAL_II.preset_text(0), "001")
        self.assertEqual(FRACTAL_II.preset_text(767), "768")

        # XL+ request
        self.assertEqual(bytes(FractalIIMappings.PRESET().request), bytes(sysex(0x14, (), 0x07)))

    def test_options(self):
        mapping = FractalIIMappings.PRESET()
        mapping.set_value(5)

        FRACTAL_II.init({
            "fractalIIModel": MODEL_AXE_FX_II,
            "fractalIIBankSize": 4,
            "fractalIIPresetDisplayOffset": 0
        })

        # Only once
        FRACTAL_II.init({ "fractalIIModel": MODEL_AXE_FX_II_XL })

        self.assertEqual(FRACTAL_II.model, MODEL_AXE_FX_II)
        self.assertEqual(FRACTAL_II.num_presets, 384)
        self.assertEqual(FRACTAL_II.num_banks, 96)
        self.assertEqual(FRACTAL_II.preset_text(5), "005")

        # Mappings created before are patched (request and set message)
        self.assertEqual(bytes(mapping.request), bytes(sysex(0x14, (), 0x03)))
        self.assertEqual(bytes(mapping.set), bytes(sysex(0x3c, (0, 5), 0x03)))

        # CC mappings are not affected
        FractalIIMappings.TUNER_ON_OFF(15, 0)

    def test_same_model(self):
        mapping = FractalIIMappings.PRESET()
        request = mapping.request

        FRACTAL_II.init({ "fractalIIModel": MODEL_AXE_FX_II_XL_PLUS })
        self.assertIs(mapping.request, request)

    def test_banks(self):
        self.assertEqual(FRACTAL_II.current_bank(None), None)
        self.assertEqual(FRACTAL_II.current_bank(12), 2)

        FRACTAL_II.selected_bank = 7
        self.assertEqual(FRACTAL_II.current_bank(12), 7)

        # A preset change resets the selected bank
        FRACTAL_II.track_preset(12)
        self.assertEqual(FRACTAL_II.selected_bank, None)

        FRACTAL_II.selected_bank = 7
        FRACTAL_II.track_preset(12)
        FRACTAL_II.track_preset(None)
        self.assertEqual(FRACTAL_II.selected_bank, 7)


class TestFractalIIBlock(unittest.TestCase):

    def test_names(self):
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.COMPRESSOR_1), "Compressor 1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.AMP_2), "Amp 2")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.DRIVE_1), "Drive 1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.DRIVE_1, True), "DRV1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.FX_LOOP_1, True), "FXL1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.SYNTH_1), "Synth 1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.PITCH_2, True), "PIT2")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.GRAPHIC_EQ_3), "Graphic EQ 3")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.VOLUME_4, True), "VOL4")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.LOOPER_1), "Looper 1")
        self.assertEqual(FractalIIBlock.name(FractalIIBlock.TONE_MATCH_1, True), "TMA1")

    def test_all(self):
        # All block constants have names, the abbreviations have 3 letters
        for key in dir(FractalIIBlock):
            value = getattr(FractalIIBlock, key)
            if key.startswith("_") or not isinstance(value, int):
                continue

            self.assertIsNotNone(FractalIIBlock.name(value), key)
            self.assertEqual(len(FractalIIBlock.name(value, True)), 4, key)

    def test_invalid(self):
        self.assertIsNone(FractalIIBlock.name(99))
        self.assertIsNone(FractalIIBlock.name(171))
        self.assertIsNone(FractalIIBlock.name(139))     # Input
        self.assertIsNone(FractalIIBlock.name(140))     # Output
        self.assertIsNone(FractalIIBlock.name(None))
        self.assertIsNone(FractalIIBlock.name("AMP"))


class TestFractalIIParsing(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_preset(self):
        mapping = FractalIIMappings.PRESET()

        # Hardware capture (XL+, preset 699)
        self.assertTrue(mapping.parse(hex_message("F0 00 01 74 07 14 05 3B 28 F7")))
        self.assertEqual(mapping.value, 699)

        # Other model byte, other function, no SysEx, too short, own request
        self.assertFalse(mapping.parse(preset_answer(5, 0x03)))
        self.assertFalse(mapping.parse(sysex(0x29, [5, 0])))
        self.assertFalse(mapping.parse(bytearray([0xb0, 1, 2])))
        self.assertFalse(mapping.parse(bytearray([0xf0, 0x00])))
        self.assertFalse(mapping.parse(bytes(mapping.request)))
        self.assertEqual(mapping.value, 699)

    def test_preset_model(self):
        FRACTAL_II.init({ "fractalIIModel": MODEL_AXE_FX_II })
        mapping = FractalIIMappings.PRESET()

        self.assertFalse(mapping.parse(preset_answer(5)))
        self.assertTrue(mapping.parse(preset_answer(5, 0x03)))
        self.assertEqual(mapping.value, 5)

    def test_feedback(self):
        mapping = FractalIIMappings.SCENE()

        mapping.feedback(3)
        self.assertEqual(mapping.value, 3)

        # The next answer is skipped
        self.assertTrue(mapping.parse(sysex(0x29, [1])))
        self.assertEqual(mapping.value, 3)

        self.assertTrue(mapping.parse(sysex(0x29, [1])))
        self.assertEqual(mapping.value, 1)

    def test_scene(self):
        mapping = FractalIIMappings.SCENE()

        self.assertTrue(mapping.parse(sysex(0x29, [6])))
        self.assertEqual(mapping.value, 6)


    def test_preset_name(self):
        mapping = FractalIIMappings.PRESET_NAME()

        self.assertTrue(mapping.parse(name_answer("Cliffs of Dover")))
        self.assertEqual(mapping.value, "Cliffs of Dover")

        # Null terminated
        self.assertTrue(mapping.parse(sysex(0x0f, [ord(c) for c in "Clean"] + [0] + [0x41] * 26)))
        self.assertEqual(mapping.value, "Clean")

    def test_block_states(self):
        mapping = FractalIIMappings.BLOCK_STATES()

        # Examples of the Fractal spec: Amp 1 on/X, Cab 1 on/X, Drive 1 off/X
        self.assertTrue(mapping.parse(hex_message("F0 00 01 74 07 0E 03 4A 10 53 06 03 4E 18 63 06 02 62 30 2B 78 F7")))
        self.assertEqual(mapping.value, bytes([106, 3, 108, 3, 133, 2]))

        # mTroll captures: Amp 1 on/Y, Amp 1 bypassed
        self.assertEqual(_decode_blocks(hex_message("F0 00 01 74 07 0E 01 4A 10 53 06 F7")), bytes([106, 1]))
        self.assertEqual(_decode_blocks(hex_message("F0 00 01 74 07 0E 02 4A 10 53 06 F7")), bytes([106, 2]))

        # Generated records
        self.assertTrue(mapping.parse(block_states_answer([(170, False, False, 127, 3), (100, True, True)])))
        self.assertEqual(mapping.value, block_states([(170, False, False), (100, True, True)]))

        # Empty grid
        self.assertTrue(mapping.parse(push_message(0x0e)))
        self.assertEqual(mapping.value, b"")

    def test_target_name(self):
        mapping = FractalIIPresetTargetNameMapping()
        mapping.set_target(200)

        self.assertFalse(mapping.parse(name_by_number_answer(201, "Other")))
        self.assertEqual(mapping.value, None)

        self.assertTrue(mapping.parse(name_by_number_answer(200, "Lead")))
        self.assertEqual(mapping.value, "Lead")

        # Same target: name kept
        mapping.set_target(200)
        self.assertEqual(mapping.value, "Lead")

        # New target: name requested again
        mapping.set_target(3)
        self.assertEqual(mapping.value, None)
        self.assertEqual(bytes(mapping.request), bytes(sysex(0x15, [0, 3])))

        self.assertFalse(mapping.parse(name_answer("Current")))

    def test_target_name_unique(self):
        self.assertNotEqual(FractalIIPresetTargetNameMapping().name, FractalIIPresetTargetNameMapping().name)

    def test_tempo(self):
        mapping = FractalIIMappings.TEMPO_BPM()

        # Example of the Fractal spec: 138 BPM
        self.assertTrue(mapping.parse(sysex(0x2f, [0x0a, 0x01])))
        self.assertEqual(mapping.value, 138)

        # The own query
        self.assertFalse(mapping.parse(bytes(mapping.request)))

    def test_beat(self):
        mapping = FractalIIMappings.TEMPO_BEAT()

        self.assertTrue(mapping.parse(push_message(0x10)))
        self.assertEqual(mapping.value, 1)

        mapping.value = 127
        self.assertTrue(mapping.parse(push_message(0x10)))
        self.assertEqual(mapping.value, 0)

        self.assertFalse(mapping.parse(push_message(0x10, [0])))

    def test_tuner(self):
        note = FractalIIMappings.TUNER_NOTE()
        deviance = FractalIIMappings.TUNER_DEVIANCE()

        # Note: the device counts from A (0 = A), PySwitch from C
        self.assertTrue(note.parse(push_message(0x0d, [0, 0, 63])))
        self.assertEqual(note.value, 9)

        self.assertTrue(note.parse(push_message(0x0d, [3, 0, 63])))
        self.assertEqual(note.value, 0)

        self.assertTrue(note.parse(push_message(0x0d, [2, 0, 63])))
        self.assertEqual(note.value, 11)

        # Deviance
        self.assertTrue(deviance.parse(push_message(0x0d, [0, 0, 63])))
        self.assertEqual(deviance.value, 8192)

        self.assertTrue(deviance.parse(push_message(0x0d, [0, 0, 88])))
        self.assertEqual(deviance.value, 8192 + 4096)

        self.assertTrue(deviance.parse(push_message(0x0d, [0, 0, 0])))
        self.assertEqual(deviance.value, 0)

        self.assertTrue(deviance.parse(push_message(0x0d, [0, 0, 127])))
        self.assertEqual(deviance.value, 16383)

        # Wrong length
        self.assertFalse(note.parse(sysex(0x0d, [0, 0, 63])))


class TestFractalIIPresetName(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

    def tearDown(self):
        reset_fractal_II()

    def test_refresh(self):
        client = MockFractalIIClient()
        listener = object()
        mapping = FractalIIMappings.PRESET_NAME()

        # No preset
        mapping.refresh(client, listener, None)
        self.assertEqual(client.request_calls, [])

        # Preset known: requested
        mapping.refresh(client, listener, 5)
        self.assertEqual(client.request_calls, [{ "mapping": mapping, "listener": listener }])

        # Pending: not requested again
        client.pending.append(mapping)
        mapping.refresh(client, listener, 5)
        self.assertEqual(len(client.request_calls), 1)

        # Answer
        client.pending.remove(mapping)
        mapping.parse(name_answer("Clean"))
        self.assertEqual(mapping.value, "Clean")

        # Known: not requested again
        mapping.refresh(client, listener, 5)
        self.assertEqual(len(client.request_calls), 1)

        # Preset change: name reset and requested
        mapping.refresh(client, listener, 6)
        self.assertEqual(mapping.value, None)
        self.assertEqual(len(client.request_calls), 2)

    def test_refresh_pending(self):
        client = MockFractalIIClient()
        mapping = FractalIIMappings.PRESET_NAME()

        mapping.refresh(client, None, 5)
        client.pending.append(mapping)

        # Preset change while a request is pending: its answer is skipped
        mapping.refresh(client, None, 6)
        self.assertEqual(len(client.request_calls), 1)

        self.assertTrue(mapping.parse(name_answer("Old")))
        self.assertEqual(mapping.value, None)

        # Requested again
        client.pending.remove(mapping)
        mapping.refresh(client, None, 6)
        self.assertEqual(len(client.request_calls), 2)

        self.assertTrue(mapping.parse(name_answer("New")))
        self.assertEqual(mapping.value, "New")


class TestFractalIITunerState(unittest.TestCase):

    def setUp(self):
        reset_fractal_II()

        self.period = MockPeriodCounter()
        self.mapping = FractalIIMappings.TUNER_STATE()
        self.mapping._FractalIITunerStateMapping__period = self.period
        self.mapping._FractalIITunerStateMapping__ignore = False

    def tearDown(self):
        reset_fractal_II()

    def test(self):
        mapping = self.mapping
        client = MockFractalIIClient()
        client.pending.append(mapping)

        self.assertIsInstance(mapping, _FractalIITunerStateMapping)

        # Data comes in: on (only the first message changes the state)
        self.assertTrue(mapping.parse(push_message(0x0d, [0, 0, 63])))
        self.assertEqual(mapping.value, 1)
        self.assertFalse(mapping.parse(push_message(0x0d, [0, 0, 63])))
        self.assertFalse(mapping.parse(push_message(0x0e)))

        # No timeout
        self.period.passed = 1500
        mapping.check(client)
        self.assertEqual(mapping.value, 1)

        # Timeout
        self.period.passed = 1501
        mapping.check(client)
        self.assertEqual(mapping.value, 0)
        self.assertEqual(client.notified, [mapping])

        # Already off
        mapping.check(client)
        self.assertEqual(client.notified, [mapping])

    def test_switched(self):
        mapping = self.mapping
        client = MockFractalIIClient()

        mapping.switched(client, True)
        self.assertEqual(mapping.value, 1)
        self.assertEqual(client.notified, [])        # No request

        client.pending.append(mapping)
        mapping.switched(client, False)
        self.assertEqual(mapping.value, 0)
        self.assertEqual(client.notified, [mapping])

        # Late data is ignored for a short time
        self.period.passed = 499
        self.assertFalse(mapping.parse(push_message(0x0d, [0, 0, 63])))
        self.assertEqual(mapping.value, 0)

        self.period.passed = 500
        self.assertTrue(mapping.parse(push_message(0x0d, [0, 0, 63])))
        self.assertEqual(mapping.value, 1)
