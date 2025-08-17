from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.encoder_button import ENCODER_BUTTON
from lib.pyswitch.controller.actions.AnalogAction import AnalogAction
from lib.pyswitch.controller.actions.EncoderAction import EncoderAction
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_GAIN
from lib.pyswitch.clients.kemper.mappings.pedals import MAPPING_WAH_PEDAL
from lib.pyswitch.clients.kemper.mappings.pedals import MAPPING_VOLUME_PEDAL
from lib.pyswitch.clients.kemper import KemperMappings
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *

_encoder_apply = ENCODER_BUTTON()

_encoder_cancel = ENCODER_BUTTON()


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [
            AnalogAction(
                mapping = MAPPING_VOLUME_PEDAL()
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2,
        "actions": [
            AnalogAction(
                mapping = MAPPING_WAH_PEDAL(), 
                auto_calibrate = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            EncoderAction(
                mapping = MAPPING_AMP_GAIN(), 
                accept_action = _encoder_apply, 
                cancel_action = _encoder_cancel, 
                preview_display = DISPLAY_RIG_NAME, 
                preview_reset_mapping = KemperMappings.RIG_ID()
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [
            _encoder_apply,
            
        ],
        "actionsHold": [
            _encoder_cancel,
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_HEADER_3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        "actionsHold": [
            TUNER_MODE(),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        "actionsHold": [
            BANK_UP(),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 5, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        "actionsHold": [
            BANK_DOWN(),
            
        ],
        
    },
    
]