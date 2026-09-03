import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *
from .mocks_midi import test_mapping

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.kemper import *
    
    from lib.pyswitch.clients.kemper.mappings.select import *
    from lib.pyswitch.clients.kemper.mappings.rotary import *
    from lib.pyswitch.clients.kemper.mappings.freeze import *
    from lib.pyswitch.clients.kemper.mappings.effects import *
    from lib.pyswitch.clients.kemper.mappings.rig import *
    from lib.pyswitch.clients.kemper.mappings.bank import *
    from lib.pyswitch.clients.kemper.mappings.tempo import *
    from lib.pyswitch.clients.kemper.mappings.tempo_bpm import *
    from lib.pyswitch.clients.kemper.mappings.morph import *
    from lib.pyswitch.clients.kemper.mappings.amp import *
    from lib.pyswitch.clients.kemper.mappings.cabinet import *
    from lib.pyswitch.clients.kemper.mappings.looper import *
    from lib.pyswitch.clients.kemper.mappings.pedals import *
    from lib.pyswitch.clients.kemper.mappings.system import *
    from lib.pyswitch.clients.kemper.mappings.fixed_fx import *


class TestKemperMappings(unittest.TestCase):

    def test_effect_state(self):
        self._test_mapping("State A", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_A), exp_midi_channel = 0)
        self._test_mapping("State B", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_B, channel = 1), exp_midi_channel = 1)
        self._test_mapping("State C", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_C, channel = 2), exp_midi_channel = 2)
        self._test_mapping("State D", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_D, channel = 3), exp_midi_channel = 3)
        self._test_mapping("State X", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_X, channel = 4), exp_midi_channel = 4)
        self._test_mapping("State MOD", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_MOD, channel = 5), exp_midi_channel = 5)
        self._test_mapping("State DLY", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_DLY, channel = 6), exp_midi_channel = 6)
        self._test_mapping("State REV", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_REV, channel = 7), exp_midi_channel = 7)
        self._test_mapping("State DLY", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL, channel = 8), exp_midi_channel = 8)
        self._test_mapping("State REV", KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL, channel = 9), exp_midi_channel = 9)

    def test_effect_type(self):
        self._test_mapping("Type A", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A))
        self._test_mapping("Type B", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B))
        self._test_mapping("Type C", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C))
        self._test_mapping("Type D", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D))
        self._test_mapping("Type X", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X))
        self._test_mapping("Type MOD", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD))
        self._test_mapping("Type DLY", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_DLY))
        self._test_mapping("Type REV", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_REV))
        self._test_mapping("Type DLY", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL))
        self._test_mapping("Type REV", KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL))

    def test_rotary_speed(self):
        self._test_mapping("Speed A", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_A))
        self._test_mapping("Speed B", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_B))
        self._test_mapping("Speed C", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_C))
        self._test_mapping("Speed D", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_D))
        self._test_mapping("Speed X", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_X))
        self._test_mapping("Speed MOD", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_MOD))
        self._test_mapping("Speed DLY", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_DLY))
        self._test_mapping("Speed REV", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_REV))
        self._test_mapping("Speed DLY", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL))
        self._test_mapping("Speed REV", MAPPING_ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL))

    def test_freeze(self):
        self._test_mapping("Freeze A", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_A))
        self._test_mapping("Freeze B", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_B))
        self._test_mapping("Freeze C", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_C))
        self._test_mapping("Freeze D", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_D))
        self._test_mapping("Freeze X", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_X))
        self._test_mapping("Freeze MOD", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_MOD))
        self._test_mapping("Freeze DLY", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_DLY))
        self._test_mapping("Freeze REV", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_REV))
        self._test_mapping("Freeze DLY", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL))
        self._test_mapping("Freeze REV", MAPPING_FREEZE(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL))

    def test_dly_rev_mix(self):
        self._test_mapping("Mix A", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_A))
        self._test_mapping("Mix B", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_B))
        self._test_mapping("Mix C", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_C))
        self._test_mapping("Mix D", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_D))
        self._test_mapping("Mix X", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_X))
        self._test_mapping("Mix MOD", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_MOD))
        self._test_mapping("Mix DLY", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_DLY))
        self._test_mapping("Mix REV", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_REV))
        self._test_mapping("Mix DLY", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL))
        self._test_mapping("Mix REV", MAPPING_DLY_REV_MIX(KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL))

    def test_effect_button(self):
        self._test_mapping("Button 1", MAPPING_EFFECT_BUTTON(1), exp_midi_channel = 0)
        self._test_mapping("Button 2", MAPPING_EFFECT_BUTTON(2, channel = 15), exp_midi_channel = 15)
        self._test_mapping("Button 3", MAPPING_EFFECT_BUTTON(3, channel = 10), exp_midi_channel = 10)
        self._test_mapping("Button 4", MAPPING_EFFECT_BUTTON(4, channel = 14), exp_midi_channel = 14)

    def test_rig_name(self):
        self._test_mapping("Rig Name", KemperMappings.RIG_NAME(), exp_nrpn_response_length = 11)

    def test_rig_id(self):
        self._test_mapping("Rig ID", KemperMappings.RIG_ID(), exp_midi_channel = 0)
        self._test_mapping("Rig ID", KemperMappings.RIG_ID(channel = 2), exp_midi_channel = 2)
        self._test_mapping("Rig ID", KemperMappings.RIG_ID(channel = 4), exp_midi_channel = 4)

    def test_rig_date(self):
        self._test_mapping("Rig Date", KemperMappings.RIG_DATE(), exp_nrpn_response_length = 11)

    def test_tuner_mode_state(self):
        self._test_mapping("Tuner", KemperMappings.TUNER_MODE_STATE(), exp_midi_channel = 0)
        self._test_mapping("Tuner", KemperMappings.TUNER_MODE_STATE(channel = 5), exp_midi_channel = 5)

    def test_tuner_note(self):
        self._test_mapping("Tuner Note", KemperMappings.TUNER_NOTE())
        self._test_mapping("Tuner", KemperMappings.TUNER_DEVIANCE())

    def test_morph_button(self):
        self._test_mapping("Morph Button", MAPPING_MORPH_BUTTON(), exp_midi_channel = 0)
        self._test_mapping("Morph Button", MAPPING_MORPH_BUTTON(channel = 5), exp_midi_channel = 5)

    def test_morph_pedal(self):
        self._test_mapping("Morph", MAPPING_MORPH_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("Morph", MAPPING_MORPH_PEDAL(channel = 5), exp_midi_channel = 5)

    def test_rig_volume(self):
        self._test_mapping("RigVol", MAPPING_RIG_VOLUME())

    def test_rig_transpose(self):
        self._test_mapping("RigTrans", MAPPING_RIG_TRANSPOSE())

    def test_rig_comment(self):
        self._test_mapping("Comment", MAPPING_RIG_COMMENT(), exp_nrpn_response_length = 11)

    def test_amp_name(self):
        self._test_mapping("Amp Name", MAPPING_AMP_NAME(), exp_nrpn_response_length = 11)

    def test_amp_state(self):
        self._test_mapping("Amp State", MAPPING_AMP_STATE())

    def test_amp_gain(self):
        self._test_mapping("Gain", MAPPING_AMP_GAIN())

    def test_cab_name(self):
        self._test_mapping("Cab Name", MAPPING_CABINET_NAME(), exp_nrpn_response_length = 11)

    def test_cab_state(self):
        self._test_mapping("Cab State", MAPPING_CABINET_STATE())

    def test_chane_bank(self):
        self._test_mapping("Next", MAPPING_NEXT_BANK(), exp_midi_channel = 0)
        self._test_mapping("Next", MAPPING_NEXT_BANK(channel = 7), exp_midi_channel = 7)
        self._test_mapping("Prev", MAPPING_PREVIOUS_BANK(channel = 0), exp_midi_channel = 0)
        self._test_mapping("Prev", MAPPING_PREVIOUS_BANK(channel = 8), exp_midi_channel = 8)

    def test_select_rig(self):
        self._test_mapping("Rig", MAPPING_RIG_SELECT(rig = 2), exp_midi_channel = 0)
        self._test_mapping("Rig", MAPPING_RIG_SELECT(rig = 2, channel = 4), exp_midi_channel = 4)

    def test_protocol_sense(self):
        self._test_mapping("Sense", KemperMappings.BIDIRECTIONAL_SENSING(), exp_nrpn_response_length = 10)

    def test_tempo_display(self):
        self._test_mapping("Tempo", MAPPING_TEMPO_DISPLAY(), exp_nrpn_response_length = 11)

    def test_tap_tempo(self):
        self._test_mapping("Tap", MAPPING_TAP_TEMPO(), exp_midi_channel = 0)
        self._test_mapping("Tap", MAPPING_TAP_TEMPO(channel = 6), exp_midi_channel = 6)

    def test_tempo_bpm(self):
        self._test_mapping("BPM", MAPPING_TEMPO_BPM())

    def test_freeze_global(self):
        self._test_mapping("Freeze", MAPPING_FREEZE_ALL_GLOBAL(), exp_midi_channel = 0)
        self._test_mapping("Freeze", MAPPING_FREEZE_ALL_GLOBAL(channel = 4), exp_midi_channel = 4)

    def test_looper(self):
        self._test_mapping("Loop", MAPPING_LOOPER_REC_PLAY_OVERDUB())
        self._test_mapping("Loop", MAPPING_LOOPER_STOP())
        self._test_mapping("Loop", MAPPING_LOOPER_TRIGGER())
        self._test_mapping("Loop", MAPPING_LOOPER_REVERSE())
        self._test_mapping("Loop", MAPPING_LOOPER_HALF_SPEED())
        self._test_mapping("Loop", MAPPING_LOOPER_CANCEL())
        self._test_mapping("Loop", MAPPING_LOOPER_ERASE())

    def test_pedals(self):
        self._test_mapping("Vol", MAPPING_VOLUME_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("Vol", MAPPING_VOLUME_PEDAL(channel = 8), exp_midi_channel = 8)
        self._test_mapping("Wah", MAPPING_WAH_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("Wah", MAPPING_WAH_PEDAL(channel = 9), exp_midi_channel = 9)
        self._test_mapping("Pitch", MAPPING_PITCH_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("Pitch", MAPPING_PITCH_PEDAL(channel = 10), exp_midi_channel = 10)

        self._test_mapping("DlMix", MAPPING_DELAY_MIX_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("DlMix", MAPPING_DELAY_MIX_PEDAL(channel = 9), exp_midi_channel = 9)
        self._test_mapping("Feed", MAPPING_DELAY_FEEDBACK_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("Feed", MAPPING_DELAY_FEEDBACK_PEDAL(channel = 9), exp_midi_channel = 9)
        self._test_mapping("RvMix", MAPPING_REVERB_MIX_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("RvMix", MAPPING_REVERB_MIX_PEDAL(channel = 7), exp_midi_channel = 7)
        self._test_mapping("RvTime", MAPPING_REVERB_TIME_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("RvTime", MAPPING_REVERB_TIME_PEDAL(channel = 15), exp_midi_channel = 15)
        self._test_mapping("OutVol", MAPPING_VOLUME_OUTPUT_PEDAL(), exp_midi_channel = 0)
        self._test_mapping("OutVol", MAPPING_VOLUME_OUTPUT_PEDAL(channel = 11), exp_midi_channel = 11)

    def test_system(self):
        self._test_mapping("MainVol", MAPPING_MAIN_VOLUME())
        self._test_mapping("MonVol", MAPPING_MONITOR_VOLUME())
        self._test_mapping("LoopVol", MAPPING_LOOPER_VOLUME())
        self._test_mapping("SpaceInt", MAPPING_SPACE_INTENSITY())

    def test_fixed_fx(self):
        self._test_mapping("TranspSt", MAPPING_FIXED_TRANSPOSE())
        self._test_mapping("FixGateSt", MAPPING_FIXED_GATE())
        self._test_mapping("FixCompSt", MAPPING_FIXED_COMP())
        self._test_mapping("FixBoost", MAPPING_FIXED_BOOST())
        self._test_mapping("FixWah", MAPPING_FIXED_WAH())
        self._test_mapping("FixChor", MAPPING_FIXED_CHORUS())

        self._test_mapping("FixAir", MAPPING_FIXED_AIR())
        self._test_mapping("FixTracker", MAPPING_FIXED_DBL_TRACKER())


    #############################################################################################


    def _test_mapping(self, exp_name, mapping, exp_midi_channel = 0, exp_nrpn_set_length = 13, exp_nrpn_request_length = 11, exp_nrpn_response_length = 13):
        test_mapping(self,
                     mapping, 
                     exp_name = exp_name,
                     exp_nrpn_set_length = exp_nrpn_set_length, 
                     exp_nrpn_request_length = exp_nrpn_request_length, 
                     exp_nrpn_response_length = exp_nrpn_response_length,
                     exp_midi_channel = exp_midi_channel,
                     kemper_nrpn = True)