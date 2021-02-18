# Homebridge MQTT-Thing Garage Door Opener
Python script for a [homebridge-mqttthing](https://github.com/arachnetech/homebridge-mqttthing) garage door opener

## Prerequisites
1. [homebridge](https://github.com/homebridge/homebridge) server installed
2. [homebridge-mqttthing](https://github.com/arachnetech/homebridge-mqttthing) plugin installed
3. [mosquitto](https://mosquitto.org/blog/2013/01/mosquitto-debian-repository/) installed

## Installation
* Install the Python [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) module
```
$ pip install paho-mqtt
```
* Install the Python [configparser](https://pypi.org/project/configparser/) module
```
$ pip install configparser
```
* Install the Python [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) module
```
$ pip install RPi.GPIO
```
## Configuration
Configuration of the [config.ini](https://github.com/TDNhd/homebridge-mqttthing-garage-door-opener/blob/main/config.ini)
* #### GPIO
|Key|Default|Description|
|------------|----|--------------------------------------------------------------------------------|
|`relay`     |`17`|sets the pin responsible for controling the relay                               |
|`reedOpen`  |`5` |sets the pin responsible for reading the reedswitch state in the closed position|
|`reedClosed`|`12`|sets the pin responsible for reading the reedswitch state in the open position  |

* #### mqtt
|Key|Default|Description|
|--------------|----------|---------------------------------------|
|`brokerAdress`|          |(Ip)-adress of your broker             |
|`port`        |`1833`    |port used                              |
|`client_id`   |`"garage"`|client ID for connecting to mqtt server|

* #### tls
|Key|Default|Description|
|------------------|------|----------------------------------------------------------|
|`tls_set`         |`True`|defines whether tls is used or not                        |
|`CA_crt`          |      |Path to your CA certificate                               |
|`Client_crt`      |      |Path to your Client certificate                           |
|`Client_key`      |      |Path to your Client key                                   |
|`tls_insecure_set`|`True`|defines whether self_signed sertificate is accepted or not|
