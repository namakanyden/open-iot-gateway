#!/usr/bin/env python3
import json
from pathlib import Path
import sys

from pydantic import ValidationError
from HumiditySenzor import HumiditySensor, HumiditySensorWithBattery
from TemperatureSenzor import TemperatureSensor, TemperatureSensorWithBattery
from line_protocol_parser import parse_line

def validate_data(device_type: str, data: dict):
    if device_type == 'humidity':
        if 'battery' in data:
            return HumiditySensorWithBattery(**data);
        else:
            return HumiditySensor(**data);
    elif device_type == 'temperature':
        if 'battery' in data:
            return TemperatureSensorWithBattery(**data);
        else:
            return TemperatureSensor(**data);
    else:
        raise KeyError(f"Schema for {device_type} is missing")

def main():
    for line in sys.stdin:
        try:
            # get data from the line
            data = parse_line(line)
            topic = data["tags"]["topic"]

            # parse the topic
            department, room, device_type, device_id = topic.split("/")
            device_id = device_id.replace(" ", "\ ")
            if device_type == 'thing':
                measurement = 'things'


            newData = {
                "department": department,
                "room": room,
                "device_type": device_type,
                "device_id": device_id,
                "topic": topic.replace(" ", "\ "),
            }
            
            data.update(newData)

            # validate the data
            senzorObj = validate_data(device_type, data)
            
            # print the line protocol
            line_protocol = senzorObj.get_line_protocol()
            print(line_protocol)
            sys.stdout.flush()

        except ValidationError as ex:
            print(f"{topic}: Validation error", file=sys.stderr)
            print(ex, file=sys.stderr)

        except KeyError as ex:
            print(f"{topic}: JSON Schema is missing", file=sys.stderr)


if __name__ == "__main__":
    main()
