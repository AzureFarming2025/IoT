from machine import Pin

class WaterPumpRelay:
    """Controls a water pump via relay."""
    def __init__(self, pin):
        self.relay = Pin(pin, Pin.OUT)
        self.off()

    def on(self):
        """Turn on for 2.5 seconds."""
        self.relay.value(1)
        print("Pump ON")

    def off(self):
        """Turn off the pump."""
        self.relay.value(0)
        print("Pump OFF")

    def toggle(self, state: bool):
        """Manual ON/OFF."""
        self.relay.value(1 if state else 0)
