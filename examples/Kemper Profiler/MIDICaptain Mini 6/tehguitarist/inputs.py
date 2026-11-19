from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.colors import Colors
from pyswitch.controller.callbacks import Callback
from pyswitch.clients.kemper import KemperEffectSlot, KemperMappings
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_HEADER_3, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2, DISPLAY_FOOTER_3
from pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE

# Allow change of switch behaviour based on rig name
class _EnableCallback(Callback):
    def __init__(self):
        Callback.__init__(self)
        
        self.mapping = KemperMappings.RIG_NAME()
        self.register_mapping(self.mapping)

    def enabled(self, action):
        text = self.mapping.value if self.mapping.value else "NO RIG" 
        if "FX" in text:
            return (action.id == 20)        
        else:
            return (action.id == 10)
        
# Create an instance of the class which can be shared by all actions which use the callback
_enable_callback = _EnableCallback()


Inputs = [

    # Switch 1 | Drive (Slot D)/FX (Slot X)
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D,
                id = 10,
                display = DISPLAY_HEADER_1,
                enable_callback = _enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X,
                id = 20,
                display = DISPLAY_HEADER_1,
                enable_callback = _enable_callback
            ),                          
        ]
    },

    # Switch 2 | Delay
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
                display = DISPLAY_HEADER_2#,
            ),
            SHOW_TEMPO(
                color = (50, 255, 50),
                led_brightness = 0.2
            )
        ]
    },

    # Switch 3 | Reverb
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV,
                # color = Colors.TURQUOISE,
                display = DISPLAY_HEADER_3
            )        
        ]
    },

    # Switch A | Rig 1 - Clean (usually)
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 1,
                color = (85, 255, 85),
                display = DISPLAY_FOOTER_1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,  
            )
        ]
    },
    
    # Switch B | Rig 3 - Crunch (usually)
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 3,
                color = Colors.ORANGE,
                display = DISPLAY_FOOTER_2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
            )
        ]
    },

    # Switch C | Rig 4 - High Gain (usually)
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            RIG_SELECT(
                rig = 4,
                color = Colors.RED,
                display = DISPLAY_FOOTER_3,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
            )
        ]
    }
]
