from lib.pyswitch.clients.kemper.actions.morph import MORPH_BUTTON
from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper import KemperEffectSlot
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
            TUNER_MODE(
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            TAP_TEMPO(
                color = Colors.LIGHT_GREEN
            ),
            SHOW_TEMPO(
                display = DISPLAY_HEADER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = '{bpm} bpm'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            MORPH_BUTTON(
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    
]
