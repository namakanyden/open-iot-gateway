#!/usr/bin/env python3
import sys

from pydantic import ValidationError
from DoorWindowSensor import DoorWindowSensor, DoorWindowSensorWithBattery
from HumiditySenzor import HumiditySensor, HumiditySensorWithBattery
from LightSenzor import LightSensor, LightSensorWithBattery
from NoiseSenzor import NoiseSensor, NoiseSenzorWithBattery
from PressureSenzor import PressureSensor, PressureSensorWithBattery
from TemperatureSenzor import TemperatureSensor, TemperatureSensorWithBattery
from line_protocol_parser import parse_line

from ThinkSenzor import ThinkSensor, ThinkSensorWithBattery

def validate_data(data: dict):
    if data['device_type'] == 'humidity':
        if 'battery' in data:
            return HumiditySensorWithBattery(**data);
        else:
            return HumiditySensor(**data);
    elif data['device_type'] == 'temperature':
        if 'battery' in data:
            return TemperatureSensorWithBattery(**data);
        else:
            return TemperatureSensor(**data);
    elif data['device_type'] == 'light':
        if 'battery' in data:
            return LightSensorWithBattery(**data);
        else:
            return LightSensor(**data);
    elif data['device_type'] == 'pressure':
        if 'battery' in data:
            return PressureSensorWithBattery(**data);
        else:
            return PressureSensor(**data);
    elif data['device_type'] == 'noise':
        if 'battery' in data:
            return NoiseSenzorWithBattery(**data);
        else:
            return NoiseSensor(**data);
    elif data['device_type'] == 'door' or data['device_type'] == 'window':
        if 'battery' in data:
            return DoorWindowSensor(**data);
        else:
            return DoorWindowSensorWithBattery(**data);
    elif data['device_type'] == 'think':
        if 'battery' in data:
            return ThinkSensor(**data);
        else:
            return ThinkSensorWithBattery(**data);
    else:
        raise KeyError(f"Schema for {data.device_type} is missing")
    
    
def line_parser(line: str) -> dict:
    data = parse_line(line)
    
    # parse topic and valid topic
    topic = None
    try:
        topic = data["tags"]["topic"]
    except:
        raise ValueError("Topic is empty")
    
    if str(topic).count("/") < 3:
        raise ValueError("Topic is not valid")
    
    department, room, device_type, device_id = topic.split("/")
    
    if not department:
        raise ValueError("Department is empty in topic")
    if not room:
        raise ValueError("Room is empty in topic")
    if not device_type:
        raise ValueError("Device type is empty in topic")
    if not device_id:
        raise ValueError("Device id is empty in topic")
    
    device_id = device_id.replace(" ", "\ ")
        
    # create new data object
    newData = {
        "department": department,
        "room": room,
        "device_type": device_type,
        "device_id": device_id,
        "ts": data["time"],
        **data.get("fields", {}),
        **data.get("tags", {})
    }
    
    return newData


def main():
    for line in sys.stdin:
        try:
            # parse the line
            data = line_parser(line)

            # validate the data
            senzorObj = validate_data(data)
            
            # print the line protocol
            line_protocol = senzorObj.get_line_protocol()
            print(line_protocol)
            sys.stdout.flush()

        except ValidationError as ex:
            print(f"Validation error", file=sys.stderr)
            print(ex, file=sys.stderr)
            
        except ValueError as ex:
            print(f"Validation error", file=sys.stderr)
            print(ex, file=sys.stderr)

        except KeyError as ex:
            print(f"Validation model missing", file=sys.stderr)


if __name__ == "__main__":
    main()
