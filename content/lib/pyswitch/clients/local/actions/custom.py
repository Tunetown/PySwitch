from ....controller.callbacks import Callback
from ....controller.actions import Action
from ....colors import Colors

# Sends a single raw, arbitrary MIDI message.
# 
# The messages have to be raw bytes, so don't forget to also add the status and (in case of SysEx) closing bytes!
def CUSTOM_MESSAGE(message,                 # Raw MIDI message bytes (as list, for example [176, 80, 0] for a control change). You can use hex values in format 0xab, too.
                   message_release = None,  # Raw MIDI message to be sent on releasing the button (default: None)
                   text = "",
                   color = Colors.WHITE,
                   led_brightness = 0.15,   # LED brighness in range [0..1]
                   display = None,
                   use_leds = True,
                   id = None,
                   enable_callback = None
    ):
    return Action({
        "callback": _CustomMessageCallback(
            message = message,
            message_release = message_release,
            color = color,
            led_brightness = led_brightness,
            text = text
        ),
        "display": display,
        "useSwitchLeds": use_leds,
        "id": id,
        "enableCallback": enable_callback
    })            


class _CustomMessageCallback(Callback):
    def __init__(self, 
                 message,
                 message_release,
                 color,
                 led_brightness,
                 text
        ):
        super().__init__()
        
        self.__message = message
        self.__message_release = message_release
        self.__color = color
        self.__text = text
        self.__led_brightness = led_brightness

    def init(self, appl, listener = None):
        self.__appl = appl

    def push(self):
        self.__appl.client.midi.send(self.__message)

    def release(self):
        if self.__message_release:
            self.__appl.client.midi.send(self.__message_release)
    
    def update_displays(self):
        self.action.switch_color = self.__color
        self.action.switch_brightness = self.__led_brightness

        if self.action.label:
            self.action.label.text = self.__text
            self.action.label.back_color = self.__color
