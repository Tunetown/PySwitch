# display.py — plain DisplayLabel layout (works with Option A category overrides)

from pyswitch.clients.kemper import KemperRigNameCallback
from pyswitch.clients.kemper import TunerDisplayCallback
from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.ui.elements import BidirectionalProtocolState

# ───────────────────────────── UI constants / layout ─────────────────────────
_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    
}

_DISPLAY_WIDTH  = const(
    240
)
_DISPLAY_HEIGHT = const(
    240
)

# ───────────────────────────── Header labels (A–D) ───────────────────────────
DISPLAY_HEADER_1 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 0, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_HEADER_2 = DisplayLabel(
    bounds = DisplayBounds(
        x = 60, 
        y = 0, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_HEADER_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 120, 
        y = 0, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_HEADER_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 180, 
        y = 0, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)

# ───────────────────────────── Footer labels (X,MOD,DLY,REV) ─────────────────
DISPLAY_FOOTER_1 = DisplayLabel(
    bounds = DisplayBounds(
        x = 0, 
        y = 180, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_FOOTER_2 = DisplayLabel(
    bounds = DisplayBounds(
        x = 60, 
        y = 180, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_FOOTER_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 120, 
        y = 180, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)
DISPLAY_FOOTER_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 180, 
        y = 180, 
        w = 60, 
        h = 60
    ), 
    layout = {
        "font": "/fonts/R25.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        
    }
)

# ───────────────────────────── Center rig name (full) ────────────────────────
# Leave rig name unmodified so you can see it in full.
DISPLAY_RIG_NAME = DisplayLabel(
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
    callback = KemperRigNameCallback(
        show_rig_id = True
    )
)

# ───────────────────────────── Splash composition ────────────────────────────
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
            DISPLAY_HEADER_3,
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_4,
            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_3,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_4,
            DISPLAY_RIG_NAME,
            BidirectionalProtocolState(
                DisplayBounds(
                    x = 232, 
                    y = 60, 
                    w = 8, 
                    h = 8
                )
            ),
            
        ]
    )
)
