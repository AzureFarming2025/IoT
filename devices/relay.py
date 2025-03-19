from machine import Pin

class Relay:
    def __init__(self, pin):
        """Initialize the relay."""
        self.relay = Pin(pin, Pin.OUT)

    def toggle(self, state):
        """Turn relay ON (True) or OFF (False)."""
        self.relay.value(state)
