import unittest
from unittest.mock import patch

from .test_client import (
    Client, ControlChange, MockAdafruitMIDI, MockClientRequestListener,
    MockParameterMapping,
)


class RecordingListener(MockClientRequestListener):
    def __init__(self, name, events):
        super().__init__()
        self.name = name
        self.events = events

    def parameter_changed(self, mapping):
        super().parameter_changed(mapping)
        self.events.append((self.name, mapping.value))


class TestClientFinishedRequests(unittest.TestCase):
    def mapping(self, name, request_control=100):
        return MockParameterMapping(
            name=name,
            request=ControlChange(request_control, 0),
            response=ControlChange(20, 0),
        )

    def test_request_with_listener_restarts_finished_request_before_cleanup(self):
        midi = MockAdafruitMIDI.MIDI()
        client = Client(midi, {"maxRequestLifetimeMillis": 200})
        mapping = self.mapping("finished-requeue")
        old_listener = MockClientRequestListener()
        new_listener = MockClientRequestListener()
        with patch("lib.pyswitch.misc.monotonic", return_value=0):
            client.request(mapping, old_listener)
            old_request = client.get_matching_request(mapping)
            old_request.terminate()
            old_request.terminate()
        with patch("lib.pyswitch.misc.monotonic", return_value=5):
            client.request(mapping, new_listener)
            new_request = client.get_matching_request(mapping)
            self.assertIsNot(new_request, old_request)
            self.assertFalse(new_request.finished)
            self.assertEqual(new_request.listeners, [new_listener])
            self.assertEqual(len(midi.messages_sent), 2)
            client.request(mapping, new_listener)
            self.assertIs(client.get_matching_request(mapping), new_request)
            self.assertEqual(len(midi.messages_sent), 2)
        with patch("lib.pyswitch.misc.monotonic", return_value=5.1):
            client.receive(None)
            self.assertFalse(new_request.finished)
        message = ControlChange(20, 7)
        mapping.outputs_parse = [{"message": message, "value": 7}]
        with patch("lib.pyswitch.misc.monotonic", return_value=5.15):
            self.assertTrue(client.receive(message))
        self.assertEqual(old_listener.request_terminated_calls, [mapping])
        self.assertEqual(old_listener.parameter_changed_calls, [])
        self.assertEqual(new_listener.parameter_changed_calls, [mapping])
        self.assertEqual(new_listener.request_terminated_calls, [])
        self.assertEqual(client.requests, [])

    def test_finished_request_without_listener_remains_a_noop(self):
        midi = MockAdafruitMIDI.MIDI()
        client = Client(midi, {})
        mapping = self.mapping("finished-without-listener")
        listener = MockClientRequestListener()
        client.request(mapping, listener)
        request = client.get_matching_request(mapping)
        request.terminate()
        client.request(mapping)
        self.assertEqual(client.requests, [request])
        self.assertEqual(len(midi.messages_sent), 1)
        self.assertEqual(listener.request_terminated_calls, [mapping])

    def test_requeued_request_merges_listeners_before_cleanup(self):
        midi = MockAdafruitMIDI.MIDI()
        client = Client(midi, {})
        mapping = self.mapping("finished-merge")
        first, second, third = [MockClientRequestListener() for _ in range(3)]
        client.request(mapping, first)
        client.get_matching_request(mapping).terminate()
        client.request(mapping, second)
        client.request(mapping, third)
        active = [request for request in client.requests if not request.finished]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].listeners, [second, third])
        self.assertEqual(len(midi.messages_sent), 2)

    def test_dependency_can_requeue_finished_request_during_receive(self):
        midi = MockAdafruitMIDI.MIDI()
        client = Client(midi, {})
        first = self.mapping("dependency-first", 100)
        second = self.mapping("dependency-second", 101)
        first.depends = second
        second.depends = first
        events = []
        first_listener = RecordingListener("first", events)
        second_listener = RecordingListener("second", events)
        client.request(first, first_listener)
        client.request(second, second_listener)
        message = ControlChange(20, 7)
        for mapping in [first, second]:
            mapping.outputs_parse = [{"message": message, "value": 7}]
        self.assertTrue(client.receive(message))
        self.assertEqual(events, [("first", 7), ("second", 7)])
        self.assertEqual(len(midi.messages_sent), 3)
        self.assertEqual(client.requests, [])
        self.assertFalse(client.receive(message))
        self.assertEqual(events, [("first", 7), ("second", 7)])
