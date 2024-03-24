import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from LightSenzor import LightSensor, LightSensorWithBattery

class TestLightSensor(unittest.TestCase):
    # TEST ---- LightSensor ----
    def test_LightSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "topic": "kpi/A1/light/123fa",
            "ts": 1234567892,
            "value": 20,
            "unit": "lm"
        }
        
        light = None
        try:
            light = LightSensor(**data)
        except Exception:
            self.fail("LightSensor(**data) raised Exception !")
    
        self.assertNotEqual(light, None)
        self.assertEqual(light.department.value, "kpi")
        self.assertEqual(light.room, "A1")
        self.assertEqual(light.device_type, "light")
        self.assertEqual(light.device_id, "123fa")
        self.assertEqual(light.topic, "kpi/A1/light/123fa")
        self.assertEqual(light.ts, 1234567892)
        self.assertEqual(light.value, 20.0)
        self.assertEqual(light.unit, "lm")
        expected_result = "light,department=kpi,room=A1,device_type=light,device_id=123fa,topic=kpi/A1/light/123fa,unit=lm value=20.0 1234567892"
        self.assertEqual(light.get_line_protocol(), expected_result)
      
        
    def test_LightSensor_negative_value(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "topic": "kpi/A1/light/123fa",
            "ts": 123456789,
            "value": -15.0,
            "unit": "lm"
        }
        
        with self.assertRaises(ValueError):
            LightSensor(**data)
            
            
    def test_LightSensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "topic": "kpi/A1/light/123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "ta"
        }
        
        with self.assertRaises(ValueError):
            LightSensor(**data)
            
            
    def test_LightSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            LightSensor(**data)
            
    
    def test_LightSensor_normalize_candela(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "topic": "kpi/A1/light/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "cd"
        }
        
        light = None
        try:
            light = LightSensor(**data)
        except Exception:
            self.fail("LightSensor(**data) raised Exception !")
        
        self.assertEqual(light.normalize_value(), 0)
        light.value = 100
        self.assertEqual(light.normalize_value(), 100.0)
        light.value = -20
        self.assertEqual(light.normalize_value(), -20.0)
        
        
    # TEST ---- LightSensorWithBattery ----
    def test_LightSensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "light",
            "device_id": "123fa",
            "topic": "kpi/A1/light/123fa",
            "ts": 1234567892,
            "value": 15.0,
            "unit": "cd",
            "battery": 90
        }
        
        lightBattery = None
        try:
            lightBattery = LightSensorWithBattery(**data)
        except Exception:
            self.fail("NoiseSenzorWithBattery(**data) raised Exception !")
        
        self.assertNotEqual(lightBattery, None)
        self.assertEqual(lightBattery.department.value, "kpi")
        self.assertEqual(lightBattery.room, "A1")
        self.assertEqual(lightBattery.device_type, "light")
        self.assertEqual(lightBattery.device_id, "123fa")
        self.assertEqual(lightBattery.topic, "kpi/A1/light/123fa")
        self.assertEqual(lightBattery.ts, 1234567892)
        self.assertEqual(lightBattery.value, 15.0)
        self.assertEqual(lightBattery.unit, "cd")
        self.assertEqual(lightBattery.battery, 90)
        expected_result = "light,department=kpi,room=A1,device_type=light,device_id=123fa,topic=kpi/A1/light/123fa,battery=90,unit=lm value=15.0 1234567892"
        self.assertEqual(lightBattery.get_line_protocol(), expected_result)

if __name__ == '__main__':
    unittest.main()