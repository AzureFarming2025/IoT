from machine import Pin, SoftI2C
from lib.ssd1306 import SSD1306_I2C

class OLEDDisplay:
    def __init__(self, scl_pin, sda_pin, width=128, height=64, freq=400000):
        """Initialize OLED display via I2C interface."""
        try:
            i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
            self.oled = SSD1306_I2C(width, height, i2c)
        except Exception as e:
            print(f"[ERROR] Failed to initialize OLED: {e}")
            self.oled = None

    def draw_icon(self, x, y, pattern):
        """
        Draw an 8x8 bitmap icon on the OLED display at (x, y).
        :param x: Horizontal position
        :param y: Vertical position
        :param pattern: List of 8 bytes representing the bitmap
        """
        for row in range(8):
            line = pattern[row]
            for col in range(8):
                pixel_on = (line >> (7 - col)) & 0x01
                self.oled.pixel(x + col, y + row, pixel_on)

    def update(self, temp, hum, moisture, light):
        """Update the OLED screen with sensor data and icons."""
        if not self.oled:
            print("[WARNING] OLED is not initialized.")
            return

        # Fallback values if sensors fail
        temp = temp or 0.0
        hum = hum or 0.0
        moisture = moisture or 0.0
        light = light or 0.0

        self.oled.fill(0)

        # 8x8 icons (each row is a byte in binary)
        icon_temp = [0x18, 0x18, 0x18, 0x18, 0x5A, 0x7E, 0x3C, 0x18]
        icon_hum  = [0x10, 0x28, 0x44, 0x82, 0x82, 0x44, 0x28, 0x10]
        icon_soil = [0x00, 0x42, 0x24, 0x18, 0x18, 0x24, 0x42, 0x00]
        icon_light= [0x18, 0x3C, 0x7E, 0xDB, 0x7E, 0x3C, 0x18, 0x00]

        # Draw icons and text
        self.draw_icon(0, 0, icon_temp)
        self.oled.text(f"{temp:.1f}C", 12, 0)

        self.draw_icon(0, 16, icon_hum)
        self.oled.text(f"{hum:.1f}%", 12, 16)

        self.draw_icon(0, 32, icon_soil)
        self.oled.text(f"{moisture:.1f}%", 12, 32)

        self.draw_icon(0, 48, icon_light)
        self.oled.text(f"{light:.1f}%", 12, 48)

        self.oled.show()
