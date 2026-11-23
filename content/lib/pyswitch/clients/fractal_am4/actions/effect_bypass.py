from ....controller.actions import Action
from .. import FractalAM4Callback, FractalAM4Mappings, FractalAM4Label, FractalAM4Block, NUM_SLOTS, COLOR_EFFECT

# Effect bypass like the effects mode of the AM4: bypasses/engages the block in a slot (1..4) or a fixed block type.
# LEDs: bright = engaged, dim = bypassed, off = slot empty / block not in the preset.
def EFFECT_BYPASS(slot = 1,                               # Slot [1..4] (the block in this slot is switched)
                  block = None,                           # Alternatively: block type (see FractalAM4Block), if in the preset. If set, slot is ignored.
                  label = FractalAM4Label.LONG_NAME,      # Label: LONG_NAME, SHORT_NAME (see FractalAM4Label)
                  display = None,
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: effect color)
                  text = None                             # Custom label text
    ):
    if block != None:
        slot = None
    elif slot == None or slot < 1 or slot > NUM_SLOTS:
        raise Exception(f"Invalid slot: { slot }")

    return Action({
        "callback": _FractalAM4BypassCallback(
            slot = slot - 1 if slot != None else None,
            block = block,
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


class _FractalAM4BypassCallback(FractalAM4Callback):
    def __init__(self, slot, block, label, color, text):
        # The blocks of the slots are in the name table
        self.__mapping_table = FractalAM4Mappings.NAME_TABLE()

        super().__init__(
            color = color if color else COLOR_EFFECT,
            text = text,
            mappings = [self.__mapping_table]
        )

        self.__slot = slot
        self.__block = block
        self.__short = (label == FractalAM4Label.SHORT_NAME)
        self.__mapping = None

    def update(self):
        super().update()

        # Bypass state of the block (only while it is in the preset)
        if self.__mapping:
            self._appl.client.request(self.__mapping, self)

    def push(self):
        mapping = self.__mapping
        if not mapping or mapping.value == None:
            return

        value = 0 if mapping.value else 1

        self._appl.client.set(mapping, value)
        mapping.feedback(value)

        self.update_displays()

    def update_displays(self):
        block = self.__current_block()

        if block:
            self.__mapping = FractalAM4Mappings.BYPASS(block)
            bypassed = self.__mapping.value
            led = self.OFF if bypassed == None else (self.DIM if bypassed else self.BRIGHT)
        else:
            self.__mapping = None
            led = self.OFF

        name_block = block if block else self.__block
        name = FractalAM4Block.name(name_block, self.__short) if name_block else None

        self._show(led, self._color, name if name else "")

    # Returns the block to switch if it is in the preset, or None
    def __current_block(self):
        table = self.__mapping_table.value
        if not table:
            return None

        blocks = table[3]

        if self.__slot != None:
            return blocks[self.__slot] or None

        return self.__block if self.__block in blocks else None
