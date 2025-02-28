import iot.wifi
import iot.mqtt_client
from iot.config import IOT_HUB_DEVICE_ID
import devices.dht_sensor
import devices.oled_display
import time

# ✅ Connect Wi-Fi
if iot.wifi.connect_wifi():
    mqtt = iot.mqtt_client.connect_mqtt()
    if mqtt:
        while True:
            temp, hum = devices.dht_sensor.read_dht()
            devices.oled_display.update_display(temp, hum)
            if temp is not None and hum is not None:
                message = f'{{"temperature": {temp}, "humidity": {hum}}}'
                mqtt.publish(f"devices/{IOT_HUB_DEVICE_ID}/messages/events/", message)
                print(f"📤 Sent to Azure: {message}")
            time.sleep(5)
    else:
        print("❌ MQTT connection failed.")
else:
    print("❌ Wi-Fi connection failed.")
