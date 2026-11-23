from ....controller.actions import Action
from .. import FractalIICallback, FractalIIMappings, COLOR_UTILITY

# Utility: Tuner. Switches the tuner on/off with the tuner CC of the device (I/O > CTRL > Tuner, default CC 15).
# The state is derived from the tuner data sent by the device, which requires DIN MIDI and
# I/O > MIDI > SEND REALTIME SYSEX = TUNER or ALL on the device.
def TUNER(cc = 15,                                # Tuner CC as set on the device (I/O > CTRL > Tuner)
          midi_channel = 1,                       # MIDI channel of the device in range [1..16] (I/O > MIDI > Channel)
          display = None,
          id = False,
          use_leds = True,
          enable_callback = None,
          color = None,                           # Color override (default: utility category color)
          text = "Tuner"                          # Label text
    ):
    return Action({
        "callback": _FractalIITunerCallback(
            cc = cc,
            channel = midi_channel - 1,
            color = color if color else COLOR_UTILITY,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


class _FractalIITunerCallback(FractalIICallback):
    def __init__(self, cc, channel, color, text):
        self.__mapping = FractalIIMappings.TUNER_STATE()

        super().__init__(
            color = color,
            text = text,
            mappings = [self.__mapping]
        )

        self.__mapping_on_off = FractalIIMappings.TUNER_ON_OFF(cc, channel)

    def update(self):
        super().update()
        self.__mapping.check(self._appl.client)

    def push(self):
        on = (self.__mapping.value != 1)
        client = self._appl.client

        client.set(self.__mapping_on_off, 127 if on else 0)
        self.__mapping.switched(client, on)

        self.update_displays()

    def update_displays(self):
        self._show(self.BRIGHT if self.__mapping.value == 1 else self.DIM, self._color, "Tuner")
