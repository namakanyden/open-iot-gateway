import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ThinkSenzor import ThinkSensor, ThinkSensorWithBattery

class TestThinkSensor(unittest.TestCase):
    # TEST ---- ThinkSensor ----
    def test_ThinkSensor_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "think",
            "device_id": "123fa",
            "topic": "kpi/A1/think/123fa",
            "ts": 1234567892,
            "value": 2030
        }
        
        think = None
        try:
            think = ThinkSensor(**data)
        except Exception:
            self.fail("ThinkSensor(**data) raised Exception !")
    
        self.assertNotEqual(think, None)
        self.assertEqual(think.department.value, "kpi")
        self.assertEqual(think.room, "A1")
        self.assertEqual(think.device_type, "think")
        self.assertEqual(think.device_id, "123fa")
        self.assertEqual(think.topic, "kpi/A1/think/123fa")
        self.assertEqual(think.ts, 1234567892)
        self.assertEqual(think.value, 2030.0)
        expected_result = "think,department=kpi,room=A1,device_type=think,device_id=123fa,topic=kpi/A1/think/123fa value=2030.0 1234567892"
        self.assertEqual(think.get_line_protocol(), expected_result)
            
            
    def test_ThinkSensor_missing_arguments(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "think",
            "device_id": "123fa",
            "ts": 123456789
        }
        
        with self.assertRaises(ValueError):
            ThinkSensor(**data)
            
        
    # TEST ---- ThinkSensorWithBattery ----
    def test_ThinkSensorWithBattery_correct_input_data(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "think",
            "device_id": "123fa",
            "topic": "kpi/A1/think/123fa",
            "ts": 1234567892,
            "value": 15.0,
            "battery": 90
        }
        
        thinkBattery = None
        try:
            thinkBattery = ThinkSensorWithBattery(**data)
        except Exception:
            self.fail("ThinkSensorWithBattery(**data) raised Exception !")
        
        self.assertNotEqual(thinkBattery, None)
        self.assertEqual(thinkBattery.department.value, "kpi")
        self.assertEqual(thinkBattery.room, "A1")
        self.assertEqual(thinkBattery.device_type, "think")
        self.assertEqual(thinkBattery.device_id, "123fa")
        self.assertEqual(thinkBattery.topic, "kpi/A1/think/123fa")
        self.assertEqual(thinkBattery.ts, 1234567892)
        self.assertEqual(thinkBattery.value, 15.0)
        self.assertEqual(thinkBattery.battery, 90)
        expected_result = "think,department=kpi,room=A1,device_type=think,device_id=123fa,topic=kpi/A1/think/123fa,battery=90 value=15.0 1234567892"
        self.assertEqual(thinkBattery.get_line_protocol(), expected_result)

if __name__ == '__main__':
    unittest.main()