from micropython import const

from ....controller.actions import PushButtonAction
from .. import FractalCallback, FractalMappings, FractalBlock, FractalChannel, FractalLabel, FractalSecondPress, COLOR_EFFECT, _inc_dec, _both
from ..mappings.effects import MAPPING_BLOCK_BYPASS, MAPPING_BLOCK_CHANNEL

# Effect: Bypass. Engages/bypasses a block (fixed block type and instance, like the FC Effect functions).
def EFFECT_BYPASS(block,                                  # Block type (see FractalBlock)
                  instance = 1,                           # Block instance (1-based)
                  label = FractalLabel.LONG_NAME,         # Label: LONG_NAME, SHORT_NAME, SHORT_NAME_CHANNEL, LONG_NAME_CHANNEL (see FractalLabel)
                  display = None,
                  mode = PushButtonAction.LATCH,          # Switch mode (see PushButtonAction)
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: effect category color)
                  text = None                             # Custom label text
    ):
    return PushButtonAction({
        "callback": FractalEffectCallback(
            function = FractalEffectCallback.BYPASS,
            block = block,
            instance = instance,
            label = label,
            color = color,
            text = text
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


#####################################################################################################################


# Callback for all effect functions. Reads the block state from the status dump (shared by all effect callbacks).
class FractalEffectCallback(FractalCallback):

    # Functions
    BYPASS = const(0)
    CHANNEL_SELECT = const(1)
    CHANNEL_TOGGLE = const(2)
    CHANNEL_INC_DEC = const(3)

    def __init__(self,
                 function,
                 block,
                 instance,
                 label,
                 color,
                 text,
                 channel = 0,                  # CHANNEL_SELECT: channel, CHANNEL_TOGGLE: primary channel
                 secondary = 0,                # CHANNEL_TOGGLE: secondary channel
                 second_press = None,          # CHANNEL_SELECT: 2nd press option (see FractalSecondPress)
                 step = 1,                     # CHANNEL_INC_DEC
                 wrap = True,                  # CHANNEL_INC_DEC
                 lower_limit = None,           # CHANNEL_INC_DEC
                 upper_limit = None            # CHANNEL_INC_DEC
        ):
        if block < 0 or block >= len(FractalBlock.NAMES):
            raise Exception("Invalid block: " + repr(block))

        self.__mapping = FractalMappings.STATUS_DUMP()

        super().__init__(
            color = color if color else COLOR_EFFECT,
            text = text,
            mappings = [self.__mapping]
        )

        self.__function = function
        self.__block = block
        self.__instance = instance
        self.__label = label
        self.__channel = channel
        self.__secondary = secondary
        self.__second_press = second_press
        self.__step = step
        self.__wrap = wrap
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit

        self.__id = FractalBlock.effect_id(block, instance)
        self.__mapping_bypass = MAPPING_BLOCK_BYPASS(self.__id)
        self.__mapping_channel = MAPPING_BLOCK_CHANNEL(self.__id) if function != self.BYPASS else None

        # Block state from the dump: present, engaged, channel, number of channels
        self.__present = False
        self.__engaged = False
        self.__current_channel = None
        self.__num_channels = 0
        self.__evaluated_dump = self           # Never a dump value

        self.__previous_channel = None
        self.__pushed = False

    # Block state
    @property
    def present(self):
        return self.__present

    @property
    def engaged(self):
        return self.__engaged

    @property
    def channel(self):
        return self.__current_channel

    # Called by PushButtonAction (bypass function)
    def state_changed_by_user(self):
        self.__evaluate()

        if not self.__present:
            self.action.feedback_state(False)
            return

        self.__set_bypass(self.action.state)

    def push(self):
        if self.__function == self.BYPASS:
            return

        self.__evaluate()

        if self.__function == self.CHANNEL_INC_DEC:
            self.__pushed = True

        if self.__present:
            current = self.__current_channel
            target = self.__target()

            if self.__function == self.CHANNEL_SELECT and current == target:
                # 2nd press
                if self.__second_press == FractalSecondPress.SMART_BYPASS:
                    self.__set_bypass(not self.__engaged)
                    target = None
                elif self.__second_press == FractalSecondPress.PREVIOUS_CHANNEL and self.__previous_channel != None:
                    target = self.__previous_channel
                else:
                    target = None

            if target != None and target != current:
                self.__previous_channel = current
                self.__set_channel(target)

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        self.__evaluate()

        function = self.__function
        present = self.__present
        engaged = self.__engaged
        current = self.__current_channel

        # LED state
        if not present:
            led = self.OFF

        elif function == self.BYPASS:
            led = self.BRIGHT if engaged else self.DIM

        elif function == self.CHANNEL_SELECT:
            if self.__second_press == FractalSecondPress.SMART_BYPASS:
                led = self.BRIGHT if (current == self.__channel and engaged) else self.DIM
            elif not engaged:
                led = self.OFF
            else:
                led = self.BRIGHT if current == self.__channel else self.DIM

        elif function == self.CHANNEL_TOGGLE:
            if current == self.__channel:
                led = self.BRIGHT
            elif current == self.__secondary:
                led = self.DIM
            else:
                led = self.OFF

        else:
            led = self.BRIGHT if self.__pushed else self.DIM

        if function == self.BYPASS:
            self.action.feedback_state(present and engaged)

        self._show(led, self._color, self.__get_text())

    # Sends a bypass message and shows the state locally
    def __set_bypass(self, engaged):
        self._appl.client.set(self.__mapping_bypass, 1 if engaged else 0)

        self.__engaged = engaged
        self.__set_feedback()

    # Sends a channel message and shows the channel locally
    def __set_channel(self, channel):
        self._appl.client.set(self.__mapping_channel, channel)

        self.__current_channel = channel
        self.__set_feedback()

    # Keeps the local state until the next dump has been received (the next answer is skipped, as it can
    # answer a request sent before the set message)
    def __set_feedback(self):
        self.__mapping.feedback(self.__mapping.value)
        self.__evaluated_dump = self.__mapping.value

    # Reads the block state from the status dump (if it changed and no local feedback is active)
    def __evaluate(self):
        dump = self.__mapping.value

        if dump is self.__evaluated_dump:
            return

        self.__evaluated_dump = dump

        self.__present = False

        if dump == None:
            return

        id = self.__id
        for i in range(0, len(dump) - 2, 3):
            if dump[i] + 128 * dump[i + 1] != id:
                continue

            data = dump[i + 2]

            self.__present = True
            self.__engaged = not (data & 0x01)
            self.__current_channel = (data >> 1) & 0x07
            self.__num_channels = (data >> 4) & 0x07
            return

    # Channel to select when pressed
    def __target(self):
        function = self.__function

        if function == self.CHANNEL_SELECT:
            return self.__channel

        if function == self.CHANNEL_TOGGLE:
            return self.__secondary if self.__current_channel == self.__channel else self.__channel

        if function == self.CHANNEL_INC_DEC and self.__current_channel != None:
            return _inc_dec(
                self.__current_channel,
                self.__step,
                self.__wrap,
                self.__lower_limit if self.__lower_limit != None else 0,
                self.__upper_limit if self.__upper_limit != None else max(self.__num_channels - 1, 0)
            )

        return None

    # Label text
    def __get_text(self):
        label = self.__label
        block = self.__block
        instance = self.__instance
        current = self.__current_channel if self.__present else None

        # Channel for the "+ Channel" labels: the switch's channel for Channel Select, else the current one
        channel = self.__channel if self.__function == self.CHANNEL_SELECT else current

        if label == FractalLabel.LONG_NAME:
            return f"{ FractalBlock.NAMES[block] } { instance }"

        if label == FractalLabel.LONG_NAME_CHANNEL:
            return f"{ FractalBlock.NAMES[block] } { instance }" + (f" { FractalChannel.NAMES[channel] }" if channel != None else "")

        short = f"{ FractalBlock.ABBREVIATIONS[block] }{ instance }"

        if label == FractalLabel.SHORT_NAME_CHANNEL:
            return short + (f" { FractalChannel.NAMES[channel] }" if channel != None else "")

        if label == FractalLabel.CURRENT_CHANNEL:
            return short + (f" { FractalChannel.NAMES[current] }" if current != None else "")

        if label == FractalLabel.BOTH_CHANNELS:
            return short + " " + _both(
                FractalChannel.NAMES[self.__channel],
                FractalChannel.NAMES[self.__secondary],
                current == self.__channel,
                current == self.__secondary
            ).replace(" ", "")

        if label == FractalLabel.DESTINATION_CHANNEL:
            target = self.__target() if self.__present else None
            return short + (f" { FractalChannel.NAMES[target] }" if target != None else "")

        if label == FractalLabel.ACTION:
            return f"{ short } +{ self.__step }" if self.__step > 0 else f"{ short } { self.__step }"

        return short
