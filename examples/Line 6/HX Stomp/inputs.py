from pyswitch.clients.local.actions.custom import CUSTOM_MESSAGE
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_PAGE

from pyswitch.controller.callbacks import Callback
from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *


# Custom callback function
class _EnableSetSelectorCallback(Callback):
    def __init__(self, pager):
        Callback.__init__(self)
        self.__pager = pager

    # For Action enable/disable callbacks, there must be a enabled(action) method.
    def enabled(self, action):
        return self.__pager.current_page_id == 100

_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.RED,
            "text": 'E F F E C T S',

        },
        {
            "id": 2,
            "color": Colors.WHITE,
            "text": 'S N A P S H O T S',

        },
        {
            "id": 3,
            "color": Colors.DARK_GREEN,
            "text": 'G U I T A R  1',

        },
        {
            "id": 4,
            "color": Colors.GREEN,
            "text": 'G U I T A R  2',

        },
        {
            "id": 5,
            "color": Colors.BLUE,
            "text": 'B A S S',

        },
        {
            "id": 6,
            "color": Colors.LIGHT_BLUE,
            "text": 'P R E S E T S',

        },
        {
            "id": 100,
            "color": Colors.TURQUOISE,
            "text": 'S E T S',

        },

    ],
    display = DISPLAY_PAGE,
    select_page = 1,
    led_brightness = 0.05
)


