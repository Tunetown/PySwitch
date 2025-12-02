from micropython import const

from adafruit_midi.control_change import ControlChange
from adafruit_midi.system_exclusive import SystemExclusive
from adafruit_midi.program_change import ProgramChange

from ...misc import PeriodCounter, do_print, PYSWITCH_VERSION
from ...colors import Colors
from ...controller.callbacks import Callback
from ...controller.client import ClientParameterMapping, ClientTwoPartParameterMapping
from ...ui.elements import TunerDisplay


####################################################################################################################

# Definitions of devices
NRPN_PRODUCT_TYPE_PROFILER = const(0x00)                     # Kemper Profiler
NRPN_PRODUCT_TYPE_PROFILER_PLAYER = const(0x02)              # Kemper Profiler Player

# This defines which type of device to control
NRPN_PRODUCT_TYPE = NRPN_PRODUCT_TYPE_PROFILER_PLAYER

# Defines how many rigs one bank has
NUM_RIGS_PER_BANK = 5

# Defines how many banks there are
NUM_BANKS = 125

# Bank colors
BANK_COLORS = [
    Colors.BLUE,
    Colors.YELLOW,
    Colors.RED,
    Colors.LIGHT_GREEN,
    Colors.PURPLE
]

####################################################################################################################

# Basic values for all NRPN messages
NRPN_MANUFACTURER_ID = [0x00, 0x20, 0x33]       # Kemper manufacturer ID
NRPN_DEVICE_ID_OMNI = const(0x7f)               # Omni (all devices, only supported mode)
NRPN_INSTANCE = const(0x00)                     # Instance ID for NRPN. The profiler only supports instance 0.

# NRPN Address pages
NRPN_ADDRESS_PAGE_STRINGS = const(0x00)

# NRPN Function codes
NRPN_FUNCTION_REQUEST_SINGLE_PARAMETER = const(0x41)
NRPN_FUNCTION_REQUEST_STRING_PARAMETER = const(0x43)
NRPN_FUNCTION_REQUEST_EXT_STRING_PARAMETER = const(0x47)
NRPN_FUNCTION_RESPONSE_SINGLE_PARAMETER = const(0x01)
NRPN_FUNCTION_RESPONSE_STRING_PARAMETER = const(0x03)
NRPN_FUNCTION_SET_SINGLE_PARAMETER = const(0x01)

# Generally used NRPN values
NRPN_PARAMETER_OFF = const(0)
NRPN_PARAMETER_ON = const(1)

# Converts a value in [0..1] to the full NRPN range ([0..16383])
def NRPN_VALUE(value):
    return int(16383 * value)

####################################################################################################################


# Callback for DisplayLabel to show the rig name and/or ID.
class KemperRigNameCallback(Callback):
    DEFAULT_TEXT = f"PySwitch { PYSWITCH_VERSION }"   # Deprecated! Dont use this for new configurations! Use f"PySwitch { PYSWITCH_VERSION }" instead.

    def __init__(self, 
                 show_name = True,     # Show the rig name in the label
                 show_rig_id = False   # Show the rig ID (like 1-1) in the label. Can be False, 'rig', 'bank' or True (to show both rig and bank)
    ):
        Callback.__init__(self)

        # Rig name
        self.__show_name = show_name
        if show_name:
            self.__mapping_name = KemperMappings.RIG_NAME()
            self.register_mapping(self.__mapping_name)

        # Rig ID
        self.__show_rig_id = show_rig_id
        if show_rig_id:
            self.__mapping_id = KemperMappings.RIG_ID()
            self.register_mapping(self.__mapping_id)    

        self.__preselect_initialized = None    

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

    def update(self):
        super().update()

        if "preselectedBank" in self.__appl.shared:
            if self.__preselect_initialized != self.__appl.shared["preselectedBank"]:
                self.__preselect_initialized = self.__appl.shared["preselectedBank"]

                if self.__show_name:
                    self.parameter_changed(self.__mapping_name)
                elif self.__show_rig_id:
                    self.parameter_changed(self.__mapping_id)
        else:
            self.__preselect_initialized = None

    def update_label(self, label):
        if "preselectedBank" in self.__appl.shared:
            label.text = f"Bank { str(self.__appl.shared["preselectedBank"] + 1) }"
            return
        
        if self.__show_name:
            name = self.__mapping_name.value if self.__mapping_name.value else self.DEFAULT_TEXT

        if self.__show_rig_id and self.__mapping_id.value != None:
            bank = int(self.__mapping_id.value / NUM_RIGS_PER_BANK)
            rig = self.__mapping_id.value % NUM_RIGS_PER_BANK

            if self.__show_rig_id == 'rig':
                rig_id_str = f"{ repr(rig + 1) }"
            elif self.__show_rig_id == 'bank':
                rig_id_str = f"{ repr(bank + 1) }"
            else:
                rig_id_str = f"{ repr(bank + 1) }-{ repr(rig + 1) }"

            if self.__show_name:
                label.text = f"{ rig_id_str } { name }"
            else:
                label.text = f"{ rig_id_str }"
                
        elif self.__show_name:
            label.text = name


