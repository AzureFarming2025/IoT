import socket
import ssl
import ujson
from umqtt.robust import MQTTClient
from iot.config import IOT_HUB_NAME, IOT_HUB_DEVICE_ID, IOT_HUB_SAS_TOKEN

class MQTTClient:
    def __init__(self, iot_behavior):
        """Connect ESP32 to Azure IoT Hub using MQTT + SSL."""
        self.iot = iot_behavior
        self.client = self.connect_mqtt()
        self.client.set_callback(self.on_message)
        self.client.subscribe("devices/your-device/messages/devicebound/#")  # C2D Commands

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
            self.client = client
        except Exception as e:
            print(f"❌ MQTT connection failed: {e}")

    def on_message(self, topic, msg):
        """Handle incoming MQTT C2D commands."""
        payload = ujson.loads(msg.decode())
        if self.iot.mode == "manual":
            if payload["actuator"] == "water":
                self.iot.device_control.set_watering(payload["value"] == "on")
            elif payload["actuator"] == "relay":
                self.iot.device_control.toggle_relay(payload["value"] == "on")

    def publish_telemetry(self, message):
        """Publish telemetry data to Azure IoT Hub."""
        self.client.publish(f"devices/{IOT_HUB_DEVICE_ID}/messages/events/", message)
        print(f"📤 Sent telemetry: {message}")

    def update_device_twin(self, message):
        """ Update Device Twin Reported Properties. """
        twin_update = ujson.dumps({
            "reported": {
                "temperature": temp,
                "humidity": hum
            }
        })
        self.client.publish(f"$iothub/twin/PATCH/properties/reported/?$rid=1", twin_update)
        print(f"📤 Sent Device Twin Update: {twin_update}")
