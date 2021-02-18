# Homebridge MQTT-Thing Garage Door Opener
Python script for a [homebridge-mqttthing](https://github.com/arachnetech/homebridge-mqttthing) garage door opener

## Prerequisites
1. [homebridge](https://github.com/homebridge/homebridge) server installed
2. [homebridge-mqttthing](https://github.com/arachnetech/homebridge-mqttthing) plugin installed

## Configuration
### GPIO
|Key|Default|Description|
|-|-|-|
|relay|17|sets the pin responsible for controling the relay|
|reedOpen|5|sets the pin responsible for reading the reedswitch state in the closed position|
|reedClosed|12|sets the pin responsible for reading the reedswitch state in the open position|

### mqtt

