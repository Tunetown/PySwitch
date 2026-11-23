from ....colors import Colors
from ....controller.callbacks import Callback
from ....ui.elements import TunerDisplay
from .. import FractalIIMappings, FRACTAL_II

# Splash callback for the tuner display. Pass your default display root element as default splash, and a
# tuner display will be shown while the tuner is on (requires DIN MIDI and I/O > MIDI > SEND REALTIME SYSEX = TUNER
# or ALL on the device). Releasing any switch while the tuner is shown switches it off (tuner CC).
class FractalIITunerDisplayCallback(Callback):
    def __init__(self,
                 splash_default,                           # Default DisplayElement (root of default display to be shown when not in tuner mode)
                 splash_tuner = None,                      # DisplayElement to be shown when tuner is engaged
                 color_in_tune = Colors.LIGHT_GREEN,
                 color_out_of_tune = Colors.ORANGE,
                 color_neutral = Colors.WHITE,
                 calibration_high = 8192 + 350,            # Threshold value above which the note is out of tune (8192 + 8192 = 50 cents)
                 calibration_low = 8192 - 350,             # Threshold value below which the note is out of tune
                 note_names = None,                        # If set, this must be a tuple or list of 12 note name strings starting at C.
                 strobe = False,                           # If set, all available switch LEDs will act as a strobe tuner.
                 strobe_color = Colors.WHITE,              # LED color for strobe tuner
                 strobe_dim = 0.1,                         # Dim factor for strobe tuner in range [0..1]
                 strobe_speed = 1000,                      # Higher values make the strobe tuner go slower. 1000 is the recommended speed to start from.
                 strobe_max_fps = 120,                     # Maximum cumulative frame rate for update of strobe tuner LEDs
                 strobe_reverse = True,                    # If False, the strobe is rotating clockwise when too high / ccw when too low. If True, the other way round.
                 process_overridden_actions = False,       # If set, when in tuner mode, the underlying actions will also be processed after disabling the tuner.
                 tuner_cc = 15,                            # Tuner CC as set on the device (I/O > CTRL > Tuner), used to switch the tuner off
                 midi_channel = 1                          # MIDI channel of the device in range [1..16] (I/O > MIDI > Channel)
        ):
        Callback.__init__(self)

        self.__mapping = FractalIIMappings.TUNER_STATE()
        self.register_mapping(self.__mapping)

        self.__splash_tuner = splash_tuner
        self.__splash_default = splash_default
        self.__process_overridden_actions = process_overridden_actions
        self.__pushed_before = False
        self.__mapping_on_off = FractalIIMappings.TUNER_ON_OFF(tuner_cc, midi_channel - 1)

        if not self.__splash_tuner:
            self.__splash_tuner = TunerDisplay(
                mapping_note = FractalIIMappings.TUNER_NOTE(),
                mapping_deviance = FractalIIMappings.TUNER_DEVIANCE(),
                bounds = self.__splash_default.bounds,
                scale = 3,
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf"
                },
                color_in_tune = color_in_tune,
                color_out_of_tune = color_out_of_tune,
                color_neutral = color_neutral,
                calibration_high = calibration_high,
                calibration_low = calibration_low,
                note_names = note_names
            )

        if strobe:
            from ....controller.strobe import StrobeController

            self.__strobe_controller = StrobeController(
                mapping_state = self.__mapping,
                mapping_deviance = FractalIIMappings.TUNER_DEVIANCE(),
                dim_factor = strobe_dim,
                speed = strobe_speed,
                color = strobe_color,
                max_fps = strobe_max_fps,
                reverse = strobe_reverse
            )
        else:
            self.__strobe_controller = None

    def init(self, appl, listener = None):
        Callback.init(self, appl, listener)
        self.__appl = appl

        FRACTAL_II.init(appl.config)

        if self.__strobe_controller:
            self.__strobe_controller.init(appl)

    def update(self):
        Callback.update(self)
        self.__mapping.check(self.__appl.client)

    def parameter_changed(self, mapping):
        super().parameter_changed(mapping)

        if mapping != self.__mapping:
            return

        if self.__mapping.value == 1:
            # Tuner on
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = self

                    if not self.__process_overridden_actions:
                        input.color = Colors.WHITE
                        input.brightness = 0
        else:
            # Tuner off
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = None

                    for action in input.actions:
                        action.reset()

    def push(self):
        self.__pushed_before = True
        return self.__process_overridden_actions

    def release(self):
        if not self.__pushed_before:
            # This prevents that the tuner button switches off the tuner immediately at releasing
            return

        self.__pushed_before = False

        client = self.__appl.client
        client.set(self.__mapping_on_off, 0)
        self.__mapping.switched(client, False)

        return self.__process_overridden_actions

    def get_root(self):
        if self.__mapping.value != 1:
            return self.__splash_default
        else:
            return self.__splash_tuner