####################################################################################################################


# Splash Callback for on-demand Tuner display. Pass your default display root element as default splash,
# and a genuine tuner display will be used when the tuner is activated. You can also define your own tuner
# display optionally.
class TunerDisplayCallback(Callback):
    def __init__(self, 
                 splash_default,                           # Default DisplayElement (root of default display to be shown when not in tuner mode)
                 splash_tuner = None,                      # DisplayElement to be shown when tuner is engaged
                 color_in_tune = Colors.LIGHT_GREEN,
                 color_out_of_tune = Colors.ORANGE,
                 color_neutral = Colors.WHITE,
                 calibration_high = 8192 + 350,            # Threshold value above which the note is out of tune
                 calibration_low = 8192 - 350,             # Threshold value above which the note is out of tune
                 note_names = None,                        # If set, this must be a tuple or list of 12 note name strings starting at C.
                 
                 strobe = False,                           # If set, all available switch LEDs will act as a strobe tuner.
                 strobe_color = Colors.WHITE,              # LED color for strobe tuner
                 strobe_dim = 0.1,                         # Dim factor for strobe tuner in range [0..1]
                 strobe_speed = 1000,                      # Higher values make the strobe tuner go slower. 1000 is the recommended speed to 
                                                           # start from.
                 strobe_max_fps = 120,                     # Maximum cumulative frame rate for update of strobe tuner LEDs. Reduce this to save processing power.
                                                           # The number will be divided by the amount of available switches to get the real max. frame rate (that's
                                                           # why it is called cumulative ;)
                 strobe_reverse = True,                    # If False, the strobe is rotating clockwise when too high / ccw when too low. If True, the other way round.
                 process_overridden_actions = False        # If set, when in tuner mode, the underlying actions will also be processed after disabling the tuner. 
                                                           # Also the LEDs keep their initial state (if strobe is disabled of course)
        ):
        Callback.__init__(self)

        self.__mapping = KemperMappings.TUNER_MODE_STATE()
        self.register_mapping(self.__mapping)
        
        self.__splash_tuner = splash_tuner
        self.__splash_default = splash_default
        self.__process_overridden_actions = process_overridden_actions
        self.__pushed_before = False
        
        if not self.__splash_tuner:
            self.__splash_tuner = TunerDisplay(
                mapping_note = KemperMappings.TUNER_NOTE(),
                mapping_deviance = KemperMappings.TUNER_DEVIANCE(),                
                bounds = self.__splash_default.bounds,                
                scale = 3,
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf"
                },
                color_in_tune = color_in_tune,
                color_out_of_tune = color_out_of_tune,
                color_neutral = color_neutral,
                calibration_high = calibration_high,
                calibration_low = calibration_low,
                note_names = note_names
            )

        if strobe:
            from ...controller.strobe import StrobeController

            self.__strobe_controller = StrobeController(
                mapping_state = KemperMappings.TUNER_MODE_STATE(),
                mapping_deviance = KemperMappings.TUNER_DEVIANCE(),
                dim_factor = strobe_dim,
                speed = strobe_speed,
                color = strobe_color,
                max_fps = strobe_max_fps,
                reverse = strobe_reverse
            )
        else:
            self.__strobe_controller = None

    def init(self, appl, listener = None):
        Callback.init(self, appl, listener)
        self.__appl = appl

        if self.__strobe_controller:
            self.__strobe_controller.init(appl)

    def parameter_changed(self, mapping):
        super().parameter_changed(mapping)
        
        if mapping != self.__mapping:
            return
        
        if self.__mapping.value == 1:
            # Tuner on
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = self
                    
                    if not self.__process_overridden_actions:
                        input.color = Colors.WHITE
                        input.brightness = 0
        else:
            # Tuner off
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = None

                    for action in input.actions:
                        action.reset()

    def push(self):
        self.__pushed_before = True
        return self.__process_overridden_actions

    def release(self):
        if not self.__pushed_before:            
            # This prevents that the tuner button switches off the tuner immediately at releasing 
            return
        
        self.__pushed_before = False
        self.__appl.client.set(self.__mapping, 0)

        return self.__process_overridden_actions

    def get_root(self):
        if self.__mapping.value != 1:
            return self.__splash_default
        else:
            return self.__splash_tuner
        

