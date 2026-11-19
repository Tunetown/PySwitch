from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ...kemper import NRPN_VALUE
from ....colors import Colors

from ..mappings.rig import MAPPING_RIG_VOLUME

# Volume boost function, based on setting rig volume to a certain boost value.
def RIG_VOLUME_BOOST(boost_volume,                              # Boost volume: A value in range [0..1] (corresponding to the range of the
                                                                # rig volume parameter of the Kemper. Some examples: 0.5 is 0dB, 0.625 is +3dB, 0.75 is +6dB, 1.0 is +12dB
                     display = None, 
                     mode = PushButtonAction.HOLD_MOMENTARY, 
                     color = Colors.PINK, 
                     id = False, 
                     use_leds = True, 
                     text = "RigBoost", 
                     remember_off_value = True,                 # If set, the boost will return to the former rig volume at disabling
                     enable_callback = None
    ):
    return PushButtonAction({
        "callback": BinaryParameterCallback(
            mapping = MAPPING_RIG_VOLUME(),
            text = text,
            color = color,
            value_enable = NRPN_VALUE(boost_volume),
            value_disable = NRPN_VALUE(0.5) if not remember_off_value else "auto",    # 0.5 = 0dB
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })