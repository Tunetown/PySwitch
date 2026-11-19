from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.kemper.actions.effect_button import EFFECT_BUTTON

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_BUTTON(
                display = DISPLAY_HEADER_1,
                num = 1
            )
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            EFFECT_BUTTON(
                display = DISPLAY_HEADER_2,
                num = 2
            )
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            EFFECT_BUTTON(
                display = DISPLAY_FOOTER_1,
                num = 3
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            EFFECT_BUTTON(
                display = DISPLAY_FOOTER_2,
                num = 4
            )
        ]
    }
]
