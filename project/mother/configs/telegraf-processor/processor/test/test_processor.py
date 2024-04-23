import io
import os
import unittest
import sys
from unittest.mock import patch, MagicMock

from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from processor import line_parser, validate_data, main

class TestProcessor(unittest.TestCase):
    # TEST ----- main -----
    def test_main_valid_working(self):
        # Mocking sys.stdin
        with patch('sys.stdin', new_callable=io.StringIO) as mock_stdin:
            mock_stdin.write("temperture,topic=kpi/kronos/temperature/ad34,unit=F value=25.1 1465839830100400200\n")
            mock_stdin.write("humidity,topic=kpi/duna/humidity/af234,battery=82,unit=% value=56 1465839830100400200\n")
            mock_stdin.seek(0)
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                main()
                self.assertEqual(mock_stdout.getvalue(),"temperature,department=kpi,room=kronos,device_type=temperature,device_id=ad34,topic=kpi/kronos/temperature/ad34,unit=C value=-3.8333333333333326 1465839830100400200\nhumidity,department=kpi,room=duna,device_type=humidity,device_id=af234,topic=kpi/duna/humidity/af234,battery=82,unit=% value=56.0 1465839830100400200\n")
                    
                    
    def test_line_parser_valid_line(self):
        line = "temperature,topic=kpi/kronos/temperature/ad34,unit=F value=25.1 1465839830100400200\n"
        result = line_parser(line)
        
        self.assertEqual(result["department"], "kpi")
        self.assertEqual(result["room"], "kronos")
        self.assertEqual(result["device_type"], "temperature")
        self.assertEqual(result["device_id"], "ad34")
        self.assertEqual(result["ts"], 1465839830100400200)
        self.assertEqual(result["unit"], "F")
        self.assertEqual(result["value"], 25.1)
        
        
    def test_line_parser_line_with_spaces(self):
        line = "humidity,topic=kpi/duna/humidity/af234,battery=82,unit=% value=56 1465839830100400200\n"
        result = line_parser(line)
        
        self.assertEqual(result["department"], "kpi")
        self.assertEqual(result["room"], "duna")
        self.assertEqual(result["device_type"], "humidity")
        self.assertEqual(result["device_id"], "af234")
        self.assertEqual(result["ts"], 1465839830100400200)
        self.assertEqual(result["unit"], "%")
        self.assertEqual(result["value"], 56)
        
        
    def test_line_parser_line_with_additional_fields(self):
        line = "temperature,topic=kpi/kronos/temperature/ad34,unit=F,battery=90,location=room1 value=25.1 1465839830100400200\n"
        result = line_parser(line)
        
        self.assertEqual(result["department"], "kpi")
        self.assertEqual(result["room"], "kronos")
        self.assertEqual(result["device_type"], "temperature")
        self.assertEqual(result["device_id"], "ad34")
        self.assertEqual(result["ts"], 1465839830100400200)
        self.assertEqual(result["unit"], "F")
        self.assertEqual(result["value"], 25.1)
        self.assertEqual(result["battery"], '90')
        self.assertEqual(result["location"], "room1")
        
    
    def test_line_parser_line_with_no_topic(self):
        line = "temperature,unit=F value=25.1 1465839830100400200\n"
        
        with self.assertRaises(ValueError) as context:
            line_parser(line)
        
        self.assertEqual(str(context.exception), "Topic is empty")
        
    
    def test_line_parser_line_with_empty_department(self):
        line = "temperature,topic=/kronos/temperature/ad34,unit=F value=25.1 1465839830100400200\n"
        
        with self.assertRaises(ValueError) as context:
            line_parser(line)
        
        self.assertEqual(str(context.exception), "Department is empty in topic")
    
    def test_line_parser_line_with_small_topic(self):
        line = "temperature,topic=temperature/ad34,unit=F value=25.1 1465839830100400200\n"
        
        with self.assertRaises(ValueError) as context:
            line_parser(line)
        
        self.assertEqual(str(context.exception), "Topic is not valid")
    
    def test_validate_data_humidity_sensor(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 1234567892,
            "value": 50,
            "unit": "%"
        }
        
        result = validate_data(data)
        
        self.assertEqual(result.department.value, "kpi")
        self.assertEqual(result.room, "A1")
        self.assertEqual(result.device_type, "humidity")
        self.assertEqual(result.device_id, "123fa")
        self.assertEqual(result.topic, "kpi/A1/humidity/123fa")
        self.assertEqual(result.ts, 1234567892)
        self.assertEqual(result.value, 50)
        self.assertEqual(result.unit, "%")
        
        
    def test_validate_data_humidity_sensor_with_battery(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "humidity",
            "device_id": "123fa",
            "topic": "kpi/A1/humidity/123fa",
            "ts": 1234567892,
            "value": 50,
            "unit": "%",
            "battery": 80
        }
        
        result = validate_data(data)
        
        self.assertEqual(result.department.value, "kpi")
        self.assertEqual(result.room, "A1")
        self.assertEqual(result.device_type, "humidity")
        self.assertEqual(result.device_id, "123fa")
        self.assertEqual(result.topic, "kpi/A1/humidity/123fa")
        self.assertEqual(result.ts, 1234567892)
        self.assertEqual(result.value, 50)
        self.assertEqual(result.unit, "%")
        self.assertEqual(result.battery, 80)
        
    def test_validate_data_temperature_sensor(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 21.5,
            "unit": "C"
        }
        
        result = validate_data(data)
        
        self.assertEqual(result.department.value, "kpi")
        self.assertEqual(result.room, "A1")
        self.assertEqual(result.device_type, "temperature")
        self.assertEqual(result.device_id, "123fa")
        self.assertEqual(result.topic, "kpi/A1/temperature/123fa")
        self.assertEqual(result.ts, 1234567892)
        self.assertEqual(result.value, 21.5)
        self.assertEqual(result.unit, "C")
        
    def test_validate_data_temperature_sensor_with_battery(self):
        data = {
            "department": "kpi",
            "room": "A1",
            "device_type": "temperature",
            "device_id": "123fa",
            "topic": "kpi/A1/temperature/123fa",
            "ts": 1234567892,
            "value": 21.5,
            "unit": "C",
            "battery": 90
        }
        
        result = validate_data(data)
        
        self.assertEqual(result.department.value, "kpi")
        self.assertEqual(result.room, "A1")
        self.assertEqual(result.device_type, "temperature")
        self.assertEqual(result.device_id, "123fa")
        self.assertEqual(result.topic, "kpi/A1/temperature/123fa")
        self.assertEqual(result.ts, 1234567892)
        self.assertEqual(result.value, 21.5)
        self.assertEqual(result.unit, "C")
        self.assertEqual(result.battery, 90)


if __name__ == '__main__':
    unittest.main()# TEST ----- line_parser -----
