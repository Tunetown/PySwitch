from lib.pyswitch.clients.kemper.actions.rig_transpose import ENCODER_RIG_TRANSPOSE
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from lib.pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from lib.pyswitch.clients.kemper.actions.effect_state_extended_names import EFFECT_STATE_EXT
from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.encoder_button import ENCODER_BUTTON
from lib.pyswitch.colors import Colors
from lib.pyswitch.controller.actions import PushButtonAction
from lib.pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *
from lib.pyswitch.clients.kemper.actions.effect_state import KemperEffectEnableCallback

# Current Bank/Rig display: Define a custom text callback for all RIG_SELECTs, to get rid of the "Rig " prefix of the original.
def _text_callback(action, bank, rig):
    return f"{bank + 1}-{rig + 1}"

# Category names: Instead of using EFFECT_STATE, you can define the PushButtonAction manually, overriding the
# callback to deliver different effect category names: First override the respective method:
class MyKemperEffectEnableCallback(KemperEffectEnableCallback):
    def get_effect_category_text(self, category, kpp_type):
        if category == self.CATEGORY_CHORUS:
            return "Mod Ch/Tr"
        elif category == self.CATEGORY_PHASER_FLANGER:
            return "Mod Ph/Fl"
        else:
            # Fall back to the original implementation for all others
            return super().get_effect_category_text(category, kpp_type)

# Now define our custom action, which is used instead of EFFECT_STATE
def MY_EFFECT_STATE(slot_id, display = None):
    return PushButtonAction({
        "callback": MyKemperEffectEnableCallback(slot_id),
        "mode": PushButtonAction.HOLD_MOMENTARY,
        "display": display,
        "useSwitchLeds": True
    })

_accept = ENCODER_BUTTON()

_cancel = ENCODER_BUTTON()


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            BANK_UP(
                preselect = True, 
                text = 'Bank up'
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            BANK_DOWN(
                preselect = True, 
                text = 'Bank dn'
            ),
            
        ],
        "actionsHold": [
            TUNER_MODE(),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1, 
                rig_btn_morph = True
            ),
            
        ],
        "actionsHold": [
            RIG_SELECT(
                rig = 1, 
                display = DISPLAY_FOOTER_2, 
                use_leds = False, 
                color = Colors.WHITE, 
                text_callback = _text_callback
            ),
            
        ],
        "holdTimeMillis": 9999999,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2, 
                rig_btn_morph = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3, 
                rig_btn_morph = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4, 
                rig_btn_morph = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 5, 
                rig_btn_morph = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [
            _accept,
            
        ],
        "actionsHold": [
            _cancel,
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            ENCODER_RIG_TRANSPOSE(
                accept_action = _accept, 
                cancel_action = _cancel, 
                preview_display = DISPLAY_RIG_NAME
            ),
            
        ],
        
    },
    
]
