from micropython import const

from ....controller.actions import Action
from .. import FractalCallback, FractalMappings, FractalLabel, FRACTAL, COLOR_PRESET, _inc_dec, _both, _action_text
from ..mappings.preset import FractalPresetTargetNameMapping

# Preset functions like the FC "Preset" category. Preset numbers are 0-based (as shown by the device with
# Display Offset 0), positions in a bank are 1-based. Bank size: option "fractalBankSize" in config.py.

_SELECT = const(0)
_SELECT_IN_BANK = const(1)
_TOGGLE = const(2)
_TOGGLE_IN_BANK = const(3)
_INC_DEC = const(4)


# Preset: Select by Number
def PRESET_SELECT(preset,                                 # Preset number (0-based)
                  second_press_previous = False,          # If enabled, pressing the switch again loads the previously loaded preset
                  label = FractalLabel.NAME,              # Label: NAME, NUMBER, P_NUM (see FractalLabel)
                  display = None,
                  midi_channel = 1,                       # MIDI Channel in range [1..16]
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: preset category color)
                  text = None                             # Custom label text
    ):
    return _create(_SELECT, preset, None, 1, False, None, None, second_press_previous, label, display, midi_channel, id, use_leds, enable_callback, color, text)

# Preset: Select in Bank
def PRESET_SELECT_IN_BANK(position,                       # Position in the bank [1..bank size]
                          second_press_previous = False,  # If enabled, pressing the switch again loads the previously loaded preset
                          label = FractalLabel.NAME,      # Label: NAME, NUMBER, P_NUM (see FractalLabel)
                          display = None,
                          midi_channel = 1,               # MIDI Channel in range [1..16]
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                   # Color override (default: preset category color)
                          text = None                     # Custom label text
    ):
    return _create(_SELECT_IN_BANK, position, None, 1, False, None, None, second_press_previous, label, display, midi_channel, id, use_leds, enable_callback, color, text)

# Preset: Toggle by Number
def PRESET_TOGGLE(primary,                                # Primary preset number (0-based)
                  secondary,                              # Secondary preset number (0-based)
                  label = FractalLabel.BOTH_NUM,          # Label: BOTH_NUM, DESTINATION_NAME, DESTINATION_NUM, CURRENT_NAME, CURRENT_NUM (see FractalLabel)
                  display = None,
                  midi_channel = 1,                       # MIDI Channel in range [1..16]
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: preset category color)
                  text = None                             # Custom label text
    ):
    return _create(_TOGGLE, primary, secondary, 1, False, None, None, False, label, display, midi_channel, id, use_leds, enable_callback, color, text)

# Preset: Toggle in Bank
def PRESET_TOGGLE_IN_BANK(primary,                        # Primary position in the bank [1..bank size]
                          secondary,                      # Secondary position in the bank [1..bank size]
                          label = FractalLabel.BOTH_P_NUM,# Label: BOTH_P_NUM, BOTH_NUM, DESTINATION_NAME, DESTINATION_NUM, CURRENT_NAME, CURRENT_NUM (see FractalLabel)
                          display = None,
                          midi_channel = 1,               # MIDI Channel in range [1..16]
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                   # Color override (default: preset category color)
                          text = None                     # Custom label text
    ):
    return _create(_TOGGLE_IN_BANK, primary, secondary, 1, False, None, None, False, label, display, midi_channel, id, use_leds, enable_callback, color, text)

# Preset: Increment / Decrement
def PRESET_INC_DEC(step = 1,                              # Step size: positive for next, negative for previous presets
                   wrap = True,                           # Wrap around at the ends
                   lower_limit = None,                    # Lowest preset (0-based) or None for no limit
                   upper_limit = None,                    # Highest preset (0-based) or None for no limit
                   label = FractalLabel.ACTION,           # Label: ACTION, DESTINATION_NAME, DESTINATION_NUM, CURRENT_NAME, CURRENT_NUM (see FractalLabel)
                   display = None,
                   midi_channel = 1,                      # MIDI Channel in range [1..16]
                   id = False,
                   use_leds = True,
                   enable_callback = None,
                   color = None,                          # Color override (default: preset category color)
                   text = None                            # Custom label text
    ):
    return _create(_INC_DEC, None, None, step, wrap, lower_limit, upper_limit, False, label, display, midi_channel, id, use_leds, enable_callback, color, text)


