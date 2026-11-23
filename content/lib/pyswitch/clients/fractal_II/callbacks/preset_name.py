from ....controller.callbacks import Callback
from .. import FractalIIMappings, FRACTAL_II

# Callback for DisplayLabel to show the current preset name and/or number (like the FC main display).
class FractalIIPresetNameCallback(Callback):
    def __init__(self,
                 show_name = True,       # Show the preset name
                 show_number = False,    # Show the preset number (3 digits, regarding the fractalIIPresetDisplayOffset option)
                 default_text = ""       # Text shown when no preset information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalIIMappings.PRESET()
        self.register_mapping(self.__mapping)

        # The name is not polled: it is only requested after preset changes (see update())
        self.__mapping_name = FractalIIMappings.PRESET_NAME() if show_name else None

        self.__show_number = show_number
        self.__default_text = default_text

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

        FRACTAL_II.init(appl.config)

    def update(self):
        super().update()

        if self.__mapping_name:
            self.__mapping_name.refresh(self.__appl.client, self, self.__mapping.value)

    def update_label(self, label):
        preset = self.__mapping.value
        FRACTAL_II.track_preset(preset)

        name = self.__mapping_name.value if self.__mapping_name else None

        if preset == None or (self.__mapping_name and name == None):
            label.text = self.__default_text
            return

        if not self.__show_number:
            label.text = name
        elif not self.__mapping_name:
            label.text = FRACTAL_II.preset_text(preset)
        else:
            label.text = f"{ FRACTAL_II.preset_text(preset) } { name }"
