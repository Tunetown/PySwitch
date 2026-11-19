from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ....colors import Colors

# Generic switch action which can be used for all parameter mappings. This is designed to work with 
# parameters providing Feedback from the client by requesting parameters actively (like the Kemper is able to do).
# 
# If you want to just send MIDI messages or control devices with no feedback, use the Custom MIDI Message instead.
def BINARY_SWITCH(mapping, 
                  display = None, 
                  text = "", 
                  mode = PushButtonAction.HOLD_MOMENTARY, 
                  color = Colors.WHITE, 
                  id = False, 
                  use_leds = True, 
                  enable_callback = None,
                  value_on = 1,
                  value_off = 0,
                  reference_value = None,
                  comparison_mode = BinaryParameterCallback.GREATER_EQUAL,
                  display_dim_factor_on = None,                               # Dim factor in range [0..1] for on state (display label) Optional.
                                                                              # If None, the global config value will be used
                                                                              # If "off", the global off config value will be used.
                  display_dim_factor_off = None,                              # Dim factor in range [0..1] for off state (display label) Optional.
                                                                              # If None, the global config value will be used
                                                                              # If "on", the global on config value will be used.
                  led_brightness_on = None,                                   # LED brightness [0..1] for on state (Switch LEDs) Optional.
                                                                              # If None, the global config value will be used    
                                                                              # If "off", the global off config value will be used.
                  led_brightness_off = None,                                  # LED brightness [0..1] for off state (Switch LEDs) Optional.
                                                                              # If None, the global config value will be used
                                                                              # If "on", the global on config value will be used.
                  use_internal_state = False                                  # If enabled, the callback will not wait until a MIDI value comes in, the state is displayed as-is any time.
    ):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = mapping,
            text = text,
            color = color,
            value_enable = value_on,
            value_disable = value_off,
            reference_value = reference_value,
            comparison_mode = comparison_mode,
            display_dim_factor_on = display_dim_factor_on,
            display_dim_factor_off = display_dim_factor_off,
            led_brightness_on = led_brightness_on,
            led_brightness_off = led_brightness_off,
            use_internal_state = use_internal_state
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })
