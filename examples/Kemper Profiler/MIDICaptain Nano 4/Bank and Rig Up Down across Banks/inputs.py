from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN


Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_UP(
                display = DISPLAY_HEADER_1,
                keep_bank = False
            )                         
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            BANK_UP(
                display = DISPLAY_HEADER_2
            )
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_DOWN(
                display = DISPLAY_FOOTER_1,
                keep_bank = False
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            BANK_DOWN(
                display = DISPLAY_FOOTER_2
            )
        ]
    }
]
