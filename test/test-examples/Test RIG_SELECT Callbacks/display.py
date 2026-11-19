##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

from micropython import const
from pyswitch.misc import DEFAULT_LABEL_COLOR #, Colors

from pyswitch.ui.elements import DisplaySplitContainer, DisplayBounds
from pyswitch.ui.elements import DisplayLabel, BIDIRECTIONAL_PROTOCOL_STATE_DOT, PERFORMANCE_DOT
from pyswitch.ui.ui import HierarchicalDisplayElement

from pyswitch.clients.kemper import KemperRigNameCallback, TunerDisplayCallback

#############################################################################################################################################

# Layout used for the action labels (only used here locally)
_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1
}

DISPLAY_HEADER_1 = DisplayLabel(layout = _ACTION_LABEL_LAYOUT)
DISPLAY_HEADER_2 = DisplayLabel(layout = _ACTION_LABEL_LAYOUT)
DISPLAY_FOOTER_1 = DisplayLabel(layout = _ACTION_LABEL_LAYOUT)
DISPLAY_FOOTER_2 = DisplayLabel(layout = _ACTION_LABEL_LAYOUT)

#############################################################################################################################################

# Some only locally used constants
_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)
_SLOT_HEIGHT = const(40)                 # Slot height on the display

#############################################################################################################################################

# The DisplayBounds class is used to easily layout the default display in a subtractive way. Initialize it with all available space:
_display_bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT)

# Default display
_bounds_default = _display_bounds.clone()

Splashes = TunerDisplayCallback(
    splash_default = HierarchicalDisplayElement(
        bounds = _bounds_default,
        children = [
            # Header area (referenced by ID in the action configurations)
            DisplaySplitContainer(
                bounds = _bounds_default.remove_from_top(_SLOT_HEIGHT),
                children = [
                    DISPLAY_HEADER_1,
                    DISPLAY_HEADER_2
                ]
            ),

            # Footer area (referenced by ID in the action configurations)
            DisplaySplitContainer(
                bounds = _bounds_default.remove_from_bottom(_SLOT_HEIGHT),
                children = [
                    DISPLAY_FOOTER_1,
                    DISPLAY_FOOTER_2
                ]
            ),

            # Rig name
            DisplayLabel(
                bounds = _bounds_default,   # Takes what is left over

                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": KemperRigNameCallback.DEFAULT_TEXT,
                },

                callback = KemperRigNameCallback()
            ),

            # Bidirectional protocol state indicator (dot)
            BIDIRECTIONAL_PROTOCOL_STATE_DOT(_bounds_default),

            # Performance indicator (dot)
            PERFORMANCE_DOT(_bounds_default.translated(0, 7)),
        ]
    )
)
