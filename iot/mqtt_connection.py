import socket
import ssl
import ujson
from umqtt.robust import MQTTClient
from iot.config import IOT_HUB_NAME, IOT_HUB_DEVICE_ID, IOT_HUB_SAS_TOKEN

class MQTT_CONNECTION:
    def __init__(self, iot_behavior):
        """Connect ESP32 to Azure IoT Hub using MQTT + SSL."""
        self.iot = iot_behavior
        self.client = self.connect_mqtt()
        print("✅ MQTT connection built successful.")
        self.client.set_callback(self.on_message)
        self.client.subscribe(f"devices/{IOT_HUB_DEVICE_ID}/messages/devicebound/#")  # C2D Commands
        print("✅ MQTT subscription successful.")
        
    def connect_mqtt(self):
        """Establish MQTT connection to Azure IoT Hub."""
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

    def on_message(self, topic, msg):
        print("📩 Raw message received")
        try:
            payload = ujson.loads(msg)
            self.iot.route_command(payload)
        except Exception as e:
            print("❌ Failed:", e)

    def publish_telemetry(self, message):
        """Publish telemetry data to Azure IoT Hub."""
        telemetry = ujson.dumps(message)
        self.client.publish(f"devices/{IOT_HUB_DEVICE_ID}/messages/events/", telemetry.encode('utf-8'))
        print(f"📤 Sent telemetry: {telemetry}")

    def update_device_twin(self, message):
        """Update Device Twin Reported Properties."""
        twin_update = ujson.dumps({
            "reported": message
        })
        self.client.publish(f"$iothub/twin/PATCH/properties/reported/?$rid=1", twin_update.encode('utf-8'))
        print(f"📤 Sent Device Twin Update: {twin_update}")

