from ....controller.callbacks import Callback
from .. import FractalMappings, FRACTAL

# Callback for DisplayLabel to show the current scene name and/or number (like the FC main display).
class FractalSceneNameCallback(Callback):
    def __init__(self,
                 show_name = True,       # Show the scene name
                 show_number = False,    # Show the scene number (1-8)
                 default_text = ""       # Text shown when no scene information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalMappings.SCENE()
        self.register_mapping(self.__mapping)

        # Scene names are invalidated on preset changes, so the preset is needed
        self.__mapping_preset = None
        if show_name:
            self.__mapping_preset = FractalMappings.PRESET()
            self.register_mapping(self.__mapping_preset)

        self.__show_name = show_name
        self.__show_number = show_number
        self.__default_text = default_text
        self.__name_mapping = None

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

        FRACTAL.init(appl.config)

    def update(self):
        super().update()

        # Scene name (only requested when not yet received)
        if self.__name_mapping and self.__name_mapping.value == None:
            self.__appl.client.request(self.__name_mapping, self)

    def update_label(self, label):
        scene = self.__mapping.value

        if self.__mapping_preset:
            FRACTAL.track_preset(self.__mapping_preset.value)

        if scene == None:
            self.__name_mapping = None
            label.text = self.__default_text
            return

        if not self.__show_name:
            label.text = f"Scene { scene + 1 }"
            return

        self.__name_mapping = FractalMappings.SCENE_NAME(scene)
        name = self.__name_mapping.value

        if name == None:
            label.text = self.__default_text
        elif self.__show_number:
            label.text = f"{ scene + 1 } { name }"
        else:
            label.text = name
