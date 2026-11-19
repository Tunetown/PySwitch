from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.colors import Colors
from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.mappings.rotary import MAPPING_ROTARY_SPEED
from pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_STATE

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_HEADER_1
            )
        ],
        "actionsHold": [
            TUNER_MODE()
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = DISPLAY_HEADER_2
            )
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            BINARY_SWITCH(
                mapping = MAPPING_ROTARY_SPEED(
                    slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A
                ),
                display = DISPLAY_FOOTER_1,
                color = Colors.DARK_BLUE,
                text = "A: Fast"
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            BINARY_SWITCH(
                mapping = MAPPING_AMP_STATE(),
                display = DISPLAY_FOOTER_2,
                color = Colors.GRAY,
                text = "Amp"
            )
        ]
    }
]
