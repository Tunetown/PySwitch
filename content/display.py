from pyswitch.clients.kemper import KemperRigNameCallback
from pyswitch.clients.kemper import TunerDisplayCallback
from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR, Colors
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel

_LABEL_FONT = "/fonts/H20.pcf"
_PAGE_FONT = "/fonts/R25.pcf"
_RIG_FONT = "/fonts/PTSans-NarrowBold-40.pcf"

_LAYOUT_1 = {
    "font": _LABEL_FONT,
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1,
    "lineSpacing": 0.9
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
_RIG_ID_HEIGHT = const(
    40
)
_RIG_NAME_HEIGHT = const(
    160
)
_RIG_ID_Y = const(40)
_RIG_NAME_Y = const (50)


HEADER_1 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = 0,
        y = 0,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
# HEADER_1A = DisplayLabel(
#     layout = {
#         "font": _LABEL_FONT,
#         "text": "t N c\nB W C",
#     },
#     bounds = DisplayBounds(
#         x = 0,
#         y = _SLOT_HEIGHT,
#         w = _SLOT_WIDTH,
#         h = _SLOT_HEIGHT
#     )
# )
HEADER_2 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH,
        y = 0,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
HEADER_3 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 2,
        y = 0,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
HEADER_4 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 3,
        y = 0,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
# HEADER_4A = DisplayLabel(
#     layout = {
#         "font": _LABEL_FONT,
#         "text": "ac DT\n ",
#     },
#     bounds = DisplayBounds(
#         x = _SLOT_WIDTH * 3,
#         y = _SLOT_HEIGHT,
#         w = _SLOT_WIDTH,
#         h = _SLOT_HEIGHT
#     )
# )


FOOTER_1 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = 0,
        y = _FOOTER_Y,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
FOOTER_2 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH,
        y = _FOOTER_Y,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
FOOTER_3 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 2,
        y = _FOOTER_Y,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)
FOOTER_4 = DisplayLabel(
    layout = _LAYOUT_1,
    bounds = DisplayBounds(
        x = _SLOT_WIDTH * 3,
        y = _FOOTER_Y,
        w = _SLOT_WIDTH,
        h = _SLOT_HEIGHT
    )
)

DISP_PAGE = DisplayLabel(
    layout = {
        "font": _PAGE_FONT,
        "backColor": (0, 0, 0),

    },
    bounds = DisplayBounds(
        x = 0,
        y = _FOOTER_Y - 20,
        w = _DISPLAY_WIDTH,
        h = 20
    ),
)

RIG_NAME = DisplayLabel(
    bounds = DisplayBounds(
        x = 0,
        y = _RIG_NAME_Y+10,
        w = _DISPLAY_WIDTH,
        h = _RIG_NAME_HEIGHT
    ),
    layout = {
        "font": _RIG_FONT,
        "lineSpacing": 0.7,
        "maxTextWidth": _DISPLAY_WIDTH,
        "text": KemperRigNameCallback.DEFAULT_TEXT,

    },
    callback = KemperRigNameCallback(
        show_name = True,
        show_rig_id = False
    )
)


Splashes = TunerDisplayCallback(
    strobe = False,
    color_in_tune = Colors.GREEN,
    color_out_of_tune = Colors.RED,
    splash_default = DisplayElement(
        bounds = DisplayBounds(
            x = 0,
            y = 0,
            w = _DISPLAY_WIDTH,
            h = _DISPLAY_HEIGHT
        ),
        children = [
            HEADER_1,
            #HEADER_1A,
            HEADER_2,
            HEADER_3,
            HEADER_4,
            #HEADER_4A,
            FOOTER_1,
            FOOTER_2,
            FOOTER_3,
            FOOTER_4,
            DisplayLabel(
                bounds = DisplayBounds(
                    x = 0,
                    y = _RIG_ID_Y+10,
                    w = _DISPLAY_WIDTH,
                    h = _RIG_ID_HEIGHT
                ),
                layout = {
                    "font": _RIG_FONT,
                },
                scale = 2,
                callback = KemperRigNameCallback(
                    show_name = False,
                    show_rig_id = True
                )
            ),
            RIG_NAME,
            DISP_PAGE,
        ]
    )
)
