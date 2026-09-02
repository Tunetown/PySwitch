import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.kemper import *
    from lib.pyswitch.clients.kemper.mappings.cabinet import *
    from lib.pyswitch.colors import Colors

    from .mocks_appl import *


class TestKemperBidirectionalProtocol(unittest.TestCase):

    def test(self):
        protocol = KemperBidirectionalProtocol(20)

        self.assertEqual(protocol.resend_period.interval, 10000)
        self.assertEqual(protocol.init_period.interval, 5000)
        self.assertEqual(protocol.sensing_period.interval, 1500)

        protocol.resend_period = MockPeriodCounter()
        protocol.init_period = MockPeriodCounter()
        protocol.sensing_period = MockPeriodCounter()

        client = MockClient()
        midi = MockMidiController()
        protocol.init(midi, client)

        self.assertEqual(protocol.get_color(), Colors.RED)

        exp_msg_init = (0xf0, 0x00, 0x20, 0x33, 0x02, 0x7f, 0x7e, 0x00, 0x40, 0x02, 0x23, 0x0a, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = NRPN_MANUFACTURER_ID,
        #     data = [
        #         NRPN_PRODUCT_TYPE,       # 0x02
        #         NRPN_DEVICE_ID_OMNI,     # 0x7f
        #         0x7e,
        #         NRPN_INSTANCE,           # 0x00
        #         0x40,
        #         0x02,                    # Parameter set
        #         0x23,                    # Flags: 100011
        #         0x0a,                    # Time lease / 2
        #     ]
        # )

        exp_msg_keepalive = (0xf0, 0x00, 0x20, 0x33, 0x02, 0x7f, 0x7e, 0x00, 0x40, 0x02, 0x22, 0x0a, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = NRPN_MANUFACTURER_ID,
        #     data = [
        #         NRPN_PRODUCT_TYPE,       # 0x02
        #         NRPN_DEVICE_ID_OMNI,     # 0x7f
        #         0x7e,
        #         NRPN_INSTANCE,           # 0x00
        #         0x40,
        #         0x02,                    # Parameter set
        #         0x22,                    # Flags: 100010
        #         0x0a,                    # Time lease / 2
        #     ]
        # )
        
        # Receive sense message in advance (shall do nothing)
        #self.assertEqual(protocol.receive(KemperMappings.BIDIRECTIONAL_SENSING().response), True)
        #self.assertEqual(protocol.state, protocol._STATE_OFFLINE)

        # First offline update: Must issue an init message
        protocol.init_period.exceed_next_time = True
        protocol.update()

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], exp_msg_init)

        # Some updating
        protocol.update()
        self.assertEqual(len(midi.messages_sent), 1)

        # Receive invalid messages
        self.assertEqual(protocol.receive((176, 9, 0)), False) #ControlChange(control = 9, value = 0)), False)
        self.assertEqual(protocol.receive(
            (0xf0, 0x00, 0x11, 0x00, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x11],
            #     data = [0x00]
            # )
        ), False)
        self.assertEqual(protocol.receive(
            (0xf0, 0x00, 0x20, 0x33, 0x01, 0x02, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = NRPN_MANUFACTURER_ID,
            #     data = [0x01, 0x02]
            # )
        ), False)

        # Receive sense message
        self.assertEqual(protocol.receive(KemperMappings.BIDIRECTIONAL_SENSING().response), True)
        self.assertEqual(protocol.state, protocol._STATE_RUNNING)
        self.assertEqual(protocol.get_color(), Colors.GREEN)

        # Some updating
        protocol.update()
        self.assertEqual(len(midi.messages_sent), 1)

        # Keep-alive
        protocol.resend_period.exceed_next_time = True
        protocol.update()
        self.assertEqual(len(midi.messages_sent), 2)
        self.assertEqual(midi.messages_sent[1], exp_msg_keepalive)

        # Some updating
        protocol.update()
        self.assertEqual(len(midi.messages_sent), 2)

        # Lost connection
        protocol.sensing_period.exceed_next_time = True
        protocol.update()
        self.assertEqual(protocol.state, protocol._STATE_OFFLINE)
        self.assertEqual(protocol.get_color(), Colors.RED)

        protocol.init_period.exceed_next_time = True
        protocol.update()
        self.assertEqual(len(midi.messages_sent), 3)
        self.assertEqual(midi.messages_sent[2], exp_msg_init)

        self.assertEqual(client.num_notify_connection_lost_calls, 1)


    def test_no_init(self):
        protocol = KemperBidirectionalProtocol(50)

        self.assertEqual(protocol.resend_period.interval, 25000)
        self.assertEqual(protocol.init_period.interval, 5000)
        self.assertEqual(protocol.sensing_period.interval, 1500)

        client = MockClient()
        midi = MockMidiController()
        protocol.init(midi, client)

        # Receive sense message in advance (shall do nothing)
        self.assertEqual(protocol.receive(KemperMappings.BIDIRECTIONAL_SENSING().response), None)
        self.assertEqual(protocol.state, protocol._STATE_OFFLINE)


    def test_is_bidirectional(self):
        protocol = KemperBidirectionalProtocol(20)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)

        self.assertEqual(protocol.is_bidirectional(KemperMappings.RIG_NAME()), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.TUNER_NOTE()), True)
        self.assertEqual(protocol.is_bidirectional(KemperMappings.TUNER_DEVIANCE()), True)

        # Not in
        self.assertEqual(protocol.is_bidirectional(MAPPING_CABINET_STATE()), False)


    def test_feedback_value(self):
        protocol = KemperBidirectionalProtocol(20)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_A)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_B)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_C)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_D)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_X)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_STATE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.EFFECT_TYPE(KemperEffectSlot.EFFECT_SLOT_ID_MOD)), True)

        self.assertEqual(protocol.feedback_value(KemperMappings.RIG_NAME()), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.TUNER_NOTE()), True)
        self.assertEqual(protocol.feedback_value(KemperMappings.TUNER_DEVIANCE()), True)

        # Not in
        self.assertEqual(protocol.feedback_value(MAPPING_CABINET_STATE()), False)
