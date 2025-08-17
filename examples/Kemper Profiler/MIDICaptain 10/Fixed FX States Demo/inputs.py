from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_TRANSPOSE
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_GATE
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_COMP
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_BOOST
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_WAH
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_CHORUS
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_AIR
from lib.pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_DBL_TRACKER

from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_TRANSPOSE,
                display = DISPLAY_HEADER_1
            ),            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_GATE,
                display = DISPLAY_HEADER_2
            ),            
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_COMP,
                display = DISPLAY_FOOTER_1
            ),            
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_BOOST,
                display = DISPLAY_FOOTER_2
            ),            
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_WAH
            )
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_CHORUS
            )
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_AIR
            )
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_DBL_TRACKER
            )
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        
    },
    
]
