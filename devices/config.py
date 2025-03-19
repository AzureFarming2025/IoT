# ------------------------------
# Sensor & Actuator Configuration
# ------------------------------

CONFIG = {
    "I2C_FREQ": 400000,
    "OLED_WIDTH": 128,
    "OLED_HEIGHT": 64,
    "NUM_PIXELS": 16
}

# ------------------------------
# Hardware Pin Assignments
# ------------------------------

HARDWARE_PINS = {
    "DHT": 27,
    "I2C_SCL": 15,
    "I2C_SDA": 2,
    "SOIL_MOISTURE": 25,
    "WATER_SERVO": 12,
    "SUNSCREEN_SERVO": 13,
    "RELAY": 2,
    "BUZZER": 14,
    "BUTTON": 33,
    "NEOPIXEL": 18
}

# ------------------------------
# LED COLOR PRESETS
# ------------------------------

LED_COLORS = {
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "off": (0, 0, 0)
}