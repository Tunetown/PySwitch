from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ....colors import Colors

from ..mappings.looper import MAPPING_LOOPER_REC_PLAY_OVERDUB, MAPPING_LOOPER_STOP, MAPPING_LOOPER_ERASE, MAPPING_LOOPER_CANCEL, MAPPING_LOOPER_TRIGGER, MAPPING_LOOPER_HALF_SPEED, MAPPING_LOOPER_REVERSE


# Looper: Play/Rec/Overdub
def LOOPER_REC_PLAY_OVERDUB(display = None, 
                            text = "Rec", 
                            color = Colors.RED, 
                            id = False, 
                            use_leds = True, 
                            enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_REC_PLAY_OVERDUB(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Looper: Stop
def LOOPER_STOP(display = None, 
                text = "Stop", 
                color = Colors.WHITE, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_STOP(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Looper: Erase
def LOOPER_ERASE(display = None, 
                text = "Erase", 
                color = Colors.LIGHT_RED, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_ERASE(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Looper: Cancel
def LOOPER_CANCEL(display = None, 
                text = "Undo", 
                color = Colors.YELLOW, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_CANCEL(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Looper: Reverse
def LOOPER_REVERSE(display = None, 
                text = "Reverse", 
                color = Colors.LIGHT_GREEN, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_REVERSE(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Trigger
def LOOPER_TRIGGER(display = None, 
                text = "Trigger", 
                color = Colors.LIGHT_BLUE, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_TRIGGER(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Looper: Half speed
def LOOPER_HALF_SPEED(display = None, 
                text = "HalfSpd", 
                color = Colors.ORANGE, 
                id = False, 
                use_leds = True, 
                enable_callback = None):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_LOOPER_HALF_SPEED(),
            text = text,
            color = color,
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })
