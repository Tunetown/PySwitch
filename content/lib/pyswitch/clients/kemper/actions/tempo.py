from ....controller.actions import PushButtonAction, Action
from ....controller.callbacks import BinaryParameterCallback, Callback
from ....clients.kemper import KemperMappings
from ....colors import Colors

from ..mappings.tempo import MAPPING_TAP_TEMPO, MAPPING_TEMPO_DISPLAY
from ..mappings.tempo_bpm import MAPPING_TEMPO_BPM, convert_bpm

# Tap tempo
def TAP_TEMPO(display = None, 
              midi_channel = 1,                   # MIDI Channel in range [1..16]
              color = Colors.DARK_GREEN, 
              id = False, 
              use_leds = False, 
              enable_callback = None
    ):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_TAP_TEMPO(midi_channel - 1),
            text = "Tap",
            color = color
        ),
        "mode": PushButtonAction.MOMENTARY,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Show tempo (blinks on every beat)
def SHOW_TEMPO(display = None, 
               midi_channel = 1,                  # MIDI Channel in range [1..16]
               change_display = None,             # If a display label is passed here, the BPM value will be shown there shortly when changed.
               change_timeout_millis = 1500,      # If change_display is set, this determines how long the values shall be shown.
               color = Colors.LIGHT_GREEN, 
               text = "{bpm} bpm",                # Text for the main label. Can contain a {bpm} token which is replaced with the current BPM value.
               id = False, 
               use_leds = True, 
               enable_callback = None, 
               led_brightness = 0.02              # LED brightness in range [0..1]
    ):
    return Action({
        "callback": _KemperShowTempoCallback(
            change_display = change_display,
            change_timeout_millis = change_timeout_millis,
            text = text,
            color = color,
            led_brightness = led_brightness,
            resolve_bpm = display or change_display,
            channel = midi_channel - 1
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


####################################################################################


class _KemperShowTempoCallback(Callback):
    def __init__(self, 
                 change_display,
                 change_timeout_millis,
                 color, 
                 text, 
                 led_brightness,
                 resolve_bpm,
                 channel
        ):
        
        super().__init__()

        self.__tempo_mapping = MAPPING_TEMPO_DISPLAY()
        self.register_mapping(self.__tempo_mapping)        

        self.__tuner_mapping = KemperMappings.TUNER_MODE_STATE(channel)
        self.register_mapping(self.__tuner_mapping)

        if resolve_bpm:
            self.__bpm_mapping = MAPPING_TEMPO_BPM()
            self.register_mapping(self.__bpm_mapping)
        else:
            self.__bpm_mapping = None

        if change_display:
            from ....controller.preview import ValuePreview

            self.__preview = ValuePreview.get(change_display)
            self.__change_timeout_millis = change_timeout_millis

            # Also listen to rig changes to avoid display BPM after each rig change
            self.__rig_id_mapping = KemperMappings.RIG_ID(channel)
            self.register_mapping(self.__rig_id_mapping)
        else:
            self.__preview = None

        self._text = text
        self._color = color
        self._led_brightness = led_brightness
        self.__current_value = None
        self.__last_bpm = None
        self.__last_rig = None

    def push(self):
        pass

    def release(self):
        pass

    def update(self):
        super().update()

        if self.__preview:
            self.__preview.update()

    def update_displays(self):
        # Tuner mode: Do nothing
        if self.__tuner_mapping.value == 1:
            return

        # LED blinking
        value = self.__tempo_mapping.value
        if value != None and value != self.__current_value:
            self.__current_value = value

            self.action.switch_color = self._color
            self.action.switch_brightness = self._led_brightness if value > 0 else 0

        # Text to show
        text = None
        if self.__bpm_mapping and self.__bpm_mapping.value != None:
            if self.__bpm_mapping.value != self.__last_bpm:
                bpm = convert_bpm(self.__bpm_mapping.value)
                text = self._text.replace('{bpm}', bpm)

                # Show in preview display? Dont do this for the first value that comes in.
                if self.__preview and self.__last_bpm != None and self.__rig_id_mapping.value == self.__last_rig:
                    self.__preview.preview(
                        text = text, 
                        timeout_millis = self.__change_timeout_millis
                    )

                self.__last_bpm = self.__bpm_mapping.value

                if self.__preview:
                    self.__last_rig = self.__rig_id_mapping.value

        if self.action.label:
            self.action.label.back_color = self._color

            if text:
                self.action.label.text = text
