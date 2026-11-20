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
    from lib.pyswitch.clients.fractal import _checksum, _sysex, _inc_dec, _both, _action_text
    from lib.pyswitch.clients.fractal.mappings.preset import FractalPresetTargetNameMapping
    from lib.pyswitch.clients.fractal.mappings.effects import *
    from lib.pyswitch.clients.fractal.mappings.tempo import *
    from lib.pyswitch.clients.fractal.mappings.looper import *

    from .mocks_appl import MockPeriodCounter
    from .mocks_fractal import *


class TestFractalHelpers(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_checksum(self):
        self.assertEqual(_checksum([0xf0, 0x00, 0x01, 0x74, 0x10, 0x0c, 0x7f], 7), 0x66)
        self.assertEqual(_checksum([0xf0, 0x00, 0x01, 0x74, 0x10, 0x0c, 0x7f, 0x22], 7), 0x66)

    def test_sysex(self):
        self.assertEqual(_sysex(0x0c, (0x7f,)), [0xf0, 0x00, 0x01, 0x74, 0x11, 0x0c, 0x7f, 0x67, 0xf7])
        self.assertEqual(_sysex(0x13), [0xf0, 0x00, 0x01, 0x74, 0x11, 0x13, checksum([0xf0, 0x00, 0x01, 0x74, 0x11, 0x13]), 0xf7])

    def test_effect_ids(self):
        self.assertEqual(FractalBlock.effect_id(FractalBlock.COMPRESSOR, 1), 46)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.AMP, 1), 58)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.AMP, 2), 59)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.DRIVE, 1), 118)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.LOOPER, 1), LOOPER_BLOCK_ID)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.RETURN, 4), 189)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.INPUT, 1), 37)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.OUTPUT, 2), 43)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.MULTIPLEXER, 1), 191)
        self.assertEqual(FractalBlock.effect_id(FractalBlock.IR_PLAYER, 2), 196)

    def test_block_tables(self):
        self.assertEqual(len(FractalBlock.NAMES), FractalBlock.IR_PLAYER + 1)
        self.assertEqual(len(FractalBlock.ABBREVIATIONS), FractalBlock.IR_PLAYER + 1)
        self.assertEqual(len(FractalBlock.SPECIAL_IDS), 4)

        for name in FractalBlock.NAMES:
            self.assertLessEqual(len(name), 10)

        self.assertEqual(FractalBlock.NAMES[FractalBlock.DRIVE], "Drive")
        self.assertEqual(FractalBlock.ABBREVIATIONS[FractalBlock.DRIVE], "DRV")
        self.assertEqual(FractalChannel.NAMES[FractalChannel.F], "F")

    def test_inc_dec(self):
        self.assertEqual(_inc_dec(3, 1, True, 0, 7), 4)
        self.assertEqual(_inc_dec(7, 1, True, 0, 7), 0)
        self.assertEqual(_inc_dec(7, 1, False, 0, 7), 7)
        self.assertEqual(_inc_dec(0, -1, True, 0, 7), 7)
        self.assertEqual(_inc_dec(0, -1, False, 0, 7), 0)
        self.assertEqual(_inc_dec(5, 2, True, 2, 6), 2)
        self.assertEqual(_inc_dec(3, -2, False, 2, 6), 2)

    def test_both(self):
        self.assertEqual(_both("A", "B", True, False), "[A] B")
        self.assertEqual(_both("A", "B", False, True), "A [B]")
        self.assertEqual(_both("A", "B", False, False), "A/B")

    def test_action_text(self):
        self.assertEqual(_action_text("Preset", 1), "Preset +1")
        self.assertEqual(_action_text("Preset", -2), "Preset -2")


###############################################################################################################


