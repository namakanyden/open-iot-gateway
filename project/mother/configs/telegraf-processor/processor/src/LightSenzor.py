from enum import Enum
from pydantic import ValidationInfo, field_validator
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Light Sensor -----------
# Light model
# Contains light value and unit
class LightUnitEnum(str, Enum):
    CANDELA = 'cd'
    LUMEN = 'lm'

class LightSensor(Device, TimeStamp):
    value: float
    unit: LightUnitEnum
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, value: str, info: ValidationInfo) -> float:
        if value < 0:
            raise ValueError("value can't be negative")
        return value
    
    def normalize_value(self) -> float:
        return self.value
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},unit=lm value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
    
# LightSensorWithBattery model
# Contains light value and unit and battery level
class LightSensorWithBattery(LightSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery},unit=lm value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
