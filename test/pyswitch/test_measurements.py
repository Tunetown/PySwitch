import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "time": MockTime,
    "gc": MockGC()
}):
    from lib.pyswitch.controller.measure import RuntimeMeasurement


class MockRuntimeMeasurementListener:
    def __init__(self):
        self.num_update_calls = 0

    def measurement_updated(self, measurement):
        self.num_update_calls += 1


class TestMeasurementRuntime(unittest.TestCase):    

    def test_measurement(self):
        m = RuntimeMeasurement(
            interval_millis = 300
        )

        self.assertEqual(m.average, 0)
        self.assertEqual(m.value, 0)

        # finish without start: Must be ignored
        MockTime.mock["monotonicReturn"] = 0.9
        m.finish()

        # Tick with 500ms
        MockTime.mock["monotonicReturn"] = 1
        m.start()
        MockTime.mock["monotonicReturn"] = 1.5
        m.finish()

        self.assertEqual(m.average, 500)
        self.assertEqual(m.value, 500)
        self.assertEqual(m.sum, 500)

        # Tick with 300ms
        MockTime.mock["monotonicReturn"] = 2
        m.start()
        MockTime.mock["monotonicReturn"] = 2.3
        m.finish()

        self.assertEqual(m.average, 400)
        self.assertEqual(m.value, 500)
        self.assertEqual(m.sum, 800)

        # Tick with 1000ms
        MockTime.mock["monotonicReturn"] = 3
        m.start()
        MockTime.mock["monotonicReturn"] = 4
        m.finish()

        self.assertEqual(m.average, 600)
        self.assertEqual(m.value, 1000)
        self.assertEqual(m.sum, 1800)

        m.reset()
        self.assertEqual(m.average, 0)
        self.assertEqual(m.value, 0)
        self.assertEqual(m.sum, 0)


    def test_update(self):
        m = RuntimeMeasurement(
            interval_millis = 300
        )

        listener_1 = MockRuntimeMeasurementListener()
        listener_2 = MockRuntimeMeasurementListener()
        m.add_listener(listener_1)
        m.add_listener(listener_2)

        MockTime.mock["monotonicReturn"] = 1

        m.update()
        self.assertEqual(listener_1.num_update_calls, 1)
        self.assertEqual(listener_2.num_update_calls, 1)

        MockTime.mock["monotonicReturn"] = 1.2

        m.update()
        self.assertEqual(listener_1.num_update_calls, 1)
        self.assertEqual(listener_2.num_update_calls, 1)

        MockTime.mock["monotonicReturn"] = 1.4

        m.update()
        self.assertEqual(listener_1.num_update_calls, 2)
        self.assertEqual(listener_2.num_update_calls, 2)

        MockTime.mock["monotonicReturn"] = 1.6

        m.update()
        self.assertEqual(listener_1.num_update_calls, 2)
        self.assertEqual(listener_2.num_update_calls, 2)

        MockTime.mock["monotonicReturn"] = 1.8

        m.update()
        self.assertEqual(listener_1.num_update_calls, 3)
        self.assertEqual(listener_2.num_update_calls, 3)



