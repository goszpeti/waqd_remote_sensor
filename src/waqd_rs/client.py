# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

class WifiClient():
    INTERIOR_MODE = 0
    EXTERIOR_MODE = 1

    def __init__(self) -> None:
        # Get wifi details and more from a secrets.py file
        try:
            from ..secrets import secrets
            #from secrets import secrets
        except ImportError:
            print("WiFi secrets are kept in secrets.py, please add them there!")
            raise
        self._secrets = secrets
        # Raspberry Pi RP2040 Pinout for Pimoroni WiFi Pack
        esp32_cs = DigitalInOut(board.GP7)
        esp32_ready = DigitalInOut(board.GP10)
        esp32_reset = DigitalInOut(board.GP11)

        spi = busio.SPI(board.GP18, board.GP19, board.GP16)

        self._esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        if self._esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", self._esp.firmware_version)
        print("MAC addr:", [hex(i) for i in self._esp.MAC_address])

    def connect(self):
        # debug
        for ap in self._esp.scan_networks():
            print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

        print("Connecting to AP...")
        while not self._esp.is_connected:
            try:
                self._esp.connect_AP(self._secrets["ssid"], self._secrets["password"])
            except RuntimeError as e:
                print("Could not connect to AP, retrying: ", e)
                continue

        print("Connected to", str(self._esp.ssid, "utf-8"), "\tRSSI:", self._esp.rssi)
        print("My IP address is", self._esp.pretty_ip(self._esp.ip_address))


    def check_waqd_connection(self):
        self._url = self._secrets["waqd_url"]
        if not self._url:
            print(secrets)
            raise RuntimeError("WAQD Url missing")
        ping = self._esp.ping(self._url)
        print("Ping waqd@%s: %d ms" % (self._url, ping))


    def post_rs_values(self, temp, hum, mode):
        if mode == self.EXTERIOR_MODE:
            node = "remoteExtSensor"
        elif mode == self.INTERIOR_MODE:
            node = "remoteIntSensor"
        else:
            raise RuntimeError("Unsupported mode")
        requests.set_socket(socket, self._esp)
#         JSON_POST_URL = "https://httpbin.org/post"
#         json_data = {"Date": "July 25, 2019"}
#         print("POSTing data to {0}: {1}".format(JSON_POST_URL, json_data))
#         response = requests.post(JSON_POST_URL, json=json_data)
#         print("-" * 40)
# 
#         json_resp = response.json()
#         # Parse out the 'json' key from json_resp dict.
#         print("JSON Data received from server:", json_resp["json"])
#         print("-" * 40)
#         response.close()
#         json_resp = response.json()

        url = "http://" + self._url + ":8080/" +  node
        myobj = {"api_ver": "0.1", 'temp': str(temp), "hum": str(hum)}
        print(url)
        try:
            response = requests.post(url, json=myobj)
            json_resp = response.json()
            response.close()
        except Exception as e:
            print("Can't post: " + str(e))


