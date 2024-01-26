# Inštalácia

## Operačný systém

Ako operačný systém budeme používať [Armbian](https://www.armbian.com/), ktorý je určený na beh na jednodoskových počítačoch, akým je aj _Raspberry Pi_. Okrem toho je pravidelne aktualizovaný a vychádza z distribúcií _Debian_ a _Ubuntu_.

Inštalovať _Armbian_ môžete priamo odtiaľto:

* verzia pre [minipočítače Raspberry Pi 3/4](https://www.armbian.com/rpi4b/)
* verzia pre [počítače s architektúrou x86](https://www.armbian.com/uefi-x86/)


### Problém s Bluetooth

Ak nedochádza k preposielaniu informácií o BLE zariadeniach v okolí do MQTT, vyskúšajte aktualizovať firmvér minipočítača _Raspberry Pi_ príkazom:

```bash
$ rpi-update
```


### Problém s obrazovkou

Ak vám po nainštalovaní distribúcie _Armbian_ na kartu a spustení minipočítača Raspberry Pi zostane čierna obrazovka, je to zrejme prednastavenou konfiguráciou grafického výstupu. V tom prípade odporúčame pridať do konfigurácie v súbore `/boot/firmware/config.txt` pre všetkých voľbu `hdmi_safe=1` a prípadne zakomentovať voľbu `hdmi_drive`.

```
[all]
hdmi_safe=1
#hdmi_drive=2
```


### Problém s orientáciou obrazovky

Ak potrebujete otočiť obrazovku, tak v tom prípade v konfiguračnom súbore potrebujete pridať voľbu:

```
display_rotate=2  # otocenie o 180°
```

Ak používate dotykový displej (napríklad [tento](https://www.raspberrypi.com/products/raspberry-pi-touch-display/)), tak miesto uvedenej voľby použite voľbu

```
lcd_rotate=2
```


## Poinštalačná konfigurácia

Prejdite procesom prvého spustenia a prvej pinštalačnej konfigurácie, kde postupne nastavíte:

* heslo pre používateľa `root` (predvolené nastavené heslo je `1234`)
* meno a heslo nového používateľa, napr.: `maker` s heslom `rekam`
* jazyk a časovú zónu
* nepripájajte sa k WiFi sieti, nakoľko zariadenie bude poskytovať WiFi sieť vlastným chytrým zariadeniam

Po nainštalovaní bude automaticky dostupná služba `ssh`.


## Nainštalovanie docker-a

```bash
$ curl -sSL https://get.docker.com/ | sh
```


## Poinštalačná konfigurácia

Základnú poinštalačnú konfiguráciu urobíme pomocou nástroja `armbian-config`, ktorý spustíte príkazom:

```bash
$ sudo armbian-config
```


### Nastavenie názvu zariadenia (hostname)

Názov zariadenia zmeníte pomocou menu `Personal > Hostname`.


### Samostatná WiFi sieť

Prejdite do časti `Network > Hotspot`. Najprv sa nainštalujú potrebné balíčky, následne vyberiete bezdrôtové rozhranie na vašom zariadení (napr. `wlan0`) a nastavíte meno WiFi siete (napr. `home-iotgw`).


## Zapnutie Bluetooth

Prejdite do časti `Network > BT install`. Process inštalácie prebehne automaticky.

Okrem toho je však potrebné dopísať do súboru `/boot/firmware/config.txt` tieto riadky do časti `[all]`:

```bash
dtparam=krnbt=on
enable_uart=0
```

Zdroj: https://www.linuxquestions.org/questions/slackware-arm-108/pri4-revision-a03111-bluetooth-problems-4175689561/page4.html

Pomocou príkazu `hcitool` zistite, ako je označené vaše Blueooth zariadenie v systéme (napr. `hci0`):

```bash
$ hcitool dev
Devices:
        hci0    B8:27:EB:A7:37:53
```


### Inštalácia nástroja Docker

Docker na vašom zariadení nainštalujete týmto príkazom

```bash
$ curl -sSL https://get.docker.com/ | sh
```

Inštalácia bude trvať niekoľko minút.

Po skončení inštalácie je potrebné používateľa pridať do skupiny `docker` nasledovným príkazom:

```bash
$ sudo usermod -aG docker $USER
```


### Reštart

Aby sa korektne aplikovali všetky zmeny, zariadenie reštartujte napríklad príkazom:

```bash
$ sudo reboot
```


## Inštalácia Core modulov

Ešte predtým, ako začneme, si projekt stiahneme zo [stránky projektu na serveri github.com](https://github.com/namakanyden/Open-IoT-Gateway) pomocou príkazu:

```bash
$ git clone https://github.com/namakanyden/open-iot-gateway.git
```

### Vytvorenie samostatnej siete

```bash
$ docker network create iotgw
```

spustenie kompozicie

```
$ docker compose up --detach
```

