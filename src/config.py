# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it

config = {
    "waqd_url": "", # IP 
    "waqd_api_key": "",
    "waqd_mode": 1, # 0=interior, 1=exterior
    "wifi_mode": "integrated", # or esp32 or None
    "sensor": "BME280",
    "air_quality_sensor": "MH-Z19", # or None
    "display": "None" # WaveShare2in9Disp
}
secrets = {
    "ssid": "",
    "password": ""
}