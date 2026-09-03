from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ...kemper import KemperMappings
from ....colors import DEFAULT_SWITCH_COLOR

# Switch tuner mode on / off
def TUNER_MODE(display = None, 
               midi_channel = 1,                       # MIDI Channel in range [1..16]
               mode = PushButtonAction.HOLD_MOMENTARY, 
               color = DEFAULT_SWITCH_COLOR, 
               text = "Tuner", 
               id = False, 
               use_leds = True, 
               enable_callback = None
    ):
    return PushButtonAction({
        "callback": _TunerModeCallback(
            text = text,
            color = color,
            channel = midi_channel - 1
        ),
        "mode": mode,   
        "display": display,            
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


# Callback for tuner mode
class _TunerModeCallback(BinaryParameterCallback):
    def __init__(self, color, text, channel):
        self.__mapping = KemperMappings.TUNER_MODE_STATE(channel)
        super().__init__(
            mapping = self.__mapping,
            comparison_mode = BinaryParameterCallback.EQUAL,
            text = text,
            color = color
        )

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

    def state_changed_by_user(self):
        # Code from BinaryParameterCallback.state_changed_by_user (implemented here directly to reduce stack size)
        self.__appl.client.set(self.__mapping, self._value_enable if self.action.state else self._value_disable)
        
        # Request value
        self.update()
