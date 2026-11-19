from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_UP(
                display = DISPLAY_HEADER_1,
                text = "Rig up"
            )                    
        ],
        "holdTimeMillis": 555,
        "holdRepeat": True
    }
]
