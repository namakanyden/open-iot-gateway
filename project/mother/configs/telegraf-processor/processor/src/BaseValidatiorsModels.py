from enum import Enum
from pydantic import BaseModel, ValidationInfo, field_validator

# Enumeration of departments
# Contains all available departments
class Department(str, Enum):
    KPI = 'kpi'
    KKUI = 'kkui'
    
# Battery model
# Contains battery level
class Battery(BaseModel):
    battery: int | None = None

    @field_validator('battery')
    @classmethod
    def battery_level_check(cls, value: int, info: ValidationInfo) -> int:
        if 0 < value <= 100:
            return value
        else:
            raise ValueError("battery level must be in range <0, 100>")
    
    def battery_get_line_protocol(self) -> str:
        return f"battery={self.battery}"
    
# TimeStamp model
# Contains timestamp for the data
class TimeStamp(BaseModel):
    ts: int
    
    @field_validator('ts')
    @classmethod
    def validate_timestamp(cls, value: int, info: ValidationInfo) -> int:
        if value < 0:
            raise ValueError("timestamp can't be negative")
        return value
    
    def timestamp_get_line_protocol(self) -> str:
        return self.ts.__str__()
    
# Address model
# Contains address of the device
class Address(BaseModel):
    department: Department
    room: str
    device_type: str
    device_id: str
    topic: str

    @field_validator('department', 'room', 'device_type', 'device_id', 'topic')
    @classmethod
    def no_space_as_value(cls, v: str, info: ValidationInfo) -> str:
        if ' ' in v:
            raise ValueError("department, room, device_type or device_id can't contain a space")
        return v
    
    def address_get_line_protocol(self) -> str:
        return f'department={self.department.value.__str__()},room={self.room},device_type={self.device_type},device_id={self.device_id},topic={self.topic}'

# Device model
# Base class contains base attributes for all devices. Grup of attributes: Address, TimeStamp
class Device(TimeStamp, Address):
    pass