from enum import Enum
from BaseValidatiorsModels import Battery, Device, TimeStamp
from pydantic import ValidationInfo, field_validator

# ----------- Humidity Sensor -----------
# HumiditySensor model
# Contains humidity value and unit
class TemperatureUnitEnum(str, Enum):
    PERCENT = '%' # Pomer aktuálneho tlaku vodnej pary k maximálnemu tlaku vodnej pary pri danej teplote (Relatívna vlhkosť)
    GM3 = 'g/m³' # Skutočné množstvo vodnej pary v ovzduší (Absolútna vlhkosť)
    GKG = 'g/kg' # Pomer hmotnosti vodnej pary k hmotnosti suchého vzduchu (Špecifická vlhkosť)

class TemperatureSensor(Device, TimeStamp):
    value: float
    unit: TemperatureUnitEnum
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, value: str, info: ValidationInfo) -> float:
        if value < 0:
            raise ValueError("value can't be negative")
        return value
    
    def normalize_value(self, value: float) -> float:
        #transform the value from absolute humidity to relative humidity
        if self.unit == TemperatureUnitEnum.GM3:
            return (self.value / 6.112) * 100
        # transform the value from specific humidity to relative humidity
        elif self.unit == TemperatureUnitEnum.GKG:
            return (self.value / (self.value + 622)) * 100
        elif self.unit == TemperatureUnitEnum.PERCENT:
            return self.value
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},unit=% value={self.normalize_value(self.value)} {super().timestamp_get_line_protocol()}"
    
# HumiditySensorWithBattery model
# Contains humidity value and unit and battery level
class TemperatureSensorWithBattery(TemperatureSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery},unit=% value={self.normalize_value(self.value)} {super().timestamp_get_line_protocol()}"
