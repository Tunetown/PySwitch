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
_SLOT_WIDTH = const(80)
_SLOT_HEIGHT = const(40)
_FOOTER_Y = const(200)
_RIG_ID_HEIGHT = const(40)
_RIG_NAME_HEIGHT = const(160)
_RIG_ID_Y = const(40)
_RIG_NAME_Y = const (50)


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


DISPLAY_PAGE = DisplayLabel(
    layout = {
        "font": "/fonts/A12.pcf",
        "backColor": (0, 0, 0)
    },
    bounds = DisplayBounds(0, _FOOTER_Y - 20, _DISPLAY_WIDTH, 20)
)


Splashes = TunerDisplayCallback(
    strobe = True,
    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
	        DISPLAY_HEADER_3,

            DISPLAY_FOOTER_1,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_3,

            DisplayLabel(
                bounds = DisplayBounds(
                    0,
                    _RIG_ID_Y,
                    _DISPLAY_WIDTH,
                    _RIG_ID_HEIGHT
                ),

                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf"
                },

                callback = KemperRigNameCallback(
                    show_name = False,
                    show_rig_id = True
                )
            ),

            DisplayLabel(
                bounds = DisplayBounds(
                    0, 
                    _RIG_NAME_Y,
                    _DISPLAY_WIDTH,
                    _RIG_NAME_HEIGHT
                ),

                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.7,
                    "maxTextWidth": 230,
                    "text": f"PySwitch { PYSWITCH_VERSION }",
                },

                callback = KemperRigNameCallback(
                    show_name = True,
                    show_rig_id = False
		)
            ),

            DISPLAY_PAGE,

            BidirectionalProtocolState(DisplayBounds(
                0, 
                _SLOT_HEIGHT,
                _DISPLAY_WIDTH,
                _RIG_NAME_HEIGHT
            ))
        ]
    )
)