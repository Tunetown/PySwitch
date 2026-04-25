import sys
import unittest
from unittest.mock import patch

from .mocks_lib import *

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
    from lib.pyswitch.clients.kemper import KemperEffectSlot
    from lib.pyswitch.clients.kemper.actions.effect_state_per_rig import (
        EFFECT_STATE_PER_RIG,
        KemperEffectEnablePerRigCallback,
    )
    from lib.pyswitch.controller.actions import PushButtonAction

    from .mocks_appl import MockClient


# Absolute rig IDs (bank 1, rigs 1-5)
_RIG_ACOU  = 0   # rig 1 "acou"
_RIG_CLEN  = 1   # rig 2 "clen"
_RIG_CRNC  = 2   # rig 3 "crnc"
_RIG_HEAVY = 3   # rig 4 "heavy"
_RIG_LEAD  = 4   # rig 5 "lead"

X   = KemperEffectSlot.EFFECT_SLOT_ID_X
MOD = KemperEffectSlot.EFFECT_SLOT_ID_MOD
C   = KemperEffectSlot.EFFECT_SLOT_ID_C
DLY = KemperEffectSlot.EFFECT_SLOT_ID_DLY
REV = KemperEffectSlot.EFFECT_SLOT_ID_REV


class _MockAppl:
    """Minimal mock application for callback init."""
    config = {}

    def __init__(self):
        self.client = MockClient()

    def add_updateable(self, _):
        pass


def _sw3_cb():
    """Switch 3: X slot for rigs clen, crnc, lead; disabled otherwise."""
    return KemperEffectEnablePerRigCallback(
        slot_id=None,
        rig_overrides={
            _RIG_CLEN:  X,
            _RIG_CRNC:  X,
            _RIG_LEAD:  X,
        }
    )


def _sw4_cb():
    """Switch 4: [MOD+C] for acou; X for heavy; disabled otherwise."""
    return KemperEffectEnablePerRigCallback(
        slot_id=None,
        rig_overrides={
            _RIG_ACOU:  [MOD, C],
            _RIG_HEAVY: X,
        }
    )


def _sw5_cb():
    """Switch 5: DLY for acou; [DLY+REV] for clen, crnc, heavy; disabled for lead."""
    return KemperEffectEnablePerRigCallback(
        slot_id=None,
        rig_overrides={
            _RIG_ACOU:  DLY,
            _RIG_CLEN:  [DLY, REV],
            _RIG_CRNC:  [DLY, REV],
            _RIG_HEAVY: [DLY, REV],
        }
    )


##############################################################################
# Tests for EFFECT_STATE_PER_RIG factory
##############################################################################

class TestEffectStatePerRigFactory(unittest.TestCase):

    def test_factory_returns_push_button_action(self):
        action = EFFECT_STATE_PER_RIG(
            slot_id=None,
            rig_overrides={_RIG_ACOU: X}
        )
        self.assertIsInstance(action, PushButtonAction)
        self.assertIsInstance(action.callback, KemperEffectEnablePerRigCallback)


##############################################################################
# Switch 3: flanger (X slot) — rigs clen, crnc, lead
##############################################################################

class TestSwitch3CurrentSlots(unittest.TestCase):

    def setUp(self):
        self.cb = _sw3_cb()

    def test_rig_acou_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_ACOU
        self.assertIsNone(self.cb._current_slots())

    def test_rig_clen_x(self):
        self.cb._rig_id_mapping.value = _RIG_CLEN
        self.assertEqual(self.cb._current_slots(), [X])

    def test_rig_crnc_x(self):
        self.cb._rig_id_mapping.value = _RIG_CRNC
        self.assertEqual(self.cb._current_slots(), [X])

    def test_rig_heavy_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_HEAVY
        self.assertIsNone(self.cb._current_slots())

    def test_rig_lead_x(self):
        self.cb._rig_id_mapping.value = _RIG_LEAD
        self.assertEqual(self.cb._current_slots(), [X])

    def test_rig_none_disabled(self):
        self.cb._rig_id_mapping.value = None
        self.assertIsNone(self.cb._current_slots())

    def test_unknown_rig_disabled(self):
        # Any rig not in rig_overrides must be disabled (slot_id=None default).
        self.cb._rig_id_mapping.value = 99
        self.assertIsNone(self.cb._current_slots())


