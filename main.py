import iot.wifi
import iot.mqtt_client
from iot.config import IOT_HUB_DEVICE_ID
import devices.dht_sensor
# import devices.oled_display
import time
import ujson  # For JSON serialization

# ✅ Connect Wi-Fi
if iot.wifi.connect_wifi():
    mqtt = iot.mqtt_client.connect_mqtt()
    if mqtt:
        while True:
            temp, hum = devices.dht_sensor.read_dht()
            # devices.oled_display.update_display(temp, hum)

            if temp is not None and hum is not None:
                message = ujson.dumps({
                    "temperature": temp,
                    "humidity": hum
                })
                
                # 📤 Publish telemetry data
                mqtt.publish(f"devices/{IOT_HUB_DEVICE_ID}/messages/events/", message)
                print(f"📤 Sent telemetry: {message}")

                # 📤 Update Device Twin Reported Properties
                twin_update = ujson.dumps({
                    "reported": {
                        "temperature": temp,
                        "humidity": hum
                    }
                })
                mqtt.publish(f"$iothub/twin/PATCH/properties/reported/?$rid=1", twin_update)
                print(f"📤 Sent Device Twin Update: {twin_update}")

            time.sleep(10)  # Adjust as needed
    else:
        print("❌ MQTT connection failed.")
else:
    print("❌ Wi-Fi connection failed.")
