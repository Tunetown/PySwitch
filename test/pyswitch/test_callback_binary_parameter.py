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
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from .mocks_ui import *
    from .mocks_callback import *

    from lib.pyswitch.controller.actions import PushButtonAction
    from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    
    from lib.pyswitch.controller.controller import Controller


class TestBinaryParameterCallback(unittest.TestCase):
 
    def test_set_parameter(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x05, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x05]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
        appl.tick()   # TODO why is this needed??

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True            

        appl.tick()
        appl.tick()

        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.5)
        self.assertEqual(led_driver.leds[0], (100, 50, 0))
            
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))
                    

###############################################################################################


    def test_set_parameter_color_callback(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x05, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x05]
            # )
        )

        mock_data = {
            "color": [0, 0, 0],
            "expValue": None
        }

        def get_color(action, value):
            self.assertEqual(action, action_1)
            self.assertEqual(value, mock_data["expValue"])
            return mock_data["color"]

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            color_callback = get_color,
            led_brightness_on = 0.5,
            led_brightness_off = 0.1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True        
            
        mock_data["color"] = (100, 100, 50)            
        mock_data["expValue"] = 10
        mapping_1.value = 10

        appl.tick()
        appl.tick()

        self.assertEqual(appl.inputs[0].color, (100, 100, 50))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.5)
        self.assertEqual(led_driver.leds[0], (50, 50, 25))
        
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        mock_data["color"] = (100, 200, 50)
        mock_data["expValue"] = 3
        mapping_1.value = 3

        appl.tick()
        appl.tick()
        
        self.assertEqual(appl.inputs[0].color, (100, 200, 50))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (10, 20, 5))
        

###############################################################################################
 

    def test_set_parameter_no_response(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
        appl.tick()   # TODO why is this needed?
        
        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True            

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))
        
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))
    

###############################################################################################


    def test_set_parameter_value_disable_auto(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x05, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x21],
            #     data = [0x01, 0x02, 0x03, 0x05]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 11,
            value_disable = "auto",
            comparison_mode = BinaryParameterCallback.GREATER_EQUAL
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })

        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
            ],
            period_counter = period
        )

        appl.init()

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        answer_msg_2 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        # Build scene:
        # Check if nothing crashes if set is called before a value came in
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 11)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)
        
        self.assertEqual(action_1.state, True)

        # Step 2
        switch_1.shall_be_pushed = False
        self.assertEqual(cb._value_disable, "auto")

        appl.tick()
        appl.tick()
        
        # Nothing must have been sent because we still have no disabling value
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        
        self.assertEqual(action_1.state, False)

        # Receive a value
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1,
            answer_msg_2
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_2,
                "value": 6
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, False)
        self.assertEqual(cb._value_disable, 6)

        # Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 11)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)
        
        self.assertEqual(action_1.state, True)

        # Receive a value when state is True (must not override the remembered value)
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 100
            }
        ]
        
        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        self.assertEqual(cb._value_disable, 6)
                
        # Disable again
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 3)
        self.assertEqual(mapping_1.set_value_calls[2], 6)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 3)
        self.assertEqual(appl._Controller__midi.messages_sent[2], mapping_1.set)
                    
        self.assertEqual(action_1.state, False)


