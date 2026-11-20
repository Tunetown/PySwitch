from micropython import const

from ....controller.actions import Action
from .. import FractalCallback, FractalMappings, FractalLabel, FRACTAL, NUM_SCENES, COLOR_SCENE, _inc_dec, _both, _action_text

# Scene functions like the FC "Scene" category. Scenes are 1-based.

_SELECT = const(0)
_TOGGLE = const(1)
_INC_DEC = const(2)


# Scene: Select
def SCENE_SELECT(scene,                                   # Scene [1..8]
                 second_press_previous = False,           # If enabled, pressing the switch again selects the previous scene
                 label = FractalLabel.NAME,               # Label: NAME, NUMBER (see FractalLabel)
                 display = None,
                 id = False,
                 use_leds = True,
                 enable_callback = None,
                 color = None,                            # Color override (default: scene category color)
                 text = None                              # Custom label text
    ):
    return _create(_SELECT, scene, None, 1, False, None, None, second_press_previous, label, display, id, use_leds, enable_callback, color, text)

# Scene: Toggle
def SCENE_TOGGLE(primary,                                 # Primary scene [1..8]
                 secondary,                               # Secondary scene [1..8]
                 label = FractalLabel.BOTH_NUM,           # Label: BOTH_NUM, DESTINATION_NAME, DESTINATION_NUM, CURRENT_NAME, CURRENT_NUM (see FractalLabel)
                 display = None,
                 id = False,
                 use_leds = True,
                 enable_callback = None,
                 color = None,                            # Color override (default: scene category color)
                 text = None                              # Custom label text
    ):
    return _create(_TOGGLE, primary, secondary, 1, False, None, None, False, label, display, id, use_leds, enable_callback, color, text)

# Scene: Increment / Decrement
def SCENE_INC_DEC(step = 1,                               # Step size: positive for next, negative for previous scenes
                  wrap = True,                            # Wrap around from scene 8 to 1 and vice versa
                  lower_limit = None,                     # Lowest scene [1..8] or None for no limit
                  upper_limit = None,                     # Highest scene [1..8] or None for no limit
                  label = FractalLabel.ACTION,            # Label: ACTION, DESTINATION_NAME, DESTINATION_NUM, CURRENT_NAME, CURRENT_NUM (see FractalLabel)
                  display = None,
                  id = False,
                  use_leds = True,
                  enable_callback = None,
                  color = None,                           # Color override (default: scene category color)
                  text = None                             # Custom label text
    ):
    return _create(_INC_DEC, None, None, step, wrap, lower_limit, upper_limit, False, label, display, id, use_leds, enable_callback, color, text)


def _create(function, primary, secondary, step, wrap, lower_limit, upper_limit, second_press_previous, label, display, id, use_leds, enable_callback, color, text):
    return Action({
        "callback": _FractalSceneCallback(
            function = function,
            primary = primary,
            secondary = secondary,
            step = step,
            wrap = wrap,
            lower_limit = lower_limit,
            upper_limit = upper_limit,
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


class _FractalSceneCallback(FractalCallback):
    def __init__(self, function, primary, secondary, step, wrap, lower_limit, upper_limit, second_press_previous, label, color, text):
        if (primary != None and (primary < 1 or primary > NUM_SCENES)) or (secondary != None and (secondary < 1 or secondary > NUM_SCENES)):
            raise Exception("Invalid scene")

        self.__mapping = FractalMappings.SCENE()
        mappings = [self.__mapping]

        # Scene names are invalidated on preset changes, so the preset is needed
        self.__uses_names = label in (FractalLabel.NAME, FractalLabel.DESTINATION_NAME, FractalLabel.CURRENT_NAME)
        if self.__uses_names:
            self.__mapping_preset = FractalMappings.PRESET()
            mappings.append(self.__mapping_preset)

        super().__init__(
            color = color if color else COLOR_SCENE,
            text = text,
            mappings = mappings
        )

        # Internally, scenes are 0-based
        self.__function = function
        self.__primary = primary - 1 if primary != None else None
        self.__secondary = secondary - 1 if secondary != None else None
        self.__step = step
        self.__wrap = wrap
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__second_press_previous = second_press_previous
        self.__label = label

        self.__previous = None
        self.__pushed = False
        self.__name_mapping = None

    def update(self):
        super().update()

        # Scene name (only requested when not yet received)
        if self.__name_mapping and self.__name_mapping.value == None:
            self._appl.client.request(self.__name_mapping, self)

    def push(self):
        current = self.__mapping.value

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

        self._appl.client.set(self.__mapping, target)
        self.__mapping.feedback(target)

        self.update_displays()

    def release(self):
        if self.__pushed:
            self.__pushed = False
            self.update_displays()

    def update_displays(self):
        current = self.__mapping.value
        function = self.__function

        if self.__uses_names:
            FRACTAL.track_preset(self.__mapping_preset.value)

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

    # Returns the scene to select when pressed (0-based) or None
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
            self.__upper_limit - 1 if self.__upper_limit != None else NUM_SCENES - 1
        )

    # Label text
    def __get_text(self, current):
        label = self.__label

        if label == FractalLabel.ACTION:
            return _action_text("Scene", self.__step)

        if label == FractalLabel.BOTH_NUM:
            return "Scene " + _both(
                self.__primary + 1,
                self.__secondary + 1,
                current == self.__primary,
                current == self.__secondary
            )

        scene = current if (label == FractalLabel.CURRENT_NAME or label == FractalLabel.CURRENT_NUM) else self.__target(current)
        if scene == None:
            self.__name_mapping = None
            return ""

        if label == FractalLabel.NUMBER or label == FractalLabel.DESTINATION_NUM or label == FractalLabel.CURRENT_NUM:
            return f"Scene { scene + 1 }"

        # Names
        self.__name_mapping = FractalMappings.SCENE_NAME(scene)
        return self.__name_mapping.value if self.__name_mapping.value != None else ""
