from pyswitch.clients.local.callbacks.splashes import SplashesCallback
from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.clients.fractal_am4.callbacks.preset_name import FractalAM4PresetNameCallback
from pyswitch.clients.fractal_am4.callbacks.scene_name import FractalAM4SceneNameCallback

_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H15.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    "maxTextWidth": 58,
    
}

_DISPLAY_WIDTH = const(
    240
)
_DISPLAY_HEIGHT = const(
    240
)
_SLOT_WIDTH = const(
    60
)
_SLOT_HEIGHT = const(
    40
)
_FOOTER_Y = const(
    200
)
_PRESET_NAME_Y = const(
    40
)
_PRESET_NAME_HEIGHT = const(
    80
)
_SCENE_NAME_Y = const(
    120
)
_SCENE_NAME_HEIGHT = const(
    40
)

_PAGE_Y = const(
    160
)

DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 0, 
        y = 0, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH, 
        y = 0, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_HEADER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 2, 
        y = 0, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_HEADER_4 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 3, 
        y = 0, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 0, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_FOOTER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 2, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_FOOTER_4 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 3, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)
DISPLAY_PAGE = DisplayLabel(
    layout = {
        "font": "/fonts/H20.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        
    }, 
    bounds = DisplayBounds(
        x = 0, 
        y = _PAGE_Y, 
        w = _DISPLAY_WIDTH, 
        h = 40
    )
)

Splashes = SplashesCallback(
    splashes = DisplayElement(
        bounds = DisplayBounds(
            x = 0, 
            y = 0, 
            w = _DISPLAY_WIDTH, 
            h = _DISPLAY_HEIGHT
        ), 
        children = [
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_3,
            DISPLAY_HEADER_4,
            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_3,
            DISPLAY_FOOTER_4,
            DisplayLabel(
                bounds = DisplayBounds(
                    x = 0, 
                    y = _PRESET_NAME_Y, 
                    w = _DISPLAY_WIDTH, 
                    h = _PRESET_NAME_HEIGHT
                ), 
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": "AM4",
                    
                }, 
                callback = FractalAM4PresetNameCallback(
                    show_name = True, 
                    show_number = True
                )
            ),
            DisplayLabel(
                bounds = DisplayBounds(
                    x = 0, 
                    y = _SCENE_NAME_Y, 
                    w = _DISPLAY_WIDTH, 
                    h = _SCENE_NAME_HEIGHT
                ), 
                layout = {
                    "font": "/fonts/H20.pcf",
                    
                }, 
                callback = FractalAM4SceneNameCallback(
                    show_name = True, 
                    show_number = True
                )
            ),
            DISPLAY_PAGE,
            
        ]
    )
)
