from micropython import const
from lib.pyswitch.ui.ui import DisplayElement, DisplayBounds
from lib.pyswitch.ui.elements import DisplayLabel, BidirectionalProtocolState
from lib.pyswitch.clients.kemper import KemperRigNameCallback, TunerDisplayCallback
from lib.pyswitch.misc import PYSWITCH_VERSION

_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(240)

Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),
        children = [
            DisplayLabel(
                bounds = DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT),

                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf",
                    "lineSpacing": 0.8,
                    "maxTextWidth": 220,
                    "text": f"PySwitch { PYSWITCH_VERSION }",
                },

                callback = KemperRigNameCallback()
            ),

            BidirectionalProtocolState(DisplayBounds(0, 0, _DISPLAY_WIDTH, _DISPLAY_HEIGHT))
        ]
    )
)
