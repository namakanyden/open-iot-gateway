import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from NoiseSenzor import NoiseSensor, NoiseSenzorWithBattery

class TestNoiseSensor(unittest.TestCase):
    # TEST ---- NoiseSensor ----
    def test_NoiseSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 1234567892,
            "value": 20,
            "unit": "dB"
        }
        
        noise = None
        try:
            noise = NoiseSensor(**data)
        except Exception:
            self.fail("NoiseSensor(**data) raised Exception !")
    
        self.assertNotEqual(noise, None)
        self.assertEqual(noise.department.value, "kpi")
        self.assertEqual(noise.room, "A1")
        self.assertEqual(noise.device_type, "noise")
        self.assertEqual(noise.device_id, "123fa")
        self.assertEqual(noise.topic, "kpi/A1/noise/123fa")
        self.assertEqual(noise.ts, 1234567892)
        self.assertEqual(noise.value, 20.0)
        self.assertEqual(noise.unit, "dB")
        expected_result = "noise,department=kpi,room=A1,device_type=noise,device_id=123fa,topic=kpi/A1/noise/123fa,unit=dB value=20.0 1234567892"
        self.assertEqual(noise.get_line_protocol(), expected_result)
      
        
    def test_NoiseSensor_negative_value(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 123456789,
            "value": -15.0,
            "unit": "db"
        }
        
        with self.assertRaises(ValueError):
            NoiseSensor(**data)
            
            
    def test_NoiseSensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 123456789,
            "value": 15.0,
            "unit": "g/m"
        }
        
        with self.assertRaises(ValueError):
            NoiseSensor(**data)
            
            
    def test_NoiseSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            NoiseSensor(**data)
            
    
    def test_PressureSensor_normalize_bel(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "B"
        }
        
        pressure = None
        try:
            pressure = NoiseSensor(**data)
        except Exception:
            self.fail("NoiseSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 0)
        pressure.value = 100
        self.assertEqual(pressure.normalize_value(), 1000.0)
        pressure.value = -20
        self.assertEqual(pressure.normalize_value(), -200.0)
        
        
    def test_PressureSensor_normalize_neper(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "Np"
        }
        
        pressure = None
        try:
            pressure = NoiseSensor(**data)
        except Exception:
            self.fail("NoiseSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 0)
        pressure.value = 100
        self.assertEqual(pressure.normalize_value(), 868.5889638065037)
        pressure.value = -10
        self.assertEqual(pressure.normalize_value(), -86.85889638065036)
            
        
    # TEST ---- NoiseSensorWithBattery ----
    def test_NoiseSensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "noise",
            "device_id": "123fa",
            "topic": "kpi/A1/noise/123fa",
            "ts": 1234567892,
            "value": 15.0,
            "unit": "Np",
            "battery": 90
        }
        
        noiseBattery = None
        try:
            noiseBattery = NoiseSenzorWithBattery(**data)
        except Exception:
            self.fail("NoiseSenzorWithBattery(**data) raised Exception !")
        
        self.assertNotEqual(noiseBattery, None)
        self.assertEqual(noiseBattery.department.value, "kpi")
        self.assertEqual(noiseBattery.room, "A1")
        self.assertEqual(noiseBattery.device_type, "noise")
        self.assertEqual(noiseBattery.device_id, "123fa")
        self.assertEqual(noiseBattery.topic, "kpi/A1/noise/123fa")
        self.assertEqual(noiseBattery.ts, 1234567892)
        self.assertEqual(noiseBattery.value, 15.0)
        self.assertEqual(noiseBattery.unit, "Np")
        self.assertEqual(noiseBattery.battery, 90)
        expected_result = "noise,department=kpi,room=A1,device_type=noise,device_id=123fa,topic=kpi/A1/noise/123fa,battery=90,unit=dB value=130.28834457097554 1234567892"
        self.assertEqual(noiseBattery.get_line_protocol(), expected_result)

if __name__ == '__main__':
    unittest.main()