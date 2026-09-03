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
    from lib.pyswitch.clients.kemper import *
    from lib.pyswitch.clients.kemper.callbacks.convert_volume import *


class TestKemper(unittest.TestCase):

    def test_nrpn_value(self):
        self.assertEqual(NRPN_VALUE(0), 0)
        self.assertEqual(NRPN_VALUE(0.1), 1638)
        self.assertEqual(NRPN_VALUE(0.5), 8191)
        self.assertEqual(NRPN_VALUE(0.9), 14744)
        self.assertEqual(NRPN_VALUE(1), 16383)


##########################################################################################################


    def test_effect_slots_consistency(self):
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_A, 0)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_B, 1)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_C, 2)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_D, 3)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_X, 4)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_MOD, 5)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_DLY, 6)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_REV, 7)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL, 8)
        self.assertEqual(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL, 9)

        self.assertEqual(len(KemperEffectSlot.EFFECT_SLOT_NAME), 10)
        self.assertEqual(len(KemperEffectSlot.CC_EFFECT_SLOT_ENABLE), 10)
        self.assertEqual(len(KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE), 10)
        self.assertEqual(len(KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES), 10)


##########################################################################################################


    def test_convert_volume(self):
        # No offset
        self._test_convert_volume(0, 0, "-94.9dB")
        self._test_convert_volume(30, 0, "-16.8dB")
        self._test_convert_volume(40, 0, "-14.4dB")
        self._test_convert_volume(50, 0, "-12.0dB")
        self._test_convert_volume(60, 0, "-9.6dB")
        self._test_convert_volume(70, 0, "-7.2dB")
        self._test_convert_volume(80, 0, "-4.8dB")
        self._test_convert_volume(90, 0, "-2.4dB")
        self._test_convert_volume(100, 0, "0.0dB")

        # With offset
        self._test_convert_volume(0, 12, "-82.9dB")
        self._test_convert_volume(30, 12, "-4.8dB")
        self._test_convert_volume(40, 12, "-2.4dB")
        self._test_convert_volume(50, 12, "0.0dB")
        self._test_convert_volume(60, 12, "+2.4dB")
        self._test_convert_volume(70, 12, "+4.8dB")
        self._test_convert_volume(80, 12, "+7.2dB")
        self._test_convert_volume(90, 12, "+9.6dB")
        self._test_convert_volume(100, 12, "+12.0dB")

    def _test_convert_volume(self, value, offset, exp_result):
        self.assertEqual(convert_volume(value, offset), exp_result)
