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
    from lib.pyswitch.clients.fractal_am4 import _pack, _unpack, _float, _uint, _inc_dec, _action_text

    from .mocks_fractal_am4 import *


# Messages as captured from AM4-Edit by mcp-midi-control (SYSEX-MAP.md), plus the mode select messages confirmed
# by forum users. The client must produce exactly these bytes.
GOLDEN = {
    "name table": "F0 00 01 74 15 01 4E 01 00 00 1F 00 00 00 00 00 41 F7",
    "amp bypass on": "F0 00 01 74 15 01 3A 00 03 00 01 00 00 00 04 00 00 00 10 03 78 46 F7",
    "amp bypass off": "F0 00 01 74 15 01 3A 00 03 00 01 00 00 00 04 00 00 00 00 00 00 2D F7",
    "drive bypass on": "F0 00 01 74 15 01 76 00 03 00 01 00 00 00 04 00 00 00 10 03 78 0A F7",
    "reverb bypass on": "F0 00 01 74 15 01 42 00 03 00 01 00 00 00 04 00 00 00 10 03 78 3E F7",
    "name A01": "F0 00 01 74 15 01 4E 01 0B 00 12 00 00 00 04 00 00 00 00 00 00 43 F7",
    "name A02": "F0 00 01 74 15 01 4E 01 0B 00 12 00 00 00 04 00 00 40 00 00 00 03 F7",
    "name Z04": "F0 00 01 74 15 01 4E 01 0B 00 12 00 00 00 04 00 33 40 00 00 00 30 F7",
    "mode presets": "F0 00 01 74 15 12 48 4A F7",
    "mode scenes": "F0 00 01 74 15 12 49 4B F7",
    "mode effects": "F0 00 01 74 15 12 4A 48 F7",
    "mode amp": "F0 00 01 74 15 12 58 5A F7",
    "mode tuner": "F0 00 01 74 15 12 18 1A F7",
}


