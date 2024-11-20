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
    "adafruit_midi": MockAdafruitMIDI(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "gc": MockGC()
}):
    #from lib.pyswitch.controller.Controller import Controller
    from .mocks_appl import *
    from .mocks_ui import *
    from .mocks_callback import *

    from adafruit_midi.system_exclusive import SystemExclusive

    from lib.pyswitch.controller.actions.actions import ParameterAction
    from lib.pyswitch.misc import compare_midi_messages, DEFAULT_LABEL_COLOR



class TestActionParameter(unittest.TestCase):
 
    def test_set_parameter(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "valueEnable": 10,
            "valueDisable": 3,
            "color": (200, 100, 0),
            "ledBrightness": {
                "on": 0.5,
                "off": 0.1
            }
        })
        
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
            ]
        )

        # Build scene:
        # Step 1: Enable
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], 10)

            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.5)
            self.assertEqual(led_driver.leds[0], (100, 50, 0))
            
            return True        
        
        # Step 2: Disable
        def prep2():
            switch_1.shall_be_pushed = False

        def eval2():
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[1], 3)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.1)
            self.assertEqual(led_driver.leds[0], (20, 10, 0))
                        
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


    def test_set_parameter_value_disable_auto(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x21],
                data = [0x01, 0x02, 0x03, 0x05]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "valueEnable": 11,
            "valueDisable": "auto",
            "comparisonMode": ParameterAction.GREATER_EQUAL
        })
        
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

        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_2 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Check if nothing crashes if set is called before a value came in
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], 11)

            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set))
            
            self.assertEqual(action_1.state, True)

            return True

        
        def prep2():
            switch_1.shall_be_pushed = False
            self.assertEqual(action_1._value_disable, "auto")

        def eval2():
            # Nothing must have been sent because we still have no disabling value
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(len(appl._midi.messages_sent), 1)
            
            self.assertEqual(action_1.state, False)

            return True
        
        # Receive a value
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1,
                answer_msg_2
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_2,
                    "value": 6
                }
            ]

            return True

        def eval3():            
            self.assertEqual(action_1.state, False)
            self.assertEqual(action_1._value_disable, 6)

            return True     
        
        # Enable
        def prep4():
            switch_1.shall_be_pushed = True

        def eval4():
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[1], 11)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set))
            
            self.assertEqual(action_1.state, True)

            return True        
        
        # Receive a value when state is True (must not override the remembered value)
        def prep5():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 100
                }
            ]
            
            return True

        def eval5():            
            self.assertEqual(action_1.state, True)
            self.assertEqual(action_1._value_disable, 6)

            return True  
                
        # Disable again
        def prep6():
            switch_1.shall_be_pushed = False

        def eval6():
            self.assertEqual(len(mapping_1.set_value_calls), 3)
            self.assertEqual(mapping_1.set_value_calls[2], 6)

            self.assertEqual(len(appl._midi.messages_sent), 3)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[2], mapping_1.set))
                        
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


###############################################################################################


    def test_set_parameter_values_disable_auto(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()
        
        mapping_1 = MockParameterMapping(
            set = [
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x01, 0x02, 0x03, 0x04]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x01, 0x02, 0x03, 0x05]
                )
            ],
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x11, 0x21],
                data = [0x01, 0x02, 0x03, 0x05]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,            
            "valueEnable": [11, 12],
            "valueDisable": [4, "auto"],
            "comparisonMode": ParameterAction.GREATER_EQUAL
        })
        
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

        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        # Build scene:
        # Check if nothing crashes if set is called before a value came in
        def prep1():
            switch_1.shall_be_pushed = True

            self.assertEqual(action_1._update_value_disabled, [False, True])

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 0)            
                        
            self.assertEqual(len(appl._midi.messages_sent), 0)
            
            self.assertEqual(action_1.state, True)

            return True

        
        def prep2():
            switch_1.shall_be_pushed = False
            self.assertEqual(action_1._value_disable, [4, "auto"])

        def eval2():
            self.assertEqual(len(mapping_1.set_value_calls), 0)

            self.assertEqual(len(appl._midi.messages_sent), 0)
            
            self.assertEqual(action_1.state, False)

            return True
        
        # Receive a value
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 7
                }
            ]
            
            return True

        def eval3():            
            self.assertEqual(action_1.state, False)
            self.assertEqual(action_1._value_disable, [4, 7])

            return True     
        
        # Enable
        def prep4():
            switch_1.shall_be_pushed = True

        def eval4():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], [11, 12])

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set[0]))
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set[1]))
            
            self.assertEqual(action_1.state, True)

            return True        
        
        # Receive a value when state is True (must not override the remembered value)
        def prep5():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 100
                }
            ]
            
            return True

        def eval5():            
            self.assertEqual(action_1.state, True)
            self.assertEqual(action_1._value_disable, [4, 7])

            return True     
        
        # Disable again
        def prep6():
            switch_1.shall_be_pushed = False

        def eval6():
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[1], [4, 7])

            self.assertEqual(len(appl._midi.messages_sent), 4)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[2], mapping_1.set[0]))
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[3], mapping_1.set[1]))
                        
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


