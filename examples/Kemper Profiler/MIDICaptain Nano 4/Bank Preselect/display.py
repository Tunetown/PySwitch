from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement, DisplayBounds
from pyswitch.ui.elements import DisplayLabel, BidirectionalProtocolState
from pyswitch.clients.kemper import KemperRigNameCallback, TunerDisplayCallback
from pyswitch.misc import PYSWITCH_VERSION

_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1
}


_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)
_SLOT_WIDTH = const(120)
_SLOT_HEIGHT = const(40)
_FOOTER_Y = const(200)
_RIG_ID_HEIGHT = const(40)
_RIG_NAME_HEIGHT = const(160)
_RIG_ID_Y = const(160)



DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, 0, _SLOT_WIDTH, _SLOT_HEIGHT)
)


DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(_SLOT_WIDTH, _FOOTER_Y, _SLOT_WIDTH, _SLOT_HEIGHT)
)


Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,

            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,

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

                callback = KemperRigNameCallback(
                    show_name = True,
                    show_rig_id = False
                )
            ),

            DisplayLabel(
                bounds = DisplayBounds(
                    0,
                    _RIG_ID_Y,
                    _DISPLAY_WIDTH,
                    _RIG_ID_HEIGHT
                ),

                layout = {
                    "font": "/fonts/H20.pcf"
                },

                callback = KemperRigNameCallback(
                    show_name = False,
                    show_rig_id = True
                )
            ),

            BidirectionalProtocolState(DisplayBounds(
                0, 
                _SLOT_HEIGHT,
                _DISPLAY_WIDTH,
                _RIG_NAME_HEIGHT
            ))
        ]
    )
)
