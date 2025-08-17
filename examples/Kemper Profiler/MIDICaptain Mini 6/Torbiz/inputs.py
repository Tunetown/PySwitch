from lib.pyswitch.clients.kemper.actions.morph import MORPH_DISPLAY
from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from lib.pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.hardware.devices.pa_midicaptain_mini_6 import *


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            RIG_SELECT(
                rig = 1, 
                rig_btn_morph = True, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            RIG_SELECT(
                rig = 2, 
                rig_btn_morph = True, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            RIG_SELECT(
                rig = 3, 
                rig_btn_morph = True, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            MORPH_DISPLAY(),
            
        ],
        "actionsHold": [
            BANK_UP(
                use_leds = False
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 4, 
                rig_btn_morph = True, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 5, 
                rig_btn_morph = True, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            TAP_TEMPO(
                use_leds = False
            ),
            SHOW_TEMPO(
                change_display = DISPLAY_RIG_NAME, 
                text = '{bpm} bpm'
            ),
            MORPH_DISPLAY(),
            
        ],
        "actionsHold": [
            BANK_DOWN(
                use_leds = False
            ),
            
        ],
        
    },
    
]
