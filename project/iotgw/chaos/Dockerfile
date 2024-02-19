FROM python:3.11-slim

# https://docs.balena.io/learn/develop/runtime/#d-bus-communication-with-host-os
ENV INITSYSTEM=on
ENV DBUS_SYSTEM_BUS_ADDRESS unix:path=/host/run/dbus/system_bus_socket
ENV UDEV=on

RUN apt-get update &&\
    apt-get install -y build-essential libudev-dev udev

WORKDIR /chaos

COPY . /chaos

RUN pip install --no-cache-dir -r requirements.txt

CMD service udev restart && python main.py
