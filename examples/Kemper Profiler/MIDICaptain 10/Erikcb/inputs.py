from pyswitch.clients.kemper.actions.looper import LOOPER_REC_PLAY_OVERDUB
from pyswitch.clients.kemper.actions.looper import LOOPER_STOP
from pyswitch.clients.kemper.actions.looper import LOOPER_ERASE
from pyswitch.clients.kemper.actions.looper import LOOPER_CANCEL
from pyswitch.clients.kemper.actions.looper import LOOPER_TRIGGER
from pyswitch.clients.kemper.actions.looper import LOOPER_HALF_SPEED
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP
from pyswitch.clients.kemper.actions.bank_up_down import BANK_DOWN
from pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.controller.actions.AnalogAction import AnalogAction
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.kemper import KemperEffectSlot
from pyswitch.controller.actions import PushButtonAction
from pyswitch.clients.kemper.mappings.pedals import MAPPING_WAH_PEDAL
from pyswitch.clients.kemper.mappings.pedals import MAPPING_VOLUME_PEDAL
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_HEADER_4
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_FOOTER_4
from pyswitch.hardware.devices.pa_midicaptain_10 import *

_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "text": 'RIGㅤㅤㅤㅤㅤㅤ',
            
        },
        {
            "id": 2,
            "text": 'LOOPER',
            
        },
        
    ], 
    use_leds = False
)


# Defines the switch assignments and other inputs
Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [
            AnalogAction(
                mapping = MAPPING_VOLUME_PEDAL(), 
                auto_calibrate = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2,
        "actions": [
            AnalogAction(
                mapping = MAPPING_WAH_PEDAL(), 
                auto_calibrate = True
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            LOOPER_TRIGGER(
                text = 'Trigger', 
                color = Colors.LIGHT_GREEN, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_HEADER_1, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_HEADER_3, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            LOOPER_HALF_SPEED(
                text = 'HalfSpd', 
                color = Colors.YELLOW, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_HEADER_2, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D, 
                display = DISPLAY_HEADER_4, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            TUNER_MODE(
                mode = PushButtonAction.LATCH, 
                color = (209, 115, 221), 
                text = 'Tuner', 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY, 
                display = DISPLAY_FOOTER_3, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_FOOTER_1, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "holdTimeMillis": 350,
        
    },
        {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV, 
                display = DISPLAY_FOOTER_4, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            TAP_TEMPO(
                use_leds = True, 
                color = (255, 162, 0), 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_FOOTER_2, 
                mode = PushButtonAction.LATCH, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            BANK_UP(
                id = None, 
                text = 'Bank up'
            ),
            
        ],
        "actionsHold": [],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1, 
                rig_btn_morph = True, 
                id = 1, 
                morph_color_base = Colors.GREEN, 
                morph_color_morphed = Colors.RED, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_REC_PLAY_OVERDUB(
                text = 'Rec', 
                color = Colors.LIGHT_RED, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2, 
                rig_btn_morph = True, 
                id = 1, 
                morph_color_base = Colors.GREEN, 
                morph_color_morphed = Colors.RED, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_STOP(
                text = 'Stop', 
                color = Colors.LIGHT_BLUE, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3, 
                rig_btn_morph = True, 
                id = 1, 
                morph_color_base = Colors.GREEN, 
                morph_color_morphed = Colors.RED, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_ERASE(
                text = 'Erase', 
                color = Colors.RED, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4, 
                rig_btn_morph = True, 
                id = 1, 
                morph_color_base = Colors.GREEN, 
                morph_color_morphed = Colors.RED, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_CANCEL(
                text = 'Undo', 
                color = Colors.DARK_PURPLE, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [],
        "holdTimeMillis": 350,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            BANK_DOWN(),
            
        ],
        "holdTimeMillis": 350,
        "actionsHold": [
            _pager,
            
        ],
        
    },
    
]
