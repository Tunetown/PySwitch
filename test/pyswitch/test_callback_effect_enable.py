import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "usb_midi": MockUsbMidi(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from .mocks_ui import *
    from .mocks_callback import *

    from lib.pyswitch.controller.callbacks.effect_enable import EffectEnableCallback
    from lib.pyswitch.controller.actions import PushButtonAction

    from lib.pyswitch.controller.controller import Controller


class MockEffectEnableCallback(EffectEnableCallback):
    def get_effect_category(self, kpp_effect_type):
        return kpp_effect_type * 10

    def get_effect_category_color(self, category, kpp_type):
        return (category, category + 2, category * 4)

    def get_effect_category_text(self, category, kpp_type):
        return "name" + repr(category)


###############################################################################################


class TestCallbackEffectEnable(unittest.TestCase):

    def test_requests(self):
        switch_1 = MockSwitch()
        
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
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_type_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x10, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x10]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x10, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x10]
            # )
        )

        cb = MockEffectEnableCallback(
            mapping_state = mapping_1,
            mapping_type = mapping_type_1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True
        })
        
        period = MockPeriodCounter()

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

        answer_msg_param = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        answer_msg_type = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
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
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_type_1.request)
        
        # Receive type
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 0
            }
        ]            

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        #self.assertEqual(len(appl._Controller__midi.messages_sent), 2)

        self.assertEqual(mapping_type_1.value, 0)
        self.assertEqual(cb._EffectEnableCallback__effect_category, 0)
        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (0, 2, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertEqual(led_driver.leds[0], (0, 0, 0))

        # Push switch (must stay false when not assigned)
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        #self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        
        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (0, 2, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertEqual(led_driver.leds[0], (0, 0, 0))
        
        # Receive other value (not pushed)
        switch_1.shall_be_pushed = False

        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 1
            }
        ]
            
        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_type_1.value, 1)
        self.assertEqual(cb._EffectEnableCallback__effect_category, 10)
        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (10, 12, 40))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertAlmostEqual(led_driver.leds[0], (int(10*0.02), int(12*0.02), int(40*0.02)))

        # Receive status enabled
        appl._Controller__midi.next_receive_messages = [
            answer_msg_param
        ]
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_param,
                "value": 1
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        self.assertEqual(mapping_1.value, 1)
        self.assertEqual(action_1.state, True)

        self.assertEqual(appl.inputs[0].color, (10, 12, 40))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.3)
        self.assertAlmostEqual(led_driver.leds[0], (int(10*0.3), int(12*0.3), int(40*0.3)))
        
        # Receive non-assigned type again
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 0
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_type_1.value, 0)
        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (0, 2, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertEqual(led_driver.leds[0], (0, 0, 0))
        

###########################################################################################################


    def test_requests_with_label(self):
        switch_1 = MockSwitch()

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

        mapping_type_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x10, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x10]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x10, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x10]
            # )
        )

        cb = MockEffectEnableCallback(
            mapping_state = mapping_1,
            mapping_type = mapping_type_1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "useSwitchLeds": True
        })

        period = MockPeriodCounter()
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

        action_1.label = MockDisplayLabel()

        answer_msg_param = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0x44, 0xf7)
        # SystemExclusive(
        #     manufacturer_id = [0x00, 0x10, 0x20],
        #     data = [0x00, 0x00, 0x09, 0x44]
        # )

        answer_msg_type = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
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
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_type_1.request)
        
        # Receive type (not assigned)
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 0
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)

        self.assertEqual(mapping_type_1.value, 0)
        self.assertEqual(cb._EffectEnableCallback__effect_category, 0)

        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (0, 2, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertEqual(led_driver.leds[0], (0, 0, 0))
        
        self.assertEqual(action_1.label.text, "name0")
        self.assertEqual(action_1.label.back_color, (0, 0, 0))

        # Push switch (must show as off when not assigned)
        switch_1.shall_be_pushed = True

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 4)
        
        self.assertEqual(action_1.state, False)

        self.assertEqual(appl.inputs[0].color, (0, 2, 0))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertEqual(led_driver.leds[0], (0, 0, 0))

        self.assertEqual(action_1.label.text, "name0")
        self.assertEqual(action_1.label.back_color, (0, 0, 0))

        # Receive other value 
        switch_1.shall_be_pushed = False

        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 1
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(mapping_type_1.value, 1)
        self.assertEqual(cb._EffectEnableCallback__effect_category, 10)

        self.assertEqual(appl.inputs[0].color, (10, 12, 40))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertAlmostEqual(led_driver.leds[0], (int(10*0.02), int(12*0.02), int(40*0.02)))

        self.assertEqual(action_1.state, False)

        self.assertEqual(action_1.label.text, "name10")
        self.assertEqual(action_1.label.back_color, (int(10*0.2), int(12*0.2), int(40*0.2)))
        
        # Receive other value 
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 2
            }
        ]

        appl.tick()
        appl.tick()
    
        self.assertEqual(cb._EffectEnableCallback__effect_category, 20)

        self.assertEqual(appl.inputs[0].color, (20, 22, 80))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.02)
        self.assertAlmostEqual(led_driver.leds[0], (int(20*0.02), int(22*0.02), int(80*0.02)))

        self.assertEqual(action_1.state, False)

        self.assertEqual(action_1.label.text, "name20")
        self.assertAlmostEqual(action_1.label.back_color, (int(20*0.2), int(22*0.2), int(80*0.2)))

        # Receive enabled status
        period.exceed_next_time = True
        appl._Controller__midi.next_receive_messages = [
            answer_msg_param
        ]
        mapping_type_1.outputs_parse = []
        mapping_1.outputs_parse = [
            {
                "message": answer_msg_param,
                "value": 1
            }
        ]

        appl.tick()
        appl.tick()
        
        self.assertEqual(cb._EffectEnableCallback__effect_category, 20)

        self.assertEqual(action_1.state, True)

        self.assertEqual(appl.inputs[0].color, (20, 22, 80))
        self.assertAlmostEqual(appl.inputs[0].brightness, 0.3)
        self.assertAlmostEqual(led_driver.leds[0], (int(20*0.3), int(22*0.3), int(80*0.3)))

        self.assertEqual(action_1.label.text, "name20")
        self.assertEqual(action_1.label.back_color, (20, 22, 80))


