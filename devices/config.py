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
    "DHT": 22,
    "I2C_SCL": 15,
    "I2C_SDA": 2,
    "SOIL_MOISTURE_LDR": 32,
    "LIGHT_LDR": 33,
    "WATER_PUMP": 12,
    "LOCK_SERVO": 13,
    "RGB_R": 26,
    "RGB_G": 25,
    "RGB_B": 27,
    "BUZZER": 14,
    "NEOPIXEL": 4,
    # "RELAY": 2,
    # "BUTTON": 33,
}

# ------------------------------
# LED COLOR PRESETS
# ------------------------------

AUTOMATE_LED_PRESETS = {
    "seedling": {
        "color": (0, 0, 255),     # Blue
        "brightness": 0.3        
    },
    "growth": {
        "color": (0, 255, 128),   # Cyan-Green
        "brightness": 0.6         
    },
    "vegetative": {
        "color": (0, 255, 0),     # Green
        "brightness": 0.8        
    },
    "pre-flower": {
        "color": (255, 255, 0),   # Yellow
        "brightness": 0.7         
    },
    "flower": {
        "color": (255, 0, 255),   # Purple
        "brightness": 1.0        
    },
    "full-spectrum": {
        "color": (255, 255, 255), # White
        "brightness": 0.8         
    },
    "stress-warning": {
        "color": (255, 0, 0),     # Red
        "brightness": 0.5         
    }
}
