# WAQD-RemoteSensor

Remote sensor to interact with WAQD https://github.com/goszpeti/WeatherAirQualityDevice weather station based on a Raspberry Pi Pico with CircuitPython.

## Features

- communication via WLAN to WAQD server (uses ESP32)
- supported sensor is currently DHT22 (may be extended later)
- battery driven (currently powerbank for experiments)
- casing (TODO)
- EPaper display (TODO, may not be enough GPIO pins)

## Used Hardware

- Raspberry Pi Pico
- Pimoroni Pico Wireless Pack (ESP32) or Pico W
- DHT22 or BME280
- USB Powerbank

## Wiring

* ESP32: https://cdn.shopify.com/s/files/1/0174/1800/files/pico-wireless-pinout-diagram_600x600.png?v=1620826291
* DHT22 with GP27

## Software setup

* Flash CircuitPython 8.X on the Pico with the following instructions: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
* Get CircuiPython 8.x libs from https://circuitpython.org/libraries
* Copy the following files/directories to the Picos lib folder:
 * adafruit_dht.mpy
 * adafruit_requests.mpy
 * adafruit_bus_device
 * adafruit_esp32spi
* Copy the files in /src to the root directory

## Architectre

* CircuitPython and Lib have many drivers and has more functions then proprietary drivers
* BLE does does not work out of the box with a generic ESP32 (may need NINA firmware)
* WLAN server of WAQD will be used with a versioned JSON Api
 * Currently only temp and hum supported, may be extended with more sensors

