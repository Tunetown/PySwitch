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


class _EnableCallback(Callback):
    def __init__(self):
        Callback.__init__(self)
        
        self.mapping = KemperMappings.RIG_VOLUME()
        self.register_mapping(self.mapping)

    def enabled(self, action):  
        if self.mapping.value == None:
            return (action.id == 10)        
        elif action.id == 20:
            return (self.mapping.value >= NRPN_VALUE(0.5))
        elif action.id == 10:
            return (self.mapping.value < NRPN_VALUE(0.5))
        
_enable_callback = _EnableCallback()

# Defines the switch assignments
Switches = [

    # Switch 1
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            KemperActionDefinitions.RIG_SELECT(
                id = 10,
                rig = 1,                
                display = DISPLAY_HEADER_1,
                display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
                enable_callback = _enable_callback
            ),
            KemperActionDefinitions.RIG_SELECT(
                id = 20,
                rig = 1,                
                display = DISPLAY_HEADER_1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                enable_callback = _enable_callback
            )
        ]
    },

    # Switch 2
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            KemperActionDefinitions.RIG_SELECT(
                id = 10,
                rig = 2,
                rig_off = 5,
                display = DISPLAY_HEADER_2,
                display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
                enable_callback = _enable_callback
            ),
            KemperActionDefinitions.RIG_SELECT(
                id = 20,
                rig = 2,
                rig_off = 5,
                display = DISPLAY_HEADER_2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                enable_callback = _enable_callback
            )
        ]
    },

    # Switch A
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            HoldAction({
                "actions": [
                    KemperActionDefinitions.RIG_AND_BANK_SELECT(
                        id = 10,
                        rig = 4,
                        bank = 4,
                        display = DISPLAY_FOOTER_1,
                        display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
                        enable_callback = _enable_callback
                    ),
                    KemperActionDefinitions.RIG_AND_BANK_SELECT(
                        id = 20,
                        rig = 4,
                        bank = 4,
                        display = DISPLAY_FOOTER_1,
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                        enable_callback = _enable_callback
                    )
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
                        id = 10,
                        rig = 4,
                        bank = 4,
                        rig_off = 3,
                        bank_off = 3,
                        display = DISPLAY_FOOTER_2,
                        display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
                        enable_callback = _enable_callback
                    ),
                    KemperActionDefinitions.RIG_AND_BANK_SELECT(
                        id = 20,
                        rig = 4,
                        bank = 4,
                        rig_off = 3,
                        bank_off = 3,
                        display = DISPLAY_FOOTER_2,
                        display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                        enable_callback = _enable_callback
                    )
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