####################################################################################################################


# Kemper specific SysEx message with defaults which are valid most of the time
class KemperNRPNMessage(SystemExclusive):

    def __init__(
            self, 
            function_code,
            address_page,
            address_number,
            manufacturer_id = NRPN_MANUFACTURER_ID, 
            product_type = NRPN_PRODUCT_TYPE,
            device_id = NRPN_DEVICE_ID_OMNI
        ):

        # Adafruit SystemExclusive
        super().__init__(
            manufacturer_id,                 # [0x00, 0x20, 0x33]
            [
                product_type,                # 0x02 (Player), 0x00 (Profiler)
                device_id,                   # 0x7f (omni) or manually set via parameter
                function_code,               # Selects the function, for example 0x41 for requesting a single parameter
                NRPN_INSTANCE,               # 0x00
                address_page,                # Controller MSB (address page)
                address_number               # Controller LSB (address number of parameter)
            ]
        )
        
# Kemper specific SysEx message for extended parameters 
class KemperNRPNExtendedMessage(SystemExclusive):
    
    def __init__(
            self, 
            function_code,
            controller,     # Must be a list
            manufacturer_id = NRPN_MANUFACTURER_ID, 
            product_type = NRPN_PRODUCT_TYPE,
            device_id = NRPN_DEVICE_ID_OMNI
        ):

        # Adafruit SystemExclusive
        super().__init__(
            manufacturer_id,                 # [0x00, 0x20, 0x33]
            [
                product_type,                # 0x02 (Player), 0x00 (Profiler)
                device_id,                   # 0x7f (omni) or manually set via parameter
                function_code,               # Selects the function, for example 0x41 for requesting a single parameter
                NRPN_INSTANCE                # 0x00                
            ] + controller
        )


####################################################################################################################


