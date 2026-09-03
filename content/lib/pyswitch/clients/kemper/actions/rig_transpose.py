from ....controller.actions.EncoderAction import EncoderAction
from ..mappings.rig import MAPPING_RIG_TRANSPOSE
from .. import KemperMappings

# Adjusts the global rig transpose value.
def ENCODER_RIG_TRANSPOSE(
    midi_channel = 1,              # MIDI Channel in range [1..16]
    accept_action = None,          # Action to acknowledge the entered value. If None, the encoder directly sets values as you turn it. 
                                   # If you pass an Encoder Button action, the value will just be displayed and the MIDI command to set 
                                   # it will be sent when the Button action is triggered.
                                   # 
                                   # If you use this, you will also need a preview display label (see below)
    cancel_action = None,          # Action to cancel a preselection (only makes sense with accept_action set). Must be of type Encoder Button, too.
    preview_display = None,        # If assigned, the adjusted value will be displayed in the passed DisplayLabel when the encoder is adjusted. 
                                   # 
                                   # This just makes sense in conjunction with an accept action (see above).
    preview_blink_color = (200, 200, 200), # Alternative color to be used when blinking.
    preview_timeout_millis = 1500, # This is the amount of time (milliseconds) after which the 
                                   # preview display will return to its normal state.
    enable_callback = None,
    id = None
):
    return EncoderAction(
        mapping = MAPPING_RIG_TRANSPOSE(),
        min_value = 28,
        max_value = 100,
        step_width = 1,
        enable_callback = enable_callback,
        id = id,
        accept_action = accept_action,
        cancel_action = cancel_action,          
        preview_display = preview_display,
        preview_timeout_millis = preview_timeout_millis,
        preview_blink_color = preview_blink_color,
        preview_reset_mapping = KemperMappings.RIG_ID(midi_channel - 1),
        convert_value = _convert_transpose,
    )

# Output conversion for transpose
def _convert_transpose(value):
    halfsteps = value - 64
    return f"Transpose: { "+" if halfsteps > 0 else ""}{ str(halfsteps) }"

