import board
import busio

class BME280Sensor():
    def __init__(self) -> None:
        import adafruit_bme280.advanced as adafruit_bme280
        i2c = busio.I2C(board.GP5, board.GP4)
        self._driver = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def read_values(self):
        try:
            # Print the values to the serial port
            temperature_c = self._driver.temperature
            humidity = self._driver.humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
            self.temperature = temperature_c
            self.humidity = humidity
            self.pressure = self._driver.pressure

        except RuntimeError as error:
            print(error.args[0])

class DHTSensor():
    def __init__(self, pin) -> None:
        # Initial the dht device, with data pin connected to:
        import adafruit_dht
        self._dhtDevice = adafruit_dht.DHT22(pin) # board.GP27
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def read_values(self):
        try:
            # Print the values to the serial port
            temperature_c = self._dhtDevice.temperature
            humidity = self._dhtDevice.humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
            self.temperature = temperature_c
            self.humidity = humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self._dhtDevice.exit()
            raise error