# Kemper Effect slot IDs, MIDI addresses and display properties
class KemperEffectSlot:
    
    # IDs for the available effect slots
    EFFECT_SLOT_ID_A = const(0)
    EFFECT_SLOT_ID_B = const(1)
    EFFECT_SLOT_ID_C = const(2)
    EFFECT_SLOT_ID_D = const(3)
    
    EFFECT_SLOT_ID_X = const(4)
    EFFECT_SLOT_ID_MOD = const(5)
    EFFECT_SLOT_ID_DLY = const(6)
    EFFECT_SLOT_ID_REV = const(7)

    EFFECT_SLOT_ID_DLY_NO_SPILL = const(8)
    EFFECT_SLOT_ID_REV_NO_SPILL = const(9)

    EFFECT_SLOT_NAME = (
        "A",
        "B",
        "C",
        "D",
        
        "X",
        "MOD",
        "DLY",
        "REV",

        "DLYns",
        "REVns"
    )

    # CC Address for Effect Slot enable/disable. Order has to match the one defined above!
    CC_EFFECT_SLOT_ENABLE = (
        const(17),    # Slot A
        const(18),    # Slot B
        const(19),    # Slot C
        const(20),    # Slot D

        const(22),    # Slot X
        const(24),    # Slot MOD
        const(27),    # Slot DLY (with Spillover)
        const(29),    # Slot REV (with Spillover)

        const(26),    # Slot DLY (without Spillover)
        const(28)     # Slot REV (without Spillover)
    )

    # Slot address pages. Order has to match the one defined above!
    NRPN_SLOT_ADDRESS_PAGE = (
        const(0x32),   # Slot A
        const(0x33),   # Slot B
        const(0x34),   # Slot C
        const(0x35),   # Slot D

        const(0x38),   # Slot X
        const(0x3a),   # Slot MOD
        const(0x3c),   # Slot DLY
        const(0x3d),   # Slot REV

        const(0x3c),   # Slot DLY
        const(0x3d)    # Slot REV
    )    

    # Freeze parameter addresses on page 0x7d (Looper and Delay Freeze) for all slots. 
    # Order has to match the one defined above!
    NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES = [
        const(0x6b),   # Slot A
        const(0x6c),   # Slot B
        const(0x6d),   # Slot C
        const(0x6e),   # Slot D

        const(0x6f),   # Slot X
        const(0x71),   # Slot MOD
        const(0x72),   # Slot DLY
        const(0x73),   # Slot REV

        const(0x72),   # Slot DLY
        const(0x73)    # Slot REV
    ]   

####################################################################################################################

# ControlChange Addresses
_CC_TUNER_MODE = const(31)
_CC_RIG_INDEX_PART_1 = const(32) # The second part will be sent as program change.

# NRPN parameters for effect slots
_NRPN_EFFECT_PARAMETER_ADDRESS_TYPE = const(0x00) 
_NRPN_EFFECT_PARAMETER_ADDRESS_STATE = const(0x03)

# NRPN String parameters
_NRPN_STRING_PARAMETER_ID_RIG_NAME = const(0x01)
_NRPN_STRING_PARAMETER_ID_RIG_DATE = const(0x03)

