from ....controller.actions import Action
from ....misc import PeriodCounter
from .. import FractalIICallback, FractalIIMappings, FractalIILabel, COLOR_UTILITY

# Utility: Tap Tempo. Taps with the tap tempo CC of the device (I/O > CTRL > Tap Tempo, default CC 14). The LED flashes
# on every beat (requires DIN MIDI and I/O > MIDI > SEND REALTIME SYSEX = TEMPO or ALL on the device).
def TAP_TEMPO(label = FractalIILabel.FUNCTION,    # Label: FUNCTION ("Tap Tempo") or BPM (see FractalIILabel)
              cc = 14,                            # Tap tempo CC as set on the device (I/O > CTRL > Tap Tempo)
              midi_channel = 1,                   # MIDI channel of the device in range [1..16] (I/O > MIDI > Channel)
              display = None,
              id = False,
              use_leds = True,
              enable_callback = None,
              color = None,                       # Color override (default: utility category color)
              text = None,                        # Custom label text
              flash_millis = 100                  # Duration of the LED flash on every beat (milliseconds)
    ):
    return Action({
        "callback": _FractalIITapTempoCallback(
            label = label,
            cc = cc,
            channel = midi_channel - 1,
            color = color if color else COLOR_UTILITY,
            text = text,
            flash_millis = flash_millis
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


class _FractalIITapTempoCallback(FractalIICallback):
    def __init__(self, label, cc, channel, color, text, flash_millis):
        self.__mapping_beat = FractalIIMappings.TEMPO_BEAT()
        mappings = [self.__mapping_beat]

        self.__mapping_bpm = None
        if label == FractalIILabel.BPM:
            self.__mapping_bpm = FractalIIMappings.TEMPO_BPM()
            mappings.append(self.__mapping_bpm)

        super().__init__(
            color = color,
            text = text,
            mappings = mappings
        )

        self.__mapping_tap = FractalIIMappings.TAP_TEMPO(cc, channel)
        self.__flash = PeriodCounter(flash_millis)
        self.__flashing = False
        self.__last_beat = None

    def update(self):
        super().update()

        if self.__flashing and self.__flash.passed > self.__flash.interval:
            self.__flashing = False
            self.update_displays()

    def push(self):
        self._appl.client.set(self.__mapping_tap, 127)

    def update_displays(self):
        beat = self.__mapping_beat.value
        if beat != None and beat != self.__last_beat:
            self.__last_beat = beat
            self.__flashing = True
            self.__flash.reset()

        if self.__mapping_bpm:
            text = f"{ self.__mapping_bpm.value } bpm" if self.__mapping_bpm.value != None else ""
        else:
            text = "Tap Tempo"

        self._show(self.BRIGHT if self.__flashing else self.DIM, self._color, text)
