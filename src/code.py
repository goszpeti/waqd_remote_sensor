import board
import time

from waqd_rs.dht22 import DHTSensor
from waqd_rs.client import WifiClient

client = WifiClient()
client.connect()
client.check_waqd_connection()

sensor = DHTSensor(board.GP27)

while True:
    sensor.read_values()
    client.post_rs_values(sensor.temperature, sensor.humidity, WifiClient.EXTERIOR_MODE)
    time.sleep(2.0)
