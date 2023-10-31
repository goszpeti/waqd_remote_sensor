import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import time


class IntegratedWifiClient():
    def __init__(self) -> None:
        import wifi
        self._radio = wifi.radio

    def connect(self, ssid: str, password: str):
        for ap in self._radio.start_scanning_networks():
            print(f"\t{ap.ssid}\t\tRSSI: {ap.rssi}")
        self._radio.stop_scanning_networks()
        print("Connecting to AP...")
        self._radio.connect(ssid, password, timeout=15)
        #print("Connected to", self._radio.ap_info.ssid, "\tRSSI:", self._radio.ap_info.rssi)
        print("My IP address is", str(self._radio.ipv4_address))

        from socketpool import SocketPool
        self._socket_pool = SocketPool(self._radio)
        self.session = requests.Session(self._socket_pool)

    def check_connection(self, url: str):
        from ipaddress import IPv4Address
        address = IPv4Address(url)
        ping = self._radio.ping(address)

        if not ping:
            print(f"{url} cannot be found!")
            return False
        print("Ping waqd@%s: %d ms" % (url, ping))
        return True

class Esp32WifiClient():
    def __init__(self) -> None:
        # Get wifi details and more from a secrets.py file
        # Raspberry Pi RP2040 Pinout
        from adafruit_esp32spi import adafruit_esp32spi
        esp32_cs = DigitalInOut(board.GP7)
        esp32_ready = DigitalInOut(board.GP10)
        esp32_reset = DigitalInOut(board.GP11)

        spi = busio.SPI(board.GP18, board.GP19, board.GP16)

        self._esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset, debug=True)

        if self._esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", self._esp.firmware_version)
        print("MAC addr:", [hex(i) for i in self._esp.MAC_address])

    def connect(self, ssid, password):
        # debug
        for ap in self._esp.scan_networks():
            print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

        print("Connecting to AP...")
        while not self._esp.is_connected:
            try:
                self._esp.connect_AP(ssid, password)
            except RuntimeError as e:
                print("could not connect to AP, retrying: ", e)
                continue

        print("Connected to", str(self._esp.ssid, "utf-8"), "\tRSSI:", self._esp.rssi)
        print("My IP address is", self._esp.pretty_ip(self._esp.ip_address))
        import adafruit_esp32spi.adafruit_esp32spi_socket as socket
        requests.set_socket(socket, self._esp)


    def check_connection(self, url: str):
        ping = self._esp.ping(url)
        print("Ping waqd@%s: %d ms" % (url, ping))
        if ping > 65534:
            print(f"{url} cannot be found!")
            return False
        return True

class WeatherStationWifiSensor():
    INTERIOR_MODE = 0
    EXTERIOR_MODE = 1

    def __init__(self, waqd_url: str, waqd_api_key: str, wifi_mode: str, ssid: str, password: str) -> None:
        self._waqd_url = waqd_url
        self._waqd_api_key = waqd_api_key
        self._waqd_reachable = False
        self._enabled = True
        if wifi_mode.lower() == "esp32":
            from waqd_rs.wifi import Esp32WifiClient
            self._wifi_client = Esp32WifiClient()
        elif wifi_mode.lower() == "integrated":
            self._wifi_client = IntegratedWifiClient()
        elif wifi_mode.lower() == "none":
            self._enabled = False
            print("Wifi disabled!")
            return
        else:
            print("Wifi mode invalid!")
            return
        self._wifi_client.connect(ssid, password)
        self._waqd_reachable = self._wifi_client.check_connection(waqd_url)


    def post_rs_values(self, temp, hum, pressure, mode):
        if not self._enabled:
            return
        if not self._waqd_reachable:
            self._wifi_client.check_connection(self._waqd_url)
            return
        if mode == self.EXTERIOR_MODE:
            node = "api/remoteExtSensor"
        elif mode == self.INTERIOR_MODE:
            node = "api/remoteIntSensor"
        else:
            raise RuntimeError("Unsupported mode")

        url = "http://" + self._waqd_url + ":80/" +  node + "?APPID=" + self._waqd_api_key
        myobj = {"api_ver": "0.1", "temp": str(temp), "hum": str(hum), "baro": str(pressure)}
        try:
            response = self._wifi_client.session.post(url, json=myobj) #, ) # response requests 
            response.close()
        except Exception as e:
            print("Can't post: " + str(e))

