from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN, FOO_RIG
from pyswitch.clients.kemper.actions.foo import FOO1, FOO2

_foo = "Must be removed"

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_UP(
                display = DISPLAY_HEADER_1,
                text = "Rig up"
            )                         
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            BANK_UP(
                display = DISPLAY_HEADER_2
            ),
            RIG_DOWN(),
            RIG_UP(some=val, 
                   
                   
                   numb=78, large={"d":{"e":{"f":8}}}, arr=[{"f": 8, "j": [3, 5,6]}, None, "g"]),
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_DOWN(
                display = DISPLAY_FOOTER_1,text="Rig dn"
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
