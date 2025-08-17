##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

from micropython import const
from lib.pyswitch.colors import DEFAULT_LABEL_COLOR
from lib.pyswitch.misc import PYSWITCH_VERSION

from lib.pyswitch.ui.ui import DisplayElement, DisplayBounds
from lib.pyswitch.ui.elements import DisplayLabel, BidirectionalProtocolState

from lib.pyswitch.clients.kemper import KemperRigNameCallback, TunerDisplayCallback

#############################################################################################################################################

# Layout used for the action labels (only used here locally)
_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1
}

#############################################################################################################################################

# Some only locally used constants
_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)
_SLOT_WIDTH = const(120)                 # Slot width on the display
_SLOT_HEIGHT = const(40)                 # Slot height on the display
_FOOTER_Y = const(200)
_RIG_NAME_HEIGHT = const(160)

#############################################################################################################################################

# Header
DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)

# Footer
DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)


Splashes = TunerDisplayCallback(
    #strobe = True,
        process_overridden_actions = True,     # <=  Insert this line

    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            # Header area
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,

            # Footer area 
            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,
        
            # Rig name
            DisplayLabel(
                bounds = DisplayBounds(
                    0, 
                    _SLOT_HEIGHT,
                    _DISPLAY_WIDTH,
                    _RIG_NAME_HEIGHT
                ),

                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": f"PySwitch { PYSWITCH_VERSION }",
                },

                callback = KemperRigNameCallback()
            ),

            # Bidirectional protocol state indicator (dot)
            BidirectionalProtocolState(DisplayBounds(
                0, 
                _SLOT_HEIGHT,
                _DISPLAY_WIDTH,
                _RIG_NAME_HEIGHT
            ))
        ]
    )
)
