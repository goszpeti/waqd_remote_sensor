import board
import busio
import time

class MHZ19Sensor():
    """ Based on https://github.com/overflo23/MH-Z19_MicroPython/tree/main"""
    def __init__(self, tx=board.GP0, rx=board.GP1):
        self._tx = tx
        self._rx = rx
        self._init_sensor()
        self.ppm = -1

    def _init_sensor(self):
        self.uart = busio.UART(self._tx, self._rx , baudrate=9600, bits=8, parity=None, stop=1, timeout=10)


    def stop(self):
        if self.uart:
            self.uart.deinit()

    def read_values(self):
        try:
            self.uart.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            time.sleep(0.1)
            s = self.uart.read(9)
            print(f"read {s}")
            try:
                z = bytearray(s)
            except:
                return 0
            crc = self.crc8(s)
            if crc != z[8]:
                print("CRC Error")
                # we should restart the uart comm here..
                self.stop()
                time.sleep(1)
                self._init_sensor()
                return 0
            self.ppm = ord(chr(s[2])) * 256 + ord(chr(s[3]))
        except RuntimeError as error:
            print(error.args[0])

    def crc8(self, a):
        crc = 0x00
        count = 1
        b = bytearray(a)
        while count < 8:
            crc += b[count]
            count = count+1
        # Truncate to 8 bit
        crc %= 256
        # Invert number with xor
        crc = ~crc & 0xFF
        crc += 1
        return crc

class BME280Sensor():
    def __init__(self, sda=board.GP26, scl=board.GP27) -> None:
        import adafruit_bme280.advanced as adafruit_bme280
        i2c = busio.I2C(scl, sda)
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
