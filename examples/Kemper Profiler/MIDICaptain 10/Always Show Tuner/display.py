from pyswitch.clients.kemper import KemperRigNameCallback
from pyswitch.clients.kemper import TunerDisplayCallback
from pyswitch.clients.kemper import KemperMappings
from micropython import const
from pyswitch.colors import Colors
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.ui.elements import BidirectionalProtocolState
from pyswitch.ui.elements import TunerDisplay

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
_RIG_NAME_HEIGHT = const(
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


DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = 0, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)

DISPLAY_TUNER = TunerDisplay(
    mapping_deviance = KemperMappings.TUNER_DEVIANCE(), 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    ), 
    color_in_tune = Colors.LIGHT_GREEN, 
    color_out_of_tune = Colors.ORANGE, 
    color_neutral = Colors.WHITE, 
    calibration_high = 8192 + 350, 
    calibration_low = 8192 - 350
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
        show_rig_id = True
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
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
            DISPLAY_FOOTER_1,
            DISPLAY_TUNER,
            DISPLAY_RIG_NAME,
            BidirectionalProtocolState(
                DisplayBounds(
                    x = 0, 
                    y = _SLOT_HEIGHT, 
                    w = _DISPLAY_WIDTH, 
                    h = _RIG_NAME_HEIGHT
                )
            ),
            
        ]
    )
)
