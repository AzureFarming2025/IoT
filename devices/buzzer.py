from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin):
        """Initialize the buzzer on the given pin."""
        self.buzzer = PWM(Pin(pin))

    def beep(self, freq=700, duration=0.5):
        """Make the buzzer beep at a given frequency and duration."""
        self.buzzer.freq(freq)
        self.buzzer.duty(70)
        time.sleep(duration)
        self.buzzer.duty(0)
