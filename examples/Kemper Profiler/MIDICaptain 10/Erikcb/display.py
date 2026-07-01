##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

from pyswitch.clients.kemper import KemperRigNameCallback
from pyswitch.clients.kemper import TunerDisplayCallback
from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel

#############################################################################################################################################

# Layout used for the action labels (only used here locally)
_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    
}

#############################################################################################################################################

# Some only locally used constants
_DISPLAY_WIDTH = const(
    240
)
_DISPLAY_HEIGHT = const(
    240
)
_SLOT_WIDTH = const(
    120
)                 # Slot width on the display
_SLOT_HEIGHT = const(
    40
)                 # Slot height on the display
_FOOTER_Y = const(
    200
)
_RIG_NAME_HEIGHT = const(
    160
)

#############################################################################################################################################

# Header

DISPLAY_HEADER_1 = DisplayLabel(
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }, 
    bounds = DisplayBounds(
        x = 0, 
        y = 0, 
        w = 130, 
        h = 30
    )
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }, 
    bounds = DisplayBounds(
        x = 130, 
        y = 0, 
        w = 110, 
        h = 30
    )
)

DISPLAY_HEADER_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 30, 
        w = 130, 
        h = 30
    ), 
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)

DISPLAY_HEADER_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 130, 
        y = 30, 
        w = 110, 
        h = 30
    ), 
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)

# Footer

DISPLAY_FOOTER_1 = DisplayLabel(
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }, 
    bounds = DisplayBounds(
        x = 0, 
        y = 180, 
        w = 130, 
        h = 30
    )
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }, 
    bounds = DisplayBounds(
        x = 130, 
        y = 180, 
        w = 110, 
        h = 30
    )
)

DISPLAY_FOOTER_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 210, 
        w = 130, 
        h = 30
    ), 
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)

DISPLAY_FOOTER_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 130, 
        y = 210, 
        w = 110, 
        h = 30
    ), 
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)








Splashes = TunerDisplayCallback(
    process_overridden_actions = True, 
    splash_default = DisplayElement(
        bounds = DisplayBounds(
            x = 0, 
            y = 0, 
            w = _DISPLAY_WIDTH, 
            h = _DISPLAY_HEIGHT
        ), 
        children = [
            DisplayLabel(
                bounds = DisplayBounds(
                    x = 0, 
                    y = 60, 
                    w = 240, 
                    h = 120
                ), 
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": KemperRigNameCallback.DEFAULT_TEXT,
                    
                }, 
                callback = KemperRigNameCallback(), 
                scale = 1
            ),
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_4,
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_3,
            DISPLAY_FOOTER_4,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_3,
            
        ]
    )
)