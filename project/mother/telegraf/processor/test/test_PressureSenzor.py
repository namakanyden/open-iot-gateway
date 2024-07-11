import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from PressureSenzor import PressureSensor, PressureSensorWithBattery

class TestPressureSensor(unittest.TestCase):
    # TEST ---- PressureSensor ----
    def test_PressureSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "topic": "kpi/A1/pressure/123fa",
            "ts": 1234567892,
            "value": 2.3,
            "unit": "Pa"
        }
        
        pressure = None
        try:
            pressure = PressureSensor(**data)
        except Exception:
            self.fail("HumiditySensor(**data) raised Exception !")
        
        self.assertNotEqual(pressure, None)
        self.assertEqual(pressure.department.value, "kpi")
        self.assertEqual(pressure.room, "A1")
        self.assertEqual(pressure.device_type, "pressure")
        self.assertEqual(pressure.device_id, "123fa")
        self.assertEqual(pressure.topic, "kpi/A1/pressure/123fa")
        self.assertEqual(pressure.ts, 1234567892)
        self.assertEqual(pressure.value, 2.3)
        self.assertEqual(pressure.unit, "Pa")
        expected_result = "pressure,department=kpi,room=A1,device_type=pressure,device_id=123fa,topic=kpi/A1/pressure/123fa,unit=Pa value=2.3 1234567892"
        self.assertEqual(pressure.get_line_protocol(), expected_result)
        
            
    def test_PressureSensor_invalid_unit(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "ts": 1234567892,
            "value": 15.0,
            "unit": "g/m"
        }
        
        with self.assertRaises(ValueError):
            PressureSensor(**data)
        
            
    def test_PressureSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            PressureSensor(**data)
            
            
    def test_PressureSensor_normalize_Bar(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "topic": "kpi/A1/pressure/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "bar"
        }
        
        pressure = None
        try:
            pressure = PressureSensor(**data)
        except Exception:
            self.fail("PressureSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 0)
        pressure.value = 15
        self.assertEqual(pressure.normalize_value(), 1500000)
        pressure.value = -13
        self.assertEqual(pressure.normalize_value(), -1300000)
        
        
    def test_PressureSensor_normalize_psi(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "ppressure",
            "device_id": "123fa",
            "topic": "kpi/A1/pressure/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "psi"
        }
        
        pressure = None
        try:
            pressure = PressureSensor(**data)
        except Exception:
            self.fail("PressureSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 0)
        pressure.value = 100
        self.assertEqual(pressure.normalize_value(), 689476.0)
        pressure.value = -20
        self.assertEqual(pressure.normalize_value(), -137895.2)
        
        
    def test_PressureSensor_normalize_atm(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "topic": "kpi/A1/pressure/123fa",
            "ts": 1234567892,
            "value": 0,
            "unit": "atm"
        }
        
        pressure = None
        try:
            pressure = PressureSensor(**data)
        except Exception:
            self.fail("PressureSensor(**data) raised Exception !")
        
        self.assertEqual(pressure.normalize_value(), 0)
        pressure.value = 100
        self.assertEqual(pressure.normalize_value(), 10132500.0)
        pressure.value = -10
        self.assertEqual(pressure.normalize_value(), -1013250.0)
        
        
    # TEST ---- PressureSensorWithBattery ----
    def test_PressureSensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "pressure",
            "device_id": "123fa",
            "topic": "kpi/A1/pressure/123fa",
            "ts": 1234567892,
            "value": 150,
            "unit": "Pa",
            "battery": 90
        }
        
        pressureBattery = None
        try:
            pressureBattery = PressureSensorWithBattery(**data)
        except Exception:
            self.fail("PressureSensorWithBattery(**data) raised Exception !")
    
        
        expected_result = "pressure,department=kpi,room=A1,device_type=pressure,device_id=123fa,topic=kpi/A1/pressure/123fa,battery=90,unit=Pa value=150.0 1234567892"
        self.assertEqual(pressureBattery.get_line_protocol(), expected_result)
        

if __name__ == '__main__':
    unittest.main()