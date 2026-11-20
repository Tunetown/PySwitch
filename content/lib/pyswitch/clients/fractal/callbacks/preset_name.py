from ....controller.callbacks import Callback
from .. import FractalMappings, FRACTAL

# Callback for DisplayLabel to show the current preset name and/or number (like the FC main display).
class FractalPresetNameCallback(Callback):
    def __init__(self,
                 show_name = True,       # Show the preset name
                 show_number = False,    # Show the preset number (3 digits, regarding the fractalPresetDisplayOffset option)
                 default_text = ""       # Text shown when no preset information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalMappings.PRESET()
        self.register_mapping(self.__mapping)

        self.__mapping_name = None
        if show_name:
            self.__mapping_name = FractalMappings.PRESET_NAME()
            self.register_mapping(self.__mapping_name)

        self.__show_number = show_number
        self.__default_text = default_text

    def init(self, appl, listener = None):
        super().init(appl, listener)
        FRACTAL.init(appl.config)

    def update_label(self, label):
        preset = self.__mapping.value
        FRACTAL.track_preset(preset)

        name = self.__mapping_name.value if self.__mapping_name else None

        if preset == None or (self.__mapping_name and name == None):
            label.text = self.__default_text
            return

        if not self.__show_number:
            label.text = name
        elif not self.__mapping_name:
            label.text = FRACTAL.preset_text(preset)
        else:
            label.text = f"{ FRACTAL.preset_text(preset) } { name }"
