#!/usr/bin/env python3
import json
from pathlib import Path
import sys
from jsonschema import validate, ValidationError
from line_protocol_parser import parse_line


def validate_data(schemas: dict, device_type: str, data: dict):
    schema = schemas[device_type]
    validate(data, schema)


def create_influx_line_protocol(measurement: str, tags: dict, fields: dict, timestamp: int):
    tags_string = ",".join([f"{key}={value}" for key, value in tags.items()])
    fields_string = ",".join([f"{key}={value}" for key, value in fields.items()])
    ts = timestamp * 10**9

    return f"{measurement},{tags_string} {fields_string} {ts:.0f}"


def load_schemas() -> dict:
    schemas = {}
    path = Path("/app/schemas/")

    for file in path.iterdir():
        key = file.name.rsplit(".schema.json")[0]
        with open(file) as schema:
            value = json.load(schema)
        schemas[key] = value

    return schemas


def main():
    schemas = load_schemas()

    for line in sys.stdin:
        try:
            # get data from the line
            data = parse_line(line)
            fields = data["fields"]
            topic = data["tags"]["topic"]
            measurement = data["measurement"]

            # parse the topic
            department, room, device_type, device_id = topic.split("/")
            device_id = device_id.replace(" ", "\ ")
            if device_type == 'thing':
                measurement = 'things'

            # validate the data
            validate_data(schemas, device_type, fields)
            ts = fields.pop("ts")

            tags = {
                "department": department,
                "room": room,
                "type": device_type,
                "id": device_id,
                "topic": topic.replace(" ", "\ "),
            }

            line_protocol = create_influx_line_protocol(measurement, tags, fields, ts)
            print(line_protocol)
            sys.stdout.flush()

        except ValidationError as ex:
            print(f"{topic}: Validation error", file=sys.stderr)
            print(ex, file=sys.stderr)

        except KeyError as ex:
            print(f"{topic}: JSON Schema is missing", file=sys.stderr)


if __name__ == "__main__":
    main()
