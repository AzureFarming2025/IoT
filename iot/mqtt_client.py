import socket
import ssl
from umqtt.simple import MQTTClient
# Import credentials
from iot.config import IOT_HUB_NAME, IOT_HUB_DEVICE_ID, IOT_HUB_SAS_TOKEN

def connect_mqtt():
    """Connects ESP32 to Azure IoT Hub using MQTT + SSL."""
    try:
        sock = socket.socket()
        addr = socket.getaddrinfo(f"{IOT_HUB_NAME}.azure-devices.net", 8883)[0][-1]
        sock.connect(addr)
        ssl_sock = ssl.wrap_socket(sock)
        # BUG : azure connection getting reset after initial 2 messages
        client = MQTTClient(
            client_id=IOT_HUB_DEVICE_ID,
            server=f"{IOT_HUB_NAME}.azure-devices.net",
            port=8883,
            ssl=False,  # SSL handled separately
            user=f"{IOT_HUB_NAME}.azure-devices.net/{IOT_HUB_DEVICE_ID}/?api-version=2021-04-12",
            password=IOT_HUB_SAS_TOKEN
        )
        client.sock = ssl_sock
        print("✅ Connected to Azure IoT Hub via MQTT with SSL!")
        return client
    except Exception as e:
        print(f"❌ MQTT connection failed: {e}")
        return None
