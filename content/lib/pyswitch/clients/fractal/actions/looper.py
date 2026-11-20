from ....controller.actions import Action
from ....colors import Colors
from .. import FractalCallback, FractalMappings, LOOPER_BLOCK_ID
from ..mappings.looper import *

# Looper functions like the FC "Looper" category: no parameters, automatic labels and colors. The LEDs are off
# when the current preset has no Looper block.

# Looper: Record (Overdub)
def LOOPER_RECORD(display = None, id = False, use_leds = True, enable_callback = None,
                  color = None,                   # Color override (default: red, yellow in overdub)
                  text = None                     # Custom label text
    ):
    return _create(LOOPER_BUTTON_RECORD, display, id, use_leds, enable_callback, color, text)

# Looper: Play/Stop
def LOOPER_PLAY_STOP(display = None, id = False, use_leds = True, enable_callback = None,
                     color = None,                # Color override (default: green)
                     text = None                  # Custom label text
    ):
    return _create(LOOPER_BUTTON_PLAY, display, id, use_leds, enable_callback, color, text)

# Looper: Undo/Erase
def LOOPER_UNDO(display = None, id = False, use_leds = True, enable_callback = None,
                color = None,                     # Color override (default: purple)
                text = None                       # Custom label text
    ):
    return _create(LOOPER_BUTTON_UNDO, display, id, use_leds, enable_callback, color, text)

# Looper: Once
def LOOPER_ONCE(display = None, id = False, use_leds = True, enable_callback = None,
                color = None,                     # Color override (default: blue)
                text = None                       # Custom label text
    ):
    return _create(LOOPER_BUTTON_ONCE, display, id, use_leds, enable_callback, color, text)

# Looper: Reverse
def LOOPER_REVERSE(display = None, id = False, use_leds = True, enable_callback = None,
                   color = None,                  # Color override (default: orange)
                   text = None                    # Custom label text
    ):
    return _create(LOOPER_BUTTON_REVERSE, display, id, use_leds, enable_callback, color, text)

# Looper: Half Speed
def LOOPER_HALF_SPEED(display = None, id = False, use_leds = True, enable_callback = None,
                      color = None,               # Color override (default: pink)
                      text = None                 # Custom label text
    ):
    return _create(LOOPER_BUTTON_HALF, display, id, use_leds, enable_callback, color, text)


def _create(button, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalLooperCallback(
            button = button,
            color = color,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


#####################################################################################################################


class _FractalLooperCallback(FractalCallback):

    # Per button: color, label, state bit for the bright LED (order: see LOOPER_BUTTON_*)
    _COLORS = (Colors.RED, Colors.GREEN, Colors.PURPLE, Colors.BLUE, Colors.ORANGE, Colors.PINK)
    _LABELS = ("Record", "Play", "Undo", "Once", "Reverse", "Half")
    _BITS = (LOOPER_STATE_RECORD, LOOPER_STATE_PLAY, 0, LOOPER_STATE_ONCE, LOOPER_STATE_REVERSE, LOOPER_STATE_HALF)

    def __init__(self, button, color, text):
        self.__mapping = MAPPING_LOOPER_STATE()
        self.__mapping_dump = FractalMappings.STATUS_DUMP()

        super().__init__(
            color = color,
            text = text,
            mappings = [self.__mapping, self.__mapping_dump]
        )

        self.__button = button
        self.__pushed = False

    def push(self):
        self._appl.client.set(MAPPING_LOOPER_BUTTON(self.__button), 0)

        self.__pushed = True
        self.update_displays()

    def release(self):
        self.__pushed = False
        self.update_displays()

    def update_displays(self):
        button = self.__button
        state = self.__mapping.value
        overdub = state != None and (state & LOOPER_STATE_OVERDUB)

        # Color and text
        color = self._color
        text = self._LABELS[button]

        if button == LOOPER_BUTTON_RECORD and overdub:
            text = "Overdub"
            if not color:
                color = Colors.YELLOW

        elif button == LOOPER_BUTTON_PLAY and state != None and (state & LOOPER_STATE_PLAY):
            text = "Stop"

        if not color:
            color = self._COLORS[button]

        # LED
        if state == None or not self.__has_looper():
            led = self.OFF
        elif button == LOOPER_BUTTON_UNDO:
            led = self.BRIGHT if self.__pushed else self.DIM
        elif state & self._BITS[button] or (button == LOOPER_BUTTON_RECORD and overdub):
            led = self.BRIGHT
        else:
            led = self.DIM

        self._show(led, color, text)

    # Returns if the current preset contains a Looper block (status dump)
    def __has_looper(self):
        dump = self.__mapping_dump.value
        if dump == None:
            return False

        for i in range(0, len(dump) - 2, 3):
            if dump[i] + 128 * dump[i + 1] == LOOPER_BLOCK_ID:
                return True

        return False
