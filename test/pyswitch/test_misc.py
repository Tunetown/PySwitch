import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "gc": MockGC(),
    "time": MockTime
}):
    from lib.pyswitch.misc import *


class MockUpdateable(Updateable):
    def __init__(self):
        self.num_update_calls = 0
        self.num_reset_calls = 0

    def update(self):
        self.num_update_calls += 1

    def reset(self):
        self.num_reset_calls += 1


##############################################################################


class TestMiscTools(unittest.TestCase):

    def test_get_option(self):
        self.assertEqual(get_option("", "foo"), False)
        self.assertEqual(get_option(False, "foo"), False)
        self.assertEqual(get_option(None, "foo"), False)
        self.assertEqual(get_option({}, "foo"), False)

        some = {
            "foo": 2,
            "bar": "foo"
        }
        self.assertEqual(get_option(some, "foo"), 2)
        self.assertEqual(get_option(some, "bar"), "foo")
        self.assertEqual(get_option(some, "bar", 555), "foo")
        self.assertEqual(get_option(some, "bat", 555), 555)
        self.assertEqual(get_option(some, "for"), False)
        self.assertEqual(get_option(some, "for", -4), -4)        


    def test_get_current_millis(self):
        MockTime.mock["monotonicReturn"] = 1021
        self.assertEqual(get_current_millis(), 1021000)
        
        MockTime.mock["monotonicReturn"] = 1045
        self.assertEqual(get_current_millis(), 1045000)

        MockTime.mock["monotonicReturn"] = 1045.56
        self.assertEqual(get_current_millis(), 1045560)

        MockTime.mock["monotonicReturn"] = 1045.567
        self.assertEqual(get_current_millis(), 1045567)


    # def test_format_timestamp(self):
    #     MockTime.mock["localtimeReturn"] = time.struct_time((2009, 7, 18, 6, 5, 4, 0, 0, 0))
    #     self.assertEqual(formatted_timestamp(), "2009-07-18 06:05:04")

    #     MockTime.mock["localtimeReturn"] = time.struct_time((22019, 12, 8, 12, 35, 44, 0, 0, 0))
    #     self.assertEqual(formatted_timestamp(), "22019-12-08 12:35:44")


    # def test_compare_midi_messagess_sysex(self):
    #     message_1 = SystemExclusive(
    #         manufacturer_id = [0x02, 0x03],
    #         data = [0x34, 0x45, 0x67]
    #     )
    #     message_2 = SystemExclusive(
    #         manufacturer_id = [0x02, 0x03],
    #         data = [0x34, 0x45, 0x67]
    #     )

    #     self.assertEqual(compare_midi_messages(message_1, message_2), True)
    #     self.assertEqual(compare_midi_messages(message_1, None), False)
    #     self.assertEqual(compare_midi_messages(None, message_2), False)

    #     message_1.data[1] = 0xa9
    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)

    #     message_1.data[1] = 0x45
    #     self.assertEqual(compare_midi_messages(message_1, message_2), True)

    #     message_1.manufacturer_id[1] = 0x04
    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)


    # def test_compare_midi_messagess_cc(self):
    #     message_1 = ControlChange(2, 66)
    #     message_2 = ControlChange(2, 66)

    #     self.assertEqual(compare_midi_messages(message_1, message_2), True)
    #     self.assertEqual(compare_midi_messages(message_1, None), False)
    #     self.assertEqual(compare_midi_messages(None, message_2), False)

    #     message_1.control = 67

    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)


    # def test_compare_midi_messagess_pc(self):
    #     message_1 = ProgramChange(56)
    #     message_2 = ProgramChange(56)

    #     self.assertEqual(compare_midi_messages(message_1, message_2), True)
    #     self.assertEqual(compare_midi_messages(message_1, None), False)
    #     self.assertEqual(compare_midi_messages(None, message_2), False)

    #     message_1.patch = 67

    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)


    # def test_compare_midi_messagess_unknown(self):
    #     message_1 = MIDIUnknownEvent(56)
    #     message_2 = MIDIUnknownEvent(56)

    #     self.assertEqual(compare_midi_messages(message_1, message_2), True)
    #     self.assertEqual(compare_midi_messages(message_1, None), False)
    #     self.assertEqual(compare_midi_messages(None, message_2), False)

    #     message_1.status = 67

    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)


    # def test_compare_midi_messagess_others(self):
    #     message_1 = "foo"
    #     message_2 = "bar"

    #     self.assertEqual(compare_midi_messages(message_1, message_2), False)