##############################################################################
# Switch 4: [MOD+C] for acou, X for heavy
##############################################################################

class TestSwitch4CurrentSlots(unittest.TestCase):

    def setUp(self):
        self.cb = _sw4_cb()

    def test_rig_acou_mod_and_c(self):
        self.cb._rig_id_mapping.value = _RIG_ACOU
        self.assertEqual(self.cb._current_slots(), [MOD, C])

    def test_rig_clen_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_CLEN
        self.assertIsNone(self.cb._current_slots())

    def test_rig_crnc_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_CRNC
        self.assertIsNone(self.cb._current_slots())

    def test_rig_heavy_x(self):
        self.cb._rig_id_mapping.value = _RIG_HEAVY
        self.assertEqual(self.cb._current_slots(), [X])

    def test_rig_lead_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_LEAD
        self.assertIsNone(self.cb._current_slots())


##############################################################################
# Switch 5: DLY for acou, [DLY+REV] for clen/crnc/heavy, disabled for lead
##############################################################################

class TestSwitch5CurrentSlots(unittest.TestCase):

    def setUp(self):
        self.cb = _sw5_cb()

    def test_rig_acou_dly(self):
        self.cb._rig_id_mapping.value = _RIG_ACOU
        self.assertEqual(self.cb._current_slots(), [DLY])

    def test_rig_clen_dly_and_rev(self):
        self.cb._rig_id_mapping.value = _RIG_CLEN
        self.assertEqual(self.cb._current_slots(), [DLY, REV])

    def test_rig_crnc_dly_and_rev(self):
        self.cb._rig_id_mapping.value = _RIG_CRNC
        self.assertEqual(self.cb._current_slots(), [DLY, REV])

    def test_rig_heavy_dly_and_rev(self):
        self.cb._rig_id_mapping.value = _RIG_HEAVY
        self.assertEqual(self.cb._current_slots(), [DLY, REV])

    def test_rig_lead_disabled(self):
        self.cb._rig_id_mapping.value = _RIG_LEAD
        self.assertIsNone(self.cb._current_slots())


##############################################################################
# state_changed_by_user — multi-slot AND logic
##############################################################################

