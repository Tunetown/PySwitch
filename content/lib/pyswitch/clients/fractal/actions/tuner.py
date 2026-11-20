from ....controller.actions import Action
from .. import FractalCallback, FractalMappings, COLOR_UTILITY

# Utility: Tuner. Switches the tuner on/off. The state is derived from the tuner push data, which
# requires DIN MIDI and Send Realtime Sysex = ON on the device.
def TUNER(display = None,
          id = False,
          use_leds = True,
          enable_callback = None,
          color = None,                           # Color override (default: utility category color)
          text = "Tuner"                          # Label text
    ):
    return Action({
        "callback": _FractalTunerCallback(
            color = color if color else COLOR_UTILITY,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


class _FractalTunerCallback(FractalCallback):
    def __init__(self, color, text):
        self.__mapping = FractalMappings.TUNER_STATE()

        super().__init__(
            color = color,
            text = text,
            mappings = [self.__mapping]
        )

    def update(self):
        super().update()
        self.__mapping.check(self._appl.client)

    def push(self):
        on = (self.__mapping.value != 1)
        client = self._appl.client

        client.set(FractalMappings.TUNER_ON_OFF(), 1 if on else 0)
        self.__mapping.switched(client, on)

        self.update_displays()

    def update_displays(self):
        self._show(self.BRIGHT if self.__mapping.value == 1 else self.DIM, self._color, "Tuner")
