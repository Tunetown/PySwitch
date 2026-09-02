import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from lib.pyswitch.controller.midi import MidiController, MidiRouting

    from.mocks_appl import *



class TestMidiController(unittest.TestCase):

    def test_appl_routing(self):
        sub_midi_1 = MockMidiController()
        sub_midi_2 = MockMidiController()

        # Must not throw
        midi = MidiController(
            routings = [
                MidiRouting(
                    source = MidiRouting.APPLICATION,
                    target = sub_midi_2
                ),                    
                MidiRouting(
                    source = sub_midi_1,
                    target = MidiRouting.APPLICATION
                )
            ]
        )

        # Receive
        midi_message_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_2 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        sub_midi_1.next_receive_messages = [
            midi_message_1,
            midi_message_2
        ]
        
        self.assertEqual(midi.receive(), midi_message_1)
        self.assertEqual(midi.receive(), midi_message_2)
        self.assertEqual(midi.receive(), None)

        self.assertEqual(sub_midi_1.messages_sent, [])
        self.assertEqual(sub_midi_2.messages_sent, [])

        # Send
        midi_message_3 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0xa8, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0xa8, 0x47]
        # )

        midi.send(midi_message_3)
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_3])


    def test_appl_routing_distribute(self):
        sub_midi_1 = MockMidiController()
        sub_midi_2 = MockMidiController()

        # Must not throw
        midi = MidiController(
            routings = [
                MidiRouting(
                    source = MidiRouting.APPLICATION,
                    target = sub_midi_1
                ),                    
                MidiRouting(
                    source = MidiRouting.APPLICATION,
                    target = sub_midi_2
                )
            ]
        )

        # Receive
        midi_message_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_2 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        midi.send(midi_message_1)
        self.assertEqual(sub_midi_1.messages_sent, [midi_message_1])
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_1])

        midi.send(midi_message_2)
        self.assertEqual(sub_midi_1.messages_sent, [midi_message_1, midi_message_2])
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_1, midi_message_2])


    def test_appl_routing_merge(self):
        sub_midi_1 = MockMidiController()
        sub_midi_2 = MockMidiController()

        # Must not throw
        midi = MidiController(
            routings = [
                MidiRouting(
                    source = sub_midi_1,
                    target = MidiRouting.APPLICATION
                ),                    
                MidiRouting(
                    source = sub_midi_2,
                    target = MidiRouting.APPLICATION
                )
            ]
        )

        # Receive
        midi_message_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_2 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        midi_message_3 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x88, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x88]
        # )

        sub_midi_1.next_receive_messages = [
            midi_message_1,
            midi_message_2
        ]

        sub_midi_2.next_receive_messages = [
            midi_message_3
        ]
        
        self.assertEqual(midi.receive(), midi_message_1)
        self.assertEqual(midi.receive(), midi_message_2)
        self.assertEqual(midi.receive(), midi_message_3)        
        self.assertEqual(midi.receive(), None)

        self.assertEqual(sub_midi_1.messages_sent, [])
        self.assertEqual(sub_midi_2.messages_sent, [])        


###################################################################################################


    def test_external_routings_distribute(self):
        sub_midi_1 = MockMidiController()

        sub_midi_2 = MockMidiController()
        sub_midi_3 = MockMidiController()

        # Must not throw
        midi = MidiController(
            routings = [
                MidiRouting(
                    source = sub_midi_1,
                    target = sub_midi_2
                ),
                MidiRouting(
                    source = sub_midi_1,
                    target = sub_midi_3
                )
            ]
        )

        midi_message_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_2 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        midi_message_unknown = [248]

        sub_midi_1.next_receive_messages = [
            midi_message_1,            
            midi_message_2,
            midi_message_unknown
        ]

        # Receiving triggers external routes
        midi.receive()
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_1])
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1])

        midi.receive()
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_1, midi_message_2])
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1, midi_message_2])

        midi.receive()
        self.assertEqual(sub_midi_2.messages_sent, [midi_message_1, midi_message_2, [248]])
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1, midi_message_2, [248]])

        self.assertEqual(sub_midi_1.messages_sent, [])


    def test_external_routings_merge(self):
        sub_midi_1 = MockMidiController()
        sub_midi_2 = MockMidiController()

        sub_midi_3 = MockMidiController()

        # Must not throw
        midi = MidiController(
            routings = [
                MidiRouting(
                    source = sub_midi_1,
                    target = sub_midi_3
                ),
                MidiRouting(
                    source = sub_midi_2,
                    target = sub_midi_3
                )
            ]
        )

        midi_message_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_2 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        midi_message_3 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        midi_message_4 = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x22],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        sub_midi_1.next_receive_messages = [
            midi_message_1,
            midi_message_2
        ]

        sub_midi_2.next_receive_messages = [
            midi_message_3,
            midi_message_4
        ]

        # Receiving triggers external routes
        midi.receive()
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1, midi_message_3])
        
        midi.receive()
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1, midi_message_3, midi_message_2, midi_message_4])
        
        midi.receive()
        self.assertEqual(sub_midi_3.messages_sent, [midi_message_1, midi_message_3, midi_message_2, midi_message_4])
        
        self.assertEqual(sub_midi_1.messages_sent, [])
        self.assertEqual(sub_midi_2.messages_sent, [])
        
        
    def test_no_args(self):
        # Must not throw
        MidiController([])

