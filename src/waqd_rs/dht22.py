# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht



class DHTSensor():
    def __init__(self, pin) -> None:
        # Initial the dht device, with data pin connected to:
        self._dht_driver = adafruit_dht.DHT22(pin) # board.GP27
        self.temperature = 0
        self.humidity = 0

    def read_values(self):
        try:
            # Print the values to the serial port
            temperature_c = self._dht_driver.temperature
            humidity = self._dht_driver.humidity
            print("Temp: {:.1f} C Humidity: {}% ".format(temperature_c, humidity))
            self.temperature = temperature_c
            self.humidity = humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self._dht_driver.exit()
            raise error