# Defines some useful MIDI mappings, at least all mappings used in the protocol are defined here centrally. 
# More specific mappings exist in the mappings folder.
class KemperMappings:

    # Effect slot enable/disable
    @staticmethod
    def EFFECT_STATE(slot_id):
        return ClientParameterMapping.get(
            name = f"Slot State { KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] }",
            set = ControlChange(
                KemperEffectSlot.CC_EFFECT_SLOT_ENABLE[slot_id], 
                0    # Dummy value, will be overridden
            ),
            request = KemperNRPNMessage(               
                NRPN_FUNCTION_REQUEST_SINGLE_PARAMETER, 
                KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
                _NRPN_EFFECT_PARAMETER_ADDRESS_STATE
            ),
            response = KemperNRPNMessage(
                NRPN_FUNCTION_RESPONSE_SINGLE_PARAMETER,
                KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
                _NRPN_EFFECT_PARAMETER_ADDRESS_STATE
            )
        )
    
    # Effect slot type (request only)
    @staticmethod
    def EFFECT_TYPE(slot_id):
        return ClientParameterMapping.get(
            name = f"Slot Type { KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] }",
            request = KemperNRPNMessage(               
                NRPN_FUNCTION_REQUEST_SINGLE_PARAMETER, 
                KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
                _NRPN_EFFECT_PARAMETER_ADDRESS_TYPE
            ),
            response = KemperNRPNMessage(               
                NRPN_FUNCTION_RESPONSE_SINGLE_PARAMETER, 
                KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
                _NRPN_EFFECT_PARAMETER_ADDRESS_TYPE
            )
        )

    # Rig date (request only)
    def RIG_DATE(): 
        return ClientParameterMapping.get(
            name = "Rig Date",
            request = KemperNRPNMessage(               
                NRPN_FUNCTION_REQUEST_STRING_PARAMETER, 
                NRPN_ADDRESS_PAGE_STRINGS,
                _NRPN_STRING_PARAMETER_ID_RIG_DATE
            ),
            response = KemperNRPNMessage(
                NRPN_FUNCTION_RESPONSE_STRING_PARAMETER, 
                NRPN_ADDRESS_PAGE_STRINGS,
                _NRPN_STRING_PARAMETER_ID_RIG_DATE
            ),
            type = ClientParameterMapping.PARAMETER_TYPE_STRING
        )

    # Rig name (request only)
    def RIG_NAME(): 
        return ClientParameterMapping.get(
            depends = KemperMappings.RIG_DATE(),
            name = "Rig Name",
            request = KemperNRPNMessage(               
                NRPN_FUNCTION_REQUEST_STRING_PARAMETER,             
                NRPN_ADDRESS_PAGE_STRINGS,
                _NRPN_STRING_PARAMETER_ID_RIG_NAME
            ),
            response = KemperNRPNMessage(
                NRPN_FUNCTION_RESPONSE_STRING_PARAMETER, 
                NRPN_ADDRESS_PAGE_STRINGS,
                _NRPN_STRING_PARAMETER_ID_RIG_NAME
            ),
            type = ClientParameterMapping.PARAMETER_TYPE_STRING
        )

    # Switch tuner mode on/off (no receive possible when not in bidirectional mode)
    def TUNER_MODE_STATE(): 
        return ClientParameterMapping.get(
            name = "Tuner Mode",
            set = ControlChange(
                _CC_TUNER_MODE, 
                0    # Dummy value, will be overridden
            ),
            response = KemperNRPNMessage(
                0x01,
                0x7f,
                0x7e
            )
        )

    # Tuner note (only sent in bidirectional mode)
    def TUNER_NOTE(): 
        return ClientParameterMapping.get(
            name = "Tuner Note",
            response = KemperNRPNMessage(
                0x01,
                0x7d,
                0x54
            )
        )

    # Tuner deviance from "in tune" (only sent in bidirectional mode)
    def TUNER_DEVIANCE(): 
        return ClientParameterMapping.get(
            name = "Tuner Deviance",
            response = KemperNRPNMessage(
                0x01,
                0x7c,
                0x0f
            )
        )

    # Used for state sensing in bidirection communication
    def BIDIRECTIONAL_SENSING():
        return ClientParameterMapping.get(
            name = "Sense",
            response = KemperNRPNExtendedMessage(
                0x7e,
                [
                    0x7f
                ]
            )
        ) 
    
    # Rig ID
    def RIG_ID():
        return ClientTwoPartParameterMapping.get(
            name = "Rig ID",
            response = [
                ControlChange(
                    _CC_RIG_INDEX_PART_1,
                    0    # Dummy value, will be ignored
                ),
                ProgramChange(
                    0    # Dummy value, will be ignored
                )
            ]
        )

####################################################################################################################


_PARAMETER_SET_2 = [
    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_A),

    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_B),

    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_C),

    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_D),

    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_X),

    KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD),
    KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_MOD),

    KemperMappings.RIG_NAME(),

    KemperMappings.TUNER_MODE_STATE(),
    KemperMappings.TUNER_NOTE(),
    KemperMappings.TUNER_DEVIANCE()
]

_SELECTED_PARAMETER_SET_ID = const(0x02)
_SELECTED_PARAMETER_SET = _PARAMETER_SET_2


