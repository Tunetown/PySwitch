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
    
    from lib.pyswitch.ui.ui import DisplayElement
    from lib.pyswitch.ui.elements import TunerDisplay
    from lib.pyswitch.misc import Updater

    from .mocks_appl import MockClient, MockAction, MockInputControllerDefinition


class MockStrobe:
    class StrobeController:
        def __init__(self,
                     mapping_state, 
                     mapping_deviance, 
                     dim_factor = 0, 
                     speed = 0, 
                     color = None, 
                     max_fps = 0, 
                     reverse = None 
            ):
            self.init_calls = []

            self.mapping_state = mapping_state
            self.mapping_deviance = mapping_deviance
            self.dim_factor = dim_factor
            self.speed = speed
            self.color = color 
            self.max_fps = max_fps
            self.reverse = reverse

        def init(self, appl):
            self.init_calls.append(appl)


class MockController2(Updater):
    def __init__(self, inputs = []):
        Updater.__init__(self)

        self.client = MockClient()
        self.inputs = inputs
        self.shared = {}
      

class MockFootSwitch:
    def __init__(self, actions = []):
        self.override_action = None
        self.actions = actions
        self.pixels = []




class TestKemperTunerDisplayCallback(unittest.TestCase):

    def test(self):
        self._test(process_overridden_actions = False)
        self._test(process_overridden_actions = True)

    def _test(self, process_overridden_actions):
        element = DisplayElement()

        cb = TunerDisplayCallback(
            splash_default = element,
            strobe = False,
            process_overridden_actions = process_overridden_actions
        )

        switch_action_0 = MockAction()
        switch_action_1 = MockAction()
        switch_action_2 = MockAction()
        switch_action_3 = MockAction()

        switch = MockFootSwitch(
            actions = [
                switch_action_0
            ]
        )

        switch_other_1 = MockFootSwitch(
            actions = [
                switch_action_1,
                switch_action_2
            ]
        )

        switch_other_2 = MockFootSwitch(
            actions = [
                switch_action_3
            ]
        )

        appl = MockController2(
            inputs = [
                switch_other_1,
                MockInputControllerDefinition(),
                switch,
                switch_other_2,
                MockInputControllerDefinition()
            ]
        )
        cb.init(appl)

        self.assertIn(KemperMappings.TUNER_MODE_STATE(), cb._Callback__mappings)
        
        splash_tuner = cb._TunerDisplayCallback__splash_tuner

        self.assertIsInstance(splash_tuner, TunerDisplay)

        mapping = cb._Callback__mappings[0]

        mapping.value = 0
        cb.parameter_changed(mapping)

        self.assertEqual(cb.get_root(), element)

        self.assertEqual(switch.override_action, None)
        self.assertEqual(switch_other_1.override_action, None)
        self.assertEqual(switch_other_2.override_action, None)
        
        self.assertEqual(switch_action_0.num_reset_calls, 1)
        self.assertEqual(switch_action_1.num_reset_calls, 1)
        self.assertEqual(switch_action_2.num_reset_calls, 1)
        self.assertEqual(switch_action_3.num_reset_calls, 1)

        mapping.value = 1
        cb.parameter_changed(mapping)

        self.assertEqual(cb.get_root(), splash_tuner)

        self.assertEqual(switch.override_action, cb)
        self.assertEqual(switch_other_1.override_action, cb)
        self.assertEqual(switch_other_2.override_action, cb)
        
        self.assertEqual(switch_action_0.num_reset_calls, 1)
        self.assertEqual(switch_action_1.num_reset_calls, 1)
        self.assertEqual(switch_action_2.num_reset_calls, 1)
        self.assertEqual(switch_action_3.num_reset_calls, 1)

        mapping.value = 0
        cb.parameter_changed(mapping)

        self.assertEqual(cb.get_root(), element)

        self.assertEqual(switch.override_action, None)
        self.assertEqual(switch_other_1.override_action, None)
        self.assertEqual(switch_other_2.override_action, None)
        
        self.assertEqual(switch_action_0.num_reset_calls, 2)
        self.assertEqual(switch_action_1.num_reset_calls, 2)
        self.assertEqual(switch_action_2.num_reset_calls, 2)
        self.assertEqual(switch_action_3.num_reset_calls, 2)

        self.assertEqual(cb.push(), process_overridden_actions)
        self.assertEqual(cb.release(), process_overridden_actions)


    def test_with_custom_element(self):
        element = DisplayElement()
        element_2 = DisplayElement()

        cb = TunerDisplayCallback(
            splash_default = element,
            splash_tuner = element_2,
            strobe = False
        )

        appl = MockController2()
        cb.init(appl)

        self.assertIn(KemperMappings.TUNER_MODE_STATE(), cb._Callback__mappings)
        
        mapping = cb._Callback__mappings[0]

        mapping.value = 0
        self.assertEqual(cb.get_root(), element)

        mapping.value = 1
        self.assertEqual(cb.get_root(), element_2)


    def test_with_strobe(self):
        element = DisplayElement()

        with patch.dict(sys.modules, {
            "lib.pyswitch.controller.strobe": MockStrobe(),
        }):
            cb = TunerDisplayCallback(
                splash_default = element,
                strobe = True,
                strobe_color = (3, 4, 5),
                strobe_dim = 0.75,
                strobe_speed = 1111,
                strobe_max_fps = 121,
                strobe_reverse = False
            )

        appl = MockController2()
        cb.init(appl)

        strobe = cb._TunerDisplayCallback__strobe_controller
        self.assertIsInstance(strobe, MockStrobe.StrobeController)
        self.assertEqual(strobe.init_calls, [appl])
        
        self.assertEqual(strobe.mapping_state, KemperMappings.TUNER_MODE_STATE())
        self.assertEqual(strobe.mapping_deviance, KemperMappings.TUNER_DEVIANCE())
        self.assertEqual(strobe.dim_factor, 0.75)
        self.assertEqual(strobe.speed, 1111)
        self.assertEqual(strobe.color, (3, 4, 5))
        self.assertEqual(strobe.max_fps, 121)
        self.assertEqual(strobe.reverse, False)


