from enum import Enum
from pydantic import ValidationInfo, field_validator
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Noise Sensor -----------
# Noise model
# Contains noise value and unit
class NoiseUnitEnum(str, Enum):
    BEL = 'B'
    DECIBEL = 'dB'
    NEPER = 'Np'
    

class NoiseSensor(Device, TimeStamp):
    value: float
    unit: NoiseUnitEnum
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, value: str, info: ValidationInfo) -> float:
        if value < 0:
            raise ValueError("value can't be negative")
        return value
    
    def normalize_value(self) -> float:
        # normalize bel to decibel
        if self.unit == NoiseUnitEnum.BEL:
            return self.value * 10
        # normalize neper to decibel
        elif self.unit == NoiseUnitEnum.NEPER:
            return self.value * 8.685889638065036
        # return decibel
        return self.value
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().address_get_line_protocol()},unit=dB value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
    
# HumiditySensorWithBattery model
# Contains humidity value and unit and battery level
class NoiseSenzorWithBattery(NoiseSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().address_get_line_protocol()},battery={self.battery},unit=dB value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