###############################################################################################


    def test_set_parameter_values_disable_auto(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()
        
        mapping_1 = MockParameterMapping(
            set = [
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),                
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x03, 0x04]
                # ),
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x05, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x03, 0x05]
                # )
            ],
            response = (0xf0, 0x00, 0x11, 0x21, 0x01, 0x02, 0x03, 0x05, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x11, 0x21],
            #     data = [0x01, 0x02, 0x03, 0x05]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = [11, 12],
            value_disable = [4, "auto"],
            comparison_mode = BinaryParameterCallback.GREATER_EQUAL
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })        
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
            ],
            period_counter = period
        )

        appl.init()

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        # Build scene:
        # Check if nothing crashes if set is called before a value came in
        switch_1.shall_be_pushed = True

        self.assertEqual(cb._BinaryParameterCallback__update_value_disabled, [False, True])

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 0)            
                    
        self.assertEqual(len(appl._Controller__midi.messages_sent), 0)
        
        self.assertEqual(action_1.state, True)

        # Step 2        
        switch_1.shall_be_pushed = False
        self.assertEqual(cb._value_disable, [4, "auto"])

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 0)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 0)
        
        self.assertEqual(action_1.state, False)
       
        # Receive a value
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 7
            }
        ]
        
        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, False)
        self.assertEqual(cb._value_disable, [4, 7])

        # Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], [11, 12])

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set[0])
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set[1])
        
        self.assertEqual(action_1.state, True)
        
        # Receive a value when state is True (must not override the remembered value)
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 100
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        self.assertEqual(cb._value_disable, [4, 7])

        # Disable again
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], [4, 7])

        self.assertEqual(len(appl._Controller__midi.messages_sent), 4)
        self.assertEqual(appl._Controller__midi.messages_sent[2], mapping_1.set[0])
        self.assertEqual(appl._Controller__midi.messages_sent[3], mapping_1.set[1])
                    
        self.assertEqual(action_1.state, False)


###############################################################################################


    def test_set_parameter_disable_mapping(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # )
        )

        mapping_disable_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x33, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x33, 0x04]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            mapping_disable = mapping_disable_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1,
            comparison_mode = BinaryParameterCallback.GREATER_EQUAL
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })    

        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
        appl.tick()  # TODO why is this necessary?
        
        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.5)
        self.assertEqual(led_driver.leds[0], (100, 50, 0))
        
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_disable_1.set_value_calls), 1)
        self.assertEqual(mapping_disable_1.set_value_calls[0], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_disable_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))        


###############################################################################################


    def test_set_parameter_mappings_lists(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = [
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x03, 0x04]
                # ),
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x05, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x22],
                #     data = [0x01, 0x02, 0x03, 0x05]
                # ),
                (0xf0, 0x00, 0x10, 0x22, 0x01, 0x02, 0x03, 0x88, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x22],
                #     data = [0x01, 0x02, 0x03, 0x88]
                # )
            ]
        )

        mapping_disable_1 = MockParameterMapping(
            set = [
                (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x39, 0x04, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x01, 0x02, 0x39, 0x04]
                # ),
                (0xf0, 0x00, 0x10, 0x30, 0x01, 0x02, 0x39, 0x07, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x30],
                #     data = [0x01, 0x02, 0x39, 0x07]
                # )
            ]
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            mapping_disable = mapping_disable_1,
            value_enable = [1, 2, 3],
            value_disable = [0, -1]
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })    
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()
        appl.tick()   # TODO why is this needed?
        

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], [1, 2, 3])

        self.assertEqual(len(appl._Controller__midi.messages_sent), 3)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set[0])
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set[1])
        self.assertEqual(appl._Controller__midi.messages_sent[2], mapping_1.set[2])

        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_disable_1.set_value_calls), 1)
        self.assertEqual(mapping_disable_1.set_value_calls[0], [0, -1])

        self.assertEqual(len(appl._Controller__midi.messages_sent), 5)
        self.assertEqual(appl._Controller__midi.messages_sent[3], mapping_disable_1.set[0])
        self.assertEqual(appl._Controller__midi.messages_sent[4], mapping_disable_1.set[1])


###############################################################################################


    def test_set_parameter_with_label(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1,
            display_dim_factor_on = 0.5,
            display_dim_factor_off = 0.2,
            text = "foo"
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })    
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
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
        appl.tick()  # TODO why?
        
        action_1.label = MockDisplayLabel()

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.5)
        self.assertEqual(led_driver.leds[0], (100, 50, 0))

        self.assertEqual(action_1.label.text, "foo")
        self.assertEqual(action_1.label.back_color, (100, 50, 0))
        
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))

        self.assertEqual(action_1.label.text, "foo")
        self.assertEqual(action_1.label.back_color, (40, 20, 0))
                    

