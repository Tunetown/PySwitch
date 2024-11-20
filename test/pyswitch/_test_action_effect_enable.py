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
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from.mocks_ui import *
    from .mocks_callback import *

    from adafruit_midi.system_exclusive import SystemExclusive

    from lib.pyswitch.controller.actions.actions import EffectEnableAction
    


class TestActionEffectEnable(unittest.TestCase):

    def test_requests(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": MockSlotInfoProvider(),
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()

        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_param = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_type = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 0
                }
            ]

        def eval2():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)

            self.assertEqual(mapping_type_1.value, 0)
            self.assertEqual(action_1._effect_category, 0)
            self.assertEqual(action_1.state, False)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.02)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))

            return True

        # Receive status
        def prep3():
            appl._midi.next_receive_messages = [
                answer_msg_param
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_param,
                    "value": 1
                }
            ]

        def eval3():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            
            self.assertEqual(mapping_1.value, 1)
            self.assertEqual(action_1.state, True)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))
            
            return True
        
        # Receive other value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 1
                }
            ]
            
        def eval4():
            self.assertEqual(mapping_type_1.value, 1)
            self.assertEqual(action_1._effect_category, 10)
            self.assertEqual(action_1.state, True)

            self.assertEqual(appl.switches[0].color, (10, 12, 40))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (int(10*0.3), int(12*0.3), int(40*0.3)))

            return True
        
        # Receive non-assigned type again
        def prep5():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 0
                }
            ]

        def eval5():
            self.assertEqual(mapping_type_1.value, 0)
            self.assertEqual(action_1.state, False)
            return False
        

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2,

                next = SceneStep(
                    num_pass_ticks = 5,
                    prepare = prep3,
                    evaluate = eval3,

                    next = SceneStep(
                        num_pass_ticks = 5,
                        prepare = prep4,
                        evaluate = eval4,

                        next = SceneStep(
                            num_pass_ticks = 5,
                            prepare = prep5,
                            evaluate = eval5
                        )
                    )
                )
            )
        )

        # Run process
        appl.process()


###########################################################################################################


    def test_requests_non_receivable_fxtype_mapping(self):
        appl = MockController(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": MockSwitch()
                    },
                    "actions": [
                        EffectEnableAction({
                            "mode": PushButtonAction.MOMENTARY,
                            "mapping": ClientParameterMapping(),
                            "mappingType": ClientParameterMapping(),
                            "categories": MockCategoryProvider(),
                            "slotInfo": MockSlotInfoProvider()
                        })                        
                    ]
                }
            ]
        )

        with self.assertRaises(Exception):   
            appl.update()


###########################################################################################################


    def test_requests_with_label(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": MockSlotInfoProvider(),
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        action_1.label = MockDisplayLabel()

        answer_msg_param = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_type = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 0
                }
            ]

        def eval2():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)

            self.assertEqual(mapping_type_1.value, 0)
            self.assertEqual(action_1._effect_category, 0)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.02)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))
            
            return True

        # Receive status
        def prep3():
            appl._midi.next_receive_messages = [
                answer_msg_param
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_param,
                    "value": 1
                }
            ]

        def eval3():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            
            self.assertEqual(mapping_1.value, 1)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))

            return True
        
        # Receive other value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 1
                }
            ]

        def eval4():
            self.assertEqual(mapping_type_1.value, 1)
            self.assertEqual(action_1._effect_category, 10)

            self.assertEqual(appl.switches[0].color, (10, 12, 40))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (int(10*0.3), int(12*0.3), int(40*0.3)))

            self.assertEqual(action_1.label.text, "name10")
            self.assertEqual(action_1.label.back_color, (10, 12, 40))

            return True
        
        # Receive other value 
        def prep5():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 2
                }
            ]

        def eval5():
            self.assertEqual(action_1._effect_category, 20)

            self.assertEqual(appl.switches[0].color, (20, 22, 80))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (int(20*0.3), int(22*0.3), int(80*0.3)))

            self.assertEqual(action_1.label.text, "name20")
            self.assertEqual(action_1.label.back_color, (20, 22, 80))

            return True

        # Receive disabled status
        def prep6():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_param
            ]
            mapping_type_1.outputs_parse = []
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_param,
                    "value": 0
                }
            ]

        def eval6():
            self.assertEqual(action_1._effect_category, 20)

            self.assertEqual(appl.switches[0].color, (20, 22, 80))
            self.assertEqual(appl.switches[0].brightness, 0.02)
            self.assertEqual(led_driver.leds[0], (int(20*0.02), int(22*0.02), int(80*0.02)))

            self.assertEqual(action_1.label.text, "name20")
            self.assertEqual(action_1.label.back_color, (int(20*0.2), int(22*0.2), int(80*0.2)))
            
            return False
        
        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2,

                next = SceneStep(
                    num_pass_ticks = 5,
                    prepare = prep3,
                    evaluate = eval3,

                    next = SceneStep(
                        num_pass_ticks = 5,
                        prepare = prep4,
                        evaluate = eval4,

                        next = SceneStep(
                            num_pass_ticks = 5,
                            prepare = prep5,
                            evaluate = eval5,

                            next = SceneStep(
                                num_pass_ticks = 5,
                                prepare = prep6,
                                evaluate = eval6
                            )
                        )
                    )
                )
            )
        )

        # Run process
        appl.process()


