from enum import Enum
from pydantic import ValidationInfo, field_validator
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Open/Close Sensor -----------
# OpenClose model
# Contains value about open or close state
class DoorWindowTypeEnum(str, Enum):
    DOOR = 'door'
    WINDOW = 'window'


class DoorWindowSensor(Device, TimeStamp):
    value: str
    type: DoorWindowTypeEnum = DoorWindowTypeEnum.DOOR
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, value: str, info: ValidationInfo) -> float:
        if value not in ['open', 'close']:
            raise ValueError("Invalid value. Value must be 'open' or 'close' !")
        return value
    
    def normalize_value(self) -> int:
        return 1 if self.value == 'open' else 0
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},type={self.type.value} value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
    
    
# HumiditySensorWithBattery model
# Contains humidity value and unit and battery level
class DoorWindowSensorWithBattery(DoorWindowSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery},type={self.type.value} value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