###############################################################################################


    def test_action_disabled(self):
        switch_1 = MockSwitch()

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

        mapping_type_1 = MockParameterMapping(
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x10, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x10]
            # ),
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x10, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x10]
            # )
        )

        cb_enable = MockEnabledCallback(output = True)

        cb = MockEffectEnableCallback(
            mapping_state = mapping_1,
            mapping_type = mapping_type_1
        )

        action_1 = PushButtonAction({
            "mode": PushButtonAction.MOMENTARY,
            "callback": cb,
            "enableCallback": cb_enable
        })                
        
        period = MockPeriodCounter()
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

        answer_msg_type = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x07, 0x45, 0xf7)
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
        self.assertEqual(appl._Controller__midi.messages_sent[0], mapping_1.request)
        self.assertEqual(appl._Controller__midi.messages_sent[1], mapping_type_1.request)
        
        # Receive type
        appl._Controller__midi.next_receive_messages = [
            answer_msg_type
        ]
        mapping_type_1.outputs_parse = [
            {
                "message": answer_msg_type,
                "value": 1
            }
        ]

        cb_enable.output_get = False

        appl.tick()
        appl.tick()
        
        self.assertEqual(len(appl._Controller__midi.next_receive_messages), 0)

        self.assertEqual(len(appl._Controller__midi.messages_sent), 2)
        self.assertEqual(cb._EffectEnableCallback__effect_category, 10)
        
        