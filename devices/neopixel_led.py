from machine import Pin
from neopixel import NeoPixel
import time
from devices.config import LED_COLORS

class NeoPixelLED:
    def __init__(self, pin, num_pixels, brightness=0.5):
        """
        Initialize NeoPixel strip with adjustable brightness.
        
        :param pin: GPIO pin connected to NeoPixel
        :param num_pixels: Number of LEDs in the strip
        :param brightness: Brightness scale (0.0 - 1.0)
        """
        self.np = NeoPixel(Pin(pin), num_pixels)
        self.num_pixels = num_pixels
        self.brightness = max(0.0, min(1.0, brightness))  # Clamp brightness

    def _apply_brightness(self, color):
        """Apply brightness scaling to an RGB color."""
        return tuple(int(c * self.brightness) for c in color)

    def set_color(self, color_name, brightness=None):
        """
        Set all NeoPixels to a specific color with optional brightness override.
        
        :param color_name: Name of the color (from config)
        :param brightness: Optional override for brightness (0.0 - 1.0)
        """
        if brightness is not None:
            self.brightness = max(0.0, min(1.0, brightness))  # Ensure valid range

        color = LED_COLORS.get(color_name, LED_COLORS["off"])
        adjusted_color = self._apply_brightness(color)

        for i in range(self.num_pixels):
            self.np[i] = adjusted_color
        self.np.write()
        print(f"💡 LED set to {color_name.upper()} at {self.brightness * 100:.0f}% brightness")

    def set_brightness(self, brightness):
        """
        Update brightness level dynamically and reapply current color.
        
        :param brightness: Brightness scale (0.0 - 1.0)
        """
        self.brightness = max(0.0, min(1.0, brightness))
        self.set_color("white")  # Apply new brightness with a default color
        print(f"🌟 Brightness set to {self.brightness * 100:.0f}%")

    def rainbow_effect(self, colors, delay=0.1, brightness=None):
        """
        Cycle through colors with brightness control.
        
        :param colors: List of RGB tuples
        :param delay: Time delay between transitions
        :param brightness: Optional brightness scale
        """
        if brightness is not None:
            self.brightness = max(0.0, min(1.0, brightness))  # Clamp brightness

        for _ in range(10):  # Repeat effect
            for i in range(self.num_pixels):
                self.np[i] = self._apply_brightness(colors[i % len(colors)])
            self.np.write()
            time.sleep(delay)

    def turn_off(self):
        """Turn off all LEDs."""
        self.set_color("off")
