from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.freeze import MAPPING_FREEZE
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
                display = DISPLAY_HEADER_1, 
                text = "Tap|Tune"
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            BINARY_SWITCH(
                mapping = MAPPING_FREEZE(
                    KemperEffectSlot.EFFECT_SLOT_ID_DLY
                ), 
                display = DISPLAY_HEADER_2, 
                text = "Freeze", 
                color = Colors.LIGHT_GREEN
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 4, 
                rig_off = "auto", 
                auto_exclude_rigs = (4, 5), 
                display = DISPLAY_FOOTER_1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                color = Colors.PINK, 
                text = "Synth-4"
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 5, 
                rig_off = "auto", 
                auto_exclude_rigs = (4, 5), 
                display = DISPLAY_FOOTER_2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                color = Colors.RED, 
                text = "Lead-5"
            ),
            
        ],
        
    },
    
]
