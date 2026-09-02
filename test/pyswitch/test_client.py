import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *
from .mocks_midi import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    # "adafruit_midi": MockAdafruitMIDI(),
    # "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    # "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    # "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    # "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "gc": MockGC()
}):
    from lib.pyswitch.controller.client import Client

    from.mocks_appl import *


class MockParameterMapping2(MockParameterMapping):
    pass


class TestClient(unittest.TestCase):

    def test_set(self):
        midi = MockMIDI()
        
        client = Client(
            midi = midi,
            config = {}
        )

        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        client.set(mapping_1, 33)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_1.set)
        self.assertEqual(mapping_1.set_value_calls, [33])


##############################################################################################


    def test_set_list(self):
        midi = MockMIDI()
        
        client = Client(
            midi = midi,
            config = {}
        )

        mapping_1 = MockParameterMapping(
            set = [
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x03, 0x04]
                # ),
                None,
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x33, 0x04, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x33, 0x04]
                # ),
            ]
        )

        client.set(mapping_1, [33, 55])

        self.assertEqual(len(midi.messages_sent), 2)
        self.assertEqual(midi.messages_sent[0], mapping_1.set[0])
        self.assertEqual(midi.messages_sent[1], mapping_1.set[2])
        self.assertEqual(mapping_1.set_value_calls, [[33, 55]])


##############################################################################################


    def test_set_not_settable(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        # Must not throw
        client.set(mapping_1, 33)

        
##############################################################################################


    def test_request(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        listener = MockClientRequestListener()

        client.request(mapping_1, listener)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_1.request)
        
        # Receive None
        client.receive(None)
        self.assertEqual(listener.parameter_changed_calls, [])

        # Receive ControlChange
        client.receive((176, 3, 4)) #ControlChange(3, 4))
        self.assertEqual(listener.parameter_changed_calls, [])

        # Receive correct message
        req = client.requests[0]
        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [mapping_1])
        self.assertEqual(mapping_1.value, 34)
        self.assertEqual(req.finished, True)
        self.assertEqual(client.requests, [])


##############################################################################################


    def test_request_no_listener(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        client.request(mapping_1)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_1.request)
        
        # Receive None
        client.receive(None)
        
        # Receive ControlChange
        client.receive((176, 3, 4)) #ControlChange(3, 4))
        
        # Receive correct message
        req = client.requests[0]
        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(mapping_1.value, 34)
        self.assertEqual(req.finished, True)
        self.assertEqual(client.requests, [])
        
        
##############################################################################################


    def test_request_add_listeners(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x01, 0x10, 0x20, 0x00, 0x02, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x01, 0x10, 0x20],
            #     data = [0x00, 0x02, 0x09]
            # )
        )

        listener = MockClientRequestListener()

        client.register(mapping_1, listener)

        self.assertEqual(len(midi.messages_sent), 0)
        
        self.assertEqual(len(client.requests), 1)
        req = client.requests[0]

        self.assertEqual(req.listeners, [listener])

        # Add same listener again
        client.register(mapping_1, listener)

        self.assertEqual(len(client.requests), 1)
        self.assertEqual(req.listeners, [listener])

        # Add other listener 
        listener_2 = MockClientRequestListener()
        client.register(mapping_1, listener_2)

        self.assertEqual(len(client.requests), 1)
        self.assertEqual(req.listeners, [listener, listener_2])

        # Add other mapping
        client.register(mapping_2, listener_2)

        self.assertEqual(len(client.requests), 2)
        req_2 = client.requests[1]

        self.assertEqual(req.listeners, [listener, listener_2])
        self.assertEqual(req_2.listeners, [listener_2])


