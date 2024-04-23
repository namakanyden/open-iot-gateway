from enum import Enum

from pydantic import ValidationInfo, field_validator
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Humidity Sensor -----------
# Pressure model
# Contains Pressure value and unit
class PressureUnitEnum(str, Enum):
    PASCALE = 'Pa'
    BAR = 'bar'
    POUNDSPERSQUARE = 'psi'
    ATMOSPHERE = 'atm'

class PressureSensor(Device, TimeStamp):
    value: float
    unit: PressureUnitEnum
    
    @field_validator('value')
    @classmethod
    def value_check(cls, value: int, info: ValidationInfo) -> int:
        if 0 <= value:
            return value
        else:
            raise ValueError("pressure level must be positive")
    
    def normalize_value(self) -> float:
        # transform the value from bar to pascale
        if self.unit == PressureUnitEnum.BAR:
            return self.value * 100000
        # transform the value from psi to pascale
        elif self.unit == PressureUnitEnum.POUNDSPERSQUARE:
            return self.value * 6894.76
        # transform the value from atm to pascale
        elif self.unit == PressureUnitEnum.ATMOSPHERE:
            return self.value * 101325
        elif self.unit == PressureUnitEnum.PASCALE:
            return self.value
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},unit=Pa value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
    
# PressureSensorWithBattery model
# Contains pressure value and unit and battery level
class PressureSensorWithBattery(PressureSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery},unit=Pa value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
