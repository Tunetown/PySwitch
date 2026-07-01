import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "adafruit_midi": MockAdafruitMIDI(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from adafruit_midi.system_exclusive import SystemExclusive
    from adafruit_midi.control_change import ControlChange
    
    from .mocks_misc import MockMisc
    from .mocks_callback import *

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
        
        from lib.pyswitch.controller.actions.AnalogAction import AnalogAction
        from lib.pyswitch.ui.elements import DisplayLabel
        from .mocks_appl import *


##################################################################################################################################


class TestAnalogAction(unittest.TestCase):

    def test_fix_range(self):
        self._test(
            max_value = 127,
            num_steps = 128,
            data = [
                (0, 0),
                (128, 0),
                (256, 0),
                (257, 1),
                (384, 1),
                (512, 1),
                (8192, 16),
                (16384, 32),
                (32768, 64),
                (49152, 96),
                (65278, 127),
                (65280, 127),
                (65535, 127)
            ]
        )

        self._test(
            max_value = 255,
            num_steps = 128,
            data = [
                (0, 0),
                (256, 0),
                (257, 2),
                (8192, 32),
                (16384, 64),
                (32768, 128),
                (49152, 192),
                (65279, 254),
                (65280, 255),
                (65535, 255) 
            ]
        )

        self._test(
            max_value = 127, 
            num_steps = 16,
            data = [
                (0, 0),
                (2048, 0),
                (2049, 8),
                (8192, 16),
                (16384, 32),
                (63487, 120),
                (63488, 127),
                (65535, 127)
            ]
        )

        ############################################

        self._test(
            max_value = 16383, 
            num_steps = 128,
            data = [
                (0, 0),
                (128, 0),
                (256, 0),
                (257, 128),
                (384, 128),
                (512, 128),
                (8192, 2048),
                (16384, 4096),
                (32768, 8192),
                (49152, 12288),
                (65279, 16256),
                (65280, 16383),
                (65535, 16383)
            ]
        )

    def test_auto_range(self):
        self._test(
            cc_mapping = False,
            max_value = None, 
            num_steps = 128,
            data = [
                (0, 0),
                (128, 0),
                (256, 0),
                (257, 128),
                (384, 128),
                (512, 128),
                (8192, 2048),
                (16384, 4096),
                (32768, 8192),
                (49152, 12288),
                (65279, 16256),
                (65280, 16383),
                (65535, 16383)
            ]
        )

        self._test(
            cc_mapping = True,
            max_value = None,
            num_steps = 128,
            data = [
                (0, 0),
                (128, 0),
                (256, 0),
                (257, 1),
                (384, 1),
                (512, 1),
                (8192, 16),
                (16384, 32),
                (32768, 64),
                (49152, 96),
                (65278, 127),
                (65280, 127),
                (65535, 127)
            ]
        )

    def test_transfer_function(self):
        def transfer(value):
            return round(value / 1024) + 32
        
        self._test(
            max_value = 96,
            data = [
                (0, 32),
                (128, 32),
                (256, 32),
                (257, 32),
                (384, 32),
                (512, 32),
                (8192, 40),
                (16384, 48),
                (32768, 64),
                (49152, 80),
                (65279, 96),
                (65280, 96),
                (65535, 96)
            ],
            transfer_function = transfer
        )
        
    def _test(self, data, max_value, num_steps = 1, transfer_function = None, cc_mapping = False):
        if not cc_mapping:
            mapping = MockParameterMapping(
                set = SystemExclusive(
                    manufacturer_id = [0x00, 0x10, 0x20],
                    data = [0x05, 0x07, 0x09]
                )
            )
        else:
            mapping = MockParameterMapping(
                set = ControlChange(20, 1)
            )

        action = AnalogAction(
            mapping = mapping,
            max_value = max_value,
            max_frame_rate = 10,
            num_steps = num_steps,
            transfer_function = transfer_function,
            auto_calibrate = False,
            min_raw_value = 0
        )

        action.reset()

        appl = MockController()
        action.init(appl)

        self.assertEqual(action.enabled, True)
        self.assertEqual(action._AnalogAction__period.interval, 100)
        self.assertEqual(action._AnalogAction__mapping, mapping)

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        # Call without period exceeding
        action.process(1)
        self.assertEqual(appl.client.set_calls, [])

        exp_set_calls = []
        last_value = None
        for entry in data:
            check_value = entry[0]
            exp_value = entry[1]

            if last_value != exp_value:
                exp_set_calls.append({ 
                    "mapping": mapping,
                    "value": exp_value
                })

            last_value = exp_value

            period.exceed_next_time = True
            action.process(check_value)
            
            self.assertEqual(appl.client.set_calls, exp_set_calls, "Check value: " + repr(check_value)) 

            # Call without period exceeding
            action.process(1)            
            self.assertEqual(appl.client.set_calls, exp_set_calls) 

        # Finally check if any of the possible input values exceeds the range
        if max_value != None:
            appl.client.set_calls = []
            for value in range(0, 65535, 15):
                period.exceed_next_time = True
                action.process(value)
                outval = appl.client.last_sent_message["value"]

                self.assertGreaterEqual(outval, 0)
                self.assertLessEqual(outval, max_value)


    #################################################################################

        
    def test_enable_callback(self):
        mapping = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        ecb = MockEnabledCallback(output = True)

        action = AnalogAction(
            mapping = mapping,
            enable_callback = ecb
        )

        self.assertEqual(action.enabled, True)

        ecb.output = False
        self.assertEqual(action.enabled, False)

        ecb.output = True
        self.assertEqual(action.enabled, True)


    #################################################################################

        
    def test_calibration(self):
        mapping = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        action = AnalogAction(
            mapping = mapping,
            max_value = 65535,
            max_frame_rate = 10,
            num_steps = 65536,
            auto_calibrate = True,
            cal_min_window = 0.1
        )

        appl = MockController()
        action.init(appl)

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        # Window too small
        period.exceed_next_time = True
        action.process(1111)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(100)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(6553)        
        self.assertEqual(appl.client.last_sent_message, None) 

        # Push upper border
        period.exceed_next_time = True
        action.process(6653)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 65535 }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 32762 }) 

        # Push upper border
        period.exceed_next_time = True
        action.process(12000)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 65535 }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 18041 }) 

        # Push lower border
        period.exceed_next_time = True
        action.process(10)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 0 }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 18398 }) 

        # Finally check if any of the possible input values exceeds the range
        appl.client.set_calls = []
        for value in range(0, 65535, 15):
            period.exceed_next_time = True
            action.process(value)
            outval = appl.client.last_sent_message["value"]

            self.assertGreaterEqual(outval, 0)
            self.assertLessEqual(outval, 65535)


    def test_calibration_with_range(self):
        mapping = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        action = AnalogAction(
            mapping = mapping,
            max_value = 1023,
            max_frame_rate = 10,
            num_steps = 1024,
            auto_calibrate = True,
            cal_min_window = 0.1
        )

        appl = MockController()
        action.init(appl)

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        # Window too small
        period.exceed_next_time = True
        action.process(1111)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(100)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(6553)        
        self.assertEqual(appl.client.last_sent_message, None) 

        # Push upper border
        period.exceed_next_time = True
        action.process(6653)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 1023 }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": round(32762 / 64) }) 

        # Push upper border
        period.exceed_next_time = True
        action.process(12000)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 1023 }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": round(18041 / 64) }) 

        # Push lower border
        period.exceed_next_time = True
        action.process(10)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": round(0 / 64) }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": round(18398 / 64) }) 

        # Finally check if any of the possible input values exceeds the range
        appl.client.set_calls = []
        for value in range(0, 65535, 15):
            period.exceed_next_time = True
            action.process(value)
            outval = appl.client.last_sent_message["value"]

            self.assertGreaterEqual(outval, 0)
            self.assertLessEqual(outval, 1023)
    

    def test_calibration_with_range_and_function(self):
        mapping = MockParameterMapping(
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        def transfer(value):
            return round(value / 2) + 2

        action = AnalogAction(
            mapping = mapping,
            max_value = 1023,
            max_frame_rate = 10,
            num_steps = 1024,
            transfer_function = transfer,
            auto_calibrate = True,
            cal_min_window = 0.1
        )

        appl = MockController()
        action.init(appl)

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        # Window too small
        period.exceed_next_time = True
        action.process(1111)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(100)        
        self.assertEqual(appl.client.last_sent_message, None) 

        period.exceed_next_time = True
        action.process(6553)        
        self.assertEqual(appl.client.last_sent_message, None) 

        # Push upper border
        period.exceed_next_time = True
        action.process(6653)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(65535)) }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(32762)) }) 

        # Push upper border
        period.exceed_next_time = True
        action.process(12000)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(65535)) }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(18041)) }) 

        # Push lower border
        period.exceed_next_time = True
        action.process(10)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(0)) }) 

        period.exceed_next_time = True
        action.process(3376)        
        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": transfer(round(18398)) }) 

        # Finally check if any of the possible input values exceeds the range
        appl.client.set_calls = []
        for value in range(0, 65535, 15):
            period.exceed_next_time = True
            action.process(value)
            outval = appl.client.last_sent_message["value"]

            self.assertGreaterEqual(outval, 0)
            self.assertLessEqual(outval, transfer(65535))


    #####################################################################################################################


    def test_change_display(self):
        mapping = MockParameterMapping(
            name = "PQ",
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0),
                "textColor": (4, 6, 8)          
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        
        action = AnalogAction(
            mapping = mapping,
            max_value = 100,
            num_steps = 65536,
            auto_calibrate = False,
            change_display = display,
            change_timeout_millis = 123
        )

        appl = MockController()
        action.init(appl)

        display.update_label()

        self.assertEqual(display.text, "foo")

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        period.exceed_next_time = True
        action.process(1024)
        action.update()
            
        self.assertEqual(display.text, "PQ: 1%")

        period.exceed_next_time = True
        action.process(32768)
        action.update()
            
        self.assertEqual(display.text, "PQ: 50%")

        period.exceed_next_time = True
        action.process(65535)
        action.update()
            
        self.assertEqual(display.text, "PQ: 100%")

        self.assertEqual(action._AnalogAction__preview._ValuePreview__period.interval, 123)
        action._AnalogAction__preview._ValuePreview__period = MockPeriodCounter()
        preview_period = action._AnalogAction__preview._ValuePreview__period

        preview_period.exceed_next_time = True
        action.update()
        
        self.assertEqual(display.text, "foo")


    def test_change_display_convert_value(self):
        def convert_value(value):
            return f"blubb { str(value) } bla"
        
        mapping = MockParameterMapping(
            name = "PQ",
            set = SystemExclusive(
                manufacturer_id = [0x00, 0x10, 0x20],
                data = [0x05, 0x07, 0x09]
            )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0),
                "textColor": (4, 6, 8)          
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        
        action = AnalogAction(
            mapping = mapping,
            max_value = 1000,
            num_steps = 65536,
            auto_calibrate = False,
            change_display = display,
            change_timeout_millis = 123,
            convert_value = convert_value
        )

        appl = MockController()
        action.init(appl)

        display.update_label()

        self.assertEqual(display.text, "foo")

        action._AnalogAction__period = MockPeriodCounter()
        period = action._AnalogAction__period

        period.exceed_next_time = True
        action.process(1024)
        action.update()
            
        self.assertEqual(display.text, "blubb 15 bla")

        period.exceed_next_time = True
        action.process(32768)
        action.update()
            
        self.assertEqual(display.text, "blubb 500 bla")

        period.exceed_next_time = True
        action.process(65535)
        action.update()
            
        self.assertEqual(display.text, "blubb 1000 bla")

        self.assertEqual(action._AnalogAction__preview._ValuePreview__period.interval, 123)
        action._AnalogAction__preview._ValuePreview__period = MockPeriodCounter()
        preview_period = action._AnalogAction__preview._ValuePreview__period

        preview_period.exceed_next_time = True
        action.update()
        
        self.assertEqual(display.text, "foo")
