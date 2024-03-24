import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from TemperatureSenzor import TemperatureSensor, TemperatureSensorWithBattery

class TestTemperatureSensor(unittest.TestCase):
    # TEST ---- TemperatureSensor ----
    def test_TemperatureSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 21.5,
            "unit": "C"
        }
        
        temperature = None
        try:
            temperature = TemperatureSensor(**data)
        except Exception:
            self.fail("HumiditySensor(**data) raised Exception !")
        
        self.assertNotEqual(temperature, None)
        self.assertEqual(temperature.department.value, "kpi")
        self.assertEqual(temperature.room, "A1")
        self.assertEqual(temperature.device_type, "temperature")
        self.assertEqual(temperature.device_id, "123fa")
        self.assertEqual(temperature.topic, "kpi/A1/temperature/123fa")
        self.assertEqual(temperature.ts, 1234567892)
        self.assertEqual(temperature.value, 21.5)
        self.assertEqual(temperature.unit, "C")
        expected_result = "temperature,department=kpi,room=A1,device_type=temperature,device_id=123fa,topic=kpi/A1/temperature/123fa,unit=C value=21.5 1234567892"
        self.assertEqual(temperature.get_line_protocol(), expected_result)
        
            
    def test_TemperatureSensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "ts": 1234567892,
            "value": 15.0,
            "unit": "g/m"
        }
        
        with self.assertRaises(ValueError):
            TemperatureSensor(**data)
        
            
    def test_TemperatureSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            TemperatureSensor(**data)
            
            
    def test_TemperatureSensor_normalize_Fahrenheit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "F"
        }
        
        temperature = None
        try:
            temperature = TemperatureSensor(**data)
        except Exception:
            self.fail("TemperatureSensor(**data) raised Exception !")
        
        self.assertEqual(temperature.normalize_value(), -17.77777777777778)
        temperature.value = 150
        self.assertEqual(temperature.normalize_value(), 65.55555555555556)
        temperature.value = -13
        self.assertEqual(temperature.normalize_value(), -25.0)
        
        
    def test_TemperatureSensor_normalize_kelvins(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "K"
        }
        
        temperature = None
        try:
            temperature = TemperatureSensor(**data)
        except Exception:
            self.fail("TemperatureSensor(**data) raised Exception !")
        
        self.assertEqual(temperature.normalize_value(), -273.15)
        temperature.value = 289
        self.assertEqual(temperature.normalize_value(), 15.850000000000023)
        temperature.value = 100
        self.assertEqual(temperature.normalize_value(), -173.14999999999998)
        
        
    # TEST ---- TemperatureSensorWithBattery ----
    def test_TemperatureSensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 150,
            "unit": "F",
            "battery": 90
        }
        
        temperatureBattery = None
        try:
            temperatureBattery = TemperatureSensorWithBattery(**data)
        except Exception:
            self.fail("TemperatureSensorWithBattery(**data) raised Exception !")
    
        
        expected_result = "temperature,department=kpi,room=A1,device_type=temperature,device_id=123fa,topic=kpi/A1/temperature/123fa,battery=90,unit=C value=65.55555555555556 1234567892"
        self.assertEqual(temperatureBattery.get_line_protocol(), expected_result)
        

if __name__ == '__main__':
    unittest.main()