class TestMultiSlotToggle(unittest.TestCase):
    """Test the AND-logic toggle for multi-slot buttons."""

    def _init_cb(self, cb):
        appl = _MockAppl()
        cb.init(appl)
        return appl

    # ---- Switch 4, rig acou: [MOD + C] ----------------------------------- #

    def test_sw4_acou_all_on_turns_all_off(self):
        cb = _sw4_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_ACOU

        # Both ON → pressing turns both OFF
        cb._state_map(MOD).value = 1
        cb._state_map(C).value   = 1
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        sent = {c["mapping"]: c["value"] for c in appl.client.set_calls}
        self.assertEqual(sent[cb._state_map(MOD)], 0)
        self.assertEqual(sent[cb._state_map(C)],   0)

    def test_sw4_acou_not_all_on_turns_all_on(self):
        cb = _sw4_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_ACOU

        # MOD ON, C OFF → pressing turns both ON
        cb._state_map(MOD).value = 1
        cb._state_map(C).value   = 0
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        sent = {c["mapping"]: c["value"] for c in appl.client.set_calls}
        self.assertEqual(sent[cb._state_map(MOD)], 1)
        self.assertEqual(sent[cb._state_map(C)],   1)

    def test_sw4_acou_both_off_turns_all_on(self):
        cb = _sw4_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_ACOU

        cb._state_map(MOD).value = 0
        cb._state_map(C).value   = 0
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        sent = {c["mapping"]: c["value"] for c in appl.client.set_calls}
        self.assertEqual(sent[cb._state_map(MOD)], 1)
        self.assertEqual(sent[cb._state_map(C)],   1)

    # ---- Switch 5, rig clen: [DLY + REV] --------------------------------- #

    def test_sw5_clen_all_on_turns_all_off(self):
        cb = _sw5_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_CLEN

        cb._state_map(DLY).value = 1
        cb._state_map(REV).value = 1
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        sent = {c["mapping"]: c["value"] for c in appl.client.set_calls}
        self.assertEqual(sent[cb._state_map(DLY)], 0)
        self.assertEqual(sent[cb._state_map(REV)], 0)

    def test_sw5_clen_not_all_on_turns_all_on(self):
        cb = _sw5_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_CLEN

        cb._state_map(DLY).value = 0
        cb._state_map(REV).value = 1
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        sent = {c["mapping"]: c["value"] for c in appl.client.set_calls}
        self.assertEqual(sent[cb._state_map(DLY)], 1)
        self.assertEqual(sent[cb._state_map(REV)], 1)

    # ---- Disabled rig: pressing does nothing ----------------------------- #

    def test_sw3_disabled_rig_does_nothing(self):
        cb = _sw3_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_ACOU   # acou is disabled on switch 3
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        self.assertEqual(appl.client.set_calls, [])

    def test_sw4_disabled_rig_does_nothing(self):
        cb = _sw4_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_CLEN   # clen is disabled on switch 4
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        self.assertEqual(appl.client.set_calls, [])

    def test_sw5_disabled_rig_does_nothing(self):
        cb = _sw5_cb()
        appl = self._init_cb(cb)
        cb._rig_id_mapping.value = _RIG_LEAD   # lead is disabled on switch 5
        appl.client.set_calls.clear()

        cb.state_changed_by_user()

        self.assertEqual(appl.client.set_calls, [])


##############################################################################
# Regression: string keys in rig_overrides must be normalized to int
##############################################################################

class TestRigOverrideKeyNormalization(unittest.TestCase):
    """Verify that rig_overrides accepts both int and string keys.

    The RIG_ID mapping always returns an int.  String keys like "0", "1"
    must be normalized to int in __init__ so _current_slots() can look them
    up correctly.  See issue #1 (Git commit: fix-string-keys-in-rig-overrides).
    """

    def test_int_key_matches(self):
        cb = KemperEffectEnablePerRigCallback(
            slot_id=None,
            rig_overrides={0: X}
        )
        cb._rig_id_mapping.value = 0
        self.assertEqual(cb._current_slots(), [X])

    def test_string_key_matches_after_normalization(self):
        cb = KemperEffectEnablePerRigCallback(
            slot_id=None,
            rig_overrides={"0": X}
        )
        cb._rig_id_mapping.value = 0
        self.assertEqual(cb._current_slots(), [X])

    def test_mixed_string_and_int_keys(self):
        cb = KemperEffectEnablePerRigCallback(
            slot_id=None,
            rig_overrides={
                0:    DLY,
                "1":  [DLY, REV],
                "2":  [DLY, REV],
            }
        )
        cb._rig_id_mapping.value = 0
        self.assertEqual(cb._current_slots(), [DLY])

        cb._rig_id_mapping.value = 1
        self.assertEqual(cb._current_slots(), [DLY, REV])

        cb._rig_id_mapping.value = 2
        self.assertEqual(cb._current_slots(), [DLY, REV])

    def test_rig_not_in_overrides_is_still_disabled(self):
        cb = KemperEffectEnablePerRigCallback(
            slot_id=None,
            rig_overrides={"0": X}
        )
        cb._rig_id_mapping.value = 99
        self.assertIsNone(cb._current_slots())

    def test_none_rig_id_is_still_disabled(self):
        cb = KemperEffectEnablePerRigCallback(
            slot_id=None,
            rig_overrides={"0": X}
        )
        cb._rig_id_mapping.value = None
        self.assertIsNone(cb._current_slots())
