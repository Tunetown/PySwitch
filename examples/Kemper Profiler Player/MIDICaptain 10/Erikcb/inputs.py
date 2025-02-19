##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.devices.pa_midicaptain_10 import *

#from pyswitch.misc import Colors

from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_FOOTER_1, DISPLAY_FOOTER_2, DISPLAY_HEADER_1, DISPLAY_HEADER_2

from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE

# Defines the switch assignments
Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_HEADER_1
            )                       
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = DISPLAY_HEADER_2
            )
        ]
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C,
                display = DISPLAY_FOOTER_1
            )
        ]
    },
    
    # Switch 4
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D,
                display = DISPLAY_FOOTER_2
            )
        ],
        "actionsHold": [
            TUNER_MODE()
        ]
    },

    # Switch up
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            BANK_UP()
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch C
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT(
                rig = 3,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch D
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT(
                rig = 4,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch down
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            BANK_DOWN()
        ]
    }
]