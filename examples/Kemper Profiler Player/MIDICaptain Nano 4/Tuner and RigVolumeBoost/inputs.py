##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

#from pyswitch.misc import Colors

from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_FOOTER_1, DISPLAY_FOOTER_2, DISPLAY_HEADER_1, DISPLAY_HEADER_2

from pyswitch.clients.kemper.actions.rig_volume_boost import RIG_VOLUME_BOOST
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE


# Defines the switch assignments
Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            TUNER_MODE(
                display = DISPLAY_HEADER_1
            )                         
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            RIG_VOLUME_BOOST(
                boost_volume = 0.75,     # Value im [0..1] representing the Rig Volume Knob. Examples: 0.5 = 0dB (no boost), 0.75 = +6dB, 1.0 = +12dB
                display = DISPLAY_HEADER_2
            )    
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_FOOTER_1
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = DISPLAY_FOOTER_2
            )
        ]
    }
]
