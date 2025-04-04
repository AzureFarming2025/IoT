from azure.iot.device import IoTHubDeviceClient, Message
import paho.mqtt.client as mqtt
import json

# Your Azure Device connection string
CONN_STR = "HostName=YOUR-HUB.azure-devices.net;DeviceId=esp32-2;SharedAccessKey=YOUR_KEY"

device_client = IoTHubDeviceClient.create_from_connection_string(CONN_STR)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("📥 From Wokwi:", payload)
    try:
        message = Message(payload)
        device_client.send_message(message)
        print("✅ Sent to Azure IoT Hub")
    except Exception as e:
        print("❌ Failed to send to Azure:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("wokwi/sensor")
print("🔁 Listening on 'wokwi/sensor'...")
mqtt_client.loop_forever()
