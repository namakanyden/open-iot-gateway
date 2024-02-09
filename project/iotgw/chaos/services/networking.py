from core import core


@core.message
def disable_internet():
    print("Disabling internet...")


@core.message
def disconnect_eth():
    print("Disconnecting from eth...")


@core.message
def disconnect_wn():
    print("Disconnecting from wn...")
