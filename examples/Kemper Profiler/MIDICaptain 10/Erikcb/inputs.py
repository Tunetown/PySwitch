from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *
from lib.pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_FOOTER_1, DISPLAY_FOOTER_2, DISPLAY_HEADER_1, DISPLAY_HEADER_2
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from lib.pyswitch.clients.kemper.mappings.pedals import MAPPING_VOLUME_PEDAL, MAPPING_WAH_PEDAL
from lib.pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_GAIN, MAPPING_AMP_STATE
from lib.pyswitch.controller.actions.AnalogAction import AnalogAction
from lib.pyswitch.controller.actions.EncoderAction import EncoderAction


# Defines the switch assignments and other inputs
Inputs = [
    # Pedal 1
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [
            AnalogAction(
                mapping = MAPPING_VOLUME_PEDAL(),
                auto_calibrate = True
            )
        ]
    },

    # Pedal 2
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2,
        "actions": [
            AnalogAction(
                mapping = MAPPING_WAH_PEDAL(),
                auto_calibrate = True
            )
        ]
    },

    # Wheel rotary encoder
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            EncoderAction(
                mapping = MAPPING_AMP_GAIN()
            )
        ]
    },

    # Wheel push button
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [
            BINARY_SWITCH(
                mapping = MAPPING_AMP_STATE()                
            )
        ]
    },

    ####################################################################################

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_HEADER_1
            )
        ]    
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = DISPLAY_HEADER_2          
            )
        ]    
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
                display = DISPLAY_FOOTER_1
            )
        ]    
    },
    
    # Switch 4
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV,
                display = DISPLAY_FOOTER_2
            )
        ],
        "actionsHold": [
            TUNER_MODE()
        ]    
    },

   # Switch up
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            BANK_UP()
        ]
    },


    # ########################################################################################

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                rig_btn_morph = True
            )    
        ]
    },

    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                rig_btn_morph = True
            )    
        ]
    },

    # Switch C
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                rig_btn_morph = True
            )    
        ]
    },

    # Switch D
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                rig_btn_morph = True
            )    
        ]
    },

      # Switch down
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            BANK_DOWN()
        ]
    }
]
