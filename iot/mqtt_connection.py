import ujson
from umqtt.robust import MQTTClient
from iot.config import IOT_HUB_NAME, IOT_HUB_DEVICE_ID, IOT_HUB_SAS_TOKEN

class MQTT_CONNECTION:
    def __init__(self, iot_behavior):
        """Connect ESP32 to Azure IoT Hub using MQTT + TLS."""
        self.iot = iot_behavior
        self.client = self.connect_mqtt()
        if self.client:
            print("✅ MQTT connection successful.")
            self.client.set_callback(self.on_message)
            self.client.subscribe(f"devices/{IOT_HUB_DEVICE_ID}/messages/devicebound/#")
            print("✅ Subscribed to C2D messages.")
        
    def connect_mqtt(self):
        """Establish MQTT over TLS connection to Azure IoT Hub."""
        try:
            client = MQTTClient(
                client_id=IOT_HUB_DEVICE_ID,
                server=f"{IOT_HUB_NAME}.azure-devices.net",
                user=f"{IOT_HUB_NAME}.azure-devices.net/{IOT_HUB_DEVICE_ID}/?api-version=2021-04-12",
                password=IOT_HUB_SAS_TOKEN,
                port=8883,
                keepalive=3600,
                ssl=True  # ✅ MicroPython only supports boolean flag
            )
            client.connect()  # ✅ Required to establish the connection
            print("✅ Connected to Azure IoT Hub via MQTT+TLS!")
            return client
        except Exception as e:
            print(f"❌ MQTT connection failed: {e}")
            return None

    def on_message(self, topic, msg):
        print("📩 Message received from Azure")
        try:
            payload = ujson.loads(msg)
            self.iot.route_command(payload)
        except Exception as e:
            print("❌ JSON decode failed:", e)

    def publish_telemetry(self, message):
        """Publish telemetry data to Azure IoT Hub."""
        if self.client:
            telemetry = ujson.dumps(message)
            self.client.publish(f"devices/{IOT_HUB_DEVICE_ID}/messages/events/", telemetry.encode('utf-8'))
            print(f"📤 Sent telemetry: {telemetry}")

    def update_device_twin(self, message):
        """Send reported properties to device twin."""
        if self.client:
            twin_update = ujson.dumps({
                "reported": message
            })
            self.client.publish(f"$iothub/twin/PATCH/properties/reported/?$rid=1", twin_update.encode('utf-8'))
            print(f"📤 Sent device twin update: {twin_update}")