from ....controller.callbacks import Callback
from ....controller.actions import Action

# Sends a bunch of messages in rotating fashion. The messages as well as the colors and texts will be rotated on each press. 
# 
# The messages have to be raw bytes, so don't forget to also add the status and (in case of SysEx) closing bytes!
# You can use lists or tuples for all parameters where multiple values are passed.
def ROTATING_MESSAGES(messages = None,              # Raw MIDI messages bytes (as list of rotating messages in list format, for example [[176, 80, 0], [176, 89, 1]] for two alternating control change messages). You can use hex values in format 0xab, too.
                      messages_release = None,      # Raw MIDI messages to be sent on releasing the button. Same format and handling as the messages parameter. 
                      led_colors = None,            # List of colors to rotate for the LEDs                      
                      led_brightness = 0.15,        # LED brighness in range [0..1]                      
                      display = None,
                      display_colors = None,        # List of colors to rotate for the display label. If not set, the led colors will be used.
                      texts = "",                   # List of texts for each of the rotating states
                      use_leds = True,
                      id = None,
                      enable_callback = None,
                      num_leds = 1                  # If greater than one, led_colors must be a list of lists, each entry having exactly this amount of colors, which will be rotated.
    ):
    if num_leds > 1:
        # The first action will send messages and drive the display. The others just set LEDs
        return [
            Action({
                "callback": _CustomMessagesCallback(
                    messages = messages if i == 0 else None,
                    messages_release = messages_release if i == 0 else None,
                    led_colors = led_colors[i],
                    led_brightness = led_brightness,
                    display_colors = display_colors if i == 0 else None,
                    texts = texts if i == 0 else None
                ),
                "display": display if i == 0 else None,
                "useSwitchLeds": use_leds,
                "id": id,
                "enableCallback": enable_callback
            })            
            for i in range(num_leds)
        ]

    else:
        return Action({
            "callback": _CustomMessagesCallback(
                messages = messages,
                messages_release = messages_release,
                led_colors = led_colors,
                led_brightness = led_brightness,
                display_colors = display_colors,
                texts = texts
            ),
            "display": display,
            "useSwitchLeds": use_leds,
            "id": id,
            "enableCallback": enable_callback
        })


class _CustomMessagesCallback(Callback):
    def __init__(self, 
                 messages,
                 messages_release,
                 led_colors,
                 led_brightness,
                 display_colors,
                 texts
        ):
        super().__init__()
        
        self.__messages = messages
        self.__messages_release = messages_release
        self.__led_colors = led_colors
        self.__led_brightness = led_brightness
        self.__display_colors = display_colors if display_colors else led_colors
        self.__texts = texts

        self.__messages_pos = 0
        self.__messages_release_pos = 0
        self.__led_colors_pos = 0
        self.__display_colors_pos = 0
        self.__texts_pos = 0

    def init(self, appl, listener = None):
        self.__appl = appl

    def push(self):
        if self.__messages:
            self.__appl.client.midi.send(self.__messages[self.__messages_pos])

    def release(self):
        if self.__messages_release:
            self.__appl.client.midi.send(self.__messages_release[self.__messages_release_pos])

        self.__next_step()
        self.update_displays()

    def __next_step(self):
        self.__messages_pos += 1
        self.__messages_release_pos += 1
        self.__led_colors_pos += 1
        self.__display_colors_pos += 1
        self.__texts_pos += 1

        if self.__messages and self.__messages_pos >= len(self.__messages):
            self.__messages_pos = 0

        if self.__messages_release and self.__messages_release_pos >= len(self.__messages_release):
            self.__messages_release_pos = 0

        if self.__led_colors and self.__led_colors_pos >= len(self.__led_colors):
            self.__led_colors_pos = 0

        if self.__display_colors and self.__display_colors_pos >= len(self.__display_colors):
            self.__display_colors_pos = 0

        if self.__texts and self.__texts_pos >= len(self.__texts):
            self.__texts_pos = 0

    def update_displays(self):
        if self.__led_colors:
            self.action.switch_color = self.__led_colors[self.__led_colors_pos]
            self.action.switch_brightness = self.__led_brightness

        if self.action.label:
            if self.__texts:
                self.action.label.text = self.__texts[self.__texts_pos]
                
            if self.__display_colors:
                self.action.label.back_color = self.__display_colors[self.__display_colors_pos]
