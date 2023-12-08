# Notes

## Bluetooth on RPi 4

* do suboru `/boot/firmware/config.txt` treba pridat a upravit tieto riadky:

    ```bash
    dtparam=krnbt=on
    enable_uart=0
    ```

  zdroj: https://www.linuxquestions.org/questions/slackware-arm-108/pri4-revision-a03111-bluetooth-problems-4175689561/page4.html


## Zaujímavé nástroje

* [mqttwarn](https://mqttwarn.readthedocs.io/en/latest/) - A highly configurable MQTT message router, where the routing targets are notification plugins, primarily written in Python.
