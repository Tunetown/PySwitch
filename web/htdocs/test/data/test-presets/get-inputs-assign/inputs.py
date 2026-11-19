##############################################################################################################################################
# 
# Definition of actions for switches
#
##############################################################################################################################################
 
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2

from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE

_deferred = RIG_DOWN(
    display = DISPLAY_FOO
)

_deferred_2 = RIG_UP(
    display = DISPLAY_HEADER_1,
    text = "foo",
    id = 303
)

# Defines the switch assignments
Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [ 
            _deferred_2                        
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [ 
            BANK_UP()            
        ],
        "actionsHold": [
            TUNER_MODE(
                display = DISPLAY_HEADER_2
            ),
            _deferred
        ]
    },
]