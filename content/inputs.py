from pyswitch.clients.kemper.actions.amp import AMP_GAIN
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.local.actions.encoder_button import ENCODER_BUTTON
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from pyswitch.hardware.devices.pa_midicaptain_10 import *

_accept = ENCODER_BUTTON()

_cancel = ENCODER_BUTTON()

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            AMP_GAIN(
                accept_action = _accept, 
                cancel_action = _cancel, 
                preview_display = DISPLAY_RIG_NAME, 
                step_width = 40
            ),
            
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
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            TAP_TEMPO(
                use_leds = False
            ),
            SHOW_TEMPO(
                change_display = DISPLAY_RIG_NAME, 
                text = '{bpm} bpm'
            ),
            
        ],
        "actionsHold": [
            TUNER_MODE(
                use_leds = False, 
                text = 'Tuner'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actionsHold": [
            BANK_DOWN(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = 'Bank dn'
            ),
            
        ],
        "actions": [
            RIG_SELECT(
                rig = 1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT(
                rig = 3, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT(
                rig = 4, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actionsHold": [
            BANK_UP(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = 'Bank up'
            ),
            
        ],
        "actions": [
            RIG_SELECT(
                rig = 5, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [
            _accept,
            
        ],
        "actionsHold": [
            _cancel,
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [],
        
    },
    
]
