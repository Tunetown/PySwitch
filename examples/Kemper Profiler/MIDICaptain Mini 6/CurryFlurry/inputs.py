from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.effect_button import EFFECT_BUTTON


Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,

                # Remove/comment out the next two lines to make the LED use the kemper original colors (red <> blue) for morph state
                morph_color_base = (0, 0, 0),
                morph_color_morphed = (255, 255, 255),   # r, g, b
                rig_btn_morph = True
            )
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 5,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,

                morph_color_base = (0, 0, 0),
                morph_color_morphed = (255, 255, 255),   # r, g, b
                rig_btn_morph = True
            )
        ]
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            EFFECT_BUTTON(
                num = 2
            )
        ],
        "actionsHold": [
            BANK_UP()
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,

                morph_color_base = (0, 0, 0),
                morph_color_morphed = (255, 255, 255),   # r, g, b
                rig_btn_morph = True
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,

                morph_color_base = (0, 0, 0),
                morph_color_morphed = (255, 255, 255),   # r, g, b
                rig_btn_morph = True
            )
        ]
    },

    # Switch C
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,

                morph_color_base = (0, 0, 0),
                morph_color_morphed = (255, 255, 255),   # r, g, b
                rig_btn_morph = True
            )
        ],
        "actionsHold": [
            BANK_DOWN()            
        ]
    }
]
