from lib.pyswitch.clients.kemper import KemperRigNameCallback
from lib.pyswitch.clients.kemper import TunerDisplayCallback
from micropython import const
from lib.pyswitch.colors import DEFAULT_LABEL_COLOR
from lib.pyswitch.ui.ui import DisplayElement
from lib.pyswitch.ui.ui import DisplayBounds
from lib.pyswitch.ui.elements import DisplayLabel

_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    
}

_DISPLAY_WIDTH = const(
    240
)
_DISPLAY_HEIGHT = const(
    240
)
_SLOT_WIDTH = const(
    120
)
_SLOT_HEIGHT = const(
    40
)
_FOOTER_Y = const(
    200
)
_RIG_ID_HEIGHT = const(
    40
)
_RIG_NAME_HEIGHT = const(
    160
)
_RIG_ID_Y = const(
    160
)


_LABEL_LAYOUT = {
    "font": "/fonts/PTSans-NarrowBold-40.pcf",
    "text": "",
    "backColor": (0, 0, 0),
    
}


_LABEL_LAYOUT = {
    "font": "/fonts/PTSans-NarrowBold-40.pcf",
    "text": "",
    "backColor": (0, 0, 0),
    
}


DISPLAY_HEADER_1 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 0, 
        w = 48, 
        h = 40
    ), 
    layout = _LABEL_LAYOUT
)
DISPLAY_HEADER_2 = DisplayLabel(
    bounds = DisplayBounds(
        x = 48, 
        y = 0, 
        w = 48, 
        h = 40
    ), 
    layout = _LABEL_LAYOUT
)
DISPLAY_HEADER_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 96, 
        y = 0, 
        w = 48, 
        h = 40
    ), 
    layout = _LABEL_LAYOUT
)
DISPLAY_HEADER_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 144, 
        y = 0, 
        w = 48, 
        h = 40
    ), 
    layout = _LABEL_LAYOUT
)
DISPLAY_HEADER_5 = DisplayLabel(
    bounds = DisplayBounds(
        x = 192, 
        y = 0, 
        w = 48, 
        h = 40
    ), 
    layout = _LABEL_LAYOUT
)


DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 0, 
        y = 200, 
        w = 48, 
        h = 40
    )
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 48, 
        y = 200, 
        w = 48, 
        h = 40
    )
)
DISPLAY_FOOTER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 96, 
        y = 200, 
        w = 48, 
        h = 40
    )
)

DISPLAY_FOOTER_4 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 144, 
        y = 200, 
        w = 48, 
        h = 40
    )
)

DISPLAY_FOOTER_5 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 192, 
        y = 200, 
        w = 48, 
        h = 40
    )
)

DISPLAY_RIG_NAME = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = _SLOT_HEIGHT, 
        w = _DISPLAY_WIDTH, 
        h = _RIG_NAME_HEIGHT
    ), 
    layout = {
        "font": "/fonts/PTSans-NarrowBold-40.pcf",
        "lineSpacing": 0.8,
        "maxTextWidth": 220,
        "text": KemperRigNameCallback.DEFAULT_TEXT,
        
    }, 
    callback = KemperRigNameCallback(
        show_name = True, 
        show_rig_id = False
    )
)

Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        bounds = DisplayBounds(
            x = 0, 
            y = 0, 
            w = _DISPLAY_WIDTH, 
            h = _DISPLAY_HEIGHT
        ), 
        children = [
            DISPLAY_FOOTER_1,
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_3,
            DISPLAY_HEADER_4,
            DISPLAY_HEADER_5,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_3,
            DISPLAY_FOOTER_4,
            DISPLAY_FOOTER_5,
            DISPLAY_RIG_NAME,
            
        ]
    )
)
