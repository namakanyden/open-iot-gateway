import logging

import pyudev
import threading
import signal
import os


class DeviceMonitor:
    def __init__(self, subsystem):
        self.logger = logging.getLogger("usb")
        self.subsystem_to_monitor = subsystem

        self.__connect_callbacks = []
        self.__disconnect_callbacks = []

        self.__monitor_thread = threading.Thread(target=self.__monitor)
        self.__monitor_thread.daemon = True
        self.__monitor_thread.start()

    def connect(self, func):
        self.__connect_callbacks.append(func)
        return func

    def disconnect(self, func):
        self.__disconnect_callbacks.append(func)
        return func

    def __monitor(self):
        try:
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem=self.subsystem_to_monitor)

            for device in iter(monitor.poll, None):
                self.call_decorated(device)

        except ImportError:
            self.logger.critical("udev is not installed or supported on this device.")
            os._exit(1)
        except SystemExit:
            self.logger.critical("udev is not installed or supported on this device.")
            os._exit(1)

    def call_decorated(self, device):
        logging.debug(f"Found {device.action} : {device.get('DEVTYPE')} : {device.device_path}.")

        if device.get('DEVTYPE') == "usb_device":
            if device.action == "remove":
                for func in self.__disconnect_callbacks:
                    func(device)
            elif device.action == "add":
                for func in self.__connect_callbacks:
                    func(device)
