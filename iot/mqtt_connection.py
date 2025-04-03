import network
import time
from umqtt.simple import MQTTClient
import ujson

# Your local MQTT broker IP (e.g., your computer)
MQTT_BROKER = "192.168.0.100"

# Wi-Fi Setup
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("Wokwi-GUEST", "")
while not sta.isconnected():
    time.sleep(0.1)
print("✅ WiFi connected")

client = MQTTClient("esp32-wokwi", MQTT_BROKER)
client.connect()
print("✅ Connected to local MQTT broker")

while True:
    data = {
        "temp": 26,
        "humidity": 55
    }
    payload = ujson.dumps(data)
    print("📤 Sending:", payload)
    client.publish("wokwi/sensor", payload)
    time.sleep(5)
