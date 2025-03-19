from devices.config import HARDWARE_PINS, LED_COLORS
from devices.servo import ServoMotor
from devices.relay import Relay
from devices.neopixel_led import NeoPixelLED
from devices.buzzer import Buzzer
from devices.oled_display import OLEDDisplay

class ActuatorManager:
    def __init__(self):
        """Initialize all actuator devices separately."""
        self.water_servo = ServoMotor(HARDWARE_PINS["WATER_SERVO"])
        self.sunscreen_servo = ServoMotor(HARDWARE_PINS["SUNSCREEN_SERVO"])
        self.relay = Relay(HARDWARE_PINS["RELAY"])
        self.np = NeoPixelLED(HARDWARE_PINS["NEOPIXEL"], 16)
        self.oled = OLEDDisplay(HARDWARE_PINS["I2C_SCL"], HARDWARE_PINS["I2C_SDA"])
        self.buzzer = Buzzer(HARDWARE_PINS["BUZZER"])

    # 🚰 Water System Control
    def set_watering(self, state):
        """Turn water system ON (90°) or OFF (0°)."""
        angle = 90 if state else 0
        self.water_servo.set_angle(angle)
        print(f"🚰 Watering {'ON' if state else 'OFF'}")

    # 🌞 Sunscreen Adjustment
    def adjust_sunscreen(self, temperature):
        """Adjust sunscreen position based on temperature."""
        angle = 0 if temperature < 35 else 45 if temperature < 37 else 90
        self.sunscreen_servo.set_angle(angle)
        print(f"🌞 Sunscreen adjusted to {angle}°")

    # ⚡ Relay Toggle
    def toggle_relay(self, state):
        """Turn relay ON or OFF."""
        self.relay.toggle(state)
        print(f"⚡ Relay {'ON' if state else 'OFF'}")

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
        :param color_name: Name of the color (from config)
        :param brightness: Optional brightness scale (0.0 - 1.0)
        """
        self.np.set_color(color_name, brightness)
    
    # 🔆 Adjust Brightness
    def set_led_brightness(self, brightness):
        """
        Adjust LED brightness without changing color.
        :param brightness: Brightness scale (0.0 - 1.0)
        """
        self.np.set_brightness(brightness)

    # 📟 OLED Display Update
    def set_display(self, temp, hum, moisture):
        """Display sensor data on OLED."""
        self.oled.update(temp, hum, moisture)
        print(f"🌡 Temp: {temp}°C | 💧 Humidity: {hum}% | 🌱 Soil Moisture: {moisture}%")
