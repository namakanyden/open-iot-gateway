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
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 1234567892,
            "value": 20,
            "unit": "%"
        }
        
        humidity = None
        try:
            humidity = HumiditySensor(**data)
        except Exception:
            self.fail("HumiditySensor(**data) raised Exception !")
    
        self.assertNotEqual(humidity, None)
        self.assertEqual(humidity.department.value, "kpi")
        self.assertEqual(humidity.room, "A1")
        self.assertEqual(humidity.device_type, "humidity")
        self.assertEqual(humidity.device_id, "123fa")
        self.assertEqual(humidity.topic, "kpi/A1/humidity/123fa")
        self.assertEqual(humidity.ts, 1234567892)
        self.assertEqual(humidity.value, 20.0)
        self.assertEqual(humidity.unit, "%")
        expected_result = "humidity,department=kpi,room=A1,device_type=humidity,device_id=123fa,topic=kpi/A1/humidity/123fa,unit=% value=20.0 1234567892"
        self.assertEqual(humidity.get_line_protocol(), expected_result)
      
        
    def test_HumiditySensor_negative_value(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 123456789,
            "value": -15.0,
            "unit": "%"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
            
    def test_HumiditySensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m"
        }
        
        with self.assertRaises(ValueError):
            HumiditySensor(**data)
            
            
    def test_HumiditySensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
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
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 1234567892,
            "value": 15.0,
            "unit": "%",
            "battery": 90
        }
        
        humidityBattery = None
        try:
            humidityBattery = HumiditySensorWithBattery(**data)
        except Exception:
            self.fail("HumiditySensorWithBattery(**data) raised Exception !")
        
        self.assertNotEqual(humidityBattery, None)
        self.assertEqual(humidityBattery.department.value, "kpi")
        self.assertEqual(humidityBattery.room, "A1")
        self.assertEqual(humidityBattery.device_type, "humidity")
        self.assertEqual(humidityBattery.device_id, "123fa")
        self.assertEqual(humidityBattery.topic, "kpi/A1/humidity/123fa")
        self.assertEqual(humidityBattery.ts, 1234567892)
        self.assertEqual(humidityBattery.value, 15.0)
        self.assertEqual(humidityBattery.unit, "%")
        self.assertEqual(humidityBattery.battery, 90)
        expected_result = "humidity,department=kpi,room=A1,device_type=humidity,device_id=123fa,topic=kpi/A1/humidity/123fa,battery=90,unit=% value=15.0 1234567892"
        self.assertEqual(humidityBattery.get_line_protocol(), expected_result)

if __name__ == '__main__':
    unittest.main()