from machine import Pin
import dht

class DHTSensor:
    def __init__(self, pin):
        """Initialize the DHT sensor."""
        self.sensor = dht.DHT22(Pin(pin))

    def read(self):
        """Read temperature and humidity from the sensor."""
        try:
            self.sensor.measure()
            return self.sensor.temperature(), self.sensor.humidity()
        except Exception as e:
            print(f"[ERROR] DHT Read Failed: {e}")
            return None, None