###############################################################################################
 
 
    def test_set_parameter_disable_mapping(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            )
        )

        mapping_disable_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x33, 0x04]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingDisable": mapping_disable_1,
            "valueEnable": 10,
            "valueDisable": 3,
            "color": (200, 100, 0),
            "ledBrightness": {
                "on": 0.5,
                "off": 0.1
            }
        })
        
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
            ]
        )

        # Build scene:
        # Step 1: Enable
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], 10)

            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.5)
            self.assertEqual(led_driver.leds[0], (100, 50, 0))
            
            return True        
        
        # Step 2: Disable
        def prep2():
            switch_1.shall_be_pushed = False

        def eval2():
            self.assertEqual(len(mapping_disable_1.set_value_calls), 1)
            self.assertEqual(mapping_disable_1.set_value_calls[0], 3)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_disable_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.1)
            self.assertEqual(led_driver.leds[0], (20, 10, 0))
                        
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


    def test_set_parameter_mappings_lists(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = [
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x01, 0x02, 0x03, 0x04]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x22],
                    data = [0x01, 0x02, 0x03, 0x05]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x22],
                    data = [0x01, 0x02, 0x03, 0x88]
                )
            ]
        )

        mapping_disable_1 = MockParameterMapping(
            set = [
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x01, 0x02, 0x39, 0x04]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x30],
                    data = [0x01, 0x02, 0x39, 0x07]
                )
            ]
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "mappingDisable": mapping_disable_1,
            "valueEnable": [1, 2, 3],
            "valueDisable": [0, -1]
        })
        
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ]
        )

        # Build scene:
        # Step 1: Enable
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], [1, 2, 3])

            self.assertEqual(len(appl._midi.messages_sent), 3)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set[0]))
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set[1]))
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[2], mapping_1.set[2]))

            return True        
        
        # Step 2: Disable
        def prep2():
            switch_1.shall_be_pushed = False

        def eval2():
            self.assertEqual(len(mapping_disable_1.set_value_calls), 1)
            self.assertEqual(mapping_disable_1.set_value_calls[0], [0, -1])

            self.assertEqual(len(appl._midi.messages_sent), 5)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[3], mapping_disable_1.set[0]))
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[4], mapping_disable_1.set[1]))

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


    def test_set_parameter_with_label(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "valueEnable": 10,
            "valueDisable": 3,
            "color": (200, 100, 0),
            "ledBrightness": {
                "on": 0.5,
                "off": 0.1
            },
            "displayDimFactor": {
                "on": 0.5,
                "off": 0.2
            },

            "text": "foo",
            "textDisabled": "bar"
        })
        
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
            ]
        )

        action_1.label = MockDisplayLabel()

        # Build scene:
        # Step 1: Enable
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], 10)

            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.5)
            self.assertEqual(led_driver.leds[0], (100, 50, 0))

            self.assertEqual(action_1.label.text, "foo")
            self.assertEqual(action_1.label.back_color, (100, 50, 0))
            
            return True        
        
        # Step 2: Disable
        def prep2():
            switch_1.shall_be_pushed = False

        def eval2():
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[1], 3)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set))

            self.assertEqual(appl.switches[0].color, (200, 100, 0))
            self.assertEqual(appl.switches[0].brightness, 0.1)
            self.assertEqual(led_driver.leds[0], (20, 10, 0))

            self.assertEqual(action_1.label.text, "bar")
            self.assertEqual(action_1.label.back_color, (40, 20, 0))
                        
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


    def test_set_parameter_with_label_no_text(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            )
        )

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "valueEnable": 10,
            "valueDisable": 3,
            "color": ((200, 100, 0), (10, 20, 30)),
            "ledBrightness": {
                "on": 0.5,
                "off": 0.1
            }
        })
        
        led_driver = MockNeoPixelDriver()

        appl = MockController(
            led_driver = led_driver,
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": (0, 1)
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ]
        )

        action_1.label = MockDisplayLabel()

        # Build scene:
        # Step 1: Enable
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            self.assertEqual(len(mapping_1.set_value_calls), 1)
            self.assertEqual(mapping_1.set_value_calls[0], 10)

            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[0], mapping_1.set))

            self.assertEqual(appl.switches[0].colors, [(200, 100, 0), (10, 20, 30)])
            self.assertEqual(appl.switches[0].brightnesses, [0.5, 0.5])
            self.assertEqual(led_driver.leds[0], (100, 50, 0))
            self.assertEqual(led_driver.leds[1], (5, 10, 15))

            self.assertEqual(action_1.label.text, "")
            self.assertEqual(action_1.label.back_color, [(200, 100, 0), (10, 20, 30)])
            
            return True        
        
        # Step 2: Disable
        def prep2():
            switch_1.shall_be_pushed = False

        def eval2():
            self.assertEqual(len(mapping_1.set_value_calls), 2)
            self.assertEqual(mapping_1.set_value_calls[1], 3)

            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertTrue(compare_midi_messages(appl._midi.messages_sent[1], mapping_1.set))

            self.assertEqual(appl.switches[0].colors, [(200, 100, 0), (10, 20, 30)])
            self.assertEqual(appl.switches[0].brightnesses, [0.1, 0.1])
            self.assertEqual(led_driver.leds[0], (20, 10, 0))
            self.assertEqual(led_driver.leds[1], (1, 2, 3))

            self.assertEqual(action_1.label.text, "")
            self.assertEqual(action_1.label.back_color, [(40, 20, 0), (2, 4, 6)])
                        
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


    def test_request(self):
        self._test_request(ParameterAction.GREATER, 1, 0, 0, 0, False)
        self._test_request(ParameterAction.GREATER, 1, 0, 1, 0, False)
        self._test_request(ParameterAction.GREATER, 1, 0, 2, 0)
        self._test_request(ParameterAction.GREATER, 1, 0, 16383, 0)

        self._test_request(ParameterAction.GREATER_EQUAL, 1, 0, 0, 0, False)
        self._test_request(ParameterAction.GREATER_EQUAL, 1, 0, 1, 0)
        self._test_request(ParameterAction.GREATER_EQUAL, 1, 0, 2, 0)
        self._test_request(ParameterAction.GREATER_EQUAL, 1, 0, 16383, 0)

        self._test_request(ParameterAction.EQUAL, 1, 0, 0, 0, False)
        self._test_request(ParameterAction.EQUAL, 1, 0, 1, 0)
        self._test_request(ParameterAction.EQUAL, 1, 0, 2, 0, False)

        self._test_request(ParameterAction.LESS_EQUAL, 1, 2, 0, 2)
        self._test_request(ParameterAction.LESS_EQUAL, 1, 2, 1, 2)
        self._test_request(ParameterAction.LESS_EQUAL, 1, 2, 2, 2, False)
        self._test_request(ParameterAction.LESS_EQUAL, 1, 2, 3, 2, False)

        self._test_request(ParameterAction.LESS, 1, 2, 0, 2)
        self._test_request(ParameterAction.LESS, 1, 2, 1, 2, False)
        self._test_request(ParameterAction.LESS, 1, 2, 2, 2, False)
        self._test_request(ParameterAction.LESS, 1, 2, 3, 2, False)

        self._test_request(ParameterAction.NO_STATE_CHANGE, 1, 2, 0, 2, False)
        self._test_request(ParameterAction.NO_STATE_CHANGE, 1, 2, 1, 2, False)
        self._test_request(ParameterAction.NO_STATE_CHANGE, 1, 2, 2, 2, False)
        self._test_request(ParameterAction.NO_STATE_CHANGE, 1, 2, 3, 2, False)

        with self.assertRaises(Exception):
            self._test_request("invalid", 0, 1, 0, 1)


    def _test_request(self, mode, value_on, value_off, test_value_on, test_value_off, exp_state_on = True, exp_state_off = False):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        action_1 = ParameterAction({
            "mapping": mapping_1,
            "comparisonMode": mode,
            "valueEnable": value_on + 4,
            "valueDisable": value_off,
            "referenceValue": value_on
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_2 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertEqual(appl._midi.messages_sent[0], mapping_1.request)
            return True

        # Step without update
        def eval2():
            self.assertEqual(len(appl._midi.messages_sent), 1)
            return True

        # Receive value 
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1,
                answer_msg_2
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": test_value_on
                }
            ]

        def eval3():
            self.assertEqual(mapping_1.value, test_value_on)
            self.assertEqual(action_1.state, exp_state_on)

            return True
        
        # Receive value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": test_value_off
                }
            ]

        def eval4():
            self.assertEqual(mapping_1.value, test_value_off)
            self.assertEqual(action_1.state, exp_state_off)

            return False

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
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


    def test_request_mappings_lists(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            request = [
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x05, 0x27, 0x09]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x21],
                    data = [0x05, 0x27, 0x0a]
                )
            ],
            response = [
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x00, 0x30, 0x19]
                ),
                SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x21],
                    data = [0x00, 0x30, 0x1d]
                )
            ]
        )

        action_1 = ParameterAction({
            "mapping": mapping_1,
            "valueEnable": [1, 2, 3],
            "valueDisable": [0, -1, -2]
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_2 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 2)
            self.assertEqual(appl._midi.messages_sent[0], mapping_1.request[0])
            self.assertEqual(appl._midi.messages_sent[1], mapping_1.request[1])
            return True

        # Step without update
        def eval2():
            self.assertEqual(len(appl._midi.messages_sent), 2)
            return True

        # Receive value 
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1,
                answer_msg_2
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 2
                }
            ]

        def eval3():
            self.assertEqual(mapping_1.value, 2)

            return True
        
        # Receive value 
        def prep4():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 66
                }
            ]

        def eval4():
            self.assertEqual(mapping_1.value, 66)

            return False

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
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


    def test_request_callback(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x03, 0x04]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x01, 0x02, 0x07, 0x09]
            )
        )

        that = self

        class MockCallback2(MockCallback):
            def __init__(self, mappings = None, output = None):
                super().__init__(mappings = mappings, output = output)

                self.exp_value = None
                self.label_color = None
                self.label_text = None
                self.pixel_color = None
                self.pixel_brightness = None

            def get(self, data):
                ret = super().get(data)

                action = data[0]
                mapping = data[1]

                that.assertEqual(action, action_1)
                that.assertEqual(mapping, mapping_1)

                if mapping.value != None and self.exp_value != None:
                    that.assertEqual(mapping.value, self.exp_value)

                if ret:                    
                    action.label.text = self.label_text
                    action.label.back_color = self.label_color

                    action.switch_color = self.pixel_color
                    action.switch_brightness = self.pixel_brightness

                return ret

        cb = MockCallback2(mappings = [mapping_1])

        action_1 = ParameterAction({
            "mode": PushButtonAction.MOMENTARY,
            "mapping": mapping_1,
            "updateDisplays": cb,
            "color": (200, 200, 200),
            "text": "foo",
            "ledBrightness": {
                "on": 1,
                "off": 0.5
            },
            "displayDimFactor": {
                "on": 1,
                "off": 0.5
            }
        })

        led_driver = MockNeoPixelDriver()
        period = MockPeriodCounter()

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
        
        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        answer_msg_2 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x07, 0x45]
        )

        # Build scene:
        # Check cb is not called on set
        def prep1():
            switch_1.shall_be_pushed = True

        def eval1():
            cb.get_calls = []
            return True        
        
        # Receive value: Default behaviour
        def prep2():
            switch_1.shall_be_pushed = False

            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1,
                answer_msg_2
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 1
                }
            ]

            cb.output_get = False
            cb.exp_value = 1

        def eval2():
            self.assertIn((action_1, mapping_1), cb.get_calls)
            self.assertEqual(mapping_1.value, 1)

            self.assertEqual(action_1.label.back_color, (200, 200, 200))
            self.assertEqual(action_1.label.text, "foo")

            self.assertEqual(action_1.switch.color, (200, 200, 200))
            self.assertEqual(action_1.switch.brightness, 1)

            return True
        
        # Receive value: Callback does all things
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1,
                answer_msg_2
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 22
                }
            ]

            cb.output_get = True
            cb.label_color = (244, 233, 211)
            cb.label_text = "bar"
            cb.pixel_color = (22, 33, 44)
            cb.pixel_brightness = 0.4
            cb.exp_value = 22

        def eval3():
            self.assertEqual(mapping_1.value, 22)

            self.assertEqual(action_1.label.back_color, (244, 233, 211))
            self.assertEqual(action_1.label.text, "bar")

            self.assertEqual(action_1.switch.color, (22, 33, 44))
            self.assertEqual(action_1.switch.brightness, 0.4)

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
                    evaluate = eval3
                )
            )
        )

        # Run process
        appl.process()
        
        
