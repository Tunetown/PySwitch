from lib.pyswitch.clients.kemper import KemperRigNameCallback
from lib.pyswitch.clients.kemper import TunerDisplayCallback
from micropython import const
from lib.pyswitch.colors import DEFAULT_LABEL_COLOR
from lib.pyswitch.ui.ui import DisplayElement
from lib.pyswitch.ui.ui import DisplayBounds
from lib.pyswitch.ui.elements import DisplayLabel
from lib.pyswitch.ui.elements import BidirectionalProtocolState
from lib.pyswitch.misc import PYSWITCH_VERSION
from lib.pyswitch.controller.callbacks.parameter_display import ParameterDisplayCallback
from lib.pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_NAME


class _MyDisplayCallback(ParameterDisplayCallback):
    def __init__(self):
        super().__init__(
            mapping = MAPPING_AMP_NAME()
      )


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
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT, 
    bounds = DisplayBounds(
        x = _SLOT_WIDTH, 
        y = _FOOTER_Y, 
        w = _SLOT_WIDTH, 
        h = _SLOT_HEIGHT
    )
)

DISPLAY_RIG_NAME = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 40, 
        w = 240, 
        h = 160
    ), 
    layout = {
        "font": "/fonts/PTSans-NarrowBold-40.pcf",
        "lineSpacing": 0.8,
        "maxTextWidth": 220,
        "text": f"PySwitch { PYSWITCH_VERSION }",
        
    }, 
    callback = KemperRigNameCallback()
)

DISPLAY_LABEL_1 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 160, 
        w = 240, 
        h = 40
    ), 
    layout = {
        "font": "/fonts/H20.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }, 
    callback = _MyDisplayCallback()
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
            DISPLAY_FOOTER_2,
            BidirectionalProtocolState(
                DisplayBounds(
                    x = 232, 
                    y = 40, 
                    w = 8, 
                    h = 8
                )
            ),
            DISPLAY_RIG_NAME,
            DISPLAY_LABEL_1,
            
        ]
    )
)
