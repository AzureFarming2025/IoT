import network
import time
import ujson
from iot.config import WIFI_SSID, WIFI_PASSWORD

class WiFi:
    def connect(self):
        """Connect ESP32 to Wi-Fi."""
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 20
        while not sta_if.isconnected() and timeout > 0:
            print("⏳ Connecting to Wi-Fi...")
            time.sleep(1)
            timeout -= 1

        if sta_if.isconnected():
            print(f"✅ Wi-Fi connected! IP: {sta_if.ifconfig()[0]}")
            return True
        else:
            print("❌ Wi-Fi connection failed!")
            return False
