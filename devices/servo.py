from machine import Pin, PWM

class ServoMotor:
    def __init__(self, pin):
        """Initialize a servo motor on the given pin."""
        self.servo = PWM(Pin(pin), freq=50)

    def set_angle(self, angle):
        """Set servo angle (0-180 degrees)."""
        self.servo.duty(int(40 + (angle / 180) * 115))