###########################################################################################################


    def test_show_effect_slot_names(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()
        slotinfo = MockSlotInfoProvider()
        slotinfo.output = "foo"

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": slotinfo,
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period,
            config = {
                "showEffectSlotNames": True
            }
        )

        action_1.label = MockDisplayLabel()

        answer_msg_param = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_type = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 0
                }
            ]

        def eval2():
            return True

        # Receive status
        def prep3():
            appl._midi.next_receive_messages = [
                answer_msg_param
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_param,
                    "value": 1
                }
            ]

        def eval3():
            return True
        
        # Receive other value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 1
                }
            ]

        def eval4():
            self.assertEqual(action_1.label.text, "foo: name10")
            return False
        

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2,

                next = SceneStep(
                    num_pass_ticks = 5,
                    prepare = prep3,
                    evaluate = eval3,

                    next = SceneStep(
                        num_pass_ticks = 5,
                        prepare = prep4,
                        evaluate = eval4
                    )
                )
            )
        )

        # Run process
        appl.process()


###############################################################################################


    def test_action_disabled(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()
        cb = MockCallback(output = True)

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": MockSlotInfoProvider(),
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_type = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 1
                }
            ]

            cb.output_get = False

        def eval2():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertEqual(action_1._effect_category, 10)
            
            return False

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2
            )
        )

        # Run process
        appl.process()


###############################################################################################


    def test_request_timeout(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": MockSlotInfoProvider(),
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        appl.client._cleanup_terminated_period = MockPeriodCounter()
        wa = []

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            period.exceed_next_time = True
            appl.client._cleanup_terminated_period.exceed_next_time = True

            appl.client._requests[0].lifetime = MockPeriodCounter()
            appl.client._requests[0].lifetime.exceed_next_time = True
            wa.append(appl.client._requests[0])

        def eval2():
            self.assertEqual(len(appl.client._requests), 0)
            self.assertEqual(wa[0].finished, True)

            return False

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2
            )
        )

        # Run process
        appl.process()


##############################################################################################


    def test_reset(self):
        switch_1 = MockSwitch()

        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        mapping_type_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x10]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x10]
            )
        )

        cp = MockCategoryProvider()

        action_1 = EffectEnableAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingType": mapping_type_1,
            "categories": cp,
            "slotInfo": MockSlotInfoProvider(),
            "color": (10, 50, 100)
        })
        
        period = MockPeriodCounter()
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": [0]
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_param = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_type = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)            
            self.assertEqual(appl._midi.messages_sent[0], mapping_type_1.request)
            
            return True

        # Receive type
        def prep2():
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 0
                }
            ]

        def eval2():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)

            self.assertEqual(mapping_type_1.value, 0)
            self.assertEqual(action_1._effect_category, 0)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.02)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))

            return True

        # Receive status
        def prep3():
            appl._midi.next_receive_messages = [
                answer_msg_param
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_param,
                    "value": 1
                }
            ]

        def eval3():
            self.assertEqual(len(appl._midi.next_receive_messages), 0)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            
            self.assertEqual(mapping_1.value, 1)

            self.assertEqual(action_1.state, True)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))
            
            return True
        
        # Receive other value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_type
            ]
            mapping_type_1.outputs_parse = [
                {
                    "message": answer_msg_type,
                    "value": 1
                }
            ]

        def eval4():
            self.assertEqual(mapping_type_1.value, 1)
            self.assertEqual(action_1._effect_category, 10)
            self.assertEqual(action_1.state, True)

            self.assertEqual(appl.switches[0].color, (10, 12, 40))
            self.assertEqual(appl.switches[0].brightness, 0.3)
            self.assertEqual(led_driver.leds[0], (int(10*0.3), int(12*0.3), int(40*0.3)))

            return True
        
        # Receive non-assigned type again
        def prep5():
            action_1.reset()

            self.assertEqual(action_1._effect_category, 0)
            self.assertEqual(action_1.state, False)

            self.assertEqual(appl.switches[0].color, (0, 0, 0))
            self.assertEqual(appl.switches[0].brightness, 0.02)
            self.assertEqual(led_driver.leds[0], (0, 0, 0))

        def eval5():
            return False
        

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                prepare = prep2,
                evaluate = eval2,

                next = SceneStep(
                    num_pass_ticks = 5,
                    prepare = prep3,
                    evaluate = eval3,

                    next = SceneStep(
                        num_pass_ticks = 5,
                        prepare = prep4,
                        evaluate = eval4,

                        next = SceneStep(
                            num_pass_ticks = 5,
                            prepare = prep5,
                            evaluate = eval5
                        )
                    )
                )
            )
        )

        # Run process
        appl.process()