_enable_set_select_callback = _EnableSetSelectorCallback(
    _pager
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_1,
                text = '',
                id = 100,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_1,
                text = '',
                id = 6,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 0],
                display = DISPLAY_HEADER_1,
                text = 'JC-120',
                id = 3,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 6],
                color = Colors.ORANGE,
                display = DISPLAY_HEADER_1,
                text = 'G6',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_1,
                text = '',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 18],
                color = Colors.DARK_BLUE,
                display = DISPLAY_HEADER_1,
                text = 'B0',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_1,
                text = '',
                id = 2,
                enable_callback = _pager.enable_callback
            ),
        ],
        "actionsHold": [
            _pager,

        ],
        "holdTimeMillis": 600,

    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            CUSTOM_MESSAGE(
                message = [176, 52, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_HEADER_2,
                text = 'FS4',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_2,
                text = '',
                id = 100,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 1],
                color = Colors.PURPLE,
                display = DISPLAY_HEADER_2,
                text = 'AC/DC',
                id = 3,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 7],
                color = Colors.ORANGE,
                display = DISPLAY_HEADER_2,
                text = 'G7',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 19],
                color = Colors.DARK_BLUE,
                display = DISPLAY_HEADER_2,
                text = 'B1',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_2,
                text = '',
                id = 6,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_2,
                text = '',
                id = 2,
                enable_callback = _pager.enable_callback
            ),

        ],
        "actionsHold": [],
        "holdRepeat": True,
        "holdTimeMillis": 600,

    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            CUSTOM_MESSAGE(
                message = [176, 53, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_HEADER_3,
                text = 'FS5',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_3,
                text = '',
                id = 100,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 8],
                color = Colors.ORANGE,
                display = DISPLAY_HEADER_3,
                text = 'G8',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 2],
                color = Colors.TURQUOISE,
                display = DISPLAY_HEADER_3,
                text = 'Bluesy',
                id = 3,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 20],
                color = Colors.DARK_BLUE,
                display = DISPLAY_HEADER_3,
                text = 'B2',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_3,
                text = '',
                id = 6,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_HEADER_3,
                text = '',
                id = 2,
                enable_callback = _pager.enable_callback
            ),

        ],
        "actionsHold": [
            _pager.proxy(
                page_id = 6
            ),

        ],
        "holdRepeat": True,
        "holdTimeMillis": 600,

    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            CUSTOM_MESSAGE(
                message = [176, 72, 0],
                color = Colors.LIGHT_BLUE,
                display = DISPLAY_FOOTER_1,
                text = 'Down',
                id = 6,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 49, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_FOOTER_1,
                text = 'FS1',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 69, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_FOOTER_1,
                text = '1',
                id = 2,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 3],
                color = Colors.LIGHT_GREEN,
                display = DISPLAY_FOOTER_1,
                text = 'Eriza',
                id = 3,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 9],
                color = Colors.ORANGE,
                display = DISPLAY_FOOTER_1,
                text = 'G9',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 21],
                color = Colors.DARK_BLUE,
                display = DISPLAY_FOOTER_1,
                text = 'B5',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            _pager.proxy(
                page_id = 3,
                enable_callback = _enable_set_select_callback
            ),
            CUSTOM_MESSAGE(
                message = [],
                color = Colors.DARK_GRAY,
                display = DISPLAY_FOOTER_1,
                use_leds = False,
                text = 'G1',
                id = 100,
                enable_callback = _pager.enable_callback
            ),

        ],
        "actionsHold": [
            _pager.proxy(
                page_id = 100
            ),

        ],
        "holdRepeat": False,
        "holdTimeMillis": 600,

    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            CUSTOM_MESSAGE(
                message = [176, 50, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_FOOTER_2,
                text = 'FS2',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 69, 1],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_FOOTER_2,
                text = '2',
                id = 2,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 4],
                color = Colors.LIGHT_RED,
                display = DISPLAY_FOOTER_2,
                text = 'Diezel',
                id = 3,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 10],
                color = Colors.ORANGE,
                display = DISPLAY_FOOTER_2,
                text = 'G10',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 22],
                color = Colors.DARK_BLUE,
                display = DISPLAY_FOOTER_2,
                text = 'B6',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            _pager.proxy(
                page_id = 4,
                enable_callback = _enable_set_select_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 127, 0],
                color = Colors.DARK_GRAY,
                display = DISPLAY_FOOTER_2,
                use_leds = False,
                text = 'G2',
                id = 100,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 127, 0],
                color = Colors.DARK_GRAY,
                led_brightness = 0,
                display = DISPLAY_FOOTER_2,
                text = '',
                id = 6,
                enable_callback = _pager.enable_callback
            ),

        ],
        "actionsHold": [
            _pager.proxy(
                page_id = 2
            ),

        ],
        "holdRepeat": False,
        "holdTimeMillis": 600,

    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            CUSTOM_MESSAGE(
                message = [176, 51, 0],
                color = Colors.RED,
                display = DISPLAY_FOOTER_3,
                text = 'TAP',
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 69, 2],
                color = Colors.DARK_GRAY,
                led_brightness = 0.05,
                display = DISPLAY_FOOTER_3,
                text = '3',
                id = 2,
                enable_callback = _pager.enable_callback
            ),
            _pager.proxy(
                page_id = 5,
                enable_callback = _enable_set_select_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 127, 0],
                color = Colors.DARK_GRAY,
                display = DISPLAY_FOOTER_3,
                use_leds = False,
                text = 'Bass',
                id = 100,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [176, 72, 127],
                color = Colors.LIGHT_BLUE,
                display = DISPLAY_FOOTER_3,
                text = 'Up',
                id = 6,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 11],
                color = Colors.ORANGE,
                display = DISPLAY_FOOTER_3,
                text = 'G11',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 23],
                color = Colors.DARK_BLUE,
                display = DISPLAY_FOOTER_3,
                text = 'B7 63s',
                id = 5,
                enable_callback = _pager.enable_callback
            ),
            CUSTOM_MESSAGE(
                message = [192, 5],
                color = Colors.ORANGE,
                display = DISPLAY_FOOTER_3,
                text = 'Diezel 2',
                id = 3,
                enable_callback = _pager.enable_callback
            ),

        ],
        "actionsHold": [
            CUSTOM_MESSAGE(
                message = [176, 68, 127],
                color = Colors.RED,
                led_brightness = 0.05,
                text = ''
            ),

        ],

    },

]
