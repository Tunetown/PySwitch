from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement, DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.clients.fractal import FractalTunerDisplayCallback
from pyswitch.clients.fractal.callbacks.preset_name import FractalPresetNameCallback
from pyswitch.clients.fractal.callbacks.scene_name import FractalSceneNameCallback

_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    "maxTextWidth": 118
}


_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)
_SLOT_WIDTH = const(120)
_SLOT_HEIGHT = const(40)
_FOOTER_Y = const(200)
_PRESET_NAME_Y = const(40)
_PRESET_NAME_HEIGHT = const(120)
_SCENE_NAME_Y = const(160)
_SCENE_NAME_HEIGHT = const(40)


# Switches 1-2
DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)

# Switches A-B (B: current page)
DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)


Splashes = FractalTunerDisplayCallback(
    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,

            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,

            # Preset number and name
            DisplayLabel(
                bounds = DisplayBounds(0, _PRESET_NAME_Y, _DISPLAY_WIDTH, _PRESET_NAME_HEIGHT),
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": "Fractal"
                },
                callback = FractalPresetNameCallback(
                    show_name = True,
                    show_number = True
                )
            ),

            # Scene name
            DisplayLabel(
                bounds = DisplayBounds(0, _SCENE_NAME_Y, _DISPLAY_WIDTH, _SCENE_NAME_HEIGHT),
                layout = {
                    "font": "/fonts/H20.pcf"
                },
                callback = FractalSceneNameCallback(
                    show_name = True,
                    show_number = True
                )
            )
        ]
    )
)
