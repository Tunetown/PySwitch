##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.Hardware import Hardware

from pyswitch.misc import Colors
from pyswitch.controller.actions.actions import HoldAction

from pyswitch.clients.kemper import KemperActionDefinitions, KemperEffectSlot, KemperMappings, RIG_SELECT_DISPLAY_TARGET_RIG
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2


# Defines the switch assignments
Switches = [

    # Switch 1
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": 
            # Note that for RIG_SELECT_AND_MORPH you have to omit the [] brackets as this function returns a list by its own!
            KemperActionDefinitions.RIG_SELECT_AND_MORPH_STATE(
                rig = 1,                
                display = DISPLAY_HEADER_1,
                morph_only_when_enabled = True
            )        
    },

    # Switch 2
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": 
            # Note that for RIG_SELECT_AND_MORPH you have to omit the [] brackets as this function returns a list by its own!
            KemperActionDefinitions.RIG_SELECT_AND_MORPH_STATE(
                rig = 2,                
                display = DISPLAY_HEADER_2,
                morph_only_when_enabled = True
            )
    },

    # Switch A
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            HoldAction({
                "actions": 
                    # Note that for RIG_SELECT_AND_MORPH you have to omit the [] brackets as this function returns a list by its own!
                    KemperActionDefinitions.RIG_SELECT_AND_MORPH_STATE(
                        rig = 3,
                        display = DISPLAY_FOOTER_1,
                        morph_only_when_enabled = True
                    ),

                "actionsHold": [
                    KemperActionDefinitions.BANK_DOWN(
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
                    )
                ]
            })            
        ]
    },
    
    # Switch B
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            HoldAction({
                "actions": 
                    # Note that for RIG_SELECT_AND_MORPH you have to omit the [] brackets as this function returns a list by its own!
                    KemperActionDefinitions.RIG_SELECT_AND_MORPH_STATE(
                        rig = 4,
                        display = DISPLAY_FOOTER_2,
                        morph_only_when_enabled = True
                    ),

                "actionsHold": [
                    KemperActionDefinitions.BANK_UP(
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
                    )
                ]
            })            
        ]
    }
]
