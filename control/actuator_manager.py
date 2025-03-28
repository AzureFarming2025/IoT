from devices.config import HARDWARE_PINS, AUTOMATE_LED_PRESETS
from devices.servo import ServoMotor
from devices.water_pump import WaterPumpRelay
from devices.neopixel_led import NeoPixelLED
from devices.buzzer import Buzzer
from devices.oled_display import OLEDDisplay
from devices.rgb_led import RgbStatusLed
import time

class ActuatorManager:
    def __init__(self):
        """Initialize all actuator devices separately."""
        self.lock_servo = ServoMotor(HARDWARE_PINS["LOCK_SERVO"])
        self.water_pump = WaterPumpRelay(HARDWARE_PINS["WATER_PUMP"])
        self.np = NeoPixelLED(HARDWARE_PINS["NEOPIXEL"], 16)
        self.oled = OLEDDisplay(HARDWARE_PINS["I2C_SCL"], HARDWARE_PINS["I2C_SDA"])
        self.buzzer = Buzzer(HARDWARE_PINS["BUZZER"])
        self.rgb_led = RgbStatusLed(
            HARDWARE_PINS["RGB_R"],
            HARDWARE_PINS["RGB_G"],
            HARDWARE_PINS["RGB_B"],
        )
        self.current_stage = None

    # 🔒 Lock System Control
    def set_lock(self, state):
        """Turn lock system ON (90°) or OFF (0°)."""
        angle = 90 if state else 0
        self.lock_servo.set_angle(angle)
        print(f"🔒 Status :  {'LOCKED' if state else 'UNLOCKED'}")

    # 🚰 Relay Toggle
    def set_watering(self, state):
        """Turn water system ON or OFF."""
        if state:
            self.water_pump.on()
            time.sleep(2.0)
            self.water_pump.off()
            print(f"🚰 Watering Done!")
        else:
            self.water_pump.off()
            print(f"🚰 Watering OFF!")

    # 🔊 Buzzer Beep
    def beep(self, times=3):
        """Trigger buzzer beep multiple times."""
        for _ in range(times):
            self.buzzer.beep()
        print("🔊 Buzzer activated")

    # 💡 LED Color Control
    def set_led_color(self, color_name, brightness=None):
        """
        Set NeoPixel LED to a predefined color with brightness adjustment.
        :param color_name: rgb color tuple
        :param brightness: Optional brightness scale (0.0 - 1.0)
        """
        self.np.set_color(color_name, brightness)

    def set_led_preset(self, stage_name):
        """
        Set NeoPixel LED to plant growth stage preset.
        :param stage_name: One of AUTOMATE_LED_PRESETS keys
        """
        if stage_name not in AUTOMATE_LED_PRESETS:
            print(f"❌ Invalid stage name: '{stage_name}'. Skipping LED preset.")
            return
        preset = AUTOMATE_LED_PRESETS[stage_name]
        self.np.set_color(preset["color"], preset["brightness"])
        self.current_stage = stage_name
        print(f"🌿 LED set to {stage_name} preset.")


    def adjust_preset_brightness_with_light(self, light_level):
        """
        Adjust brightness of the current preset color based on external light level.
        Uses the target brightness of the current growth stage.

        :param light_level: Ambient light percentage (0~100)
        """
        if not self.current_stage or self.current_stage not in AUTOMATE_LED_PRESETS:
            print("⚠️ No preset set. Skipping LED adjustment.")
            return
        preset = AUTOMATE_LED_PRESETS[self.current_stage]
        target_brightness = preset["brightness"]
        # Assume ideal lux corresponds to full brightness of preset
        target_lux = target_brightness * 100

        if light_level >= target_lux:
            self.np.turn_off()
            print("☀️ External light sufficient. LED turned off.")
        else:
            # Adjust proportionally up to preset brightness
            brightness = max(0.2, min(preset["brightness"], (target_lux - light_level) / target_lux * preset["brightness"]))
            self.set_led_color(preset["color"], brightness=brightness)
            print(f"💡 Adjusted preset color brightness to {brightness:.2f} based on light level: {light_level}%")

    # 🔆 Adjust Brightness
    def set_led_brightness(self, brightness):
        """
        Adjust LED brightness without changing color.
        :param brightness: Brightness scale (0.0 - 1.0)
        """
        self.np.set_brightness(brightness)

    # 📟 OLED Display Update
    def set_display(self, temp, hum, moisture, light):
        """Display sensor data on OLED."""
        self.oled.update(temp, hum, moisture, light)
        # print(f"🌡 Temp: {temp}°C | 💧 Humidity: {hum}% | 🌱 Soil Moisture: {moisture}% | 🔅 Light: {light}%")

    # 📍 RGB Status LED Control
    def set_status(self, status):
        """Set RGB LED status (e.g., 'ok', 'error', 'wait', etc.)."""
        self.rgb_led.show_status(status)

    # 🌱 Smart Auto LED logic based on light sensor value (now just adjusts brightness)
    def smart_plant_led(self, light):
        """
        Adjust current preset LED brightness dynamically based on ambient light.
        """
        self.adjust_preset_brightness_with_light(light)