###############################################################################################


    def test_set_parameter_with_label_tdis(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = (200, 100, 0),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1,
            display_dim_factor_on = 0.5,
            display_dim_factor_off = 0.2,
            text = "foo",
            text_disabled = "bar"
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })    
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ]
        )

        appl.init()
        appl.tick()  # TODO why?
        
        action_1.label = MockDisplayLabel()

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.5)
        self.assertEqual(led_driver.leds[0], (100, 50, 0))

        self.assertEqual(action_1.label.text, "foo")
        self.assertEqual(action_1.label.back_color, (100, 50, 0))
            
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)

        self.assertEqual(appl.inputs[0].color, (200, 100, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))

        self.assertEqual(action_1.label.text, "bar")
        self.assertEqual(action_1.label.back_color, (40, 20, 0))
                    

###############################################################################################


    def test_set_parameter_with_label_no_text(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x01, 0x02, 0x03, 0x04, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # ),
            response = (0xf0, 0x00, 0x10, 0x21, 0x01, 0x02, 0x03, 0x04, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x21],
            #     data = [0x01, 0x02, 0x03, 0x04]
            # )
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = 10,
            value_disable = 3,
            color = ((200, 100, 0), (10, 20, 30)),
            led_brightness_on = 0.5,
            led_brightness_off = 0.1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })           
        
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": (0, 1)
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()
        appl.tick()  # Why?
        
        action_1.label = MockDisplayLabel()

        # Build scene:
        # Step 1: Enable
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 1)
        self.assertEqual(mapping_1.set_value_calls[0], 10)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.set)

        self.assertEqual(appl.inputs[0].colors, [(200, 100, 0), (10, 20, 30)])
        self.assertEqual(appl.inputs[0].brightnesses, [0.5, 0.5])
        self.assertEqual(led_driver.leds[0], (100, 50, 0))
        self.assertEqual(led_driver.leds[1], (5, 10, 15))

        self.assertEqual(action_1.label.text, "")
        self.assertEqual(action_1.label.back_color, [(200, 100, 0), (10, 20, 30)])
        
        # Step 2: Disable
        switch_1.shall_be_pushed = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(mapping_1.set_value_calls), 2)
        self.assertEqual(mapping_1.set_value_calls[1], 3)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.set)

        self.assertEqual(appl.inputs[0].colors, [(200, 100, 0), (10, 20, 30)])
        self.assertAlmostEqual(appl.inputs[0].brightnesses[0], 0.1)
        self.assertAlmostEqual(appl.inputs[0].brightnesses[1], 0.1)
        self.assertEqual(led_driver.leds[0], (20, 10, 0))
        self.assertEqual(led_driver.leds[1], (1, 2, 3))

        self.assertEqual(action_1.label.text, "")
        self.assertEqual(action_1.label.back_color, [(40, 20, 0), (2, 4, 6)])


