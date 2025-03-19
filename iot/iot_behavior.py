import time
import ujson
from iot.wifi import WiFi
from iot.mqtt_client import MQTTClient
from devices.eeprom import EEPROM
from control.sensor_manager import SensorManager
from control.actuator_manager import ActuatorManager

class IoTBehavior:
    def __init__(self):
        """Initialize IoT devices, Wi-Fi, MQTT, and Device Control."""
        self.sensors = SensorManager()
        self.actuator_manager = ActuatorManager()
        self.eeprom = EEPROM()  
        self.mode = self.eeprom.read_mode()  

        # ✅ Wi-Fi & MQTT
        self.wifi = WiFi()
        if self.wifi.connect():
            self.mqtt = MQTTClient(self)
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
        self.actuator_manager.set_display(temp, moisture, None)
        self.actuator_manager.adjust_sunscreen(temp)
        self.actuator_manager.set_watering(moisture < 25)

    def manual_mode(self):
        """Only listen for MQTT commands to control actuators."""
        print("🛠️ Manual mode active. Waiting for actuator control commands...")

    def update_system(self):
        """Read sensors and apply automation rules based on mode."""
        temp, hum, moisture_level = self.sensors.read_sensors()

        if self.mode == "automate":
            self.automate_mode(temp, moisture_level)
        else:
            self.manual_mode()
