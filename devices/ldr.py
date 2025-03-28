from machine import Pin, ADC

class LDRSensor:
    def __init__(self, pin):
        """Initialize the soil moisture sensor."""
        self.sensor = ADC(Pin(pin))
        self.sensor.atten(ADC.ATTN_11DB)

    def read(self):
        """Read soil moisture level and return percentage."""
        return self.sensor.read() / 4095 * 100
