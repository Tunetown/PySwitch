from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.effect_state_extended_names import EFFECT_STATE_EXT
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.param_change import PARAMETER_UP_DOWN
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.effects import MAPPING_DLY_REV_MIX
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.hardware.devices.pa_midicaptain_nano_4 import *


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
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
                display = DISPLAY_HEADER_2, 
                text = 'Tuner'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = -256, 
                change_display = DISPLAY_RIG_NAME, 
                text = '{val}%'
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = 256, 
                change_display = DISPLAY_RIG_NAME, 
                text = '{val}%'
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    
]
