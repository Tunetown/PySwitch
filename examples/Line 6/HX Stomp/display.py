from pyswitch.clients.local.callbacks.splashes import SplashesCallback
from micropython import const
from pyswitch.colors import Colors
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement
from pyswitch.ui.ui import DisplayBounds
from pyswitch.ui.elements import DisplayLabel
from pyswitch.controller.callbacks.parameter_display import ParameterDisplayCallback
from pyswitch.controller.client import ClientParameterMapping
from adafruit_midi.program_change import ProgramChange

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
    80
)
_SLOT_HEIGHT = const(
    40
)
_FOOTER_Y = const(
    200
)

_VERSION_Y = const(
    40
)
_VERSION_HEIGHT = const(
    160
)

DISPLAY_HEADER_1 = DisplayLabel(
    layout = {
        "font": "/fonts/H20.pcf",
        "backColor": DEFAULT_LABEL_COLOR,
        "stroke": 1,
        "text": "",

    },
    bounds = DisplayBounds(
        x = 0,
        y = 0,
        w = 80,
        h = 40
    )
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(
        x = 80,
        y = 0,
        w = 80,
        h = 40
    )
)
DISPLAY_HEADER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(
        x = 160,
        y = 0,
        w = 80,
        h = 40
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
DISPLAY_FOOTER_3 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(
        x = 160,
        y = 200,
        w = 80,
        h = 40
    )
)


DISPLAY_PAGE = DisplayLabel(
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.DARK_GRAY,

    },
    bounds = DisplayBounds(
        x = 0,
        y = 135,
        w = 240,
        h = 20
    )
)

DISPLAY_LABEL_1 = DisplayLabel(
    bounds = DisplayBounds(
        x = 170,
        y = 45,
        w = 70,
        h = 20
    ),
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "textColor": Colors.LIGHT_BLUE,
        "text": 'Presets',

    }
)

def MAPPING_RX_PROGRAM_CHANGE():
    return ClientParameterMapping.get(
        name = "ProgChg",
        response = ProgramChange(
            0    # Dummy value, will be overridden
        )
    )

_PresetNumberDisplayCallback = ParameterDisplayCallback(mapping = MAPPING_RX_PROGRAM_CHANGE())

DISPLAY_LABEL_2 = DisplayLabel(
    bounds = DisplayBounds(
        x = 60,
        y = 60,
        w = 130,
        h = 75
    ),
    layout = {
        "font": "/fonts/PT60.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "text": "",

    },
    callback = _PresetNumberDisplayCallback
)

DISPLAY_LABEL_3 = DisplayLabel(
    bounds = DisplayBounds(
        x = 165,
        y = 175,
        w = 70,
        h = 20
    ),
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "text": "Tuner",
        "textColor": Colors.LIGHT_RED,

    }
)

DISPLAY_LABEL_4 = DisplayLabel(
    bounds = DisplayBounds(
        x = 5,
        y = 175,
        w = 70,
        h = 20
    ),
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "text": 'Sets',
        "textColor": Colors.TURQUOISE,

    }
)

DISPLAY_LABEL_5 = DisplayLabel(
    bounds = DisplayBounds(
        x = 5,
        y = 45,
        w = 70,
        h = 20
    ),
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "text": 'Effects',
        "textColor": Colors.RED,

    }
)

DISPLAY_LABEL_6 = DisplayLabel(
    bounds = DisplayBounds(
        x = 85,
        y = 175,
        w = 70,
        h = 20
    ),
    layout = {
        "font": "/fonts/H15.pcf",
        "backColor": Colors.BLACK,
        "stroke": 1,
        "text": 'Snapshots',
        "textColor": Colors.WHITE,

    }
)

Splashes = SplashesCallback(
    splashes = DisplayElement(
        bounds = DisplayBounds(
            x = 0,
            y = 0,
            w = _DISPLAY_WIDTH,
            h = _DISPLAY_HEIGHT
        ),
        children = [
            DISPLAY_FOOTER_1,
            DISPLAY_LABEL_5,
            DISPLAY_FOOTER_2,
            DISPLAY_FOOTER_3,
            DISPLAY_HEADER_1,
            DISPLAY_HEADER_2,
            DISPLAY_HEADER_3,
            DISPLAY_PAGE,
            DISPLAY_LABEL_4,
            DISPLAY_LABEL_6,
            DISPLAY_LABEL_3,
            DISPLAY_LABEL_2,
            DISPLAY_LABEL_1,

        ]
    )
)
