import usb_hid
from adafruit_hid.keyboard import Keyboard

from ....controller.callbacks import Callback
from ....controller.actions import Action
from ....colors import Colors

# Sends a HID (Human Interface Device) command which emulates an USB keyboard. 
# 
# With this, the controller can work as an USB page turner for example.
def HID_KEYBOARD(
    keycodes,               # Key code(s) to send. Can be either a single key code or a list/tuple of key codes. 
                            # Search "adafruit_hid.keycode" for available key codes, for example Keycode.LEFT_ARROW.
    display = None, 
    text = "", 
    color = Colors.LIGHT_BLUE,
    led_brightness = 0.15,
    id = False, 
    use_leds = True, 
    enable_callback = None    
):
    return Action({
        "callback": HidCallback(
            keycodes = keycodes,
            text = text,
            color = color,
            led_brightness = led_brightness         
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


class HidCallback(Callback):

    def __init__(self, keycodes, text, color, led_brightness):
        super().__init__()

        self.__text = text
        self.__color = color
        self.__led_brightness = led_brightness
        self.__keycodes = [keycodes] if not isinstance(keycodes, list) and not isinstance(keycodes, tuple) else keycodes
        
    def push(self):
        kbd = self._get_keyboard()
        if not kbd:
            return

        for code in self.__keycodes:
            kbd.send(code)

    def release(self):
        pass

    def update_displays(self):
        self.action.switch_color = self.__color
        self.action.switch_brightness = self.__led_brightness

        if self.action.label:
            self.action.label.text = self.__text
            self.action.label.back_color = self.__color

    def _get_keyboard(self):
        try:
            return Keyboard(usb_hid.devices)
        except OSError:
            return None