###############################################################################################


    def test_request_timeout(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        action_1 = ParameterAction({
            "mapping": mapping_1
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1
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
            self.assertEqual(appl._midi.messages_sent[0], mapping_1.request)

            return True

        def prep2():
            period.exceed_next_time = True
            appl.client._cleanup_terminated_period.exceed_next_time = True

            appl.client._requests[0].lifetime = MockPeriodCounter()
            appl.client._requests[0].lifetime.exceed_next_time = True
            wa.append(appl.client._requests[0])

        # Step without update
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
        

###############################################################################################


    def test_force_update(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping()

        action_1 = ParameterAction({
            "mapping": mapping_1,
            "color": (200, 100, 0)
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
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

        period.exceed_next_time = True
        switch_1.shall_be_pushed = True

        appl.next_step = SceneStep(
            num_pass_ticks = 5
        )

        # Run process
        appl.process()

        self.assertEqual(action_1.label.back_color, (200, 100, 0))
        self.assertEqual(appl.switches[0].color, (200, 100, 0))

        # Update displays after force_update
        action_1.label.back_color = (2, 2, 2)
        appl.switches[0].color = (2, 2, 2)

        action_1.force_update()

        action_1.update_displays()
            
        self.assertEqual(action_1.label.back_color, (200, 100, 0))
        self.assertEqual(appl.switches[0].color, (200, 100, 0))

        ## Do not update when disabled
        #action_1.enabled = False

        #action_1.label.back_color = (2, 2, 2)
        #appl.switches[0].color = (2, 2, 2)

        #action_1.force_update()

        #action_1.update_displays()
            
        #self.assertEqual(action_1.label.back_color, (2, 2, 2))
        #self.assertEqual(appl.switches[0].color, (2, 2, 2))


###############################################################################################


    def test_reset_displays(self):
        switch_1 = MockSwitch()        
        mapping_1 = MockParameterMapping()

        action_1 = ParameterAction({
            "mapping": mapping_1,
            "color": (200, 100, 0)
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
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

        period.exceed_next_time = True
        switch_1.shall_be_pushed = True

        appl.next_step = SceneStep(
            num_pass_ticks = 5
        )

        # Run process
        appl.process()

        self.assertEqual(action_1.label.back_color, (200, 100, 0))
        self.assertEqual(appl.switches[0].color, (200, 100, 0))

        # Reset displays
        action_1.reset_display()
            
        self.assertEqual(action_1.label.back_color, DEFAULT_LABEL_COLOR)
        self.assertEqual(appl.switches[0].color, (0, 0, 0))
        self.assertEqual(appl.switches[0].brightness, 0)

        # Reset displays without label
        action_1.label = None
        appl.switches[0].color = (8, 8, 9)
        appl.switches[0].brightness = 0.3

        action_1.reset_display()
            
        self.assertEqual(appl.switches[0].color, (0, 0, 0))
        self.assertEqual(appl.switches[0].brightness, 0)


###############################################################################################


    def test_action_disabled(self):
        switch_1 = MockSwitch()
        
        mapping_1 = MockParameterMapping(
            request = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            ),
            response = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x00, 0x00, 0x09]
            )
        )

        cb = MockCallback(output = True)

        action_1 = ParameterAction({
            "mapping": mapping_1,
            "enableCallback": cb
        })
        
        period = MockPeriodCounter()

        appl = MockController(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            switches = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period
        )

        answer_msg_1 = SystemExclusive(
            manufacturer_id = [0x00, 0x10, 0x20],
            data = [0x00, 0x00, 0x09, 0x44]
        )

        # Build scene:
        # Send update request
        def prep1():
            period.exceed_next_time = True

        def eval1():
            self.assertEqual(len(appl._midi.messages_sent), 1)
            self.assertEqual(appl._midi.messages_sent[0], mapping_1.request)
            return True

        # Step without update
        def eval2():
            self.assertEqual(len(appl._midi.messages_sent), 1)
            return True

        # Receive value 
        def prep3():
            period.exceed_next_time = True
            appl._midi.next_receive_messages = [
                answer_msg_1
            ]
            mapping_1.outputs_parse = [
                {
                    "message": answer_msg_1,
                    "value": 1
                }
            ]
            cb.output_get = False

        def eval3():
            self.assertEqual(mapping_1.value, 1)
            
            self.assertEqual(action_1.state, True)

            return False
        

        # Build scenes hierarchy
        appl.next_step = SceneStep(
            num_pass_ticks = 5,
            prepare = prep1,
            evaluate = eval1,

            next = SceneStep(
                num_pass_ticks = 5,
                evaluate = eval2,

                next = SceneStep(
                    num_pass_ticks = 5,
                    prepare = prep3,
                    evaluate = eval3
                )
            )
        )

        # Run process
        appl.process()