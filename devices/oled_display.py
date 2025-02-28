from machine import Pin, SPI
import time

import sys
import os
# Add lib/ to the module search path
sys.path.append("/lib")
# Import the SH1106 module
from sh1106 import SH1106_SPI

# SPI Configuration
SPI_SCK = 18
SPI_MOSI = 23
SPI_MISO = 19  # Not used in SPI OLED

spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))

# OLED Display Pins
OLED_DC = Pin(13)
OLED_RST = Pin(14)
OLED_CS = Pin(12)

def init_oled():
    """Initialize SH1106 OLED display."""
    OLED_RST.init(OLED_RST.OUT)
    OLED_RST.value(0)
    time.sleep(0.1)
    OLED_RST.value(1)
    time.sleep(0.1)

    return SH1106_SPI(128, 64, spi, OLED_DC, OLED_RST, OLED_CS)

oled = init_oled()

def update_display(temp, hum):
    """Update OLED with sensor readings."""
    oled.fill(0)
    if temp is not None and hum is not None:
        oled.text(f"Temp: {temp}C", 10, 10)
        oled.text(f"Hum: {hum}%", 10, 25)
    else:
        oled.text("Sensor Error!", 10, 10)
    oled.show()
