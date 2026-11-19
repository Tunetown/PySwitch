from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN


Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1,                
                display = DISPLAY_HEADER_1,
                morph_only_when_enabled = True
            )
        ]     
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2,                
                display = DISPLAY_HEADER_2,
                morph_only_when_enabled = True
            )
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3,
                display = DISPLAY_FOOTER_1,
                morph_only_when_enabled = True
            )
        ],

        "actionsHold": [
            BANK_DOWN(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4,
                display = DISPLAY_FOOTER_2,
                morph_only_when_enabled = True
            )
        ],

        "actionsHold": [
            BANK_UP(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    }
]
