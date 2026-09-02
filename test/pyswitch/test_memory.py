import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "gc": MockGC()
}):
    from .mocks_misc import MockMisc
    from gc import gc_mock_data

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
        
        from lib.pyswitch.stats import Memory


class TestMemory(unittest.TestCase):

    def test_watch(self):
        self._test_watch(False)
        self._test_watch(True)


    def _test_watch(self, only_if_changed):
        MockMisc.reset_mock()
        gc_mock_data().reset()

        gc_mock_data().output_mem_free = 1024 * 1024
        gc_mock_data().output_mem_alloc = 3333
        
        Memory.start("foo")
        
        self.assertEqual(len(MockMisc.msgs), 1)
        self.assertIn("foo", MockMisc.latest_msg())     
        self.assertIn(MockMisc.format_size(1024 * 1024), MockMisc.latest_msg())        # Free memory
        self.assertIn(MockMisc.format_size(1024 * 1024 + 3333), MockMisc.latest_msg()) # Total memory

        # Use 333 bytes
        gc_mock_data().output_mem_free = 1024 * 1024 - 333
        
        Memory.watch("bar", only_if_changed)
        
        self.assertEqual(len(MockMisc.msgs), 2)
        self.assertIn("bar", MockMisc.latest_msg())     
        self.assertIn("Allocated", MockMisc.latest_msg())     
        self.assertIn(MockMisc.format_size(1024 * 1024 - 333), MockMisc.latest_msg())            # Free memory
        self.assertIn(MockMisc.format_size(333), MockMisc.latest_msg())     # Total memory

        # Use 0 bytes
        #gc_mock_data().output_mem_free = 1024 * 1024 - 333
        
        Memory.watch("bar2", only_if_changed)
        
        self.assertEqual(len(MockMisc.msgs), 3 if not only_if_changed else 2)
        if not only_if_changed:
            self.assertIn("bar2", MockMisc.latest_msg())     
            self.assertNotIn("Allocated", MockMisc.latest_msg())     
            self.assertNotIn("Released", MockMisc.latest_msg())     
            self.assertIn(MockMisc.format_size(1024 * 1024 - 333), MockMisc.latest_msg())            # Free memory
            self.assertNotIn(MockMisc.format_size(333), MockMisc.latest_msg())     # Total memory

        # Free 100 bytes
        gc_mock_data().output_mem_free = 1024 * 1024 - 233
        
        Memory.watch("bar3", only_if_changed)
        
        self.assertEqual(len(MockMisc.msgs), 4 if not only_if_changed else 3)
        self.assertIn("bar3", MockMisc.latest_msg())     
        self.assertIn("Released", MockMisc.latest_msg())     
        self.assertIn(MockMisc.format_size(1024 * 1024 - 233), MockMisc.latest_msg())            # Free memory
        self.assertIn(MockMisc.format_size(100), MockMisc.latest_msg())  # Total memory

