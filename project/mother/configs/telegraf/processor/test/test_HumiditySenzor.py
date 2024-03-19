import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from HumiditySenzor import HumiditySensor, HumiditySensorWithBattery

class TestHumiditySensor(unittest.TestCase):
    # TEST ---- HumiditySensor ----
    def test_HumiditySensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m³"
        }
        
        senzor = HumiditySensor(**data)
        
        expected_result = "Humidity,department=kpi,room=A1,device_type=Humidity,device_id=123fa,unit=% value=245.41884816753927 123456789"
        self.assertEqual(senzor.get_line_protocol(), expected_result)
        
    def test_HumiditySensor_negative_value(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": -15.0,
            "unit": "g/m³"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
    def test_HumiditySensor_negative_timestamp(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": -123456789,
            "value": 15.0,
            "unit": "g/m³"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
    def test_HumiditySensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
    def test_HumiditySensor_invalid_department(self):
        data = {
            "department": "kpi ",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m³"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
    def test_HumiditySensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
        
    # TEST ---- HumiditySensorWithBattery ----
    def test_HumiditySensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m³",
            "battery": 90
        }
        
        senzor = HumiditySensorWithBattery(**data)
        
        expected_result = "Humidity,department=kpi,room=A1,device_type=Humidity,device_id=123fa,battery=90,unit=% value=245.41884816753927 123456789"
        self.assertEqual(senzor.get_line_protocol(), expected_result)
        
    def test_HumiditySensorWithBattery_negative_battery(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "Humidity",
            "device_id": "123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m³",
            "battery": -90
        }
        
        with self.assertRaises(ValueError):
            HumiditySensorWithBattery(**data)

if __name__ == '__main__':
    unittest.main()