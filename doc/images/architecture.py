#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.iot import IotSensor, IotDeviceGateway, IotActuator
from diagrams.aws.general import MobileClient
from diagrams.aws.iot import IotHttp

room_attr={
    # "fontsize": "45",
    "bgcolor": "transparent",
    "fontname": "bold",
    # "width": "10"
}

cloud_attr={
    # "fontsize": "45",
    "bgcolor": "transparent",
    "fontname": "bold",
    # "width": "10",
}

with Diagram('Smart Department (architecture)', show=False, direction='BT', filename='architecture'):
    with Cluster('Room 1', graph_attr=room_attr):
        # 1st layer
        sensor1 = IotSensor('Sensor')
        actuator1 = IotActuator('Actuator')
        sensor2 = IotSensor('Sensor')
        actuator2 = IotActuator('Actuator')

        # 2nd layer
        iotgw = IotDeviceGateway('IoT Gateway')

    with Cluster('Room 2', graph_attr=room_attr):
        # 1st layer
        sensor3 = IotSensor('Sensor')
        actuator3 = IotActuator('Actuator')
        sensor4 = IotSensor('Sensor')
        actuator4 = IotActuator('Actuator')

        # 2nd layer
        iotgw2 = IotDeviceGateway('IoT Gateway')

    # 3rd layer
    with Cluster('Cloud', graph_attr=cloud_attr):
        mother = IotDeviceGateway('Mother')
        service1 = IotHttp('Service')
        service2 = IotHttp('Service')

    # clients
    phone1 = MobileClient('Client')
    phone2 = MobileClient('Client')

    # render
    [ sensor1, actuator1, sensor2, actuator2 ] >> Edge() << iotgw >> Edge() << mother
    [ sensor3, actuator3, sensor4, actuator4 ] >> Edge() << iotgw2 >> Edge() << mother

    mother >> Edge() << [ service1, service2 ]
    service1 >> Edge() << phone1
    service2 >> Edge() << phone2
