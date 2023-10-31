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
    secrets.get("waqd_api_key", ""),
    config.get("wifi_mode", "None"),
    secrets.get("ssid", ""),
    secrets.get("password", "")
)

### sensor setup
sensor = None
co2_sensor = None
if config.get("sensor", "").lower() == "dht22":
    from waqd_rs.sensor import DHTSensor
    sensor = DHTSensor(board.GP27)
elif config.get("sensor", "").lower() == "bme280":
    from waqd_rs.sensor import BME280Sensor
    sensor = BME280Sensor()
if config.get("air_quality_sensor", "").lower() == "mh-z19":
    from waqd_rs.sensor import MHZ19Sensor
    co2_sensor = MHZ19Sensor()

sensor_values = {
    "hum": -1,
    "temp": -1,
    "baro": -1,
    "co2": -1,
}
while True:
    if sensor:
        sensor.read_values()
        sensor_values.update({"temp": sensor.temperature, "hum": sensor.humidity, "baro": sensor.pressure})
        wifi_client.post_rs_values(sensor_values.get("temp", 0), sensor_values.get("hum", 0), 
                                   sensor_values.get("baro", 0), config.get("waqd_mode", 1))
    if co2_sensor:
        co2_sensor.read_values()
        sensor_values.update({"co2": co2_sensor.ppm})
    if disp:
        disp.draw_main(sensor_values.get("temp", 0), sensor_values.get("hum", 0), 
                       sensor_values.get("co2", 0), config.get("waqd_mode", 1))
    time.sleep(CYCLE_TIME_S)
