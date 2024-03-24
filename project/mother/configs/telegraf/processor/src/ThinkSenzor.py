from enum import Enum
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Think Sensor -----------
# Temperature model
# Contains only value

class ThinkSensor(Device, TimeStamp):
    value: float
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()} value={self.value} {super().timestamp_get_line_protocol()}"
    
# ThinkSensorWithBattery model
# Contains value and battery level
class ThinkSensorWithBattery(ThinkSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery} value={self.value} {super().timestamp_get_line_protocol()}"
