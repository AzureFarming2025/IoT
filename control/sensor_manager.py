import time

from devices.config import HARDWARE_PINS
from devices.dht_sensor import DHTSensor
from devices.ldr import LDRSensor

class SensorManager:
    def __init__(self):
        """Initialize all sensors separately."""
        self.dht_sensor = DHTSensor(HARDWARE_PINS["DHT"])
        self.soil_sensor = LDRSensor(HARDWARE_PINS["SOIL_MOISTURE_LDR"])
        self.light_sensor = LDRSensor(HARDWARE_PINS["LIGHT_LDR"])

    def read_sensors(self):
        """Read all sensor values and return them."""
        temp, hum = self.dht_sensor.read()
        moisture = self.soil_sensor.read()
        light = self.light_sensor.read()
        return temp, hum, moisture, light

