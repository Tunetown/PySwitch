from ....controller.actions import PushButtonAction
from .. import FractalIICallback, FractalIIMappings, FractalIIBlock, FractalIIChannel, FractalIILabel, FractalIISecondPress, COLOR_EFFECT, _both

# Effect: Bypass. Engages/bypasses a block (like the FC Effect functions).
def EFFECT_BYPASS(block = FractalIIBlock.AMP_1,           # Block (see FractalIIBlock)
                  label = FractalIILabel.LONG_NAME,       # Label: LONG_NAME, SHORT_NAME, SHORT_NAME_CHANNEL, LONG_NAME_CHANNEL (see FractalIILabel)
                  display = None,
                  mode = PushButtonAction.LATCH,          # Switch mode (see PushButtonAction)
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: effect category color)
                  text = None                             # Custom label text
    ):
    return PushButtonAction({
        "callback": FractalIIEffectCallback(
            function = FractalIIEffectCallback.BYPASS,
            block = block,
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


# Callback for all effect functions. Reads the block state from the block states answer (shared by all effect callbacks).
class FractalIIEffectCallback(FractalIICallback):

    # Functions
    BYPASS = 0
    CHANNEL_SELECT = 1
    CHANNEL_TOGGLE = 2

    def __init__(self,
                 function,
                 block,
                 label,
                 color,
                 text,
                 channel = 0,                  # CHANNEL_SELECT: channel
                 second_press = None           # CHANNEL_SELECT: 2nd press option (see FractalIISecondPress)
        ):
        if FractalIIBlock.name(block) == None:
            raise Exception("Invalid block: " + repr(block))

        self.__mapping = FractalIIMappings.BLOCK_STATES()

        super().__init__(
            color = color if color else COLOR_EFFECT,
            text = text,
            mappings = [self.__mapping]
        )

        self.__function = function
        self.__block = block
        self.__label = label
        self.__channel = channel
        self.__second_press = second_press

        self.__mapping_bypass = FractalIIMappings.BYPASS(block)
        self.__mapping_channel = FractalIIMappings.CHANNEL(block) if function != self.BYPASS else None

        # Block state from the block states answer: present, engaged, channel
        self.__present = False
        self.__engaged = False
        self.__current_channel = None
        self.__evaluated = self               # Never a block states value

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

        if self.__present:
            current = self.__current_channel
            target = self.__target()

            if self.__function == self.CHANNEL_SELECT and current == target:
                # 2nd press
                if self.__second_press == FractalIISecondPress.SMART_BYPASS:
                    self.__set_bypass(not self.__engaged)
                    target = None
                elif self.__second_press == FractalIISecondPress.PREVIOUS_CHANNEL:
                    target = 1 - current
                else:
                    target = None

            if target != None:
                self.__set_channel(target)

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
            if self.__second_press == FractalIISecondPress.SMART_BYPASS:
                led = self.BRIGHT if (current == self.__channel and engaged) else self.DIM
            elif not engaged:
                led = self.OFF
            else:
                led = self.BRIGHT if current == self.__channel else self.DIM

        else:
            led = self.BRIGHT if current == FractalIIChannel.X else self.DIM

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

    # Keeps the local state until the next block states answer has been received (the next answer is skipped, as
    # it can answer a request sent before the set message)
    def __set_feedback(self):
        self.__mapping.feedback(self.__mapping.value)
        self.__evaluated = self.__mapping.value

    # Reads the block state from the block states answer (if it changed and no local feedback is active)
    def __evaluate(self):
        states = self.__mapping.value

        if states is self.__evaluated:
            return

        self.__evaluated = states
        self.__present = False

        if states == None:
            return

        block = self.__block
        for i in range(0, len(states) - 1, 2):
            if states[i] != block:
                continue

            flags = states[i + 1]

            self.__present = True
            self.__engaged = (flags & 0x01) != 0
            self.__current_channel = FractalIIChannel.X if (flags & 0x02) else FractalIIChannel.Y
            return

    # Channel to select when pressed
    def __target(self):
        if self.__function == self.CHANNEL_SELECT:
            return self.__channel

        # Toggle
        return 1 - self.__current_channel

    # Label text
    def __get_text(self):
        label = self.__label
        block = self.__block
        current = self.__current_channel if self.__present else None

        # Channel for the "+ Channel" labels: the switch's channel for Channel Select, else the current one
        channel = self.__channel if self.__function == self.CHANNEL_SELECT else current

        if label == FractalIILabel.LONG_NAME:
            return FractalIIBlock.name(block)

        if label == FractalIILabel.LONG_NAME_CHANNEL:
            return FractalIIBlock.name(block) + (f" { FractalIIChannel.NAMES[channel] }" if channel != None else "")

        short = FractalIIBlock.name(block, True)

        if label == FractalIILabel.SHORT_NAME_CHANNEL:
            return short + (f" { FractalIIChannel.NAMES[channel] }" if channel != None else "")

        if label == FractalIILabel.CURRENT_CHANNEL:
            return short + (f" { FractalIIChannel.NAMES[current] }" if current != None else "")

        if label == FractalIILabel.BOTH_CHANNELS:
            return short + " " + _both("X", "Y", current == FractalIIChannel.X, current == FractalIIChannel.Y).replace(" ", "")

        if label == FractalIILabel.DESTINATION_CHANNEL:
            target = self.__target() if current != None else None
            return short + (f" { FractalIIChannel.NAMES[target] }" if target != None else "")

        return short
