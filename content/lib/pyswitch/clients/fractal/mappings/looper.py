from micropython import const
from .. import FractalParameterMapping, _sysex, _response

# Looper buttons
LOOPER_BUTTON_RECORD = const(0)
LOOPER_BUTTON_PLAY = const(1)
LOOPER_BUTTON_UNDO = const(2)
LOOPER_BUTTON_ONCE = const(3)
LOOPER_BUTTON_REVERSE = const(4)
LOOPER_BUTTON_HALF = const(5)

# Looper state bits
LOOPER_STATE_RECORD = const(0x01)
LOOPER_STATE_PLAY = const(0x02)
LOOPER_STATE_OVERDUB = const(0x04)
LOOPER_STATE_ONCE = const(0x08)
LOOPER_STATE_REVERSE = const(0x10)
LOOPER_STATE_HALF = const(0x20)

# Looper state (bit field, see above)
def MAPPING_LOOPER_STATE():
    return FractalParameterMapping.get(
        name = "Looper State",
        request = _sysex(0x0f, (0x7f,)),
        response = _response(0x0f)
    )

# Press a looper button (the value is ignored)
def MAPPING_LOOPER_BUTTON(button):
    return FractalParameterMapping.get(
        name = f"Looper Button { button }",
        set = _sysex(0x0f, (button,)),
        set_bytes = 0
    )
