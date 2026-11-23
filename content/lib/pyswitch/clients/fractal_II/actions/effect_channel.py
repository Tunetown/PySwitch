from ....controller.actions import Action
from .. import FractalIIBlock, FractalIIChannel, FractalIILabel
from .effect_bypass import FractalIIEffectCallback

# Effect channel functions like the FC "Effect" category. The Axe-Fx II blocks have the channels X and Y (see FractalIIChannel).


# Effect: Channel Select
def EFFECT_CHANNEL_SELECT(block = FractalIIBlock.AMP_1,           # Block (see FractalIIBlock)
                          channel = FractalIIChannel.Y,           # Channel to select (see FractalIIChannel)
                          second_press = None,                    # Pressing the switch while its channel is active: None (no function), SMART_BYPASS or PREVIOUS_CHANNEL (the other channel) (see FractalIISecondPress)
                          label = FractalIILabel.SHORT_NAME_CHANNEL, # Label: SHORT_NAME_CHANNEL, LONG_NAME_CHANNEL, SHORT_NAME, LONG_NAME, DESTINATION_CHANNEL (see FractalIILabel)
                          display = None,
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                           # Color override (default: effect category color)
                          text = None                             # Custom label text
    ):
    return _create(FractalIIEffectCallback.CHANNEL_SELECT, block, channel, second_press, label, display, id, use_leds, enable_callback, color, text)

# Effect: Channel Toggle (X/Y). The LED is bright on X and dim on Y.
def EFFECT_CHANNEL_TOGGLE(block = FractalIIBlock.AMP_1,           # Block (see FractalIIBlock)
                          label = FractalIILabel.BOTH_CHANNELS,   # Label: BOTH_CHANNELS, DESTINATION_CHANNEL, CURRENT_CHANNEL, SHORT_NAME, LONG_NAME (see FractalIILabel)
                          display = None,
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                           # Color override (default: effect category color)
                          text = None                             # Custom label text
    ):
    return _create(FractalIIEffectCallback.CHANNEL_TOGGLE, block, 0, None, label, display, id, use_leds, enable_callback, color, text)


def _create(function, block, channel, second_press, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": FractalIIEffectCallback(
            function = function,
            block = block,
            label = label,
            color = color,
            text = text,
            channel = channel,
            second_press = second_press
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })
