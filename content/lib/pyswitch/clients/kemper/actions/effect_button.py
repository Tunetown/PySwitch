from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ....misc import Colors

from ..mappings.effects import MAPPING_EFFECT_BUTTON

# Effect Button I-IIII (set only). num must be a number (1 to 4).
# NOTE: The state of the display will be toggled no matter what the real status on the Kemper is (the Kemper does not report the state at all sadly). 
# If you dont want this behaviour, you can set "use_internal_state = False".
def EFFECT_BUTTON(num, text = None, display = None, color = Colors.LIGHT_GREEN, id = False, use_leds = True, enable_callback = None, use_internal_state = True):
    if not text:
        if num == 1:
            text = "FX I"
        elif num == 2:
            text = "FX II"
        elif num == 3:
            text = "FX III"
        elif num == 4:
            text = "FX IIII"

    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_EFFECT_BUTTON(num),
            text = text,
            color = color,
            use_internal_state = use_internal_state
        ),
        "mode": PushButtonAction.LATCH,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })