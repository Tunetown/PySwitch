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
    from lib.pyswitch.clients.kemper.actions.morph import KemperMorphCallback
    from lib.pyswitch.colors import Colors
    from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    from lib.pyswitch.controller.controller import Controller
    
    from .mocks_appl import *
    from .mocks_callback import *


class TestKemperMorphCallback(unittest.TestCase):

    def test_colors(self):
        self._test_colors(color = "kemper", set_internal_state = True)
        self._test_colors(color = "kemper", set_internal_state = False)
        self._test_colors(color = (3, 4, 5))


    def _test_colors(self, color, set_internal_state = False):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = KemperMorphCallback(
            mapping = mapping_1, 
            text = "foo", 
            value_enable = 127, 
            value_disable = 0, 
            reference_value = 8191, 
            comparison_mode = BinaryParameterCallback.GREATER_EQUAL, 
            led_brightness_on = 0.5,
            led_brightness_off = 0.1,
            display_dim_factor_on = 0.5,
            display_dim_factor_off = 0.1,
            color = color,
            set_internal_state = set_internal_state
        )

        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertEqual(cb._text, "foo")

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()
        midi = MockMidiController()
        
        appl = Controller(
            led_driver = led_driver,
            midi = midi,
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()

        answer_msg = (0xf0, 0xbb, 0x10, 0x25, 0xaa, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0xbb, 0x10, 0x25],
        #     data = [0xaa, 0x00, 0x07, 0x47]
        # )

        # Build scene:
        # Step 1
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 0
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, Colors.RED if color == "kemper" else color)
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)            
        
        # Step 2
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 16383
            }
        ]    

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, Colors.BLUE if color == "kemper" else color)
        self.assertEqual(appl.inputs[0].brightness, 0.5)
                    
        # Step 3
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 8191
            }
        ]    

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, (128, 0, 127) if color == "kemper" else color)
        self.assertEqual(appl.inputs[0].brightness, 0.5)


###################################################################################################################


    def test_colors_overrides(self):
        self._test_colors_overrides((0, 0, 0), (200, 200, 200), (99, 99, 99))
        self._test_colors_overrides((255, 255, 255), (205, 205, 205), (231, 231, 231))
        self._test_colors_overrides((200, 0, 20), (100, 100, 100), (151, 49, 59))
        

    def _test_colors_overrides(self, color_base, color_morph, color_intermediate):
        self._do_test_colors_overrides(
            color_base = color_base,
            color_morph = color_morph,
            color_intermediate = color_intermediate,
            set_internal_state = False
        )
        self._do_test_colors_overrides(
            color_base = color_base,
            color_morph = color_morph,
            color_intermediate = color_intermediate,
            set_internal_state = True
        )

    def _do_test_colors_overrides(self, color_base, color_morph, color_intermediate, set_internal_state):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = KemperMorphCallback(
            mapping = mapping_1, 
            text = "foo", 
            value_enable = 127, 
            value_disable = 0, 
            reference_value = 8191, 
            comparison_mode = BinaryParameterCallback.GREATER_EQUAL, 
            led_brightness_on = 0.5,
            led_brightness_off = 0.1,
            display_dim_factor_on = 0.5,
            display_dim_factor_off = 0.1,
            color = "kemper",
            color_base = color_base,
            color_morph = color_morph,
            set_internal_state = set_internal_state
        )

        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertEqual(cb._text, "foo")

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()
        midi = MockMidiController()
        
        appl = Controller(
            led_driver = led_driver,
            midi = midi,
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()

        answer_msg = (0xf0, 0xbb, 0x10, 0x25, 0xaa, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0xbb, 0x10, 0x25],
        #     data = [0xaa, 0x00, 0x07, 0x47]
        # )

        # Build scene:
        # Step 1
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 0
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, color_base)
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)            
        
        # Step 2
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 16383
            }
        ]    

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, color_morph)
        self.assertEqual(appl.inputs[0].brightness, 0.5)
                    
        # Step 3
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": 8191
            }
        ]    

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, color_intermediate)
        self.assertEqual(appl.inputs[0].brightness, 0.5)
                

#############################################################################################


    def test_push(self):
        self._test_push(suppress_send = False, set_internal_state = False)
        self._test_push(suppress_send = True, set_internal_state = False)
        self._test_push(suppress_send = False, set_internal_state = True)


    def _test_push(self, suppress_send, set_internal_state):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = KemperMorphCallback(
            mapping = mapping_1, 
            value_enable = 127, 
            value_disable = 0, 
            suppress_send = suppress_send,
            set_internal_state = set_internal_state
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()
        midi = MockMidiController()

        appl = Controller(
            led_driver = led_driver,
            midi = midi,
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()
        
        # Set a value in advance
        answer_msg = (0xf0, 0xbb, 0x10, 0x25, 0xaa, 0x00, 0x07, 0x47, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0xbb, 0x10, 0x25],
        #     data = [0xaa, 0x00, 0x07, 0x47]
        # )

        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.value = 1111
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": mapping_1.value
            }
        ]
        
        appl.tick()    

        self.assertEqual(appl.inputs[0].color, (238, 0, 17))
        if set_internal_state:
            self.assertEqual(appl.shared["morphStateOverride"], 1111)
        else:
            self.assertNotIn("morphStateOverride", appl.shared)

        # Build scene:
        # Step 1
        switch_1.shall_be_pushed = True
        appl.tick()    
        switch_1.shall_be_pushed = False
        appl.tick()

        if suppress_send:
            self.assertEqual(len(mapping_1.set_value_calls), 0)    
            self.assertEqual(len(appl._Controller__midi.messages_sent), 0)
        else:
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[0], 127)
            self.assertEqual(mapping_1.set_value_calls[1], 0)

            self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
            self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)
            self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)
        
        if set_internal_state:
            self.assertEqual(appl.shared["morphStateOverride"], 0)
            self.assertEqual(appl.inputs[0].color, Colors.RED)
        else:
            self.assertNotIn("morphStateOverride", appl.shared)
            self.assertEqual(appl.inputs[0].color, (238, 0, 17))

        # If set_internal_state == True, incoming messages will not change the state        
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.value = 1111
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": mapping_1.value
            }
        ]    
        
        appl.tick()
        appl.tick()
        
        if set_internal_state:
            self.assertEqual(appl.inputs[0].color, Colors.RED)
        else:
            self.assertEqual(appl.inputs[0].color, (238, 0, 17))

        # Changed values will be regarded     
        midi.next_receive_messages = [
            answer_msg
        ]
        mapping_1.value = 1112
        mapping_1.outputs_parse = [
            {
                "message": answer_msg,
                "value": mapping_1.value
            }
        ]    
        
        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, (238, 0, 17))
                    