##############################################################################################


    def test_request_list(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_1 = MockParameterMapping(
            request = [
                (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x05, 0x07, 0x09]
                # ),
                None,
                (0xf0, 0x00, 0x10, 0x24, 0x05, 0x07, 0x79, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x24],
                #     data = [0x05, 0x07, 0x79]
                # )
            ],
            response = [
                (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x00, 0x00, 0x09]
                # ),
                (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0xa9, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x00, 0x00, 0xa9]
                # ),
                None,
                (0xf0, 0x00, 0x10, 0x23, 0x00, 0x00, 0x07, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x23],
                #     data = [0x00, 0x00, 0x07]
                # )
            ]
        )

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        answer_msg_2 = (0xf0, 0x00, 0x10, 0x25, 0x00, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x25],
        #     data = [0x00, 0x00, 0x07, 0x47]
        # )

        answer_msg_3 = (0xf0, 0xbb, 0x10, 0x25, 0xaa, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0xbb, 0x10, 0x25],
        #     data = [0xaa, 0x00, 0x07, 0x47]
        # )

        answer_msg_4 = (0xf0, 0xbb, 0x10, 0x25, 0xaa, 0x00, 0x07, 0x88, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0xbb, 0x10, 0x25],
        #     data = [0xaa, 0x00, 0x07, 0x47]
        # )

        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 33,
                "valueIndex": 0
            },
            {
                "message": answer_msg_2,
                "value": 22,
                "valueIndex": 1
            },
            {
                "message": answer_msg_3,
                "value": 34,
                "valueIndex": 2
            }
        ]

        mapping_1.output_result_finished = False

        listener = MockClientRequestListener()

        # Request value
        client.request(mapping_1, listener)
        req = client.requests[0]

        self.assertEqual(len(midi.messages_sent), 2)
        self.assertEqual(midi.messages_sent[0], mapping_1.request[0])
        self.assertEqual(midi.messages_sent[1], mapping_1.request[2])
        
        # Receive None
        client.receive(None)
        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, None)

        # Receive ControlChange
        client.receive((176, 3, 4)) #ControlChange(3, 4))
        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, None)
                
        # Receive unregistered message
        client.receive(answer_msg_4)
        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, None)

        # Receive correct message 2 before 1
        client.receive(answer_msg_2)

        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, [None, 22])

        self.assertEqual(req.finished, False)
        self.assertIn(req, client.requests)

        # Receive correct message 1
        client.receive(answer_msg_1)

        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, [33, 22])
        
        self.assertEqual(req.finished, False)
        self.assertIn(req, client.requests)

        # Receive correct message 3 and finish
        mapping_1.output_result_finished = True
        client.receive(answer_msg_3)

        self.assertEqual(listener.parameter_changed_calls, [mapping_1])
        self.assertEqual(mapping_1.value, [33, 22, 34])        

        self.assertEqual(req.finished, True)
        self.assertEqual(client.requests, [])


##############################################################################################


    def test_request_endless(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {
                "maxRequestLifetimeMillis": 0
            }
        )

        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        listener = MockClientRequestListener()

        client.register(mapping_1, listener)

        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )
        
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        req = client.requests[0]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [mapping_1])        
        
        self.assertEqual(mapping_1.value, 34)
        self.assertEqual(req.finished, False)
        self.assertTrue(req in client.requests)


##############################################################################################


    def test_request_endless_no_listener(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {
                "maxRequestLifetimeMillis": 0
            }
        )

        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        client.register(mapping_1)

        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )
        
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        req = client.requests[0]

        client.receive(answer_msg)
        
        self.assertEqual(mapping_1.value, 34)
        self.assertEqual(req.finished, False)
        self.assertTrue(req in client.requests)


##############################################################################################


    def test_request_terminate(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {}
        )

        mapping_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        listener = MockClientRequestListener()

        client.request(mapping_1, listener)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_1.request)
        
        req = client.requests[0]        
        req.terminate()
        self.assertEqual(req.finished, True)

        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_1.value, None)
        
        self.assertEqual(client.requests, [])


##############################################################################################


    def test_request_timeout(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {}
        )

        mapping_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        listener = MockClientRequestListener()

        client.request(mapping_1, listener)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_1.request)
        
        req = client.requests[0]        
        req.lifetime = MockPeriodCounter()
        client._Client__cleanup_terminated_period = MockPeriodCounter()
        
        client.receive(None)
        
        self.assertEqual(req.finished, False)

        req.lifetime.exceed_next_time = True
        client._Client__cleanup_terminated_period.exceed_next_time = True
        client.receive(None)

        self.assertEqual(req.finished, True)
        

##############################################################################################


    def test_request_dependency(self):        
        midi = MockMIDI()

        client = Client(
            midi = midi,
            config = {},
        )

        mapping_dep = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_1 = MockParameterMapping(
            depends = mapping_dep,
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x19, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x19]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x19, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x19]
            # )
        )

        listener = MockClientRequestListener()

        client.request(mapping_1, listener)

        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(midi.messages_sent[0], mapping_dep.request)
        
        # Receive dependency message
        req = client.requests[0]
        answer_msg = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        mapping_dep.outputs_parse = [
            {
                "message": answer_msg,
                "value": 34
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [])
        self.assertEqual(mapping_dep.value, 34)
        self.assertEqual(mapping_1.value, None)
        self.assertEqual(req.finished, True)

        # Receive dependency message
        self.assertEqual(len(client.requests), 1)
        req2 = client.requests[0]

        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 12
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [mapping_1])
        self.assertEqual(mapping_1.value, 12)
        self.assertEqual(req2.finished, True)
        self.assertEqual(client.requests, [])

        # Receive dependency (no value change)
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 12
            }
        ]

        client.receive(answer_msg)
        self.assertEqual(listener.parameter_changed_calls, [mapping_1])
        self.assertEqual(mapping_1.value, 12)
        self.assertEqual(client.requests, [])

