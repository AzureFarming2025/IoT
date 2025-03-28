from machine import Pin
from neopixel import NeoPixel
import time

class NeoPixelLED:
    RAINBOW_COLORS = [
    (255, 0, 0),      # Red
    (255, 128, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 255, 255),    # Cyan
    (0, 0, 255),      # Blue
    (128, 0, 255),    # Indigo
    (255, 0, 255),    # Magenta
    (255, 255, 255),  # White flash
    (0, 0, 0),        # Off (blink effect)
    ]
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
        self.rainbow_effect(self.RAINBOW_COLORS)
        self.turn_off()

    def _apply_brightness(self, color):
        """Apply brightness scaling to an RGB color."""
        return tuple(int(c * self.brightness) for c in color)

    def set_color(self, color_rgb, brightness=None):
        """
        Set all NeoPixels to a specific color with optional brightness override.

        :param color_rgb: RGB tuple (e.g., (255, 0, 0)) or a string "(255,0,0)"
        :param brightness: Optional override for brightness (0.0 - 1.0)
        """
        # Convert string to tuple if necessary
        if isinstance(color_rgb, str):
            try:
                color_rgb = tuple(int(x.strip()) for x in color_rgb.strip("()").split(","))
            except Exception as e:
                print(f"❌ Failed to parse color string '{color_rgb}': {e}")
                return
        # Validate RGB tuple
        if not isinstance(color_rgb, tuple) or len(color_rgb) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color_rgb):
            print(f"❌ Invalid color format: {color_rgb}. Expected RGB tuple.")
            return
        # Clamp brightness
        if brightness is not None:
            self.brightness = max(0.0, min(1.0, brightness))
        adjusted_color = self._apply_brightness(color_rgb)
        for i in range(self.num_pixels):
            self.np[i] = adjusted_color
        self.np.write()
        print(f"💡 LED set to {color_rgb} at {self.brightness * 100:.0f}% brightness")

    def set_brightness(self, brightness):
        """
        Update brightness level dynamically and reapply current color.
        
        :param brightness: Brightness scale (0.0 - 1.0)
        """
        self.brightness = max(0.0, min(1.0, brightness))
        self.set_color("white")  # Apply new brightness with a default color
        print(f"🌟 Brightness set to {self.brightness * 100:.0f}%")

    def rainbow_effect(self, colors=None, delay_ms=0.1, brightness=None):
        """
        Rotate rainbow effect through all NeoPixels.
        
        :param colors: List of RGB tuples
        :param delay: Time delay between transitions
        :param brightness: Optional brightness scale
        """
        if brightness is not None:
            self.brightness = max(0.0, min(1.0, brightness))
        if colors is None:
            colors = self.RAINBOW_COLORS
        color_buffer = colors[:]
        for _ in range(50):  # Number of cycles
            for i in range(self.num_pixels):
                self.np[i] = self._apply_brightness(color_buffer[i % len(color_buffer)])
            self.np.write()
            time.sleep(delay_ms / 1000)  # Convert milliseconds to seconds
            # Rotate color list to create movement
            color_buffer = color_buffer[1:] + color_buffer[:1]


    def turn_off(self):
        """Turn off all LEDs."""
        self.set_color((0,0,0))
