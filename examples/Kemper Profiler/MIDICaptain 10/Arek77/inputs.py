from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import RIG_SELECT_AND_MORPH_STATE
from lib.pyswitch.clients.kemper.actions.bank_select import BANK_SELECT
from lib.pyswitch.clients.local.actions.encoder_button import ENCODER_BUTTON
from lib.pyswitch.controller.actions.AnalogAction import AnalogAction
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from lib.pyswitch.clients.kemper.mappings.pedals import MAPPING_WAH_PEDAL
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_HEADER_4
from display import DISPLAY_HEADER_5
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_FOOTER_4
from display import DISPLAY_FOOTER_5
from lib.pyswitch.hardware.devices.pa_midicaptain_10 import *

_encoder_apply = ENCODER_BUTTON()

_encoder_cancel = ENCODER_BUTTON()


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2,
        "actions": [
            AnalogAction(
                mapping = MAPPING_WAH_PEDAL()
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
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            BANK_SELECT(
                bank = 1, 
                display = DISPLAY_HEADER_1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = " "
            ),
            
        ],
        "actionsHold": [
            BANK_SELECT(
                bank = 6, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                display = DISPLAY_FOOTER_1,
text = " "              

            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            BANK_SELECT(
                bank = 2, 
                display = DISPLAY_HEADER_2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = " "
            ),
            
        ],
        "actionsHold": [
            BANK_SELECT(
                bank = 7, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                display = DISPLAY_FOOTER_2, 
text = " "  
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            BANK_SELECT(
                bank = 3, 
                display = DISPLAY_HEADER_3, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = " "
            ),
            
        ],
        "actionsHold": [
            BANK_SELECT(
                bank = 8, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                display = DISPLAY_FOOTER_3, 
text = " "  
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            BANK_SELECT(
                bank = 4, 
                display = DISPLAY_HEADER_4, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = " "
            ),
            
        ],
        "actionsHold": [
            BANK_SELECT(
                bank = 9, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                display = DISPLAY_FOOTER_4, 
text = " "  
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            BANK_SELECT(
                bank = 5, 
                display = DISPLAY_HEADER_5, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                text = " "
            ),
            
        ],
        "actionsHold": [
            BANK_SELECT(
                bank = 10, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                display = DISPLAY_FOOTER_5, 
text = " "  
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 1, 
                rig_btn_morph = True, 
                color = Colors.DARK_BLUE
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 2, 
                rig_btn_morph = True, 
                color = Colors.YELLOW
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 3, 
                rig_btn_morph = True, 
                color = Colors.RED
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 4, 
                rig_btn_morph = True, 
                color = Colors.GREEN
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            RIG_SELECT_AND_MORPH_STATE(
                rig = 5, 
                rig_btn_morph = True, 
                color = Colors.PURPLE
            ),
            
        ],
        "actionsHold": [],
        
    },
    
]