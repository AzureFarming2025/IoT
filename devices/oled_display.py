from machine import Pin, I2C
import time
import sys

# Add the 'lib' directory to the module search path
sys.path.append("/lib")

# Import SSD1306 OLED driver (Ensure ssd1306.py is in /lib/)
from ssd1306 import SSD1306_I2C

# I2C Configuration (Adjust these if using different GPIOs)
I2C_SCL = 22  # I2C Clock (SCL) - Default ESP32 SCL
I2C_SDA = 21  # I2C Data (SDA) - Default ESP32 SDA

# Initialize I2C interface
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)

# Initialize the OLED display
oled = SSD1306_I2C(128, 64, i2c)

def update_display(temp, hum):
    """Update OLED with temperature and humidity readings."""
    oled.fill(0)  # Clear screen
    if temp is not None and hum is not None:
        oled.text(f"Temp: {temp:.1f}C", 10, 10)  # Display temperature
        oled.text(f"Hum: {hum:.1f}%", 10, 25)   # Display humidity
    else:
        oled.text("Sensor Error!", 10, 10)  # Display error message
    oled.show()  # Refresh OLED screen
