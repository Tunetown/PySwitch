PRODUCT_TYPE = 0x02  # Player
DEVICE_ID_OMNI = 0x7f
INSTANCE_ID = 0x00


class MockMIDI:
    def __init__(self):
        self.messages_sent = []
        self.next_receive_messages = []

    def receive(self):
        if self.next_receive_messages:
            return self.next_receive_messages.pop(0)
        
        return None
    
    def send(self, midi_message):
        self.messages_sent.append(midi_message)


def test_mapping(self, 
                 mapping, 
                 exp_name = None, 
                 exp_nrpn_set_length = 13, 
                 exp_nrpn_request_length = 11, 
                 exp_nrpn_response_length = 13,
                 exp_midi_channel = 0,
                 kemper_nrpn = True      # Check Kemper specific fixed NRPN digits for Sysex Messages
    ):
    message = f"Error in mapping {mapping.name}"
    
    def check_message(msg, exp_nrpn_len, exp_type):
        if not msg:
            return

        if is_list(msg):
            self.assertIsInstance(msg, tuple, message)
            for m in msg:
                check_message(m, exp_nrpn_len, exp_type)
            return

        ###########################

        self.assertIsInstance(msg, exp_type, message)

        if msg[0] == 0xf0:
            self.assertEqual(len(msg), exp_nrpn_len, message)
            self.assertEqual(msg[-1], 0xf7, message)

            for x in msg[1:-1]:
                self.assertTrue(x < 128, message)

            if kemper_nrpn:
                # For kemper mappings we define some fixed stuff which is always the same
                # TODO put this in kemper specific code
                self.assertEqual(tuple(msg[0:6]), (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI), message)                
                self.assertEqual(msg[7], INSTANCE_ID, message)

        elif msg[0] & 0xF0 == 0xB0:
            # CC
            self.assertEqual(len(msg), 3, message)
            self.assertEqual(msg[0], 176 + exp_midi_channel, message)
            self.assertTrue(msg[1] < 128, message)
            self.assertTrue(msg[2] < 128, message)

            self.assertIn(f"({exp_midi_channel})", mapping.name, message)

        elif msg[0] & 0xF0 == 0xC0:
            # PC
            self.assertEqual(len(msg), 2, message)
            self.assertEqual(msg[0], 192 + exp_midi_channel, message)
            self.assertTrue(msg[1] < 128, message)

            self.assertIn(f"({exp_midi_channel})", mapping.name, message)

        else:
            self.fail(f"No test implemnented for message: {msg}")

    # Check that the messages all have the correct type and length            
    check_message(mapping.set, exp_nrpn_set_length, bytearray)
    check_message(mapping.request, exp_nrpn_request_length, bytes)
    check_message(mapping.response, exp_nrpn_response_length, bytes)

    # Check name
    if exp_name is not None:
        self.assertIn(exp_name, mapping.name, message)


def is_list(value):
    if not value:
        return False
    
    return not isinstance(value[0], int)