from ....controller.callbacks import Callback
from .. import FractalAM4Mappings

# Callback for DisplayLabel to show the current scene name and/or number ("2 Lead")
class FractalAM4SceneNameCallback(Callback):
    def __init__(self,
                 show_name = True,       # Show the scene name (the number if the scene has no name)
                 show_number = False,    # Show the scene number (1-4)
                 default_text = ""       # Text shown when no scene information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalAM4Mappings.NAME_TABLE()
        self.register_mapping(self.__mapping)

        self.__show_name = show_name
        self.__show_number = show_number
        self.__default_text = default_text

    def update_label(self, label):
        table = self.__mapping.value

        if table == None:
            label.text = self.__default_text
            return

        scene = table[0]
        number = f"Scene { scene + 1 }"
        name = table[2][scene] if scene < len(table[2]) else ""

        if not self.__show_name or not name:
            label.text = number
        elif self.__show_number:
            label.text = f"{ scene + 1 } { name }"
        else:
            label.text = name
