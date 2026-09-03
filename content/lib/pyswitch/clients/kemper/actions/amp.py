from ....controller.actions.EncoderAction import EncoderAction
from ..mappings.amp import MAPPING_AMP_GAIN
from .. import KemperMappings

# Adjusts the amp gain with a rotary encoder.
def AMP_GAIN(
    midi_channel = 1,              # MIDI Channel in range [1..16]
    step_width = None,             # Increment/Decrement for one encoder step. Set to None for auto-detect (NRPN: 80, CC: 1)
    accept_action = None,          # Action to acknowledge the entered value. If None, the encoder directly sets values as you turn it. 
                                   # If you pass an Encoder Button action, the value will just be displayed and the MIDI command to set 
                                   # it will be sent when the Button action is triggered.
                                   # 
                                   # If you use this, you will also need a preview display label (see below)
    cancel_action = None,          # Action to cancel a preselection (only makes sense with accept_action set). Must be of type Encoder Button, too.
    preview_display = None,        # If assigned, the adjusted value will be displayed in the passed DisplayLabel when the encoder is adjusted. 
                                   # 
                                   # This just makes sense in conjunction with an accept action (see above).
    preview_timeout_millis = 1500, # This is the amount of time (milliseconds) after which the 
                                   # preview display will return to its normal state.
    preview_blink_color = (200, 200, 200), # Alternative color to be used when blinking.
    enable_callback = None,
    id = None
):
    return EncoderAction(
        mapping = MAPPING_AMP_GAIN(),
        step_width = step_width,
        enable_callback = enable_callback,
        id = id,
        accept_action = accept_action,   
        cancel_action = cancel_action,             
        preview_blink_color = preview_blink_color,
        preview_display = preview_display,
        preview_timeout_millis = preview_timeout_millis,
        preview_reset_mapping = KemperMappings.RIG_ID(midi_channel - 1),
        convert_value = _convert_gain,
    )

def _convert_gain(value):
    return f"Gain: { str(round(value / 1638.3, 1)) }"