##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.Hardware import Hardware

from pyswitch.controller.callbacks import Callback

from pyswitch.clients.kemper import KemperActionDefinitions, KemperEffectSlot, KemperMappings, NRPN_VALUE
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2


class _EnableCallback(Callback):
    def __init__(self):
        Callback.__init__(self)
        
        self.mapping = KemperMappings.RIG_VOLUME()
        self.register_mapping(self.mapping)

    def enabled(self, action):  
        if self.mapping.value == None:
            return (action.id == 10)        
        elif action.id == 30:
            return (self.mapping.value >= NRPN_VALUE(0.66))
        elif action.id == 20:
            return (self.mapping.value >= NRPN_VALUE(0.33)) and (self.mapping.value < NRPN_VALUE(0.66))
        elif action.id == 10:
            return (self.mapping.value < NRPN_VALUE(0.33))
        
_enable_callback = _EnableCallback()

# Defines the switch assignments
Switches = [

    # Switch 1
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            KemperActionDefinitions.BINARY_SWITCH(
                mapping = KemperMappings.ROTARY_SPEED(KemperEffectSlot.EFFECT_SLOT_ID_A),           
                text = "Fast",
                id = 10,
                display = DISPLAY_HEADER_1,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                id = 20,
                display = DISPLAY_HEADER_1,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.BANK_UP(
                id = 30,
                display = DISPLAY_HEADER_1,
                enable_callback = _enable_callback
            )
        ]
    },

    # Switch 2
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            KemperActionDefinitions.TAP_TEMPO(
                use_leds = False,
                id = 10,
                display = DISPLAY_HEADER_2,
                enable_callback = _enable_callback
            ),
            KemperActionDefinitions.SHOW_TEMPO(
                id = 20,
                display = DISPLAY_HEADER_2,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.BANK_DOWN(
                id = 30,
                display = DISPLAY_HEADER_2,
                enable_callback = _enable_callback
            )
        ]
    },

    # Switch A
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            KemperActionDefinitions.TUNER_MODE(
                id = 10,
                display = DISPLAY_FOOTER_1,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.EFFECT_BUTTON(
                num = 1,
                id = 20,
                display = DISPLAY_FOOTER_1,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.RIG_SELECT(
                rig = 3,
                rig_off = 1,
                id = 30,
                display = DISPLAY_FOOTER_1,
                enable_callback = _enable_callback
            )          
        ]
    },
    
    # Switch B
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            KemperActionDefinitions.MORPH_BUTTON(
                id = 10,
                display = DISPLAY_FOOTER_2,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.RIG_VOLUME_BOOST(
                boost_volume = 0.55,
                id = 20,
                display = DISPLAY_FOOTER_2,
                enable_callback = _enable_callback
            ),

            KemperActionDefinitions.RIG_AND_BANK_SELECT(
                rig = 4,
                bank = 5,
                rig_off = 3,
                bank_off = 4,
                id = 30,
                display = DISPLAY_FOOTER_2,
                enable_callback = _enable_callback
            )              
        ]
    },
]

######################################################################

Pedals = None