class TestFractalAM4Mappings(unittest.TestCase):

    def setUp(self):
        reset_fractal_am4()

    def test_golden_messages(self):
        self.assertEqual(bytearray(FractalAM4Mappings.NAME_TABLE().request), hex_message(GOLDEN["name table"]))

        for block, name in ((FractalAM4Block.AMP, "amp"), (FractalAM4Block.DRIVE, "drive"), (FractalAM4Block.REVERB, "reverb")):
            mapping = FractalAM4Mappings.BYPASS(block)
            mapping.set_value(1)
            self.assertEqual(bytearray(mapping.set), hex_message(GOLDEN[name + " bypass on"]))

        mapping = FractalAM4Mappings.BYPASS(FractalAM4Block.AMP)
        mapping.set_value(0)
        self.assertEqual(bytearray(mapping.set), hex_message(GOLDEN["amp bypass off"]))

        self.assertEqual(bytearray(FractalAM4Mappings.PRESET_NAME(0).request), hex_message(GOLDEN["name A01"]))
        self.assertEqual(bytearray(FractalAM4Mappings.PRESET_NAME(1).request), hex_message(GOLDEN["name A02"]))
        self.assertEqual(bytearray(FractalAM4Mappings.PRESET_NAME(103).request), hex_message(GOLDEN["name Z04"]))

        mode = FractalAM4Mappings.MODE()
        for value, name in ((FractalAM4Mode.PRESETS, "presets"), (FractalAM4Mode.SCENES, "scenes"), (FractalAM4Mode.EFFECTS, "effects"), (FractalAM4Mode.AMP, "amp"), (FractalAM4Mode.TUNER, "tuner")):
            mode.set_value(value)
            self.assertEqual(bytearray(mode.set), hex_message(GOLDEN["mode " + name]))

    def test_computed_messages(self):
        # Computed with the rules of spec/am4/protocol.md 3 (the same rules reproduce all golden messages)
        self.assertEqual(bytearray(FractalAM4Mappings.PRESET().request), hex_message("F0 00 01 74 15 14 04 F7"))
        self.assertEqual(bytearray(FractalAM4Mappings.BYPASS(FractalAM4Block.AMP).request), hex_message("F0 00 01 74 15 01 3A 00 03 00 0D 00 00 00 00 00 25 F7"))
        self.assertEqual(bytearray(FractalAM4Mappings.BYPASS(FractalAM4Block.GATE).request), hex_message("F0 00 01 74 15 01 12 01 03 00 0D 00 00 00 00 00 0C F7"))

        scene = FractalAM4Mappings.SCENE_SELECT()
        expected = ("00 00 00 00 00 56", "00 40 00 00 00 16", "01 00 00 00 00 57", "01 40 00 00 00 17")
        for i in range(4):
            scene.set_value(i)
            self.assertEqual(bytearray(scene.set), hex_message("F0 00 01 74 15 01 4E 01 0D 00 01 00 00 00 04 00 " + expected[i] + " F7"))

        preset = FractalAM4Mappings.PRESET_SELECT()
        preset.set_value(0)
        self.assertEqual(bytearray(preset.set), hex_message("F0 00 01 74 15 01 4E 01 0A 00 01 00 00 00 04 00 00 00 00 00 00 51 F7"))
        preset.set_value(1)
        self.assertEqual(bytearray(preset.set), hex_message("F0 00 01 74 15 01 4E 01 0A 00 01 00 00 00 04 00 00 00 10 03 78 3A F7"))
        preset.set_value(103)
        self.assertEqual(bytearray(preset.set), hex_message("F0 00 01 74 15 01 4E 01 0A 00 01 00 00 00 04 00 00 00 19 64 10 3C F7"))

    def test_singletons(self):
        self.assertIs(FractalAM4Mappings.PRESET(), FractalAM4Mappings.PRESET())
        self.assertIs(FractalAM4Mappings.BYPASS(0x3a), FractalAM4Mappings.BYPASS(0x3a))
        self.assertIsNot(FractalAM4Mappings.BYPASS(0x3a), FractalAM4Mappings.BYPASS(0x76))
        self.assertIs(FractalAM4Mappings.PRESET_NAME(5), FractalAM4Mappings.PRESET_NAME(5))
        self.assertIn(FractalAM4Mappings.PRESET_NAME(5), FRACTAL_AM4.preset_names)

    def test_pack_unpack(self):
        for raw in (b"\x00\x00\x80\x3f", b"\x01\x00\x00\x00", b"\xff\x80\x7f\x01", bytes(range(1, 33)), b"AM4 Gig Rig" + b" " * 21):
            packed = _pack(raw)
            self.assertTrue(all(b < 0x80 for b in packed))
            self.assertEqual(bytes(_unpack(packed + [0], 0, len(raw))), bytes(raw))

        self.assertEqual(len(_pack(bytes(32))), 37)
        self.assertEqual(_float(1.0), b"\x00\x00\x80\x3f")
        self.assertEqual(_uint(2), b"\x02\x00\x00\x00")

    def test_preset(self):
        mapping = FractalAM4Mappings.PRESET()

        self.assertTrue(mapping.parse(preset_answer(0)))
        self.assertEqual(mapping.value, 0)

        self.assertTrue(mapping.parse(preset_answer(103)))
        self.assertEqual(mapping.value, 103)

        # Other messages
        self.assertFalse(mapping.parse(sysex(0x12, [0x48])))
        self.assertFalse(mapping.parse(bytearray([0xb0, 0x01, 0x02])))
        self.assertFalse(mapping.parse(sysex(0x14)[:6]))
        self.assertFalse(mapping.parse(None))
        self.assertEqual(mapping.value, 103)

    def test_feedback(self):
        mapping = FractalAM4Mappings.PRESET()

        mapping.feedback(7)
        self.assertEqual(mapping.value, 7)

        # The next answer is skipped, the one after is used
        self.assertTrue(mapping.parse(preset_answer(3)))
        self.assertEqual(mapping.value, 7)

        self.assertTrue(mapping.parse(preset_answer(3)))
        self.assertEqual(mapping.value, 3)

    def test_name_table(self):
        mapping = FractalAM4Mappings.NAME_TABLE()

        msg = name_table_answer(2, "AM4 Gig Rig", ("Clean Double", "Pushed AC", "Jumped Plexi", "IIC+ Hot Lead"), (0x76, 0x3a, 0x46, 0x42))
        self.assertEqual(len(msg), 238)

        self.assertTrue(mapping.parse(msg))
        self.assertEqual(mapping.value, (2, "AM4 Gig Rig", ("Clean Double", "Pushed AC", "Jumped Plexi", "IIC+ Hot Lead"), (0x76, 0x3a, 0x46, 0x42)))

        # Empty names and slots
        self.assertTrue(mapping.parse(name_table_answer(0, "", ("", "", "", ""), (0, 0, 0, 0))))
        self.assertEqual(mapping.value, (0, "", ("", "", "", ""), (0, 0, 0, 0)))

        # Wrong length
        self.assertFalse(mapping.parse(msg[:-3] + msg[-2:]))

        # Other message of function 0x01
        self.assertFalse(mapping.parse(bypass_answer(0x3a, True)))

    def test_bypass(self):
        mapping = FractalAM4Mappings.BYPASS(FractalAM4Block.AMP)

        msg = bypass_answer(FractalAM4Block.AMP, True)
        self.assertEqual(len(msg), 64)

        self.assertTrue(mapping.parse(msg))
        self.assertEqual(mapping.value, 1)

        self.assertTrue(mapping.parse(bypass_answer(FractalAM4Block.AMP, False)))
        self.assertEqual(mapping.value, 0)

        # Other block
        self.assertFalse(mapping.parse(bypass_answer(FractalAM4Block.DRIVE, True)))

        # Write echo (action 0x01 instead of 0x0d)
        echo = bytearray(bypass_answer(FractalAM4Block.AMP, True))
        echo[10] = 0x01
        self.assertFalse(mapping.parse(echo))

    def test_preset_name_captured(self):
        client = MockFractalAM4Client()

        mapping = FractalAM4Mappings.PRESET_NAME(0)
        FRACTAL_AM4.request_name(client, mapping, None)

        # The captured answer is 63 bytes long
        self.assertTrue(mapping.parse(hex_message(NAME_ANSWER_GIG_RIG)))
        self.assertEqual(mapping.value, "AM4 Gig Rig")
        self.assertEqual(FRACTAL_AM4.pending_name, None)

        # Answers are only accepted by the mapping of the outstanding request
        self.assertFalse(mapping.parse(hex_message(NAME_ANSWER_EMPTY)))

        mapping_empty = FractalAM4Mappings.PRESET_NAME(93)
        FRACTAL_AM4.request_name(client, mapping_empty, None)
        self.assertFalse(mapping.parse(hex_message(NAME_ANSWER_EMPTY)))
        self.assertTrue(mapping_empty.parse(hex_message(NAME_ANSWER_EMPTY)))
        self.assertEqual(mapping_empty.value, "<EMPTY>")

    def test_request_name(self):
        client = MockFractalAM4Client()
        m1 = FractalAM4Mappings.PRESET_NAME(1)
        m2 = FractalAM4Mappings.PRESET_NAME(2)

        FRACTAL_AM4.request_name(client, m1, "L1")
        self.assertEqual(FRACTAL_AM4.pending_name, m1)
        self.assertEqual(client.request_calls, [{ "mapping": m1, "listener": "L1" }])

        # m1 still outstanding: m2 waits
        client.pending = [m1]
        FRACTAL_AM4.request_name(client, m2, "L2")
        self.assertEqual(FRACTAL_AM4.pending_name, m1)
        self.assertEqual(len(client.request_calls), 1)

        # The same mapping again: request (adds the listener)
        FRACTAL_AM4.request_name(client, m1, "L1")
        self.assertEqual(len(client.request_calls), 2)

        # m1 terminated (no answer): m2 is requested
        client.pending = []
        FRACTAL_AM4.request_name(client, m2, "L2")
        self.assertEqual(FRACTAL_AM4.pending_name, m2)
        self.assertEqual(client.request_calls[-1], { "mapping": m2, "listener": "L2" })

    def test_track_preset(self):
        client = MockFractalAM4Client()
        mapping = FractalAM4Mappings.PRESET_NAME(4)
        unknown = FractalAM4Mappings.PRESET_NAME(6)
        self.assertEqual(FRACTAL_AM4.needs_name(unknown), True)

        mapping.value = "Foo"
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), False)

        # Preset change: known names are read again, but kept until then
        FRACTAL_AM4.track_preset(None)
        FRACTAL_AM4.track_preset(1)
        self.assertEqual(mapping.value, "Foo")
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), True)
        self.assertEqual(FRACTAL_AM4.stale_names, [mapping])

        FRACTAL_AM4.request_name(client, mapping, "L")
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), False)

        # Same preset: nothing changes
        FRACTAL_AM4.track_preset(1)
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), False)

        FRACTAL_AM4.track_preset(2)
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), True)

        # Another request outstanding: the stale mark is kept
        client.pending = [unknown]
        FRACTAL_AM4.request_name(client, unknown, "L")
        FRACTAL_AM4.request_name(client, mapping, "L")
        self.assertEqual(FRACTAL_AM4.needs_name(mapping), True)

    def test_helpers(self):
        self.assertEqual(location_text(0), "A01")
        self.assertEqual(location_text(7), "B04")
        self.assertEqual(location_text(103), "Z04")

        self.assertEqual(FractalAM4Block.name(FractalAM4Block.DRIVE), "Drive")
        self.assertEqual(FractalAM4Block.name(FractalAM4Block.DRIVE, True), "DRV")
        self.assertEqual(FractalAM4Block.name(FractalAM4Block.GATE, True), "GTE")
        self.assertEqual(FractalAM4Block.name(0x99), None)

        self.assertEqual(FractalAM4Mode.name(FractalAM4Mode.TUNER), "Tuner")
        self.assertEqual(FractalAM4Mode.name(FractalAM4Mode.AMP), "Amp")

        self.assertEqual(_inc_dec(3, 1, True, 0, 3), 0)
        self.assertEqual(_inc_dec(3, 1, False, 0, 3), 3)
        self.assertEqual(_inc_dec(0, -1, True, 0, 3), 3)
        self.assertEqual(_inc_dec(0, -1, False, 0, 3), 0)
        self.assertEqual(_inc_dec(1, 1, True, 0, 3), 2)

        self.assertEqual(_action_text("Scene", 1), "Scene +1")
        self.assertEqual(_action_text("Scene", -2), "Scene -2")
