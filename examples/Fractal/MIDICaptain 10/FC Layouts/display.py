from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement, DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.clients.fractal import TunerDisplayCallback
from pyswitch.clients.fractal.callbacks.preset_name import FractalPresetNameCallback
from pyswitch.clients.fractal.callbacks.scene_name import FractalSceneNameCallback

_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H15.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    "maxTextWidth": 58
}


_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)
_SLOT_WIDTH = const(60)
_SLOT_HEIGHT = const(40)
_FOOTER_Y = const(200)
_PRESET_NAME_Y = const(40)
_PRESET_NAME_HEIGHT = const(90)
_SCENE_NAME_Y = const(130)
_SCENE_NAME_HEIGHT = const(40)
_PAGE_Y = const(170)
_PAGE_HEIGHT = const(30)


# Switches 1-4
DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH * 2, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_4 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH * 3, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)

# Switches A-D
DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH * 2, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_4 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH * 3, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)

# Current page (pager on switch Up)
DISPLAY_PAGE = DisplayLabel(
    layout = {
        "font": "/fonts/H20.pcf",
        "backColor": DEFAULT_LABEL_COLOR
    },
    bounds = DisplayBounds(0, _PAGE_Y, _DISPLAY_WIDTH, _PAGE_HEIGHT)
)


Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_3,
            DISPLAY_HEADER_4,

            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_3,
            DISPLAY_FOOTER_4,

            DISPLAY_PAGE,

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
