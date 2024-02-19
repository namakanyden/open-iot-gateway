import pyudev
import threading


class DeviceMonitor:
    def __init__(self, subsystem):
        self.subsystem_to_monitor = subsystem

        self.__connect_callbacks = []
        self.__disconnect_callbacks = []

        self.__monitor_thread = threading.Thread(target=self.__monitor)
        self.__monitor_thread.start()

    def connect(self, func):
        self.__connect_callbacks.append(func)

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result

        return wrapper()

    def disconnect(self, func):
        self.__disconnect_callbacks.append(func)

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result

        return wrapper()

    def __monitor(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem=self.subsystem_to_monitor)

        for device in iter(monitor.poll, None):
            if device.action == 'add':
                for func in self.__connect_callbacks:
                    func()

            elif device.action == 'remove':
                for func in self.__disconnect_callbacks:
                    func()

