import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from DoorWindowSensor import DoorWindowSensor, DoorWindowSensorWithBattery

class TestOpenCloseSensor(unittest.TestCase):
    # TEST ---- PressureSensor ----
    def test_OpenCloseSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "window",
            "device_id": "123fa",
            "topic": "kpi/A1/window/123fa",
            "ts": 1234567892,
            "value": "open",
            "type": "window"
        }
        
        window = None
        try:
            window = DoorWindowSensor(**data)
        except Exception:
            self.fail("DoorWindowSensor(**data) raised Exception !")
        
        self.assertNotEqual(window, None)
        self.assertEqual(window.department.value, "kpi")
        self.assertEqual(window.room, "A1")
        self.assertEqual(window.device_type, "window")
        self.assertEqual(window.device_id, "123fa")
        self.assertEqual(window.topic, "kpi/A1/window/123fa")
        self.assertEqual(window.ts, 1234567892)
        self.assertEqual(window.value, "open")
        self.assertEqual(window.type, "window")
        expected_result = "window,department=kpi,room=A1,device_type=window,device_id=123fa,topic=kpi/A1/window/123fa,type=window value=1 1234567892"
        self.assertEqual(window.get_line_protocol(), expected_result)

            
    def test_PressureSensor_invalid_type(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "window",
            "device_id": "123fa",
            "ts": 1234567892,
            "value": "close",
            "type": "gate"
        }
        
        with self.assertRaises(ValueError):
            DoorWindowSensor(**data)
        
            
    def test_PressureSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "door",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            DoorWindowSensor(**data)
            
            
    def test_PressureSensor_normalize_value(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "door",
            "device_id": "123fa",
            "topic": "kpi/A1/door/123fa",
            "ts": 1234567892,
            "value": "open",
            "type": "door"
        }
        
        pressure = None
        try:
            pressure = DoorWindowSensor(**data)
        except Exception:
            self.fail("DoorWindowSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 1)
        pressure.value = "close"
        self.assertEqual(pressure.normalize_value(), 0)
        
        
    # TEST ---- DoorWindowSensorWithBattery ----
    def test_DoorWindowWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "window",
            "device_id": "123fa",
            "topic": "kpi/A1/window/123fa",
            "ts": 1234567892,
            "value": "close",
            "type": "window",
            "battery": 90
        }
        
        windowBattery = None
        try:
            windowBattery = DoorWindowSensorWithBattery(**data)
        except Exception:
            self.fail("DoorWindowSensorWithBattery(**data) raised Exception !")
    
        
        expected_result = "window,department=kpi,room=A1,device_type=window,device_id=123fa,topic=kpi/A1/window/123fa,battery=90,type=window value=0 1234567892"
        self.assertEqual(windowBattery.get_line_protocol(), expected_result)
        

if __name__ == '__main__':
    unittest.main()