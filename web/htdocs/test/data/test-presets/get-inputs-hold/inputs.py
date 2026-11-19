##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2

from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE

someOtherDict = {
    "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [ RIG_UP(
                display = DISPLAY_HEADER_1,
                text = "Rig up"
            )                         
        ]
}

# Defines the switch assignments
Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [ RIG_UP(
                display = DISPLAY_HEADER_1,
                text = "Rig up",
                calculated_arg = value != None,
                # dict_arg = {
                #     "entry": 3,
                #     "str": "somestring"
                # }
            )                         
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [ BANK_UP(), None ],
        "actionsHold": [TUNER_MODE(
            display = DISPLAY_HEADER_2
        )],
        "foo": [
            TUNER_MOdDE(foo=3)
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [ RIG_DOWN(display = DISPLAY_FOOTER_1, text = "Rig dn")]
    },
    
    # Switch B
    {
        "assignment":     
            PA_MIDICAPTAIN_NANO_SWITCH_B,


        "actions": 
        [ BANK_DOWN(
                display = DISPLAY_FOOTER_2
            )
        ]
    }
]

# Some foo data
Inputs2 = [
    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [ RIG_UP(
                display = DISPLAYs_HEADER_1,
                text = "Rig ee"
            )                         
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [ BANK_UP() ],
        "actionsHold": [TUNER_MODE(
            display = DISPLAY_HEADxER_2
        )]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [ RIG_DOWN(display = DISPLAY_FOOTER_1, text = "Rig as")]
    },
    
    # Switch B
    {
        "assignment":     
            PA_MIDICAPTAIN_NANO_SWITCH_A,


        "actions": 
        [ BANK_DOWN(
                display = DISPLAY_FOOTEX_2
            )
        ]
    }
]