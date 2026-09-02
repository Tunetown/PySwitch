import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "usb_midi": MockUsbMidi(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.controller.strobe import StrobeController

    from .mocks_appl import *


class TestStrobeController(unittest.TestCase):


    def test_strobe(self):
        self._test_strobe(2)
        self._test_strobe(3)
        self._test_strobe(4)
        self._test_strobe(6)
        self._test_strobe(8)
        self._test_strobe(10)


    def _test_strobe(self, num_switches):
        self._test_strobe_directions(num_switches, interval = 10)
        self._test_strobe_directions(num_switches, interval = 60)
        self._test_strobe_directions(num_switches, interval = 330)
        self._test_strobe_directions(num_switches, interval = 1, speed = 100)   # This runs the algorithm into the max. speed threshold


    def _test_strobe_directions(self, num_switches, interval, speed = 2000, num_periods = 5):
        # Upwards
        self._test_strobe_direction(
            num_switches = num_switches,
            speed = speed,
            num_periods = num_periods,
            up = True,
            interval = interval
        )

        # Downwards
        self._test_strobe_direction(
            num_switches = num_switches,
            speed = speed,
            num_periods = num_periods,
            up = False,
            interval = interval
        )


    def _test_strobe_direction(self, num_switches, speed, num_periods, up, interval):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x10, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x10]
            # )
        )

        strobe = StrobeController(
            mapping_state = mapping_1,
            mapping_deviance = mapping_2,
            speed = speed,
            width = 0.2,
            color = (100, 0, 0),
            dim_factor = 0.5,
            max_fps = 12   # Not regarded because the period counter is overridden
        )

        switch_1 = MockFootswitch(id = 1, order = 3)
        switch_2 = MockFootswitch(id = 2, order = 2)
        switch_3 = MockFootswitch(id = 3, order = 0)
        switch_4 = MockFootswitch(id = 4, order = 100)
        switch_5 = MockFootswitch(id = 5, order = 105)
        switch_6 = MockFootswitch(id = 6, order = 102)
        switch_7 = MockFootswitch(id = 7, order = 103)
        switch_8 = MockFootswitch(id = 8, order = 104)
        switch_9 = MockFootswitch(id = 9, order = 110)
        switch_10 = MockFootswitch(id = 10, order = 106)

        switches_sorted = [
            switch_3,
            switch_2,
            switch_1,
            switch_4,
            switch_6,
            switch_7,
            switch_8,
            switch_5, 
            switch_10,
            switch_9,
        ]
        
        # Reduce switch list according to the number of switches to be tested
        while len(switches_sorted) > num_switches:
            switches_sorted.pop()

        # Create list sorted by id (for passing to the mock controller)
        switches_unsorted = [s for s in switches_sorted]
        def key_id(sw):
            return sw.id
        switches_unsorted.sort(key = key_id)

        self.assertEqual(len(switches_sorted), num_switches)
        self.assertEqual(len(switches_unsorted), num_switches)

        # Create mock controller and init the Tuner display with it
        appl = MockController(
            inputs = switches_unsorted + [MockInputControllerDefinition()]
        )
        strobe.init(appl)

        self.assertEqual(strobe._StrobeController__num_switches, num_switches) #(num_switches / 2) if num_switches > 4 else num_switches)
        self.assertEqual(strobe._StrobeController__enabled, False)
        self.assertEqual(strobe._StrobeController__period.interval, int(1000 / 12 * num_switches))

        def get_maxima(count):
            return self._find_n_maxima([s.brightness for s in switches_sorted], count)

        period = MockPeriodCounter()
        strobe._StrobeController__period = period

        # Start test ################################################

        # No update (period not exceeded)
        mapping_2.value = 0
        period.interval = interval

        strobe.parameter_changed(mapping_2)

        for switch in switches_sorted:
            self.assertEqual(switch.color, (0, 0, 0))

        for switch in switches_sorted:
            self.assertEqual(switch.brightness, 0)

        # Some value (tuner not active)
        mapping_2.value = 8191 + 111

        strobe.parameter_changed(mapping_2)

        self.assertEqual(strobe._StrobeController__enabled, False)

        for switch in switches_sorted:
            self.assertEqual(switch.color, (0, 0, 0))

        for switch in switches_sorted:
            self.assertEqual(switch.brightness, 0)
            
        # Activate
        mapping_1.value = 1
        strobe.parameter_changed(mapping_1)

        self.assertEqual(strobe._StrobeController__enabled, True)
            
        # Some value (period not exceeded)
        mapping_2.value = 8191 - 117

        strobe.parameter_changed(mapping_2)

        self.assertEqual(strobe._StrobeController__enabled, True)

        for switch in switches_sorted:
            self.assertEqual(switch.color, (0, 0, 0))

        for switch in switches_sorted:
            self.assertEqual(switch.brightness, 0)
        
        # Neutral value (this gives us the starting point)
        mapping_2.value = 8191
        period.passed = 20        
        period.exceed_next_time = True
        
        strobe.parameter_changed(mapping_2)

        for switch in switches_sorted:
            self.assertEqual(switch.color, (100, 0, 0))

        # Check maxima (must be at initial position(s) here)
        num_maxima = 1 #2 if num_switches > 4 else 1
        maxima = get_maxima(num_maxima)

        for m in range(len(maxima)):
            self.assertEqual(switches_sorted[maxima[m]].brightness, 0.5)  

        # Deactivate again
        tmp_brightnesses = [s.brightness for s in switches_sorted]
        mapping_1.value = 3
        strobe.parameter_changed(mapping_1)

        # Some value (tuner not active again)
        mapping_2.value = 8191 + 113
        period.passed = 20        
        period.exceed_next_time = True
        
        strobe.parameter_changed(mapping_2)

        self.assertEqual(strobe._StrobeController__enabled, False)

        self.assertEqual([s.brightness for s in switches_sorted], tmp_brightnesses)

        # Activate again to perform the real test
        mapping_1.value = 1
        strobe.parameter_changed(mapping_1)

        # Step through the range until the period has finished
        diff = 911  # This value must be uneven to prevent equally bright switches (these are not analysed correctly by the algorithm determining the local maxima)
        last_maxima = [m for m in maxima]
        start_maxima = -1
        check_maxima_list = []

        if num_switches <= 1:
            return

        while len(check_maxima_list) <= (num_periods * num_maxima) or maxima != start_maxima:
            mapping_2.value = (8191 + diff) if up else (8191 - diff)
            period.passed = 120           

            period.exceed_next_time = True
            strobe.parameter_changed(mapping_2)

            for switch in switches_sorted:
                self.assertEqual(switch.color, (100, 0, 0))

            maxima = get_maxima(num_maxima)
            
            # Check if the maxima move into the right direction.            
            if maxima != None:
                maxima.sort()
                
                if up:
                    next_maxima = [(m + 1) if m < (num_switches - 1) else 0 for m in last_maxima]
                else:
                    next_maxima = [(m - 1) if m > 0 else (num_switches - 1) for m in last_maxima]
                next_maxima.sort()

                #print(repr(maxima) + "  " + repr(next_maxima) + " " + repr(last_maxima))

                # There are only two allowed maxima: The current or the next
                if maxima == last_maxima:
                    pass
                elif maxima == next_maxima:
                    pass
                else:
                    self.fail("Invalid maxima for " + repr(num_switches) + " switches: " + repr(maxima) + ", last: " + repr(last_maxima) + ", data: " + repr([s.brightness for s in switches_sorted]))

                if last_maxima != maxima:
                    check_maxima_list.append(maxima)

                    if start_maxima == -1:
                        start_maxima = [m for m in last_maxima]
                
                    last_maxima = [m for m in maxima]
        
        # Check if all iterations are contained
        num_values = int(num_switches / num_maxima)
        for i in range(num_values):
            exp_maxima = [i + (n * num_values) for n in range(num_maxima)]
            self.assertIn(exp_maxima, check_maxima_list)

        self.assertGreater(len(check_maxima_list), num_periods)


    ########################################################################################


    def test_no_strobe(self):
        self._test_no_strobe(0)
        self._test_no_strobe(1)


    def _test_no_strobe(self, num_switches):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x10, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x10]
            # )
        )

        strobe = StrobeController(
            mapping_state = mapping_1,
            mapping_deviance = mapping_2
        )

        switch_1 = MockFootswitch(id = 1, order = 3)
        switches = []
        if num_switches == 1:
            switches.append(switch_1)

        # Create mock controller and init the Tuner display with it
        appl = MockController(
            inputs = switches + [MockInputControllerDefinition()]
        )
        strobe.init(appl)

        self.assertEqual(strobe._StrobeController__enabled, False)

        # Activate
        mapping_1.value = 1
        strobe.parameter_changed(mapping_1)

        self.assertEqual(strobe._StrobeController__enabled, False)


    ############################################################################################


    # Returns a list containing the indices of {count} peak values of the passed data. 
    # Taken from https://stackoverflow.com/questions/3242910/algorithm-to-locate-local-maxima
    def _find_n_maxima(self, data, count):
        if len(data) == 1:
            return [0]

        low = 0
        high = max(data) - min(data)

        for iteration in range(100):
            mid = low + (high - low) / 2.0
            maxima = self._find_maxima(data, mid)

            if len(maxima) == count:
                return maxima
            
            elif len(maxima) < count: 
                # Threshold too high
                high = mid

            else: 
                # Threshold too low
                low = mid

        # Failed
        return None 


    # Internally used by _find_n_maxima()
    def _find_maxima(self, data, threshold):
        # Search for maximum
        def search(data, threshold, index, forward):
            max_index = index
            max_value = data[index]

            if forward:
                path = range(index + 1, len(data))
            else:
                path = range(index - 1, -1, -1)
            
            for i in path:
                if data[i] > max_value:
                    max_index = i
                    max_value = data[i]
                elif max_value - data[i] > threshold:
                    break

            return max_index, i
        
        # Forward pass
        forward = set()
        index = 0
        while index < len(data) - 1:
            maximum, index = search(data, threshold, index, True)
            forward.add(maximum)
            index += 1
        
        # Reverse pass
        reverse = set()
        index = len(data) - 1
        while index > 0:
            maximum, index = search(data, threshold, index, False)
            reverse.add(maximum)
            index -= 1

        return sorted(forward & reverse)