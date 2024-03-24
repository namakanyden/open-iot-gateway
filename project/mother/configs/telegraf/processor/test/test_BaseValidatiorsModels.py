import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from BaseValidatiorsModels import Battery, Device, TimeStamp

class TestDevice(unittest.TestCase):
    # TEST ---- Device ----
    def test_device_normal_work_model(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa"
        }
    
        device = None
        try:
            device = Device(**data)
        except Exception:
            self.fail("Device(**data) raised Exception !")
            
        self.assertNotEqual(device, None)
        self.assertEqual(device.department.value, "kpi")
        self.assertEqual(device.room, "A1")
        self.assertEqual(device.device_type, "humidity")
        self.assertEqual(device.device_id, "123fa")
        self.assertEqual(device.topic, "kpi/A1/humidity/123fa")
        self.assertEqual(device.device_get_line_protocol(), "department=kpi,room=A1,device_type=humidity,device_id=123fa,topic=kpi/A1/humidity/123fa")
            
    def test_device_invalid_department(self):
        data = {
            "department": "ret",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa"
        }
        
        with self.assertRaises(ValueError):
            Device(**data)
            
    def test_device_get_line_protocol(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa"
        }
        
        device = Device(**data)
        
        self.assertEqual(device.device_get_line_protocol(), "department=kpi,room=A1,device_type=humidity,device_id=123fa,topic=kpi/A1/humidity/123fa")
      
        
    def test_device_no_space_as_value_invalid(self):
        with self.assertRaises(ValueError):
            Device(
                department="kpi ",
                room="A1",
                device_type="temperature",
                device_id="123fa",
                topic="kpi/A1/temperature/123fa"
            )
            
            
    def test_device_no_space_as_value_invalid_multiple_fields(self):
        with self.assertRaises(ValueError):
            Device(
                department="kpi",
                room="A1",
                device_type="temperature ",
                device_id="123fa",
                topic="kpi/A1/temperature/123fa"
            )
            
        with self.assertRaises(ValueError):
            Device(
                department="kpi",
                room="A1",
                device_type="temperature",
                device_id="123 fa",
                topic="kpi/A1/temperature/123fa"
            )
            
        with self.assertRaises(ValueError):
            Device(
                department="kpi",
                room="A1",
                device_type="tem perature",
                device_id="123fa",
                topic="kpi/A1/temperature/123 fa"
            )
            
    # TEST ---- Battery ----
    def test_battery_normal_work_model(self):
        data = {
            "battery": 89
        }
        
        battery = None
        try:
            battery = Battery(**data)
        except Exception:
            self.fail("Battery(**data) raised Exception !")
            
        self.assertNotEqual(battery, None)
        self.assertEqual(battery.battery, 89)
        self.assertEqual(battery.battery_get_line_protocol(), "battery=89")
    
        
    def test_battery_negative_value(self):
        data = {
            "battery": -15
        }
        
        with self.assertRaises(ValueError):
            Battery(**data)    
    
    
    def test_battery_get_line_protocol(self):
        data = {
            "battery": 89
        }
        
        battery = Battery(**data)
        
        self.assertEqual(battery.battery_get_line_protocol(), "battery=89")


    # TEST ---- TimeStamp ----
    def test_timestamp_normal_work_model(self):
        data = {
            "ts": 1234567892
        }
        
        timestamp = None
        try:
            timestamp = TimeStamp(**data)
        except Exception:
            self.fail("TimeStamp(**data) raised Exception !")
            
        self.assertNotEqual(timestamp, None)
        self.assertEqual(timestamp.ts, 1234567892)
        self.assertEqual(timestamp.timestamp_get_line_protocol(), "1234567892")
    
    def test_timestamp_negative_value(self):
        data = {
            "ts": -1234567892
        }
        
        with self.assertRaises(ValueError):
            TimeStamp(**data)
            
    def test_timestamp_get_line_protocol(self):
        data = {
            "ts": 1234567892
        }
        
        timestamp = TimeStamp(**data)
        
        self.assertEqual(timestamp.timestamp_get_line_protocol(), "1234567892")
    
if __name__ == '__main__':
    unittest.main()