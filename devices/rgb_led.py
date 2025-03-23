from machine import Pin

class RgbStatusLed:
    def __init__(self, r_pin, g_pin, b_pin, active_low=False):
        self.red = Pin(r_pin, Pin.OUT)
        self.green = Pin(g_pin, Pin.OUT)
        self.blue = Pin(b_pin, Pin.OUT)
        self.active_low = active_low
        self.show_status("off")

    def _apply(self, val):
        return not val if self.active_low else val

    def set_color(self, red=False, green=False, blue=False):
        self.red.value(self._apply(red))
        self.green.value(self._apply(green))
        self.blue.value(self._apply(blue))

    def show_status(self, status):
        status_map = {
            "off": (1, 1, 1),        # All off
            "ok": (1, 0, 1),         # Green ON
            "error": (0, 1, 1),      # Red ON
            "wait": (1, 1, 0),       # Blue ON
            "warning": (0, 0, 1),    # Yellow = Red + Green
        }
        r, g, b = status_map.get(status.lower(), (0, 0, 0))
        self.set_color(r, g, b)
        print(f"📍 Status LED: {status.upper()}")
