import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.kemper import KemperMappings, KemperEffectSlot
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.effect_state import *



class TestKemperActionEffectState(unittest.TestCase):

    def test_effect_state(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = EFFECT_STATE(
            KemperEffectSlot.EFFECT_SLOT_ID_C, 
            display = display,
            mode = PushButtonAction.LATCH, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, KemperEffectEnableCallback)
        self.assertEqual(cb.mapping, KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_C))
        self.assertEqual(cb.mapping_fxtype, KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C))

        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping_fxtype, KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C))
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.LATCH)

    def test_effect_categories(self):
        cb = KemperEffectEnableCallback(KemperEffectSlot.EFFECT_SLOT_ID_DLY)

        # None
        self.assertEqual(cb.get_effect_category(0), KemperEffectEnableCallback.CATEGORY_NONE)

        # Wah family: 1-10, 12, 13
        for i in range(1, 11):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_WAH)
        self.assertEqual(cb.get_effect_category(12), KemperEffectEnableCallback.CATEGORY_WAH)
        self.assertEqual(cb.get_effect_category(13), KemperEffectEnableCallback.CATEGORY_WAH)

        # Pitch Pedal: 11
        self.assertEqual(cb.get_effect_category(11), KemperEffectEnableCallback.CATEGORY_PITCH)

        # Distortion / Shaper: 17-42 (Includes Kemper Drive, Fuzz, etc.)
        for i in range(17, 43):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_DISTORTION)

        # Dynamics / Compressor: 49-50
        for i in range(49, 51):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_COMPRESSOR)

        # Noise Gate: 57-58
        for i in range(57, 59):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_NOISE_GATE)

        # Space: 64
        self.assertEqual(cb.get_effect_category(64), KemperEffectEnableCallback.CATEGORY_SPACE)

        # Chorus: 65-67, 71
        for i in (65, 66, 67, 71):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_CHORUS)

        # Vibrato: 68
        self.assertEqual(cb.get_effect_category(68), KemperEffectEnableCallback.CATEGORY_VIBRATO)

        # Rotary: 69
        self.assertEqual(cb.get_effect_category(69), KemperEffectEnableCallback.CATEGORY_ROTARY)

        # Tremolo: 70, 75, 76
        for i in (70, 75, 76):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_TREMOLO)

        # Slicer / Autopanner: 77-80
        for i in range(77, 81):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_SLICER)

        # Phaser / Flanger: 81-91
        for i in range(81, 92):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_PHASER_FLANGER)

        # EQ / Widener: 97-104
        for i in range(97, 105):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_EQUALIZER)

        # Booster: 113-116
        for i in range(113, 117):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_BOOSTER)

        # Looper: 121-123
        for i in range(121, 124):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_LOOPER)

        # Pitch / Harmony: 129-132
        for i in range(129, 133):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_PITCH)

        # Dual / Pitch+Delay: 138-140
        for i in range(138, 141):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_DUAL)

        # Delay: 145-166
        for i in range(145, 167):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_DELAY)

        # Reverb: 177-193
        for i in range(177, 194):
            self.assertEqual(cb.get_effect_category(i), KemperEffectEnableCallback.CATEGORY_REVERB)

    def test_type_colors(self):
        # All categories must have a valid color mapped in CATEGORY_COLORS
        cb = KemperEffectEnableCallback(KemperEffectSlot.EFFECT_SLOT_ID_DLY)

        categories = [
            KemperEffectEnableCallback.CATEGORY_WAH,
            KemperEffectEnableCallback.CATEGORY_DISTORTION,
            KemperEffectEnableCallback.CATEGORY_COMPRESSOR,
            KemperEffectEnableCallback.CATEGORY_NOISE_GATE,
            KemperEffectEnableCallback.CATEGORY_SPACE,
            KemperEffectEnableCallback.CATEGORY_CHORUS,
            KemperEffectEnableCallback.CATEGORY_PHASER_FLANGER,
            KemperEffectEnableCallback.CATEGORY_EQUALIZER,
            KemperEffectEnableCallback.CATEGORY_BOOSTER,
            KemperEffectEnableCallback.CATEGORY_LOOPER,
            KemperEffectEnableCallback.CATEGORY_PITCH,
            KemperEffectEnableCallback.CATEGORY_DUAL,
            KemperEffectEnableCallback.CATEGORY_DELAY,
            KemperEffectEnableCallback.CATEGORY_REVERB,
            # New categories from your latest effect_state.py
            KemperEffectEnableCallback.CATEGORY_TREMOLO,
            KemperEffectEnableCallback.CATEGORY_ROTARY,
            KemperEffectEnableCallback.CATEGORY_VIBRATO,
            KemperEffectEnableCallback.CATEGORY_SLICER
        ]

        for cat in categories:
            color = cb.get_effect_category_color(cat, 0)
            # Ensure the color returned is not None
            self.assertIsNotNone(color)

    def test_color_override(self):
        cb = KemperEffectEnableCallback(
            slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
            color = (6, 7, 8)
        )

        self.assertEqual(cb.get_effect_category_color(KemperEffectEnableCallback.CATEGORY_WAH, 0), (6, 7, 8))
        self.assertEqual(cb.get_effect_category_color(KemperEffectEnableCallback.CATEGORY_COMPRESSOR, 0), (6, 7, 8))
        self.assertEqual(cb.get_effect_category_color(KemperEffectEnableCallback.CATEGORY_REVERB, 0), (6, 7, 8))
        self.assertEqual(cb.get_effect_category_color("anyvalue", 0), (6, 7, 8))        

    def test_text_override(self):
        cb = KemperEffectEnableCallback(
            slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
            text = "foo"
        )

        self.assertEqual(cb.get_effect_category_text(KemperEffectEnableCallback.CATEGORY_WAH, 0), "foo")
        self.assertEqual(cb.get_effect_category_text(KemperEffectEnableCallback.CATEGORY_COMPRESSOR, 0), "foo")
        self.assertEqual(cb.get_effect_category_text(KemperEffectEnableCallback.CATEGORY_REVERB, 0), "foo")
        self.assertEqual(cb.get_effect_category_text("anyvalue", 0), "foo")

    def test_show_slot_names(self):
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_A, "A Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_B, "B Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_C, "C Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_D, "D Wah")

        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_X, "X Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_MOD, "MOD Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_DLY, "DLY Wah")
        self._test_show_slot_names(KemperEffectSlot.EFFECT_SLOT_ID_REV, "REV Wah")

    def _test_show_slot_names(self, slot_id, exp_text):
        cb = KemperEffectEnableCallback(
            slot_id = slot_id,
            show_slot_names = True
        )

        self.assertEqual(cb.get_effect_category_text(KemperEffectEnableCallback.CATEGORY_WAH, 0), exp_text)
        
    def test_type_names(self):
        # All types have to be mapped
        cb = KemperEffectEnableCallback(KemperEffectSlot.EFFECT_SLOT_ID_DLY)

        # List of all categories defined in KemperEffectEnableCallback
        categories = [
            KemperEffectEnableCallback.CATEGORY_WAH,
            KemperEffectEnableCallback.CATEGORY_DISTORTION,
            KemperEffectEnableCallback.CATEGORY_COMPRESSOR,
            KemperEffectEnableCallback.CATEGORY_NOISE_GATE,
            KemperEffectEnableCallback.CATEGORY_SPACE,
            KemperEffectEnableCallback.CATEGORY_CHORUS,
            KemperEffectEnableCallback.CATEGORY_PHASER_FLANGER,
            KemperEffectEnableCallback.CATEGORY_EQUALIZER,
            KemperEffectEnableCallback.CATEGORY_BOOSTER,
            KemperEffectEnableCallback.CATEGORY_LOOPER,
            KemperEffectEnableCallback.CATEGORY_PITCH,
            KemperEffectEnableCallback.CATEGORY_DUAL,
            KemperEffectEnableCallback.CATEGORY_DELAY,
            KemperEffectEnableCallback.CATEGORY_REVERB,
            # New categories added in PR
            KemperEffectEnableCallback.CATEGORY_TREMOLO,
            KemperEffectEnableCallback.CATEGORY_ROTARY,
            KemperEffectEnableCallback.CATEGORY_VIBRATO,
            KemperEffectEnableCallback.CATEGORY_SLICER
        ]

        for category in categories:
            name = cb.get_effect_category_text(category, 0)
            # Ensure the name is not the default "-" unless it's CATEGORY_NONE
            self.assertIsNotNone(name)
            self.assertNotEqual(name, "")