def _create(function, primary, secondary, step, wrap, lower_limit, upper_limit, second_press_previous, label, display, midi_channel, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalPresetCallback(
            function = function,
            primary = primary,
            secondary = secondary,
            step = step,
            wrap = wrap,
            lower_limit = lower_limit,
            upper_limit = upper_limit,
            second_press_previous = second_press_previous,
            label = label,
            channel = midi_channel - 1,
            color = color,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


#####################################################################################################################


class _FractalPresetCallback(FractalCallback):
    def __init__(self, function, primary, secondary, step, wrap, lower_limit, upper_limit, second_press_previous, label, channel, color, text):
        self.__mapping = FractalMappings.PRESET()
        mappings = [self.__mapping]

        self.__mapping_name = None
        if label == FractalLabel.CURRENT_NAME:
            self.__mapping_name = FractalMappings.PRESET_NAME()
            mappings.append(self.__mapping_name)

        super().__init__(
            color = color if color else COLOR_PRESET,
            text = text,
            mappings = mappings
        )

        self.__function = function
        self.__primary = primary
        self.__secondary = secondary
        self.__step = step
        self.__wrap = wrap
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__second_press_previous = second_press_previous
        self.__label = label
        self.__mapping_select = FractalMappings.PRESET_SELECT(channel)

        self.__target_name = FractalPresetTargetNameMapping() if label in (FractalLabel.NAME, FractalLabel.DESTINATION_NAME) else None
        self.__target_name_valid = False

        self.__previous = None
        self.__pushed = False
        self.__last_selected_bank = None

    def update(self):
        super().update()

        # Bank selected by a bank function (no MIDI value change)
        if FRACTAL.selected_bank != self.__last_selected_bank:
            self.__last_selected_bank = FRACTAL.selected_bank
            self.update_displays()

        # Target name (only requested when not yet received)
        if self.__target_name_valid and self.__target_name.value == None:
            self.__target_name.send_request(self._appl.client, self)

    def request_terminated(self, mapping):
        if mapping == self.__target_name:
            self.__target_name.discard()

        super().request_terminated(mapping)

    def push(self):
        current = self.__mapping.value

        if self.__function == _INC_DEC:
            self.__pushed = True
            self.update_displays()

        target = self.__target(current)
        if target == None:
            return

        if self.__second_press_previous and current == target and self.__previous != None:
            target = self.__previous

        if current != None and current != target:
            self.__previous = current

        self._appl.client.set(self.__mapping_select, target)
        self.__mapping.feedback(target)
        FRACTAL.selected_bank = None

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        current = self.__mapping.value
        FRACTAL.track_preset(current)

        function = self.__function
        target = self.__target(current)

        # Target name
        if self.__target_name:
            self.__target_name_valid = (target != None)
            if target != None:
                self.__target_name.set_target(target)

        # LED state
        if current == None:
            led = self.OFF
        elif function == _SELECT or function == _SELECT_IN_BANK:
            led = self.BRIGHT if current == self.__resolve(self.__primary, current) else self.DIM
        elif function == _INC_DEC:
            led = self.BRIGHT if self.__pushed else self.DIM
        else:
            if current == self.__resolve(self.__primary, current):
                led = self.BRIGHT
            elif current == self.__resolve(self.__secondary, current):
                led = self.DIM
            else:
                led = self.OFF

        self._show(led, self._color, self.__get_text(current, target))

    # Returns the preset to load when pressed (or None)
    def __target(self, current):
        function = self.__function

        if function == _SELECT or function == _SELECT_IN_BANK:
            return self.__resolve(self.__primary, current)

        if function == _INC_DEC:
            if current == None:
                return None

            return _inc_dec(
                current,
                self.__step,
                self.__wrap,
                self.__lower_limit if self.__lower_limit != None else 0,
                self.__upper_limit if self.__upper_limit != None else FRACTAL.num_presets - 1
            )

        # Toggle
        primary = self.__resolve(self.__primary, current)
        return self.__resolve(self.__secondary, current) if current == primary else primary

    # Returns the preset number for a parameter (positions for the "in bank" functions)
    def __resolve(self, value, current):
        if self.__function != _SELECT_IN_BANK and self.__function != _TOGGLE_IN_BANK:
            return value

        bank = FRACTAL.current_bank(current)
        if bank == None:
            return None

        preset = bank * FRACTAL.bank_size + value - 1
        return preset if preset < FRACTAL.num_presets else None

    # Label text
    def __get_text(self, current, target):
        label = self.__label

        if label == FractalLabel.NAME or label == FractalLabel.DESTINATION_NAME:
            if target == None or self.__target_name.value == None:
                return ""
            return self.__target_name.value

        if label == FractalLabel.CURRENT_NAME:
            return self.__mapping_name.value if self.__mapping_name.value != None else ""

        if label == FractalLabel.NUMBER or label == FractalLabel.DESTINATION_NUM:
            return FRACTAL.preset_text(target) if target != None else ""

        if label == FractalLabel.CURRENT_NUM:
            return FRACTAL.preset_text(current) if current != None else ""

        if label == FractalLabel.P_NUM:
            return f"P{ target % FRACTAL.bank_size + 1 }" if target != None else ""

        if label == FractalLabel.ACTION:
            return _action_text("Preset", self.__step)

        # Toggle labels
        primary = self.__resolve(self.__primary, current)
        secondary = self.__resolve(self.__secondary, current)
        if primary == None or secondary == None:
            return ""

        if label == FractalLabel.BOTH_P_NUM:
            return _both(
                f"P{ primary % FRACTAL.bank_size + 1 }",
                f"P{ secondary % FRACTAL.bank_size + 1 }",
                current == primary,
                current == secondary
            )

        return _both(
            "P" + FRACTAL.preset_text(primary),
            "P" + FRACTAL.preset_text(secondary),
            current == primary,
            current == secondary
        )
