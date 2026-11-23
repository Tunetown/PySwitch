from ....controller.actions import Action
from .. import FractalAM4Callback, FractalAM4Mappings, FractalAM4Mode, COLOR_UTILITY

# Selects a footswitch mode of the AM4 (presets, scenes, effects, amp, tuner/tap), like the AM4's mode select.
# The AM4 also shows the page of the mode (tuner mode: the tuner).
def MODE_SELECT(mode,                                     # Mode (see FractalAM4Mode)
                display = None,
                id = False,
                use_leds = True,
                enable_callback = None,
                color = None,                             # Color override (default: utility color)
                text = None                               # Custom label text
    ):
    return Action({
        "callback": _FractalAM4ModeCallback(
            mode = mode,
            color = color,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


#####################################################################################################################


class _FractalAM4ModeCallback(FractalAM4Callback):
    def __init__(self, mode, color, text):
        super().__init__(
            color = color if color else COLOR_UTILITY,
            text = text
        )

        self.__mapping = FractalAM4Mappings.MODE()
        self.__mode = mode
        self.__name = FractalAM4Mode.name(mode)
        self.__pushed = False

    def push(self):
        self.__pushed = True
        self._appl.client.set(self.__mapping, self.__mode)
        self.update_displays()

    def release(self):
        self.__pushed = False
        self.update_displays()

    def update_displays(self):
        self._show(self.BRIGHT if self.__pushed else self.DIM, self._color, self.__name)
