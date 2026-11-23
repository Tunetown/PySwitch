from micropython import const

from ....controller.actions import Action
from .. import FractalAM4Callback, FractalAM4Mappings, FractalAM4Label, FractalAM4PresetLoad, FRACTAL_AM4
from .. import NUM_PRESETS, NUM_BANKS, PRESETS_PER_BANK, COLOR_PRESET, COLOR_BANK, location_text, _inc_dec, _action_text

# Preset and bank functions like the preset mode of the AM4. Locations are 0-based (A01 = 0, A02 = 1, ..., Z04 = 103).

_SELECT = const(0)
_IN_BANK = const(1)
_INC_DEC = const(2)
_BANK = const(3)


# Preset: Select a fixed location
def PRESET_SELECT(location,                               # Location [0..103] (A01 = 0, A02 = 1, ..., Z04 = 103)
                  label = FractalAM4Label.NAME,           # Label: NAME, NUMBER (see FractalAM4Label)
                  display = None,
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: preset color)
                  text = None                             # Custom label text
    ):
    if location < 0 or location >= NUM_PRESETS:
        raise Exception(f"Invalid location: { location }")

    return _create(_SELECT, location, 1, False, None, label, display, id, use_leds, enable_callback, color, text)

# Preset: Select a preset of the current bank (like the switches of the preset mode)
def PRESET_SELECT_IN_BANK(position,                       # Position in the bank [1..4]
                          label = FractalAM4Label.NAME,   # Label: NAME, NUMBER (see FractalAM4Label)
                          display = None,
                          id = False,
                          use_leds = True,
                          enable_callback = None,
                          color = None,                   # Color override (default: preset color)
                          text = None                     # Custom label text
    ):
    if position < 1 or position > PRESETS_PER_BANK:
        raise Exception(f"Invalid position: { position }")

    return _create(_IN_BANK, position - 1, 1, False, None, label, display, id, use_leds, enable_callback, color, text)

# Preset: Increment / Decrement
def PRESET_INC_DEC(step = 1,                              # Step size: positive for next, negative for previous presets
                   wrap = True,                           # Wrap around from Z04 to A01 and vice versa
                   label = FractalAM4Label.ACTION,        # Label: ACTION, DESTINATION_NAME, NUMBER (see FractalAM4Label)
                   display = None,
                   id = False,
                   use_leds = True,
                   enable_callback = None,
                   color = None,                          # Color override (default: preset color)
                   text = None                            # Custom label text
    ):
    return _create(_INC_DEC, None, step, wrap, None, label, display, id, use_leds, enable_callback, color, text)

# Bank: Increment / Decrement (like holding switch 1 / 4 in the preset mode). Loads a preset of the target bank.
def BANK_INC_DEC(step = 1,                                # Step size: positive for next, negative for previous banks
                 preset_load = FractalAM4PresetLoad.FIRST, # Preset to load: FIRST, SAME (position) (see FractalAM4PresetLoad)
                 wrap = True,                             # Wrap around from bank Z to A and vice versa
                 label = FractalAM4Label.ACTION,          # Label: ACTION, NUMBER (see FractalAM4Label)
                 display = None,
                 id = False,
                 use_leds = True,
                 enable_callback = None,
                 color = None,                            # Color override (default: bank color)
                 text = None                              # Custom label text
    ):
    return _create(_BANK, None, step, wrap, preset_load, label, display, id, use_leds, enable_callback, color, text)


def _create(function, location, step, wrap, preset_load, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalAM4PresetCallback(
            function = function,
            location = location,
            step = step,
            wrap = wrap,
            preset_load = preset_load,
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


class _FractalAM4PresetCallback(FractalAM4Callback):
    def __init__(self, function, location, step, wrap, preset_load, label, color, text):
        self.__mapping = FractalAM4Mappings.PRESET()
        mappings = [self.__mapping]

        # The name of the current preset is in the name table
        self.__mapping_table = None
        if label in (FractalAM4Label.NAME, FractalAM4Label.DESTINATION_NAME):
            self.__mapping_table = FractalAM4Mappings.NAME_TABLE()
            mappings.append(self.__mapping_table)

        super().__init__(
            color = color if color else (COLOR_BANK if function == _BANK else COLOR_PRESET),
            text = text,
            mappings = mappings
        )

        self.__mapping_select = FractalAM4Mappings.PRESET_SELECT()
        self.__function = function
        self.__location = location      # Location (select) or position in the bank (0-based)
        self.__step = step
        self.__wrap = wrap
        self.__preset_load = preset_load
        self.__label = label

        self.__pushed = False
        self.__name_mapping = None

    def update(self):
        super().update()

        # Name of another preset (requested when not yet received, and again after preset changes)
        if self.__name_mapping and FRACTAL_AM4.needs_name(self.__name_mapping):
            FRACTAL_AM4.request_name(self._appl.client, self.__name_mapping, self)

    def push(self):
        if self.__function in (_INC_DEC, _BANK):
            self.__pushed = True

        target = self.__target(self.__mapping.value)
        if target != None:
            self._appl.client.set(self.__mapping_select, target)
            self.__mapping.feedback(target)

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        current = self.__mapping.value
        FRACTAL_AM4.track_preset(current)

        if current == None:
            led = self.OFF
        elif self.__function in (_INC_DEC, _BANK):
            led = self.BRIGHT if self.__pushed else self.DIM
        else:
            led = self.BRIGHT if current == self.__target(current) else self.DIM

        self._show(led, self._color, self.__get_text(current))

    # Returns the location to load when pressed, or None
    def __target(self, current):
        function = self.__function

        if function == _SELECT:
            return self.__location

        if current == None:
            return None

        if function == _IN_BANK:
            return (current // PRESETS_PER_BANK) * PRESETS_PER_BANK + self.__location

        if function == _INC_DEC:
            return _inc_dec(current, self.__step, self.__wrap, 0, NUM_PRESETS - 1)

        bank = _inc_dec(current // PRESETS_PER_BANK, self.__step, self.__wrap, 0, NUM_BANKS - 1)
        if self.__preset_load == FractalAM4PresetLoad.SAME:
            return bank * PRESETS_PER_BANK + current % PRESETS_PER_BANK

        return bank * PRESETS_PER_BANK

    # Label text
    def __get_text(self, current):
        label = self.__label
        function = self.__function

        if label == FractalAM4Label.ACTION:
            return _action_text("Bank" if function == _BANK else "Preset", self.__step)

        target = self.__target(current)
        if target == None:
            self.__name_mapping = None
            return ""

        if label == FractalAM4Label.NUMBER:
            if function == _BANK:
                return "Bank " + location_text(target)[0]
            return location_text(target)

        # Names: the current preset's name is in the name table, other names are read separately. As long as the 
        # name is not known, the location is shown.
        if target == current:
            self.__name_mapping = None
            table = self.__mapping_table.value
            return table[1] if table else location_text(target)

        self.__name_mapping = FractalAM4Mappings.PRESET_NAME(target)
        name = self.__name_mapping.value
        return name if name != None else location_text(target)
