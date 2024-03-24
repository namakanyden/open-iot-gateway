from enum import Enum
from BaseValidatiorsModels import Battery, Device, TimeStamp

# ----------- Humidity Sensor -----------
# Temperature model
# Contains temperature value and unit
class TemperatureUnitEnum(str, Enum):
    CELSIUS = 'C'
    FAHRENHEIT = 'F'
    KELVIN = 'K'

class TemperatureSensor(Device, TimeStamp):
    value: float
    unit: TemperatureUnitEnum
    
    def normalize_value(self) -> float:
        # transform the value from fahrenheit to celsius
        if self.unit == TemperatureUnitEnum.FAHRENHEIT:
            return (self.value - 32) * 5/9
        # transform the value from kelvin to celsius
        elif self.unit == TemperatureUnitEnum.KELVIN:
            return self.value - 273.15
        elif self.unit == TemperatureUnitEnum.CELSIUS:
            return self.value
        
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},unit=C value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
    
# HumiditySensorWithBattery model
# Contains humidity value and unit and battery level
class TemperatureSensorWithBattery(TemperatureSensor, Battery):
    
    def get_line_protocol(self) -> str:
        return f"{self.device_type},{super().device_get_line_protocol()},battery={self.battery},unit=C value={self.normalize_value()} {super().timestamp_get_line_protocol()}"
