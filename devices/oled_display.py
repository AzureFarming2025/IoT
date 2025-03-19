from machine import Pin, SoftI2C
from lib.ssd1306 import SSD1306_I2C

class OLEDDisplay:
    def __init__(self, scl_pin, sda_pin, width=128, height=64, freq=400000):
        """Initialize OLED display with I2C."""
        try:
            i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
            self.oled = SSD1306_I2C(width, height, i2c)
        except Exception as e:
            print(f"[ERROR] Failed to initialize OLED: {e}")
            self.oled = None

    def update(self, temp, hum, moisture):
        """Update OLED display with temperature & humidity."""
        if not self.oled:
            print("[WARNING] OLED is not initialized.")
            return
        self.oled.fill(0)
        self.oled.text(f"Temp: {temp:.1f}C" if temp else "Sensor Error!", 8, 10)
        self.oled.text(f"Hum: {hum:.1f}%" if hum else "", 8, 20)
        self.oled.text(f"Moisture: {moisture:.1f}%" if hum else "", 8, 30)
        self.oled.show()
