from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *
from lib.pyswitch.clients.kemper.actions.looper import LOOPER_REC_PLAY_OVERDUB
from lib.pyswitch.clients.kemper.actions.looper import LOOPER_ERASE
from lib.pyswitch.clients.kemper.actions.looper import LOOPER_REVERSE
from lib.pyswitch.clients.kemper.actions.looper import LOOPER_HALF_SPEED
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from lib.pyswitch.clients.local.actions.pager import PagerAction
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2

_pager_top = PagerAction(
                pages = [{
                    "id": 1, 
                    "color": (50, 50, 50), 
                    "text": "FX A-D", 
                    
                },
                {
                    "id": 2, 
                    "color": Colors.WHITE, 
                    "text": "FX X-REV", 
                    
                },
                ]
            )

_pager_bottom = PagerAction(
                pages = [{
                    "id": 1, 
                    "color": (50, 50, 50), 
                    "text": "Rig Select", 
                    
                },
                {
                    "id": 2, 
                    "color": Colors.WHITE, 
                    "text": "Looper", 
                    
                },
                ]
            )

Inputs = [

    # Pedal 1
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1
    },

    # Pedal 2
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2
    },

    # Wheel rotary encoder
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER
    },

    # Wheel push button
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON
    },

    ####################################################################################
    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1, "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_HEADER_1, 
                id = 1, 
                enable_callback = _pager_top.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_HEADER_1, 
                id = 2, 
                enable_callback = _pager_top.enable_callback
            ),
            
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2, "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_HEADER_2, 
                id = 1, 
                enable_callback = _pager_top.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_HEADER_2, 
                id = 2, 
                enable_callback = _pager_top.enable_callback
            ),
            
        ]
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3, "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_FOOTER_1, 
                id = 1, 
                enable_callback = _pager_top.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY, 
                display = DISPLAY_FOOTER_1, 
                id = 2, 
                enable_callback = _pager_top.enable_callback
            ),
            
        ]
    },

    # Switch 4
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4, "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D, 
                display = DISPLAY_FOOTER_2, 
                id = 1, 
                enable_callback = _pager_top.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV, 
                display = DISPLAY_FOOTER_2, 
                id = 2, 
                enable_callback = _pager_top.enable_callback
            ),
            
        ], "actionsHold": [
            
        ]
    },

    # Switch Up
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP, "actions": [
            _pager_top,
            
        ], "actionsHold": [
            BANK_UP(
                ),
            
        ]
    },

    ############################################################################

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A, "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1, 
                id = 1, 
                enable_callback = _pager_bottom.enable_callback
            ),
            LOOPER_REC_PLAY_OVERDUB(
                id = 2, 
                enable_callback = _pager_bottom.enable_callback
            ),
            
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B, "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2, 
                id = 1, 
                enable_callback = _pager_bottom.enable_callback
            ),
            LOOPER_ERASE(
                id = 2, 
                enable_callback = _pager_bottom.enable_callback
            ),
            
        ]
    },

    # Switch C
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C, "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3, 
                id = 1, 
                enable_callback = _pager_bottom.enable_callback
            ),
            LOOPER_REVERSE(
                id = 2, 
                enable_callback = _pager_bottom.enable_callback
            ),
            
        ]
    },

    # Switch D
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D, "actionsHold": [
            
        ], "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4, 
                id = 1, 
                enable_callback = _pager_bottom.enable_callback
            ),
            LOOPER_HALF_SPEED(
                id = 2, 
                enable_callback = _pager_bottom.enable_callback
            ),
            
        ]
    },

    # Switch Down
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN, "actions": [
            _pager_bottom,
            
        ], "actionsHold": [
            BANK_DOWN(
                ),
            
        ]
    }
]
