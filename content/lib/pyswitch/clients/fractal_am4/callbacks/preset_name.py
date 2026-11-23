from ....controller.callbacks import Callback
from .. import FractalAM4Mappings, location_text

# Callback for DisplayLabel to show the current preset location and/or name (like the AM4 display: "A01 Clean")
class FractalAM4PresetNameCallback(Callback):
    def __init__(self,
                 show_name = True,       # Show the preset name
                 show_number = False,    # Show the location (A01..Z04)
                 default_text = ""       # Text shown when no preset information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalAM4Mappings.PRESET()
        self.register_mapping(self.__mapping)

        self.__mapping_table = None
        if show_name:
            self.__mapping_table = FractalAM4Mappings.NAME_TABLE()
            self.register_mapping(self.__mapping_table)

        self.__show_name = show_name
        self.__show_number = show_number
        self.__default_text = default_text

    def update_label(self, label):
        preset = self.__mapping.value

        if preset == None:
            label.text = self.__default_text
            return

        number = location_text(preset)
        if not self.__show_name:
            label.text = number
            return

        table = self.__mapping_table.value
        if self.__show_number:
            label.text = f"{ number } { table[1] }".strip() if table else number
        else:
            label.text = table[1] if table else self.__default_text
