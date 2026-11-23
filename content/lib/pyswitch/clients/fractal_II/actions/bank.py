from micropython import const

from ....controller.actions import Action
from .. import FractalIICallback, FractalIIMappings, FractalIILabel, FractalIIPresetLoad, FRACTAL_II, COLOR_BANK, _inc_dec, _both, _action_text

# Bank functions like the FC "Bank" category. Banks are 1-based. Bank size: option "fractalIIBankSize" in config.py.
# With preset_load = NONE, only the bank is selected: the PRESET_..._IN_BANK switches show it until a preset is loaded.

_SELECT = const(0)
_TOGGLE = const(1)
_INC_DEC = const(2)


# Bank: Select
def BANK_SELECT(bank,                                     # Bank [1..number of banks]
                preset_load = FractalIIPresetLoad.NONE,     # Preset to load: NONE, FIRST or CURRENT (same position) (see FractalIIPresetLoad)
                second_press_previous = False,            # If enabled, pressing the switch again selects the previous bank
                label = FractalIILabel.NUMBER,              # Label: NUMBER, CURRENT_NUM (see FractalIILabel)
                display = None,
                id = False,
                use_leds = True,
                enable_callback = None,
                color = None,                             # Color override (default: bank category color)
                text = None                               # Custom label text
    ):
    return _create(_SELECT, bank, None, 1, False, None, None, preset_load, second_press_previous, label, display, id, use_leds, enable_callback, color, text)

# Bank: Toggle
def BANK_TOGGLE(primary,                                  # Primary bank [1..number of banks]
                secondary,                                # Secondary bank [1..number of banks]
                preset_load = FractalIIPresetLoad.NONE,     # Preset to load: NONE, FIRST or CURRENT (same position) (see FractalIIPresetLoad)
                label = FractalIILabel.BOTH_NUM,            # Label: BOTH_NUM, NUMBER, CURRENT_NUM (see FractalIILabel)
                display = None,
                id = False,
                use_leds = True,
                enable_callback = None,
                color = None,                             # Color override (default: bank category color)
                text = None                               # Custom label text
    ):
    return _create(_TOGGLE, primary, secondary, 1, False, None, None, preset_load, False, label, display, id, use_leds, enable_callback, color, text)

# Bank: Increment / Decrement
def BANK_INC_DEC(step = 1,                                # Step size: positive for next, negative for previous banks
                 wrap = True,                             # Wrap around at the ends
                 lower_limit = None,                      # Lowest bank (1-based) or None for no limit
                 upper_limit = None,                      # Highest bank (1-based) or None for no limit
                 preset_load = FractalIIPresetLoad.NONE,    # Preset to load: NONE, FIRST or CURRENT (same position) (see FractalIIPresetLoad)
                 label = FractalIILabel.ACTION,             # Label: ACTION, NUMBER, CURRENT_NUM (see FractalIILabel)
                 display = None,
                 id = False,
                 use_leds = True,
                 enable_callback = None,
                 color = None,                            # Color override (default: bank category color)
                 text = None                              # Custom label text
    ):
    return _create(_INC_DEC, None, None, step, wrap, lower_limit, upper_limit, preset_load, False, label, display, id, use_leds, enable_callback, color, text)


def _create(function, primary, secondary, step, wrap, lower_limit, upper_limit, preset_load, second_press_previous, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalIIBankCallback(
            function = function,
            primary = primary,
            secondary = secondary,
            step = step,
            wrap = wrap,
            lower_limit = lower_limit,
            upper_limit = upper_limit,
            preset_load = preset_load,
            second_press_previous = second_press_previous,
            label = label,
            color = color,
            text = text
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


#####################################################################################################################


class _FractalIIBankCallback(FractalIICallback):
    def __init__(self, function, primary, secondary, step, wrap, lower_limit, upper_limit, preset_load, second_press_previous, label, color, text):
        self.__mapping = FractalIIMappings.PRESET()

        super().__init__(
            color = color if color else COLOR_BANK,
            text = text,
            mappings = [self.__mapping]
        )

        # Internally, banks are 0-based
        self.__function = function
        self.__primary = primary - 1 if primary != None else None
        self.__secondary = secondary - 1 if secondary != None else None
        self.__step = step
        self.__wrap = wrap
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__preset_load = preset_load
        self.__second_press_previous = second_press_previous
        self.__label = label

        self.__previous = None
        self.__pushed = False
        self.__last_selected_bank = None

    def update(self):
        super().update()

        # Bank selected by a bank function (no MIDI value change)
        if FRACTAL_II.selected_bank != self.__last_selected_bank:
            self.__last_selected_bank = FRACTAL_II.selected_bank
            self.update_displays()

    def push(self):
        preset = self.__mapping.value
        current = FRACTAL_II.current_bank(preset)

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

        # Select the bank, optionally load a preset
        load = self.__preset_load
        if load == FractalIIPresetLoad.NONE or preset == None:
            FRACTAL_II.selected_bank = target if preset == None or target != int(preset / FRACTAL_II.bank_size) else None
        else:
            new_preset = target * FRACTAL_II.bank_size
            if load == FractalIIPresetLoad.CURRENT:
                new_preset += preset % FRACTAL_II.bank_size

            new_preset = min(new_preset, FRACTAL_II.num_presets - 1)

            self._appl.client.set(self.__mapping, new_preset)
            self.__mapping.feedback(new_preset)
            FRACTAL_II.selected_bank = None

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        preset = self.__mapping.value
        FRACTAL_II.track_preset(preset)

        current = FRACTAL_II.current_bank(preset)
        function = self.__function

        # LED state
        if current == None:
            led = self.OFF
        elif function == _SELECT:
            led = self.BRIGHT if current == self.__primary else self.DIM
        elif function == _INC_DEC:
            led = self.BRIGHT if self.__pushed else self.DIM
        elif current == self.__primary:
            led = self.BRIGHT
        elif current == self.__secondary:
            led = self.DIM
        else:
            led = self.OFF

        self._show(led, self._color, self.__get_text(current))

    # Returns the bank to select when pressed (0-based) or None
    def __target(self, current):
        function = self.__function

        if function == _SELECT:
            return self.__primary

        if function == _TOGGLE:
            return self.__secondary if current == self.__primary else self.__primary

        if current == None:
            return None

        return _inc_dec(
            current,
            self.__step,
            self.__wrap,
            self.__lower_limit - 1 if self.__lower_limit != None else 0,
            self.__upper_limit - 1 if self.__upper_limit != None else FRACTAL_II.num_banks - 1
        )

    # Label text
    def __get_text(self, current):
        label = self.__label

        if label == FractalIILabel.ACTION:
            return _action_text("Bank", self.__step)

        if label == FractalIILabel.CURRENT_NUM:
            return f"Bank { current + 1 }" if current != None else ""

        if label == FractalIILabel.BOTH_NUM:
            return _both(
                f"B{ self.__primary + 1 }",
                f"B{ self.__secondary + 1 }",
                current == self.__primary,
                current == self.__secondary
            )

        # Number of the destination bank
        target = self.__target(current)
        return f"Bank { target + 1 }" if target != None else ""
