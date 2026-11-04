import sys
import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from .mocks_lib import (
    MockAdafruitDisplayText, MockAdafruitMIDIControlChange,
    MockAdafruitMIDIMessage, MockAdafruitMIDIProgramChange,
    MockAdafruitMIDISystemExclusive, MockDisplayIO, MockDisplayShapes,
    MockGC, MockMicropython,
)

with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC(),
}):
    from adafruit_midi.system_exclusive import SystemExclusive
    from lib.pyswitch.controller.client import Client, ClientParameterMapping
    from lib.pyswitch.clients.kemper.mappings.tempo import MAPPING_TEMPO_DISPLAY


class TestSysExResponsePayloads(unittest.TestCase):
    HEADER = [0, 0, 1, 0, 4, 1]
    STRING_HEADER = [0, 0, 3, 0, 0, 1]
    TEMPO_HEADER = [0, 0, 1, 0, 0x7c, 0]

    def message(self, data):
        return SystemExclusive(manufacturer_id=[0, 0x20, 0x33], data=data)

    def mapping(self, header, value, string=False):
        return ClientParameterMapping.get(
            name=str(uuid4()),
            request=self.message([0, 0, 0x41, 0, header[4], header[5]]),
            response=self.message(header),
            value=value,
            type=ClientParameterMapping.PARAMETER_TYPE_STRING if string else 0,
        )

    def test_numeric_response_requires_both_value_bytes(self):
        mapping = self.mapping(self.HEADER, 777)
        for payload in ([], [9]):
            with self.subTest(payload=payload):
                self.assertFalse(mapping.parse(self.message(self.HEADER + payload)))
                self.assertEqual(mapping.value, 777)

    def test_numeric_response_keeps_full_14_bit_values(self):
        mapping = self.mapping(self.HEADER, None)
        for high, low, value in ((0, 0, 0), (0, 127, 127), (1, 2, 130), (127, 127, 16383)):
            with self.subTest(value=value):
                # Product and device bytes are intentionally ignored by the parser.
                self.assertTrue(mapping.parse(self.message([2, 0x7f] + self.HEADER[2:] + [high, low])))
                self.assertEqual(mapping.value, value)

    def test_tempo_pulse_keeps_its_single_byte_value_format(self):
        mapping = MAPPING_TEMPO_DISPLAY()
        for value in (0, 1, 37, 127):
            with self.subTest(value=value):
                self.assertTrue(mapping.parse(self.message(self.TEMPO_HEADER + [value])))
                self.assertEqual(mapping.value, value)
        self.assertTrue(mapping.parse(self.message(self.TEMPO_HEADER + [1, 2])))
        self.assertEqual(mapping.value, 130)
        self.assertFalse(mapping.parse(self.message(self.TEMPO_HEADER)))
        self.assertEqual(mapping.value, 130)

    def test_string_response_requires_a_trailing_nul(self):
        mapping = self.mapping(self.STRING_HEADER, "Original", string=True)
        for payload in ([], [65], [65, 66]):
            with self.subTest(payload=payload):
                self.assertFalse(mapping.parse(self.message(self.STRING_HEADER + payload)))
                self.assertEqual(mapping.value, "Original")

    def test_string_response_keeps_empty_text_and_embedded_characters(self):
        mapping = self.mapping(self.STRING_HEADER, None, string=True)
        for payload, value in (([0], ""), ([65, 0, 66, 127, 0], "A\0B\x7f")):
            with self.subTest(payload=payload):
                self.assertTrue(mapping.parse(self.message(self.STRING_HEADER + payload)))
                self.assertEqual(mapping.value, value)

    def test_incomplete_or_unrelated_headers_are_ignored(self):
        for string, header, value in ((False, self.HEADER, 777), (True, self.STRING_HEADER, "Original")):
            mapping = self.mapping(header, value, string=string)
            for data in [header[:length] for length in range(6)] + [header[:5] + [header[5] + 1]]:
                with self.subTest(string=string, data=data):
                    self.assertFalse(mapping.parse(self.message(data)))
                    self.assertEqual(mapping.value, value)

    def test_invalid_payload_leaves_the_request_waiting_for_a_valid_reply(self):
        for string, header, original, invalid, valid, expected in (
            (False, self.HEADER, 777, [], [1, 2], 130),
            (True, self.STRING_HEADER, "Original", [65, 66], [65, 0], "A"),
            (False, self.TEMPO_HEADER, 777, [], [1], 1),
        ):
            with self.subTest(string=string, header=header):
                mapping = self.mapping(header, original, string=string)
                listener = Mock()
                client = Client(Mock(), {})
                client.request(mapping, listener)
                request = client.get_matching_request(mapping)
                self.assertFalse(client.receive(self.message(header + invalid)))
                self.assertIs(client.get_matching_request(mapping), request)
                self.assertEqual(mapping.value, original)
                listener.parameter_changed.assert_not_called()
                self.assertTrue(client.receive(self.message(header + valid)))
                self.assertIsNone(client.get_matching_request(mapping))
                self.assertEqual(mapping.value, expected)
                listener.parameter_changed.assert_called_once_with(mapping)