class TestFractalState(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def tearDown(self):
        reset_fractal()

    def test_defaults(self):
        self.assertEqual(FRACTAL.model, MODEL_FM3)
        self.assertEqual(FRACTAL.bank_size, 5)
        self.assertEqual(FRACTAL.display_offset, 0)
        self.assertEqual(FRACTAL.num_presets, 512)
        self.assertEqual(FRACTAL.num_banks, 103)
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_num_presets(self):
        FRACTAL.model = MODEL_AXE_FX_III
        self.assertEqual(FRACTAL.num_presets, 1024)

        FRACTAL.model = MODEL_FM9
        self.assertEqual(FRACTAL.num_presets, 512)

        FRACTAL.bank_size = 4
        self.assertEqual(FRACTAL.num_banks, 128)

    def test_preset_text(self):
        self.assertEqual(FRACTAL.preset_text(0), "000")
        self.assertEqual(FRACTAL.preset_text(42), "042")
        self.assertEqual(FRACTAL.preset_text(511), "511")

        FRACTAL.display_offset = 1
        self.assertEqual(FRACTAL.preset_text(0), "001")
        self.assertEqual(FRACTAL.preset_text(1023), "1024")

    def test_current_bank(self):
        self.assertEqual(FRACTAL.current_bank(None), None)
        self.assertEqual(FRACTAL.current_bank(0), 0)
        self.assertEqual(FRACTAL.current_bank(4), 0)
        self.assertEqual(FRACTAL.current_bank(5), 1)

        FRACTAL.selected_bank = 7
        self.assertEqual(FRACTAL.current_bank(5), 7)
        self.assertEqual(FRACTAL.current_bank(None), 7)

    def test_track_preset(self):
        name_0 = FractalMappings.SCENE_NAME(0)
        name_5 = FractalMappings.SCENE_NAME(5)

        FRACTAL.track_preset(3)

        name_0.value = "foo"
        name_5.value = "bar"
        FRACTAL.selected_bank = 4

        # Same preset or None: no change
        FRACTAL.track_preset(3)
        FRACTAL.track_preset(None)

        self.assertEqual(name_0.value, "foo")
        self.assertEqual(FRACTAL.selected_bank, 4)

        # Change
        FRACTAL.track_preset(4)

        self.assertEqual(name_0.value, None)
        self.assertEqual(name_5.value, None)
        self.assertEqual(FRACTAL.selected_bank, None)

    def test_is_target_answer(self):
        msg_1 = preset_answer(3, "foo")
        msg_2 = preset_answer(3, "foo")

        self.assertEqual(FRACTAL.is_target_answer(msg_1, 3), False)

        FRACTAL.pending_names.append(3)

        self.assertEqual(FRACTAL.is_target_answer(msg_1, 3), True)
        self.assertEqual(FRACTAL.pending_names, [])

        # The same message object is recognized again, another one is not
        self.assertEqual(FRACTAL.is_target_answer(msg_1, 3), True)
        self.assertEqual(FRACTAL.is_target_answer(msg_2, 3), False)

    def test_init(self):
        mapping = FractalMappings.SCENE()
        mapping.set_value(0)

        FRACTAL.init({
            "fractalModel": MODEL_AXE_FX_III,
            "fractalBankSize": 3,
            "fractalPresetDisplayOffset": 1
        })

        self.assertEqual(FRACTAL.model, MODEL_AXE_FX_III)
        self.assertEqual(FRACTAL.bank_size, 3)
        self.assertEqual(FRACTAL.display_offset, 1)

        # Mappings have been patched
        self.assertEqual(list(mapping.request), list(sysex(0x0c, [0x7f], model = 0x10)))
        self.assertEqual(list(mapping.set), list(sysex(0x0c, [0x00], model = 0x10)))

        # Mappings created later use the model directly
        self.assertEqual(list(FractalMappings.STATUS_DUMP().request), list(sysex(0x13, [], model = 0x10)))

        # Only once
        FRACTAL.init({
            "fractalModel": MODEL_FM9,
            "fractalBankSize": 7
        })

        self.assertEqual(FRACTAL.model, MODEL_AXE_FX_III)
        self.assertEqual(FRACTAL.bank_size, 3)

    def test_init_defaults(self):
        mapping = FractalMappings.SCENE()

        FRACTAL.init({})

        self.assertEqual(FRACTAL.model, MODEL_FM3)
        self.assertEqual(FRACTAL.bank_size, 5)
        self.assertEqual(FRACTAL.display_offset, 0)
        self.assertEqual(list(mapping.request), list(sysex(0x0c, [0x7f])))


###############################################################################################################


class TestFractalParameterMapping(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_singleton(self):
        self.assertIs(FractalMappings.SCENE(), FractalMappings.SCENE())
        self.assertIs(FractalMappings.PRESET_SELECT(2), FractalMappings.PRESET_SELECT(2))
        self.assertIsNot(FractalMappings.PRESET_SELECT(2), FractalMappings.PRESET_SELECT(3))
        self.assertIs(FractalMappings.SCENE_NAME(3), FractalMappings.SCENE_NAME(3))

    def test_messages(self):
        self.assertEqual(list(FractalMappings.PRESET().request), list(sysex(0x0d, [0x7f, 0x7f])))
        self.assertEqual(FractalMappings.PRESET().set, None)
        self.assertEqual(FractalMappings.PRESET_NAME().request, None)
        self.assertEqual(list(FractalMappings.SCENE().request), list(sysex(0x0c, [0x7f])))
        self.assertEqual(list(FractalMappings.SCENE_NAME(6).request), list(sysex(0x0e, [6])))
        self.assertEqual(list(FractalMappings.STATUS_DUMP().request), list(sysex(0x13)))
        self.assertEqual(list(FractalMappings.TUNER_ON_OFF().set), list(sysex(0x11, [0])))
        self.assertEqual(FractalMappings.TUNER_STATE().request, None)
        self.assertEqual(list(MAPPING_TEMPO_BPM().request), list(sysex(0x14, [0x7f, 0x7f])))
        self.assertEqual(list(MAPPING_TAP_TEMPO().set), list(sysex(0x10)))
        self.assertEqual(list(MAPPING_LOOPER_STATE().request), list(sysex(0x0f, [0x7f])))
        self.assertEqual(list(MAPPING_LOOPER_BUTTON(LOOPER_BUTTON_ONCE).set), list(sysex(0x0f, [3])))
        self.assertEqual(list(MAPPING_BLOCK_BYPASS(200).set), list(sysex(0x0a, [72, 1, 0])))
        self.assertEqual(list(MAPPING_BLOCK_CHANNEL(118).set), list(sysex(0x0b, [118, 0, 0])))

    def test_parse_7bit(self):
        mapping = FractalMappings.SCENE()

        self.assertEqual(mapping.parse(sysex(0x0c, [5])), True)
        self.assertEqual(mapping.value, 5)

        # The model byte is not compared
        self.assertEqual(mapping.parse(sysex(0x0c, [6], model = 0x10)), True)
        self.assertEqual(mapping.value, 6)

        # Not matching
        self.assertEqual(mapping.parse(sysex(0x0e, [1])), False)
        self.assertEqual(mapping.parse(sysex(0x64, [0x0c, 0x01])), False)
        self.assertEqual(mapping.parse(bytearray([0xb0, 0x0c, 0x01])), False)
        self.assertEqual(mapping.parse(bytearray([0xf0, 0x00, 0x01, 0xf7])), False)
        self.assertEqual(mapping.value, 6)

        # Truncated message
        self.assertEqual(mapping.parse(bytearray([0xf0, 0x00, 0x01, 0x74, 0x11, 0x0c])), False)
        self.assertEqual(mapping.value, 6)

        # Other answers are not taken as preset
        self.assertEqual(FractalMappings.PRESET().parse(sysex(0x0c, [5])), False)

    def test_parse_14bit(self):
        mapping = FractalMappings.PRESET()

        self.assertEqual(mapping.parse(preset_answer(300, "foo")), True)
        self.assertEqual(mapping.value, 300)

        mapping = MAPPING_TEMPO_BPM()

        self.assertEqual(mapping.parse(sysex(0x14, [0x78, 0x00])), True)
        self.assertEqual(mapping.value, 120)

        self.assertEqual(mapping.parse(sysex(0x14, [0x7a, 0x01])), True)
        self.assertEqual(mapping.value, 250)

    def test_parse_string(self):
        mapping = FractalMappings.PRESET_NAME()

        self.assertEqual(mapping.parse(preset_answer(3, "  My Preset")), True)
        self.assertEqual(mapping.value, "My Preset")

        # Cut at the first NUL
        self.assertEqual(mapping.parse(sysex(0x0d, [3, 0] + name32("Other", fill = 0))), True)
        self.assertEqual(mapping.value, "Other")

        mapping = FractalMappings.SCENE_NAME(2)

        self.assertEqual(mapping.parse(sysex(0x0e, [2] + name32("Lead"))), True)
        self.assertEqual(mapping.value, "Lead")

        # Other scene
        self.assertEqual(mapping.parse(sysex(0x0e, [3] + name32("Clean"))), False)
        self.assertEqual(mapping.value, "Lead")

    def test_parse_raw(self):
        mapping = FractalMappings.STATUS_DUMP()

        payload = dump([(58, False, 1, 4), (118, True, 0, 4)])

        self.assertEqual(mapping.parse(sysex(0x13, payload)), True)
        self.assertEqual(mapping.value, payload)
        self.assertIsInstance(mapping.value, bytes)

        self.assertEqual(mapping.parse(sysex(0x13, [])), True)
        self.assertEqual(mapping.value, b'')

    def test_parse_length(self):
        mapping = FractalMappings.TUNER_NOTE()

        self.assertEqual(mapping.parse(push_message(0x11, [4, 0, 63])), True)
        self.assertEqual(mapping.value, 4)

        # Tuner on/off set message (with checksum) is not parsed
        self.assertEqual(mapping.parse(sysex(0x11, [1])), False)
        self.assertEqual(mapping.value, 4)

    def test_feedback(self):
        mapping = FractalMappings.SCENE()
        mapping.value = 1

        mapping.feedback(4)
        self.assertEqual(mapping.value, 4)

        # Next answer is skipped, but parsed
        self.assertEqual(mapping.parse(sysex(0x0c, [1])), True)
        self.assertEqual(mapping.value, 4)

        self.assertEqual(mapping.parse(sysex(0x0c, [2])), True)
        self.assertEqual(mapping.value, 2)

    def test_set_value_7bit(self):
        mapping = FractalMappings.SCENE()

        mapping.set_value(5)
        self.assertEqual(list(mapping.set), list(sysex(0x0c, [5])))

        mapping = MAPPING_BLOCK_CHANNEL(118)

        mapping.set_value(3)
        self.assertEqual(list(mapping.set), list(sysex(0x0b, [118, 0, 3])))

    def test_set_value_14bit(self):
        mapping = MAPPING_TEMPO_BPM()

        mapping.set_value(200)
        self.assertEqual(list(mapping.set), list(sysex(0x14, [72, 1])))

    def test_set_value_inverted(self):
        mapping = MAPPING_BLOCK_BYPASS(118)

        mapping.set_value(1)
        self.assertEqual(list(mapping.set), list(sysex(0x0a, [118, 0, 0])))

        mapping.set_value(0)
        self.assertEqual(list(mapping.set), list(sysex(0x0a, [118, 0, 1])))

    def test_set_value_fixed(self):
        mapping = MAPPING_LOOPER_BUTTON(LOOPER_BUTTON_REVERSE)

        mapping.set_value(0)
        self.assertEqual(list(mapping.set), list(sysex(0x0f, [4])))

        mapping = MAPPING_TAP_TEMPO()

        mapping.set_value(0)
        self.assertEqual(list(mapping.set), list(sysex(0x10)))

    def test_set_value_preset_select(self):
        mapping = FractalMappings.PRESET_SELECT(2)

        mapping.set_value(133)
        self.assertEqual([list(m) for m in mapping.set], [[0xb2, 0x00, 0x01], [0xc2, 0x05]])

        mapping.set_value(1023)
        self.assertEqual([list(m) for m in mapping.set], [[0xb2, 0x00, 0x07], [0xc2, 0x7f]])

        mapping.set_value(7)
        self.assertEqual([list(m) for m in mapping.set], [[0xb2, 0x00, 0x00], [0xc2, 0x07]])

    def test_set_value_cc(self):
        mapping = FractalParameterMapping.get(
            name = "Test CC",
            set = (0xb0, 0x10, 0x00)
        )

        mapping.set_value(99)
        self.assertEqual(list(mapping.set), [0xb0, 0x10, 99])


###############################################################################################################


class TestFractalPresetMappings(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_target_name_request(self):
        mapping = FractalPresetTargetNameMapping()

        self.assertEqual(mapping.target, 0)
        self.assertEqual(list(mapping.request), list(sysex(0x0d, [0, 0])))

        mapping.set_target(300)

        self.assertEqual(mapping.target, 300)
        self.assertEqual(list(mapping.request), list(sysex(0x0d, [0x2c, 0x02])))

    def test_target_name_unique(self):
        m1 = FractalPresetTargetNameMapping()
        m2 = FractalPresetTargetNameMapping()

        self.assertNotEqual(m1.name, m2.name)

    def test_target_name_send_request(self):
        mapping = FractalPresetTargetNameMapping()
        mapping.set_target(5)
        client = MockFractalClient()

        mapping.send_request(client, "listener")
        mapping.send_request(client, "listener")

        self.assertEqual(FRACTAL.pending_names, [5])
        self.assertEqual(client.request_calls, [
            { "mapping": mapping, "listener": "listener" },
            { "mapping": mapping, "listener": "listener" }
        ])

        mapping.discard()
        self.assertEqual(FRACTAL.pending_names, [])

        mapping.discard()
        self.assertEqual(FRACTAL.pending_names, [])

    def test_target_answer_order_target_first(self):
        self._test_target_answer(target_first = True)

    def test_target_answer_order_current_first(self):
        self._test_target_answer(target_first = False)

    def _test_target_answer(self, target_first):
        reset_fractal()

        current = FractalMappings.PRESET()
        current_name = FractalMappings.PRESET_NAME()
        target = FractalPresetTargetNameMapping()

        current.value = 1
        current_name.value = "Current"

        target.set_target(9)
        target.send_request(MockFractalClient(), None)

        msg = preset_answer(9, "Target")

        if target_first:
            self.assertEqual(target.parse(msg), True)
            self.assertEqual(current.parse(msg), False)
            self.assertEqual(current_name.parse(msg), False)
        else:
            self.assertEqual(current.parse(msg), False)
            self.assertEqual(current_name.parse(msg), False)
            self.assertEqual(target.parse(msg), True)

        self.assertEqual(target.value, "Target")
        self.assertEqual(current.value, 1)
        self.assertEqual(current_name.value, "Current")
        self.assertEqual(FRACTAL.pending_names, [])

        # Then an answer for the current preset with the same number comes in
        msg = preset_answer(9, "Target")

        self.assertEqual(current.parse(msg), True)
        self.assertEqual(current_name.parse(msg), True)
        self.assertEqual(current.value, 9)
        self.assertEqual(current_name.value, "Target")

    def test_target_name_previous(self):
        mapping = FractalPresetTargetNameMapping()
        mapping.set_target(4)
        mapping.value = "Four"

        mapping.set_target(5)
        self.assertEqual(mapping.value, None)

        # Answer for the previous target completes the request without value
        self.assertEqual(mapping.parse(preset_answer(4, "Four")), True)
        self.assertEqual(mapping.value, None)

        # Only once
        self.assertEqual(mapping.parse(preset_answer(4, "Four")), False)

        # Other presets
        self.assertEqual(mapping.parse(preset_answer(6, "Six")), False)
        self.assertEqual(mapping.parse(sysex(0x0c, [1])), False)

        self.assertEqual(mapping.parse(preset_answer(5, "Five")), True)
        self.assertEqual(mapping.value, "Five")

        # Same target: no change
        mapping.set_target(5)
        self.assertEqual(mapping.value, "Five")

    def test_target_name_model(self):
        mapping = FractalPresetTargetNameMapping()
        mapping.set_target(2)

        mapping.set_model(MODEL_FM9)
        self.assertEqual(list(mapping.request), list(sysex(0x0d, [2, 0], model = MODEL_FM9)))

        mapping.set_model(MODEL_FM3)


###############################################################################################################


class TestFractalTunerMappings(unittest.TestCase):

    def setUp(self):
        reset_fractal()

        self.mapping = FractalMappings.TUNER_STATE()
        self.period = MockPeriodCounter()
        self.mapping._FractalTunerStateMapping__period = self.period
        self.mapping._FractalTunerStateMapping__ignore = False

    def test_state(self):
        mapping = self.mapping
        client = MockFractalClient()

        # First push data: change
        self.assertEqual(mapping.parse(push_message(0x11, [9, 1, 63])), True)
        self.assertEqual(mapping.value, 1)
        self.assertEqual(self.period.num_reset_calls, 1)

        # Further data: no change notification
        self.assertEqual(mapping.parse(push_message(0x11, [9, 1, 63])), False)
        self.assertEqual(mapping.value, 1)
        self.assertEqual(self.period.num_reset_calls, 2)

        # Not tuner data
        self.assertEqual(mapping.parse(sysex(0x11, [1])), False)

        # No timeout yet
        self.period.passed = 1500
        mapping.check(client)
        self.assertEqual(mapping.value, 1)
        self.assertEqual(client.notified, [])

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
        client = MockFractalClient()

        mapping.switched(client, True)
        self.assertEqual(mapping.value, 1)
        self.assertEqual(client.notified, [mapping])

        mapping.switched(client, False)
        self.assertEqual(mapping.value, 0)
        self.assertEqual(client.notified, [mapping, mapping])

        # Late push data is ignored
        self.period.passed = 499
        self.assertEqual(mapping.parse(push_message(0x11, [9, 1, 63])), False)
        self.assertEqual(mapping.value, 0)

        self.period.passed = 500
        self.assertEqual(mapping.parse(push_message(0x11, [9, 1, 63])), True)
        self.assertEqual(mapping.value, 1)

    def test_no_request(self):
        mapping = self.mapping

        class Client:
            def get_matching_request(self, mapping):
                return None

        mapping.switched(Client(), True)
        self.assertEqual(mapping.value, 1)

    def test_note(self):
        mapping = FractalMappings.TUNER_NOTE()

        self.assertEqual(mapping.parse(push_message(0x11, [11, 5, 63])), True)
        self.assertEqual(mapping.value, 11)

    def test_deviance(self):
        mapping = FractalMappings.TUNER_DEVIANCE()

        def test(cents, expected):
            self.assertEqual(mapping.parse(push_message(0x11, [9, 1, cents])), True)
            self.assertEqual(mapping.value, expected)

        test(63, 8192)
        test(64, 8192 + 163)
        test(62, 8192 - 163)
        test(88, 8192 + 4096)
        test(113, 16383)
        test(127, 16383)
        test(13, 0)
        test(0, 0)


###############################################################################################################


class TestFractalTempoMappings(unittest.TestCase):

    def setUp(self):
        reset_fractal()

    def test_beat(self):
        mapping = MAPPING_TEMPO_BEAT()

        self.assertEqual(mapping.parse(push_message(0x10)), True)
        self.assertEqual(mapping.value, 1)

        self.assertEqual(mapping.parse(push_message(0x10)), True)
        self.assertEqual(mapping.value, 2)

        # Tap message (with checksum) is not a beat
        self.assertEqual(mapping.parse(sysex(0x10)), False)
        self.assertEqual(mapping.value, 2)

        mapping.value = 127
        self.assertEqual(mapping.parse(push_message(0x10)), True)
        self.assertEqual(mapping.value, 0)
