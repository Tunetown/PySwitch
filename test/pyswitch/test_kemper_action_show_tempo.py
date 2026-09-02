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
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.tempo import *
    from lib.pyswitch.clients.kemper.mappings.tempo import *
    from lib.pyswitch.clients.kemper.mappings.tempo_bpm import *
    

class TestKemperActionDefinitions(unittest.TestCase):

    def test_led_blink(self):
        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "displayio": MockDisplayIO(),
            "adafruit_display_text": MockAdafruitDisplayText(),
            "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
            "gc": MockGC()
        }):
            action = SHOW_TEMPO(
                color = (4, 6, 8), 
                led_brightness = 0.5,
                id = 67, 
                use_leds = True
            )

            mapping_tempo = MAPPING_TEMPO_DISPLAY()
            mapping_tuner = KemperMappings.TUNER_MODE_STATE()

            cb = action.callback
            self.assertEqual(cb._KemperShowTempoCallback__tempo_mapping, mapping_tempo)
            self.assertEqual(cb._KemperShowTempoCallback__tuner_mapping, mapping_tuner)

            self.assertEqual(action.id, 67)
            self.assertEqual(action.uses_switch_leds, True)

            appl = MockController()
            switch = MockFootswitch(actions = [action])
            action.init(appl, switch)

            action.push()  # Must not throw
            action.release()  # Must not throw

            mapping_tuner.value = 3 # Off

            mapping_tempo.value = 0
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0)

            mapping_tempo.value = 1
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0.5)

            mapping_tempo.value = 0
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0)

            mapping_tempo.value = 1
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0.5)

            # Must be off when tuner is engaged
            switch.color = (8, 9, 9)
            switch.brightness = 0.77
            
            mapping_tuner.value = 1 # On

            mapping_tempo.value = 1
            cb.update_displays()

            self.assertEqual(switch.color, (8, 9, 9))
            self.assertEqual(switch.brightness, 0.77)

            mapping_tempo.value = 0
            cb.update_displays()

            self.assertEqual(switch.color, (8, 9, 9))
            self.assertEqual(switch.brightness, 0.77)

            mapping_tempo.value = 1
            cb.update_displays()

            self.assertEqual(switch.color, (8, 9, 9))
            self.assertEqual(switch.brightness, 0.77)

            # Disable tuner again
            mapping_tuner.value = 3 # Off

            mapping_tempo.value = 0
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0)

            mapping_tempo.value = 1
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0.5)

    def test_display_with_ecb(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "displayio": MockDisplayIO(),
            "adafruit_display_text": MockAdafruitDisplayText(),
            "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
            "gc": MockGC()
        }):
            action = SHOW_TEMPO(
                display = display, 
                color = (4, 6, 8), 
                text = "{bpm} bpm",
                led_brightness = 0.5,
                use_leds = True,
                enable_callback = ecb
            )

            mapping_tempo = MAPPING_TEMPO_DISPLAY()
            mapping_tuner = KemperMappings.TUNER_MODE_STATE()
            mapping_bpm = MAPPING_TEMPO_BPM()

            cb = action.callback
            self.assertEqual(cb._KemperShowTempoCallback__tempo_mapping, mapping_tempo)
            self.assertEqual(cb._KemperShowTempoCallback__tuner_mapping, mapping_tuner)
            self.assertEqual(cb._KemperShowTempoCallback__bpm_mapping, mapping_bpm)

            appl = MockController()
            switch = MockFootswitch(actions = [action])
            action.init(appl, switch)

            mapping_tuner.value = 3 # Off

            mapping_tempo.value = 0
            mapping_bpm.value = 20 * 64
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0)
            self.assertEqual(display.text, "20 bpm")
            self.assertEqual(display.back_color, (4, 6, 8))

            mapping_tempo.value = 1
            mapping_bpm.value = 110 * 64
            cb.update_displays()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0.5)
            self.assertEqual(display.text, "110 bpm")
            self.assertEqual(display.back_color, (4, 6, 8))

            # Cover all flows
            cb.update_displays()
            cb.update()

            self.assertEqual(switch.color, (4, 6, 8))
            self.assertEqual(switch.brightness, 0.5)
            self.assertEqual(display.text, "110 bpm")
            self.assertEqual(display.back_color, (4, 6, 8))


    def test_change_display(self):
        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "displayio": MockDisplayIO(),
            "adafruit_display_text": MockAdafruitDisplayText(),
            "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
            "gc": MockGC()
        }):
            display = DisplayLabel(
                layout = {
                    "font": "foo",
                    "backColor": (0, 0, 0)                    
                },
                callback = MockDisplayLabelCallback(label_text = "foo")
            )

            action = SHOW_TEMPO(
                change_display = display, 
                change_timeout_millis = 123
            )

            mapping_tempo = MAPPING_TEMPO_DISPLAY()
            mapping_tuner = KemperMappings.TUNER_MODE_STATE()
            mapping_bpm = MAPPING_TEMPO_BPM()

            cb = action.callback
            self.assertEqual(cb._KemperShowTempoCallback__tempo_mapping, mapping_tempo)
            self.assertEqual(cb._KemperShowTempoCallback__tuner_mapping, mapping_tuner)
            self.assertEqual(cb._KemperShowTempoCallback__bpm_mapping, mapping_bpm)

            appl = MockController()
            switch = MockFootswitch(actions = [action])
            action.init(appl, switch)

            display.update_label()
            self.assertEqual(display.text, "foo")

            mapping_tuner.value = 3 # Off
            mapping_tempo.value = 0

            mapping_bpm.value = 20 * 64 - 1
            cb.update_displays()

            mapping_bpm.value = 20 * 64
            cb.update_displays()            

            self.assertEqual(display.text, "20 bpm")
            
            mapping_bpm.value = 110 * 64
            cb.update_displays()

            self.assertEqual(display.text, "110 bpm")

            self.assertEqual(cb._KemperShowTempoCallback__preview._ValuePreview__period.interval, 123)
            cb._KemperShowTempoCallback__preview._ValuePreview__period = MockPeriodCounter()
            period = cb._KemperShowTempoCallback__preview._ValuePreview__period

            period.exceed_next_time = True
            cb.update()

            self.assertEqual(display.text, "foo")
