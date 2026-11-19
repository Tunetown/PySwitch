##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.Hardware import Hardware

from pyswitch.misc import Colors
from pyswitch.controller.callbacks import Callback
from pyswitch.controller.actions.actions import PushButtonAction, HoldAction

from pyswitch.clients.kemper import KemperActionDefinitions, KemperEffectSlot, KemperMappings, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper import RIG_SELECT_DISPLAY_CURRENT_RIG, NRPN_VALUE
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2


def cb_text(action, bank, rig):
    return "CB Text"

def cb_color(action, bank, rig):
    return (123, 67, 255)


# Defines the switch assignments
Switches = [

    # Switch 1
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            KemperActionDefinitions.RIG_SELECT(
                rig = 1,                
                display = DISPLAY_HEADER_1,
                color = Colors.PINK,
                text = "Sel 1",
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
        ]
    },

    # Switch 2
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            KemperActionDefinitions.RIG_SELECT(
                rig = 2,
                rig_off = 5,
                display = DISPLAY_HEADER_2,
                text_callback = cb_text,
                color_callback = cb_color,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
        ]
    },

    # Switch A
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            HoldAction({
                "actions": [
                    KemperActionDefinitions.RIG_AND_BANK_SELECT(
                        rig = 4,
                        bank = 4,
                        display = DISPLAY_FOOTER_1,
                        color = Colors.PINK,
                        text = "Sel 4",
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
                    ),
                ],
                "actionsHold": [
                    KemperActionDefinitions.BANK_DOWN()
                ]
            })            
        ]
    },
    
    # Switch B
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            HoldAction({
                "actions": [
                    KemperActionDefinitions.RIG_AND_BANK_SELECT(
                        rig = 4,
                        bank = 4,
                        rig_off = 3,
                        bank_off = 3,
                        display = DISPLAY_FOOTER_2,
                        text_callback = cb_text,
                        color_callback = cb_color,
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
                    ),
                ],
                "actionsHold": [
                    KemperActionDefinitions.BANK_UP()
                ]
            })            
        ]
    }
]

######################################################################

Pedals = None