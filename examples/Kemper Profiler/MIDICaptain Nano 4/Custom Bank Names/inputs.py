from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG, RIG_SELECT_DISPLAY_CURRENT_RIG
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP


# Custom callback to get label text. Bank and rig come with values starting at zero (rig is in 
# range [0..4] and bank in range [0..x] depending on your player level)
def get_custom_text(action, bank, rig):
    if bank == 0:
        return "Homer " + repr(rig + 1)
    elif bank == 1:
        return "Marge " + repr(rig + 1)
    elif bank == 2:
        return "Bart " + repr(rig + 1)
    elif bank == 3:
        return "Lisa " + repr(rig + 1)
    elif bank == 4:
        return "Maggie " + repr(rig + 1)
    else:
        return "Rig " + repr(bank + 1) + "-" + repr(rig + 1)



Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_SELECT(
                rig = 1,                
                display = DISPLAY_HEADER_1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                text_callback = get_custom_text
            )
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            RIG_SELECT(
                rig = 2,               
                bank = 3,
                display = DISPLAY_HEADER_2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                text_callback = get_custom_text
            )
        ]
    },

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 1,
                rig_off = 2,                
                display = DISPLAY_FOOTER_1,
                display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
                text_callback = get_custom_text
            )
        ]
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            BANK_UP(
                display = DISPLAY_FOOTER_2,
                text_callback = get_custom_text,
                display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,
            )            
        ]
    }
]
