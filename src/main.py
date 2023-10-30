import board
import time
CYCLE_TIME_S = 10
config = {}
secrets = {}

try:
    from config import config, secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")

### display setup
disp = None
if config.get("display", "").lower() == "waveshare2in9disp":
    from waqd_rs.disp import WaveShare2in9Disp
    disp = WaveShare2in9Disp()

### wifi client setup
from waqd_rs.wifi import WeatherStationWifiSensor
wifi_client = WeatherStationWifiSensor(
    config.get("waqd_url", ""),
    config.get("waqd_api_key", ""),
    config.get("wifi_mode", "").lower(),
    secrets.get("ssid", ""),
    secrets.get("password", "")
)

### sensor setup
sensor = None
if config.get("sensor", "").lower() == "dht22":
    from waqd_rs.sensor import DHTSensor
    sensor = DHTSensor(board.GP27)
elif config.get("sensor", "").lower() == "bme280":
    from waqd_rs.sensor import BME280Sensor
    sensor = BME280Sensor()

while True:
    if sensor:
        sensor.read_values()
        wifi_client.post_rs_values(sensor.temperature, sensor.humidity, sensor.pressure, config.get("waqd_mode", 1))
        if disp:
            disp.draw_main(sensor.temperature, sensor.humidity, config.get("waqd_mode", 1))
    time.sleep(CYCLE_TIME_S)
