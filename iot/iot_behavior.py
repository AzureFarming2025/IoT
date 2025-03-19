import time
import ujson
from iot.wifi import WiFi
from iot.mqtt_connection import MQTT_CONNECTION
from devices.eeprom import EEPROM
from control.sensor_manager import SensorManager
from control.actuator_manager import ActuatorManager

class IoTBehavior:
    def __init__(self):
        """Initialize IoT devices, Wi-Fi, MQTT, and Device Control."""
        self.sensors = SensorManager()
        self.actuators = ActuatorManager()
        self.eeprom = EEPROM()  
        self.mode = self.eeprom.read_mode()  
        # ✅ Wi-Fi & MQTT
        self.wifi = WiFi()
        if self.wifi.connect():
            self.mqtt = MQTT_CONNECTION(self)
        else:
            self.mqtt = None
            print("❌ No MQTT connection due to Wi-Fi failure.")

    def set_mode(self, mode):
        """Switch between 'automate' and 'manual' mode and save to EEPROM."""
        if mode in ["automate", "manual"]:
            self.mode = mode
            self.eeprom.write_mode(mode)
            print(f"[INFO] Mode set to {self.mode.upper()}")

    def automate_mode(self, temp, moisture):
        """Automatically control actuators based on conditions."""
        self.actuators.set_display(temp, moisture, None)
        self.actuators.adjust_sunscreen(temp)
        self.actuators.set_watering(moisture < 25)

    def manual_mode(self):
        """Listen for MQTT commands to control actuators in manual mode."""
        # print("🛠️ Manual mode active. Waiting for actuator control commands...")
        pass

    def update_system(self):
        """Read sensors, send telemetry, and apply automation rules."""
        while True:
            self.mqtt.client.check_msg()
            temp, hum, moisture = self.sensors.read_sensors()

            # ✅ Apply automation if enabled
            if self.mode == "automate":
                self.automate_mode(temp, moisture)
            else:
                self.manual_mode()
            time.sleep(2)
            # # ✅ Publish Telemetry Data every 2 seconds
            # if self.mqtt:
            #     telemetry_data = ujson.dumps({
            #         "temperature": temp,
            #         "humidity": hum,
            #         "moisture": moisture
            #     })
            #     self.mqtt.publish_telemetry(telemetry_data)

            # time.sleep(2)  # Telemetry interval