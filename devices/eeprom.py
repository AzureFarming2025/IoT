import machine

class EEPROM:
    def __init__(self, address=0):
        """Initialize EEPROM storage (simulated with RTC memory)."""
        self.rtc = machine.RTC()
        self.address = address

    def read_mode(self):
        """Read mode from EEPROM (default: automate)."""
        try:
            mode = self.rtc.memory().decode()  # Read stored mode
            if mode in ["automate", "manual"]:
                return mode
        except Exception:
            pass
        return "automate"  # Default mode

    def write_mode(self, mode):
        """Write mode to EEPROM."""
        self.rtc.memory(mode.encode())
