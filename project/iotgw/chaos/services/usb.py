from main import usb


@usb.connect
def print_connect_message():
    print("USB Device connected...")


@usb.disconnect
def print_disconnect_message():
    print("USB Device disconnected...")
