from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ....colors import Colors

from ..mappings.effects import MAPPING_EFFECT_BUTTON
from .. import KemperMappings

# Effect Button I-IIII (set only). num must be a number (1 to 4).
# 
# <b>NOTE:</b> The state of the display will be toggled no matter what the real status on the Kemper is (the Kemper sadly does not report the state at all). 
# If you dont want this behaviour, you can set "use_internal_state = False".
def EFFECT_BUTTON(num,                           # Number of the Effect Button (1 to 4)
                  text = None, 
                  display = None, 
                  midi_channel = 1,              # MIDI Channel in range [1..16]
                  color = Colors.LIGHT_GREEN, 
                  id = False, 
                  use_leds = True, 
                  enable_callback = None, 
                  use_internal_state = True      # If enabled, the state of the display will be toggled no matter what the real status on the Kemper is (the Kemper sadly does not report the state at all). 
    ):
    if not text:
        if num == 1:
            text = "FX I"
        elif num == 2:
            text = "FX II"
        elif num == 3:
            text = "FX III"
        elif num == 4:
            text = "FX IIII"

    return PushButtonAction({
        "callback": _KemperEffectButtonCallback(
            mapping = MAPPING_EFFECT_BUTTON(num, midi_channel - 1),
            text = text,
            color = color,
            use_internal_state = use_internal_state,
            channel = midi_channel - 1
        ),
        "mode": PushButtonAction.LATCH,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


# Special callback which listens for changing rig ID to reset effect state
class _KemperEffectButtonCallback(BinaryParameterCallback):
    
    def __init__(self, 
                 mapping,
                 text,
                 color,
                 use_internal_state,
                 channel
    ):
        super().__init__(
            mapping = mapping,
            text = text,
            color = color,
            comparison_mode = BinaryParameterCallback.NO_STATE_CHANGE,
            use_internal_state = use_internal_state
        )

        self.__rig_mapping = KemperMappings.RIG_ID(channel)
        self.register_mapping(self.__rig_mapping)

    def parameter_changed(self, mapping):
        super().parameter_changed(mapping)
        
        if mapping != self.__rig_mapping:
            return

        if self.action.state:
            self.action.feedback_state(False)
            self.update_displays()



