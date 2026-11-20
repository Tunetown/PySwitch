from ....controller.actions import Action
from .. import FractalLabel
from .effect_bypass import FractalEffectCallback

# Effect channel functions like the FC "Effect" category. Channels: see FractalChannel (A-D, E/F for the Multiplexer).


# Effect: Channel Select
def EFFECT_CHANNEL_SELECT(block,                                  # Block type (see FractalBlock)
                          channel,                                # Channel to select (see FractalChannel)
                          instance = 1,                           # Block instance (1-based)
                          second_press = None,                    # Pressing the switch while its channel is active: None (no function), SMART_BYPASS or PREVIOUS_CHANNEL (see FractalSecondPress)
                          label = FractalLabel.SHORT_NAME_CHANNEL,# Label: SHORT_NAME_CHANNEL, LONG_NAME_CHANNEL, SHORT_NAME, LONG_NAME, DESTINATION_CHANNEL (see FractalLabel)
                          display = None,
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                           # Color override (default: effect category color)
                          text = None                             # Custom label text
    ):
    return _create(FractalEffectCallback.CHANNEL_SELECT, block, instance, channel, 0, second_press, 1, True, None, None, label, display, id, use_leds, enable_callback, color, text)

# Effect: Channel Toggle
def EFFECT_CHANNEL_TOGGLE(block,                                  # Block type (see FractalBlock)
                          primary,                                # Primary channel (see FractalChannel)
                          secondary,                              # Secondary channel (see FractalChannel)
                          instance = 1,                           # Block instance (1-based)
                          label = FractalLabel.BOTH_CHANNELS,     # Label: BOTH_CHANNELS, DESTINATION_CHANNEL, CURRENT_CHANNEL, SHORT_NAME, LONG_NAME (see FractalLabel)
                          display = None,
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                           # Color override (default: effect category color)
                          text = None                             # Custom label text
    ):
    return _create(FractalEffectCallback.CHANNEL_TOGGLE, block, instance, primary, secondary, None, 1, True, None, None, label, display, id, use_leds, enable_callback, color, text)

# Effect: Channel Increment / Decrement
def EFFECT_CHANNEL_INC_DEC(block,                                 # Block type (see FractalBlock)
                           instance = 1,                          # Block instance (1-based)
                           step = 1,                              # Step size: positive for next, negative for previous channels
                           wrap = True,                           # Wrap around at the ends
                           lower_limit = None,                    # Lowest channel (see FractalChannel) or None for no limit
                           upper_limit = None,                    # Highest channel (see FractalChannel) or None for the last channel of the block
                           label = FractalLabel.ACTION,           # Label: ACTION, DESTINATION_CHANNEL, CURRENT_CHANNEL, SHORT_NAME, LONG_NAME (see FractalLabel)
                           display = None,
                           id = False,
                           use_leds = True,
                           enable_callback = None,
                           color = None,                          # Color override (default: effect category color)
                           text = None                            # Custom label text
    ):
    return _create(FractalEffectCallback.CHANNEL_INC_DEC, block, instance, 0, 0, None, step, wrap, lower_limit, upper_limit, label, display, id, use_leds, enable_callback, color, text)


def _create(function, block, instance, channel, secondary, second_press, step, wrap, lower_limit, upper_limit, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": FractalEffectCallback(
            function = function,
            block = block,
            instance = instance,
            label = label,
            color = color,
            text = text,
            channel = channel,
            secondary = secondary,
            second_press = second_press,
            step = step,
            wrap = wrap,
            lower_limit = lower_limit,
            upper_limit = upper_limit
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })
