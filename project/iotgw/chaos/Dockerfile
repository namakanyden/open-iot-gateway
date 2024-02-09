FROM python:3.8-slim

# https://docs.balena.io/learn/develop/runtime/#d-bus-communication-with-host-os
ENV DBUS_SYSTEM_BUS_ADDRESS unix:path=/host/run/dbus/system_bus_socket

WORKDIR /chaos

COPY . /chaos

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
