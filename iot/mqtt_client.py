import socket
import ssl
from umqtt.robust import MQTTClient
# Import credentials
from iot.config import IOT_HUB_NAME, IOT_HUB_DEVICE_ID, IOT_HUB_SAS_TOKEN

def connect_mqtt():
    """Connects ESP32 to Azure IoT Hub using MQTT + SSL."""
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.verify_mode = ssl.CERT_NONE
        client = MQTTClient(
            client_id=IOT_HUB_DEVICE_ID,
            server=f"{IOT_HUB_NAME}.azure-devices.net",
            user=f"{IOT_HUB_NAME}.azure-devices.net/{IOT_HUB_DEVICE_ID}/?api-version=2021-04-12",
            password=IOT_HUB_SAS_TOKEN,
            port=8883,
            keepalive=3600, 
            ssl=context
            # ssl_params={"key": key, "cert": cert},
        )
        client.reconnect()
        print("✅ Connected to Azure IoT Hub via MQTT with SSL!")
        return client
    except Exception as e:
        print(f"❌ MQTT connection failed: {e}")
        return None
