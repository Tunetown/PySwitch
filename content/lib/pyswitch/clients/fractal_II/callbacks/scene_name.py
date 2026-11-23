from ....controller.callbacks import Callback
from .. import FractalIIMappings, FRACTAL_II

# Callback for DisplayLabel to show the current scene ("Scene 3"; the Axe-Fx II has no scene names).
class FractalIISceneNameCallback(Callback):
    def __init__(self,
                 default_text = ""       # Text shown when no scene information is available
        ):
        Callback.__init__(self)

        self.__mapping = FractalIIMappings.SCENE()
        self.register_mapping(self.__mapping)

        self.__default_text = default_text

    def init(self, appl, listener = None):
        super().init(appl, listener)
        FRACTAL_II.init(appl.config)

    def update_label(self, label):
        scene = self.__mapping.value
        label.text = f"Scene { scene + 1 }" if scene != None else self.__default_text
