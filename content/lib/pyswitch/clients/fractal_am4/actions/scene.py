from micropython import const

from ....controller.actions import Action
from .. import FractalAM4Callback, FractalAM4Mappings, FractalAM4Label, NUM_SCENES, COLOR_SCENE, _inc_dec, _action_text

# Scene functions like the scene mode of the AM4. Scenes are 1-based.

_SELECT = const(0)
_INC_DEC = const(1)


# Scene: Select
def SCENE_SELECT(scene,                                   # Scene [1..4]
                 label = FractalAM4Label.NAME,            # Label: NAME, NUMBER (see FractalAM4Label)
                 display = None,
                 id = False,
                 use_leds = True,
                 enable_callback = None,
                 color = None,                            # Color override (default: scene color)
                 text = None                              # Custom label text
    ):
    if scene < 1 or scene > NUM_SCENES:
        raise Exception(f"Invalid scene: { scene }")

    return _create(_SELECT, scene - 1, 1, False, label, display, id, use_leds, enable_callback, color, text)

# Scene: Increment / Decrement
def SCENE_INC_DEC(step = 1,                               # Step size: positive for next, negative for previous scenes
                  wrap = True,                            # Wrap around from scene 4 to 1 and vice versa
                  label = FractalAM4Label.ACTION,         # Label: ACTION, DESTINATION_NAME, NUMBER (see FractalAM4Label)
                  display = None,
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: scene color)
                  text = None                             # Custom label text
    ):
    return _create(_INC_DEC, None, step, wrap, label, display, id, use_leds, enable_callback, color, text)


def _create(function, scene, step, wrap, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalAM4SceneCallback(
            function = function,
            scene = scene,
            step = step,
            wrap = wrap,
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


class _FractalAM4SceneCallback(FractalAM4Callback):
    def __init__(self, function, scene, step, wrap, label, color, text):
        # The active scene and the scene names are in the name table
        self.__mapping = FractalAM4Mappings.NAME_TABLE()

        super().__init__(
            color = color if color else COLOR_SCENE,
            text = text,
            mappings = [self.__mapping]
        )

        self.__mapping_select = FractalAM4Mappings.SCENE_SELECT()
        self.__function = function
        self.__scene = scene
        self.__step = step
        self.__wrap = wrap
        self.__label = label
        self.__pushed = False

    def push(self):
        if self.__function == _INC_DEC:
            self.__pushed = True

        table = self.__mapping.value
        target = self.__target(table)
        if target != None:
            self._appl.client.set(self.__mapping_select, target)

            if table:
                self.__mapping.feedback((target,) + table[1:])

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        table = self.__mapping.value

        if table == None:
            led = self.OFF
        elif self.__function == _INC_DEC:
            led = self.BRIGHT if self.__pushed else self.DIM
        else:
            led = self.BRIGHT if table[0] == self.__scene else self.DIM

        self._show(led, self._color, self.__get_text(table))

    # Returns the scene to select when pressed (0-based) or None
    def __target(self, table):
        if self.__function == _SELECT:
            return self.__scene

        if table == None:
            return None

        return _inc_dec(table[0], self.__step, self.__wrap, 0, NUM_SCENES - 1)

    # Label text
    def __get_text(self, table):
        label = self.__label

        if label == FractalAM4Label.ACTION:
            return _action_text("Scene", self.__step)

        scene = self.__target(table)
        if scene == None:
            return ""

        number = f"Scene { scene + 1 }"
        if label == FractalAM4Label.NUMBER or table == None:
            return number

        # Scene without name: number
        return table[2][scene] or number
