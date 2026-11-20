from ....controller.actions.EncoderAction import EncoderAction
from .. import FractalMappings, FRACTAL

# Selects presets with a rotary encoder.
def ENCODER_PRESET_SELECT(
    midi_channel = 1,              # MIDI Channel in range [1..16]
    step_width = 0.5,              # Increment/Decrement for one encoder step. Can be set to any value greater than 0 (including float values).
    accept_action = None,          # Action to acknowledge the entered value. If None, the encoder directly selects presets as you turn it.
                                   # If you pass an Encoder Button action, the preset will just be displayed and selected when the Button action is triggered.
                                   # If you use this, you will also need a preview display label (see below)
    cancel_action = None,          # Action to cancel a preselection (only makes sense with accept_action set). Must be of type Encoder Button, too.
    preview_display = None,        # If assigned, the preset number will be displayed in the passed DisplayLabel when the encoder is adjusted.
    preview_blink_color = (200, 200, 200), # Alternative color to be used when blinking.
    preview_timeout_millis = 1500, # This is the amount of time (milliseconds) after which the preview display will return to its normal state.
    enable_callback = None,
    id = None
):
    return _FractalPresetSelectEncoderAction(
        channel = midi_channel - 1,
        step_width = step_width,
        accept_action = accept_action,
        cancel_action = cancel_action,
        preview_display = preview_display,
        preview_blink_color = preview_blink_color,
        preview_timeout_millis = preview_timeout_millis,
        enable_callback = enable_callback,
        id = id
    )


# The current preset is read from PRESET(), presets are selected with PRESET_SELECT(channel)
class _FractalPresetSelectEncoderAction(EncoderAction):
    def __init__(self, channel, step_width, accept_action, cancel_action, preview_display, preview_blink_color, preview_timeout_millis, enable_callback, id):
        self.__mapping_preset = FractalMappings.PRESET()

        super().__init__(
            mapping = FractalMappings.PRESET_SELECT(channel),
            min_value = 0,
            max_value = 511,
            step_width = step_width,
            enable_callback = enable_callback,
            id = id,
            accept_action = accept_action,
            cancel_action = cancel_action,
            preview_display = preview_display,
            preview_timeout_millis = preview_timeout_millis,
            preview_blink_color = preview_blink_color,
            preview_reset_mapping = self.__mapping_preset,
            convert_value = _convert_value
        )

    def init(self, appl):
        super().init(appl)

        FRACTAL.init(appl.config)

        # The number of presets depends on the model (config.py), which is only known now. EncoderAction keeps the
        # maximum in a private member: CPython mangles its name, MicroPython does not, so both names are set.
        setattr(self, "_EncoderAction__max_value", FRACTAL.num_presets - 1)
        setattr(self, "__max_value", FRACTAL.num_presets - 1)

    def update(self):
        super().update()
        self._appl.client.request(self.__mapping_preset)

    def _get_value(self):
        return self.__mapping_preset.value

    def _set_value(self, value):
        self.__mapping_preset.feedback(value)
        FRACTAL.selected_bank = None


def _convert_value(value):
    return "Preset " + FRACTAL.preset_text(value)
