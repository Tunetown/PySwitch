import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):   
    from .mocks_misc import MockMisc
    from .mocks_callback import *

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
        
        from lib.pyswitch.controller.actions.EncoderAction import EncoderAction

        from lib.pyswitch.clients.local.actions.encoder_button import ENCODER_BUTTON
        from lib.pyswitch.ui.elements import DisplayLabel

        from .mocks_appl import *


##################################################################################################################################


class TestEncoderAction(unittest.TestCase):

    def test_fix_range(self):
        self._test(
            cc_mapping = False,
            max_value = 1023,
            step_width = 16,
            start_pos = 4, 
            start_value = 100, 
            data = [
                (5, 116),
                (6, 132),
                (7, 148),
                (54, 900),
                (61, 1012),
                (62, 1023),
                (65, 1023),
                (10000, 1023),
                (9999, 1007),
                (9989, 847),
                (9937, 15),
                (9936, 0),
                (9910, 0),
                (1, 0),
                (2, 16),
                (3, 32),
                (5, 64)
            ]
        )

        self._test(
            cc_mapping = True,
            max_value = 127,
            step_width = 1,
            start_pos = 4, 
            start_value = 100, 
            data = [
                (5, 101),
                (6, 102),
                (7, 103),
                (24, 120),
                (31, 127),
                (61, 127),
                (62, 127),
                (65, 127),
                (10000, 127),
                (9999, 126),
                (9989, 116),
                (9919, 46),
                (9900, 27),
                (9873, 0),
                (9872, 0),
                (1, 0),
                (2, 1),
                (20, 19)
            ]
        )

    def test_custom_range(self):
        self._test(
            cc_mapping = True,
            max_value = 63,
            step_width = 0.5,
            start_pos = 1,
            start_value = 1,
            data = [
                (2, 2),
                (3, 2),
                (4, 3),
                (5, 3),
                (6, 4),
                (7, 4),
                (8, 5),
                (9, 5),
                (10, 6),
                (11, 6),
                (12, 7),
                (13, 7),
                (14, 8),
                (28, 15),
                (64, 33),
                (120, 61),
                (121, 61),
                (122, 62),
                (123, 62),
                (124, 63),
                (125, 63),
                (126, 63),
                (127, 63),
                (200, 63),
                (199, 62),
                (198, 62),
                (197, 61),
                (0, 0),
                (-1, 0),
                (-2, 0),
                (-30, 0),
                (-29, 1),
                (-28, 1),
                (-27, 2)
            ]
        )


    def test_auto_range(self):
        self._test(
            cc_mapping = False,
            max_value = None,
            step_width = None,
            start_pos = 0, 
            start_value = 0, 
            data = [
                (2, 160),
                (4, 320),
                (6, 480),
                (204, 16320),
                (206, 16383),
                (208, 16383),
                (20000, 16383),
                (19998, 16223),
                (19978, 14623),
                (19832, 2943),
                (19796, 63),
                (19794, 0),
                (2, 0),
                (4, 160),
                (6, 320),
                (10, 640)
            ]
        )

        self._test(
            cc_mapping = True,
            max_value = None,
            step_width = None,
            start_pos = 4, 
            start_value = 100, 
            data = [
                (5, 101),
                (6, 102),
                (7, 103),
                (24, 120),
                (31, 127),
                (61, 127),
                (62, 127),
                (65, 127),
                (10000, 127),
                (9999, 126),
                (9989, 116),
                (9919, 46),
                (9900, 27),
                (9873, 0),
                (9872, 0),
                (1, 0),
                (2, 1),
                (20, 19)
            ]
        )

    def _test(self, max_value, step_width, start_pos, start_value, data, cc_mapping = False):
        self._do_test(
            max_value = max_value,
            step_width = step_width,
            start_pos = start_pos,
            start_value = start_value,
            data = data,
            cc_mapping = cc_mapping,
            mapping_with_response = True
        )

        self._do_test(
            max_value = max_value,
            step_width = step_width,
            start_pos = start_pos,
            start_value = start_value,
            data = data,
            cc_mapping = cc_mapping,
            mapping_with_response = False
        )

    def _do_test(self, max_value, step_width, start_pos, start_value, data, cc_mapping, mapping_with_response):
        if not cc_mapping:
            mapping = MockParameterMapping(
                set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x10, 0x20],
                #     data = [0x05, 0x07, 0x09]
                # ),
                response = None if not mapping_with_response else (0xf0, 0x00, 0x11, 0x20, 0x05, 0x07, 0x03, 0xf7)
                # SystemExclusive(
                #     manufacturer_id = [0x00, 0x11, 0x20],
                #     data = [0x05, 0x07, 0x03]
                # )
            )
        else:
            mapping = MockParameterMapping(
                set = (176, 20, 1), #ControlChange(20, 1),
                response = None if not mapping_with_response else (176, 20, 1) #ControlChange(20, 1)
            )

        action = EncoderAction(
            mapping = mapping,
            max_value = max_value,
            step_width = step_width
        )

        appl = MockController()
        action.init(appl)

        action.reset()

        self.assertEqual(action.enabled, True)
        self.assertEqual(action._mapping, mapping)
        
        if mapping_with_response or start_value != 0:
            mapping.value = start_value

        # Start position (only catches the current mapping value and exits)
        action.process(start_pos)
        self.assertEqual(appl.client.last_sent_message, None) 

        for entry in data:
            position = entry[0]
            exp_value = entry[1]

            action.process(position)
            self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": exp_value }, repr(entry))
            
            # Simulate that the mapping value had been changed by an incoming message
            if mapping_with_response:
                mapping.value = exp_value


    def test_none_value(self):
        mapping = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        action = EncoderAction(
            mapping = mapping
        )

        appl = MockController()
        action.init(appl)

        self.assertEqual(action.enabled, True)
        self.assertEqual(action._mapping, mapping)
        
        mapping.value = None

        # Start position (only catches the current mapping value and exits)
        action.process(98)
        self.assertEqual(appl.client.last_sent_message, None) 


    #################################################################################


    def test_update(self):
        mapping = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # ),
            request = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x17, 0x09, 0xf7),
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x17, 0x09]
            # ),
            response = (0xf0, 0x00, 0x10, 0x21, 0x05, 0x07, 0x10, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x21],
            #     data = [0x05, 0x07, 0x10]
            # )
        )

        action = EncoderAction(
            mapping = mapping
        )

        appl = MockController()
        action.init(appl)

        action.update()
        self.assertEqual(appl.client.request_calls, [{ "mapping": mapping, "listener": None }]) 

        action.update()
        self.assertEqual(appl.client.request_calls, [{ "mapping": mapping, "listener": None }, { "mapping": mapping, "listener": None }]) 
        

    #################################################################################

        
    def test_enable_callback(self):
        mapping = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        ecb = MockEnabledCallback(output = True)

        action = EncoderAction(
            mapping = mapping,
            enable_callback = ecb
        )

        self.assertEqual(action.enabled, True)

        ecb.output = False
        self.assertEqual(action.enabled, False)

        ecb.output = True
        self.assertEqual(action.enabled, True)


    #################################################################################


    def test_with_display(self):
        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0)            
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )

        mapping = MockParameterMapping(
            name = "Some",
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        action = EncoderAction(
            mapping = mapping,
            preview_display = display,
            preview_timeout_millis = 123,
            max_value = 1000,
            step_width = 1
        )

        appl = MockController()
        action.init(appl)

        display.update_label()

        action.process(0)

        self.assertEqual(display.text, "foo")

        action.process(10)

        self.assertEqual(display.text, "Some: 1%")
        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(mapping.value, 10)

        action.process(200)

        self.assertEqual(display.text, "Some: 20%")
        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(mapping.value, 200)
            
        action.process(500)

        self.assertEqual(display.text, "Some: 50%")
        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(mapping.value, 500)

        action.process(1000)

        self.assertEqual(display.text, "Some: 100%")
        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(mapping.value, 1000)

        self.assertEqual(action._EncoderAction__preview._ValuePreview__period.interval, 123)
        action._EncoderAction__preview._ValuePreview__period = MockPeriodCounter()
        period = action._EncoderAction__preview._ValuePreview__period

        period.exceed_next_time = True
        action.process(1000)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(len(appl.client.set_calls), 4)

        action.process(500)

        self.assertEqual(display.text, "Some: 50%")
        self.assertEqual(len(appl.client.set_calls), 5)

        period.exceed_next_time = True
        action.process(500)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(len(appl.client.set_calls), 5)


    def test_convert_value(self):
        def convert_value(value):
            return f"{ value * 2} units"
        
        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0)            
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )

        mapping = MockParameterMapping(
            name = "Some",
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        action = EncoderAction(
            mapping = mapping,
            preview_display = display,
            preview_timeout_millis = 123,
            max_value = 1000,
            step_width = 1,
            convert_value = convert_value
        )

        appl = MockController()
        action.init(appl)

        display.update_label()

        action.process(0)

        self.assertEqual(display.text, "foo")

        action.process(10)

        self.assertEqual(display.text, "20 units")
        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(mapping.value, 10)

        action.process(200)

        self.assertEqual(display.text, "400 units")
        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(mapping.value, 200)
            
        action.process(500)

        self.assertEqual(display.text, "1000 units")
        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(mapping.value, 500)

        action.process(1000)

        self.assertEqual(display.text, "2000 units")
        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(mapping.value, 1000)

        self.assertEqual(action._EncoderAction__preview._ValuePreview__period.interval, 123)
        action._EncoderAction__preview._ValuePreview__period = MockPeriodCounter()
        period = action._EncoderAction__preview._ValuePreview__period

        period.exceed_next_time = True
        action.process(1000)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(len(appl.client.set_calls), 4)

        action.process(500)

        self.assertEqual(display.text, "1000 units")
        self.assertEqual(len(appl.client.set_calls), 5)

        period.exceed_next_time = True
        action.process(500)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(len(appl.client.set_calls), 5)
        

    def test_preselect(self):
        mapping = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        accept = ENCODER_BUTTON()

        action = EncoderAction(
            mapping = mapping,
            accept_action = accept,
            max_value = 1000,
            step_width = 1
        )

        appl = MockController()        
        action.init(appl)

        switch = MockFootswitch()
        accept.init(appl, switch)

        action.process(0)
        action.accept() # Shall do nothing
        self.assertEqual(appl.client.set_calls, [])

        action.process(1)
        self.assertEqual(appl.client.set_calls, [])

        action.process(20)
        self.assertEqual(appl.client.set_calls, [])
            
        action.process(20)
        self.assertEqual(appl.client.set_calls, [])

        accept.push()
        accept.release()

        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 19 }])


    def test_preselect_with_display(self):
        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0),
                "textColor": (4, 6, 8)          
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )

        mapping = MockParameterMapping(
            name = "Some",
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = EncoderAction(
            mapping = mapping,
            accept_action = accept,
            cancel_action = cancel,
            preview_display = display,
            preview_timeout_millis = 123,
            preview_blink_period_millis = 345,
            preview_blink_color = (2, 3, 4),
            max_value = 1000,
            step_width = 1
        )

        appl = MockController()
        action.init(appl)

        switch = MockFootswitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        display.update_label()

        action.process(0)

        self.assertEqual(display.text, "foo")
        self.assertEqual(display.text_color, (4, 6, 8))

        action.process(10)
        action.update()

        self.assertEqual(display.text, "Some: 1%")
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(display.text_color, (2, 3, 4))

        action.process(200)
        action.update()

        self.assertEqual(display.text, "Some: 20%")
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(display.text_color, (2, 3, 4))

        self.assertEqual(action._EncoderAction__preview._ValuePreview__blink_period.interval, 345)
        action._EncoderAction__preview._ValuePreview__blink_period = MockPeriodCounter()
        period_blink = action._EncoderAction__preview._ValuePreview__blink_period

        period_blink.exceed_next_time = True
        action.process(200)
        action.update()

        self.assertEqual(display.text, "Some: 20%")
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(display.text_color, (4, 6, 8))

        action.process(500)
        action.update()

        self.assertEqual(display.text, "Some: 50%")
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(display.text_color, (4, 6, 8))

        period_blink.exceed_next_time = True
        action.process(1000)
        action.update()

        self.assertEqual(display.text, "Some: 100%")
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(display.text_color, (2, 3, 4))

        accept.push()
        accept.release()

        self.assertEqual(display.text, "Some: 100%")
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 999 }])
        self.assertEqual(display.text_color, (4, 6, 8))

        self.assertEqual(action._EncoderAction__preview._ValuePreview__period.interval, 123)
        action._EncoderAction__preview._ValuePreview__period = MockPeriodCounter()
        period = action._EncoderAction__preview._ValuePreview__period

        period.exceed_next_time = True
        period_blink.exceed_next_time = True
        action.process(1000)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 999 }])
        self.assertEqual(display.text_color, (4, 6, 8))

        action.process(500)
        action.update()

        self.assertEqual(display.text, "Some: 50%")
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 999 }])
        self.assertEqual(display.text_color, (4, 6, 8))

        cancel.push()
        cancel.release()

        period.exceed_next_time = True
        action.process(500)
        action.update()
        
        self.assertEqual(display.text, "foo")
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 999 }])
        self.assertEqual(display.text_color, (4, 6, 8))

        accept.push()
        accept.release()

        self.assertEqual(display.text, "foo")
        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 999 }])
        self.assertEqual(display.text_color, (4, 6, 8))


    def test_preselect_with_reset_mapping(self):
        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0),
                "textColor": (4, 6, 8)          
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )

        mapping = MockParameterMapping(
            name = "Some",
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        mapping_reset = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x05, 0x07, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x05, 0x07, 0x09]
            # )
        )

        accept = ENCODER_BUTTON()

        action = EncoderAction(
            mapping = mapping,
            accept_action = accept,
            preview_display = display,
            preview_reset_mapping = mapping_reset,
            max_value = 1000,
            step_width = 1
        )

        appl = MockController()
        action.init(appl)

        switch = MockFootswitch()
        accept.init(appl, switch)

        action._EncoderAction__preview._ValuePreview__period = MockPeriodCounter()
        period = action._EncoderAction__preview._ValuePreview__period

        mapping_reset.value = 1

        display.update_label()
        action.process(0)

        self.assertEqual(display.text, "foo")

        action.process(10)
        action.update()

        self.assertEqual(display.text, "Some: 1%")
        self.assertEqual(appl.client.set_calls, [])

        mapping_reset.value = 2
        period.exceed_next_time = True
        action.process(10)

        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(appl.client.set_calls, [])

        accept.push()
        accept.release()

        action.process(10)
        action.update()

        self.assertEqual(display.text, "foo")
        self.assertEqual(appl.client.set_calls, [])