# Implements the internal Kemper bidirectional communication protocol
class KemperBidirectionalProtocol: #(BidirectionalProtocol):
    
    _STATE_OFFLINE = 10   # No commmunication initiated
    _STATE_RUNNING = 20   # Bidirectional communication established

    def __init__(self, time_lease_seconds):
        self.state = self._STATE_OFFLINE
        self.__time_lease_encoded = self.__encode_time_lease(time_lease_seconds)

        # This is the reponse template for the status sensing message the Profiler sends every
        # about 500ms.
        self.__mapping_sense = KemperMappings.BIDIRECTIONAL_SENSING()

        # Re-send the beacon after half of the lease time have passed
        self.resend_period = PeriodCounter(time_lease_seconds * 1000 * 0.5)

        # Period for initial beacons (those shall not be sent too often)
        self.init_period = PeriodCounter(5000)

        # Period after which communication will be regarded as broken when no sensing message comes in
        # (the device sends this roughly every 500ms so we wait 1.5 seconds which should be sufficient)
        self.sensing_period = PeriodCounter(1500)
        self.sensing_period.reset()

        self.debug = False   # This is set by the BidirectionalClient constructor
        self.__count_relevant_messages = 0
        self.__has_been_running = False
        self.__init_sent = False
        
    # Called before usage, with a midi handler.
    def init(self, midi, client):
        self.__midi = midi  
        self.__client = client

    # Must return (boolean) if the passed mapping is handled in the bidirectional protocol
    def is_bidirectional(self, mapping):
        return mapping in _SELECTED_PARAMETER_SET

    # Must return a color representation for the current state
    def get_color(self):
        return Colors.GREEN if self.state == self._STATE_RUNNING else Colors.RED
 
    # Must return (boolean) if the passed mapping should feed back the set value immediately
    # without waiting for a midi message.
    def feedback_value(self, mapping):
        return self.is_bidirectional(mapping)

    # Initialize the communication and keeps it alive when time lease exceeds
    def update(self):
        if self.state == self._STATE_OFFLINE:
            if self.init_period.exceeded:
                if self.debug:                     # pragma: no cover
                    self.__print("Initialize")

                if self.__has_been_running:
                    self.__client.notify_connection_lost()                    

                self.__init_sent = True
                self.__send_beacon(init = True)

        elif self.state == self._STATE_RUNNING:
            if self.sensing_period.exceeded:
                self.state = self._STATE_OFFLINE

                if self.debug:                     # pragma: no cover
                    self.__print("Lost connection")                

            elif self.resend_period.exceeded:
                if self.debug:                     # pragma: no cover
                    self.__print("Send keep-alive message")

                self.__send_beacon()

    # Receive sensing messages and re-init (with init = 1 again) when they stop appearing for longer then 1 second
    def receive(self, midi_message):
        if not self.__init_sent:
            return
        
        if not isinstance(midi_message, SystemExclusive):
            return False
               
        # Compare manufacturer IDs
        if midi_message.manufacturer_id != self.__mapping_sense.response.manufacturer_id:
            return False
        
        if self.debug:                     # pragma: no cover
            self.__count_relevant_messages += 1

        # Check if the message belongs to the status sense mapping. The following have to match:
        #   2: function code, (0x7e)
        #   3: instance ID,   (0x00)
        #   4: address page   (0x7f)
        #
        # The first two values are ignored (the Kemper MIDI specification implies this would contain the product type
        # and device ID as for the request, however the device just sends two zeroes)
        if midi_message.data[2:5] != self.__mapping_sense.response.data[2:5]:
            return False
        
        if self.state != self._STATE_RUNNING:
            self.resend_period.reset()
            
            if self.debug:                     # pragma: no cover
               self.__print("Connection established")

            self.__has_been_running = True
            self.state = self._STATE_RUNNING

        self.sensing_period.reset()

        return True

    # Send beacon for bidirection communication
    def __send_beacon(self, init = False):
        self.__midi.send(
            KemperNRPNExtendedMessage(
                0x7e,
                [
                    0x40,
                    _SELECTED_PARAMETER_SET_ID,
                    self.__get_flags(
                        init = init,
                        tunemode = True
                    ),
                    self.__time_lease_encoded
                ]
            )
        )

    # Encode time lease (this is done in 2 second steps for the Kemper)
    def __encode_time_lease(self, time_lease_seconds):
        return int(time_lease_seconds / 2)

    # Generates the flags byte.
    def __get_flags(self, init = False, sysex = True, echo = False, nofe = False, noctr = False, tunemode = False):
        i = 1 if init else 0
        s = 1 if sysex else 0
        e = 1 if echo else 0
        n = 1 if nofe else 0
        c = 1 if noctr else 0
        t = 1 if tunemode else 0

        return 0x00 | (i << 0) | (s << 1) | (e << 2) | (n << 3) | (c << 4) | (t << 5)

    def __print(self, msg):                     # pragma: no cover
        do_print(f"Bidirectional: { msg } (Received { repr(self.__count_relevant_messages) })")
        self.__count_relevant_messages = 0
