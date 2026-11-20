from ....controller.actions import Action
from ....misc import PeriodCounter
from .. import FractalCallback, FractalLabel, COLOR_UTILITY
from ..mappings.tempo import MAPPING_TAP_TEMPO, MAPPING_TEMPO_BEAT, MAPPING_TEMPO_BPM

# Utility: Tap Tempo. The LED flashes on every beat (requires DIN MIDI and Send Realtime Sysex = ON on the device).
def TAP_TEMPO(label = FractalLabel.FUNCTION,      # Label: FUNCTION ("Tap Tempo") or BPM (see FractalLabel)
              display = None,
              id = False,
              use_leds = True,
              enable_callback = None,
              color = None,                       # Color override (default: utility category color)
              text = None,                        # Custom label text
              flash_millis = 100                  # Duration of the LED flash on every beat (milliseconds)
    ):
    return Action({
        "callback": _FractalTapTempoCallback(
            label = label,
            color = color if color else COLOR_UTILITY,
            text = text,
            flash_millis = flash_millis
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


class _FractalTapTempoCallback(FractalCallback):
    def __init__(self, label, color, text, flash_millis):
        self.__mapping_beat = MAPPING_TEMPO_BEAT()
        mappings = [self.__mapping_beat]

        self.__mapping_bpm = None
        if label == FractalLabel.BPM:
            self.__mapping_bpm = MAPPING_TEMPO_BPM()
            mappings.append(self.__mapping_bpm)

        super().__init__(
            color = color,
            text = text,
            mappings = mappings
        )

        self.__flash = PeriodCounter(flash_millis)
        self.__flashing = False
        self.__last_beat = None

    def update(self):
        super().update()

        if self.__flashing and self.__flash.passed > self.__flash.interval:
            self.__flashing = False
            self.update_displays()

    def push(self):
        self._appl.client.set(MAPPING_TAP_TEMPO(), 0)

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
