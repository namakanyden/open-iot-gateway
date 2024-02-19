from main import usb


@usb.connect
def print_connect_message(device):
    print("USB Device connected...")


@usb.disconnect
def print_disconnect_message(device):
    print("USB Device disconnected...")