##############################################################################


class TestMiscUpdater(unittest.TestCase):

    def test_update(self):
        u1 = MockUpdateable()
        u2 = MockUpdateable()
        u3 = MockUpdateable()

        updater = Updater()
        self.assertEqual(updater.updateables, [])

        updater.add_updateable(u1)
        self.assertEqual(updater.updateables, [u1])

        updater.update()
        self.assertEqual(u1.num_update_calls, 1)
        self.assertEqual(u2.num_update_calls, 0)
        self.assertEqual(u3.num_update_calls, 0)

        updater.add_updateable(u2)
        updater.add_updateable(u3)
        self.assertEqual(updater.updateables, [u1, u2, u3])

        updater.update()
        self.assertEqual(u1.num_update_calls, 2)
        self.assertEqual(u2.num_update_calls, 1)
        self.assertEqual(u3.num_update_calls, 1)

        # Try to add same updateables again
        updater.add_updateable(u1)
        updater.add_updateable(u3)
        self.assertEqual(updater.updateables, [u1, u2, u3])


    def test_reset(self):
        u1 = MockUpdateable()
        u2 = MockUpdateable()
        u3 = MockUpdateable()

        updater = Updater()

        updater.add_updateable(u1)

        updater.reset()
        self.assertEqual(u1.num_reset_calls, 1)
        self.assertEqual(u2.num_reset_calls, 0)
        self.assertEqual(u3.num_reset_calls, 0)

        updater.add_updateable(u2)
        updater.add_updateable(u3)
        self.assertEqual(updater.updateables, [u1, u2, u3])

        updater.reset()
        self.assertEqual(u1.num_reset_calls, 2)
        self.assertEqual(u2.num_reset_calls, 1)
        self.assertEqual(u3.num_reset_calls, 1)


    def test_add_invalid(self):
        updater = Updater()

        updater.add_updateable({})
        self.assertEqual(updater.updateables, [])


##############################################################################


class TestMiscEventEmitter(unittest.TestCase):

    def test_add_listener(self):
        e = EventEmitter()
        self.assertEqual(e.listeners, [])

        class Object(object):
            pass

        listener_1 = Object()
        listener_2 = Object()

        self.assertEqual(e.add_listener(listener_1), True)
        self.assertEqual(e.listeners, [listener_1])

        self.assertEqual(e.add_listener(listener_1), False)
        self.assertEqual(e.listeners, [listener_1])

        self.assertEqual(e.add_listener(listener_2), True)
        self.assertEqual(e.listeners, [listener_1, listener_2])

        self.assertEqual(e.add_listener(listener_2), False)
        self.assertEqual(e.listeners, [listener_1, listener_2])


##############################################################################


class TestMiscPeriodCounter(unittest.TestCase):

    def test_counter(self):
        p = PeriodCounter(500)
        self.assertEqual(p.interval, 500)

        MockTime.mock["monotonicReturn"] = 1
        p.reset()
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 0)

        MockTime.mock["monotonicReturn"] = 1.2
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 200)

        MockTime.mock["monotonicReturn"] = 1.5
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 500)

        MockTime.mock["monotonicReturn"] = 1.501
        self.assertEqual(p.exceeded, True)
        self.assertEqual(p.passed, 0)

        MockTime.mock["monotonicReturn"] = 1.7
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 199)

        MockTime.mock["monotonicReturn"] = 1.9
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 399)

        MockTime.mock["monotonicReturn"] = 2
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 499)

        MockTime.mock["monotonicReturn"] = 2.003
        self.assertEqual(p.exceeded, True)
        self.assertEqual(p.passed, 0)

        MockTime.mock["monotonicReturn"] = 2.004
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 1)

        MockTime.mock["monotonicReturn"] = 2.2
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 197)

        p.reset()

        MockTime.mock["monotonicReturn"] = 2.4
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 200)

        MockTime.mock["monotonicReturn"] = 2.7
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 500)

        MockTime.mock["monotonicReturn"] = 2.701
        self.assertEqual(p.exceeded, True)
        self.assertEqual(p.passed, 0)

        MockTime.mock["monotonicReturn"] = 2.702
        self.assertEqual(p.exceeded, False)
        self.assertEqual(p.passed, 1)
