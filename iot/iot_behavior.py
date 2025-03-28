import time
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

    def automate_mode(self, temp, moisture, light):
        """Automatically control actuators based on environmental conditions."""
        self.actuators.set_display(temp, None, moisture, light)
        # 🚿 Water if soil is too dry
        if moisture < 25:
            self.actuators.set_watering(True)
        else:
            self.actuators.set_watering(False)
        # 💡 Smart LED behavior based on current light input
        self.actuators.smart_plant_led(light)
        # ✅ Status OK if everything completes
        self.actuators.set_status("ok")

    def manual_mode(self):
        """Listen for MQTT commands to control actuators in manual mode."""
        # print("🛠️ Manual mode active. Waiting for actuator control commands...")
        pass

    def route_command(self, payload):
        """Handle incoming MQTT C2D commands for manual mode."""
        try:
            print(f"📩 Received C2D message: {payload}")

            actuator = payload.get("actuator")
            value = payload.get("value") == "on"
            if actuator == "water" and self.mode == "manual":
                self.actuators.set_watering(value)
                print(f"💧 Watering system {'ON' if value else 'OFF'}")
            elif actuator == "lock":
                self.actuators.set_lock(value)
                print(f"🔒 Status :  {'LOCKED' if state else 'UNLOCKED'}")
            elif actuator == "led":
                color = payload.get("color", "off")
                if color == "preset":
                    if self.mode == "automate":
                        option = payload.get("option", "full-spectrum")
                        self.actuators.set_led_preset(option)
                    else:
                        print("❌ light preset not supported in manual mode!")
                elif self.mode == "manual":
                    brightness = payload.get("brightness", 0.5)
                    self.actuators.set_led_color(color, brightness)
                    print(f"💡 LED set to {color} (brightness: {brightness})")
            elif actuator == "rgb_led":
                state = payload.get("state", "off")
                self.actuators.set_status(state)
                print(f"💡 Status set to {state}")
            elif actuator == "buzzer":
                times = int(payload.get("times", 3))
                self.actuators.beep(times)
                print(f"🔊 buzzer played for {times} times.")
            else:
                print("❌ Unknown actuator command.")
        except Exception as e:
            print(f"❌ Failed to process C2D message: {e}")

    def update_system(self):
        """Read sensors, send telemetry, and apply automation rules."""
        while True:
            self.mqtt.client.check_msg()
            temp, hum, moisture, light = self.sensors.read_sensors()
            self.actuators.set_display(temp, hum, moisture, light)
            # ✅ Apply automation if enabled
            if self.mode == "automate":
                self.automate_mode(temp, moisture, light)
            else:
                self.manual_mode()
            time.sleep(2)
            # # ✅ Publish Telemetry Data every 5 seconds
            if self.mqtt:
                data = {
                    "temperature": temp,
                    "humidity": hum,
                    "moisture": moisture,
                    "light": light
                }
                self.mqtt.publish_telemetry(data)
                self.mqtt.update_device_twin(data)

            time.sleep(5)  # Telemetry interval