from micropython import const
from pyswitch.colors import DEFAULT_LABEL_COLOR
from pyswitch.ui.ui import DisplayElement, DisplayBounds
from pyswitch.ui.elements import DisplayLabel, BidirectionalProtocolState
from pyswitch.controller.callbacks import Callback
from pyswitch.clients.kemper import KemperRigNameCallback, TunerDisplayCallback
from pyswitch.clients.kemper.mappings.bank import MAPPING_NEXT_BANK
from pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_NAME
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
_RIG_NAME_HEIGHT = const(110)
_BANK_NAME_HEIGHT = const(50)


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


class _BankNameCallback(Callback):
    def __init__(self):
        Callback.__init__(self)
       
        # This defines that the following mappings have to be listened to.
        # In your case you need to listen to two mappings as you also need the amp name.        
        self._mapping_bank = MAPPING_NEXT_BANK()
        self._mapping_amp_name = MAPPING_AMP_NAME()

        self.register_mapping(self._mapping_bank)
        self.register_mapping(self._mapping_amp_name)

    # This will be called for updating the label whenever the mappings defined above
    # have changed.    
    def update_label(self, label):
        # This now also has to encounter the possibility that the bank mapping value is still None
        # (in case the amp name mapping gets a value first)
        current_bank = int(self._mapping_bank.value / 5) if self._mapping_bank.value != None else None
        amp_name = self._mapping_amp_name.value

        # Removed the if statement because get_custom_text always returns a value. Also
        # pass the amp name here (update_label gets called whenever one of the registered mappings has changed).
        # Beware that both values can be None now!
        label.text = self._get_custom_text(current_bank, amp_name)

    # Your bank name function. Both bank and amp_name can be None.
    def _get_custom_text(self, bank, amp_name):
        if bank == 0:
            return repr(bank + 1) + " - PAF"
        elif bank == 1:
            return repr(bank + 1) + " - P90"
        elif bank == 2:
            return repr(bank + 1) + " - EMG"
        elif bank == 3:
            return repr(bank + 1) + " - Wide-Range"
        elif bank == 4:
            return repr(bank + 1) + " - Bass"
        elif bank == 5:
            return repr(bank + 1) + " - Acoustic"
        else:
            # Standard behaviour for all other banks 
            # Here you now have also to check None state for both values or you config will crash:
            bank_display = repr(bank + 1) if bank else ""
            amp_name_display = repr(amp_name) if amp_name else ""
            
            return "Bank " + bank_display + " - " + amp_name_display
   


Splashes = TunerDisplayCallback(
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
                    _SLOT_HEIGHT + _RIG_NAME_HEIGHT,
                    _DISPLAY_WIDTH,
                    _BANK_NAME_HEIGHT
                ),
                layout = {
                    "font": "/fonts/H20.pcf",
                    "maxTextWidth": 230, 
                },
                callback = _BankNameCallback()
            ),

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

            BidirectionalProtocolState(DisplayBounds(
                0, 
                _SLOT_HEIGHT,
                _DISPLAY_WIDTH,
                _RIG_NAME_HEIGHT
            ))
        ]
    )
)