###############################################################################################


    def test_request(self):
        self._test_request(BinaryParameterCallback.GREATER, 1, 0, 0, 0, False)
        self._test_request(BinaryParameterCallback.GREATER, 1, 0, 1, 0, False)
        self._test_request(BinaryParameterCallback.GREATER, 1, 0, 2, 0)
        self._test_request(BinaryParameterCallback.GREATER, 1, 0, 16383, 0)

        self._test_request(BinaryParameterCallback.GREATER_EQUAL, 1, 0, 0, 0, False)
        self._test_request(BinaryParameterCallback.GREATER_EQUAL, 1, 0, 1, 0)
        self._test_request(BinaryParameterCallback.GREATER_EQUAL, 1, 0, 2, 0)
        self._test_request(BinaryParameterCallback.GREATER_EQUAL, 1, 0, 16383, 0)

        self._test_request(BinaryParameterCallback.EQUAL, 1, 0, 0, 0, False)
        self._test_request(BinaryParameterCallback.EQUAL, 1, 0, 1, 0)
        self._test_request(BinaryParameterCallback.EQUAL, 1, 0, 2, 0, False)

        self._test_request(BinaryParameterCallback.LESS_EQUAL, 1, 2, 0, 2)
        self._test_request(BinaryParameterCallback.LESS_EQUAL, 1, 2, 1, 2)
        self._test_request(BinaryParameterCallback.LESS_EQUAL, 1, 2, 2, 2, False)
        self._test_request(BinaryParameterCallback.LESS_EQUAL, 1, 2, 3, 2, False)

        self._test_request(BinaryParameterCallback.LESS, 1, 2, 0, 2)
        self._test_request(BinaryParameterCallback.LESS, 1, 2, 1, 2, False)
        self._test_request(BinaryParameterCallback.LESS, 1, 2, 2, 2, False)
        self._test_request(BinaryParameterCallback.LESS, 1, 2, 3, 2, False)

        self._test_request(BinaryParameterCallback.NO_STATE_CHANGE, 1, 2, 0, 2, False)
        self._test_request(BinaryParameterCallback.NO_STATE_CHANGE, 1, 2, 1, 2, False)
        self._test_request(BinaryParameterCallback.NO_STATE_CHANGE, 1, 2, 2, 2, False)
        self._test_request(BinaryParameterCallback.NO_STATE_CHANGE, 1, 2, 3, 2, False)

        with self.assertRaises(Exception):
            self._test_request("invalid", 0, 1, 0, 1)


    def _test_request(self, mode, value_on, value_off, test_value_on, test_value_off, exp_state_on = True, exp_state_off = False):
        switch_1 = MockSwitch()
        
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

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = value_on + 4,
            value_disable = value_off,
            reference_value = value_on,
            comparison_mode = mode
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })   

        period = MockPeriodCounter()

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ],
            period_counter = period
        )

        appl.init()

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        answer_msg_2 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        # Build scene:
        # Send update request
        period.exceed_next_time = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request)
        
        # Step without update
        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        
        # Receive value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1,
            answer_msg_2
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": test_value_on
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_1.value, test_value_on)
        self.assertEqual(action_1.state, exp_state_on)

        # Receive value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": test_value_off
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_1.value, test_value_off)
        self.assertEqual(action_1.state, exp_state_off)


###############################################################################################


    def test_request_mappings_lists(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            request = [
                (0xf0, 0x00, 0x10, 0x20, 0x05, 0x27, 0x09, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x05, 0x27, 0x09]
                # ),
                (0xf0, 0x00, 0x10, 0x21, 0x05, 0x27, 0x0a, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x21],
                #     data = [0x05, 0x27, 0x0a]
                # )
            ],
            response = [
                (0xf0, 0x00, 0x10, 0x20, 0x00, 0x30, 0x19, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x00, 0x30, 0x19]
                # ),
                (0xf0, 0x00, 0x10, 0x21, 0x00, 0x30, 0x1d, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x21],
                #     data = [0x00, 0x30, 0x1d]
                # )
            ]
        )

        cb = BinaryParameterCallback(
            mapping = mapping_1,
            value_enable = [1, 2, 3],
            value_disable = [0, -1, -2]
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True          
        })   

        period = MockPeriodCounter()

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ],
            period_counter = period
        )

        appl.init()

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        answer_msg_2 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x07, 0x45]
        # )

        # Build scene:
        # Send update request
        period.exceed_next_time = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request[0])
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_1.request[1])
        
        # Step without update
        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        
        # Receive value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1,
            answer_msg_2
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 2
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_1.value, 2)

        # Receive value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 66
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_1.value, 66)


###############################################################################################


    def test_action_disabled(self):
        switch_1 = MockSwitch()
        
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

        cb_enable = MockEnabledCallback(output = True)

        cb = BinaryParameterCallback(
            mapping = mapping_1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb
        })   

        period = MockPeriodCounter()

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                },
                MockInputControllerDefinition()
            ],
            period_counter = period
        )

        appl.init()

        answer_msg_1 = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        # Build scene:
        # Send update request
        period.exceed_next_time = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request)
        
        # Step without update
        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.messages_sent), 1)
        
        # Receive value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_1
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_1,
                "value": 1
            }
        ]
        cb_enable.output_get = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_1.value, 1)
        
        self.assertEqual(action_1.state, True)

