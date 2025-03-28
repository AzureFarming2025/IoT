import sys
sys.path.append("/remote")
sys.path.append("/remote/iot")
sys.path.append("/remote/control")
sys.path.append("/remote/lib")
sys.path.append("/remote/devices")

import time
from control.sensor_manager import SensorManager
from control.actuator_manager import ActuatorManager

def run_sensor_test(sensors):
    """🔍 Test sensor readings only."""
    print("\n🔬 Running Sensor Test...")
    temp, hum, moisture, light = sensors.read_sensors()
    print(f"🌡 Temp: {temp}°C | 💧 Humidity: {hum}% | 🌱 Soil Moisture: {moisture}% | 🔅 Light: {light}%")

def run_actuator_test(actuators):
    """🛠 Test actuator functions separately."""
    print("\n⚙️ Running Actuator Test...")

    # Test Water System
    print("🚰 Testing Watering System...")
    actuators.set_watering()
    # Test Relay
    print("⚡ Testing Lock servo...")
    actuators.set_lock(True)
    time.sleep(2)
    actuators.set_lock(False)

    # Test LEDs
    # print("💡 Testing LED Colors...")
    # actuators.set_led_color("red", brightness=0.8)
    # time.sleep(1)
    # actuators.set_led_color("green", brightness=0.5)
    # time.sleep(1)
    # actuators.set_led_color("yellow", brightness=0.3)
    # time.sleep(1)
    # actuators.set_led_color("off")

    # Test Buzzer
    print("🔊 Testing Buzzer...")
    actuators.beep(2)

def run_full_test():
    """🔄 Run full test: Sensor + Actuator."""
    print("🔬 Starting Full Sensor & Actuator Test...\n")

    # ✅ Initialize Sensors & Actuators
    sensors = SensorManager()
    actuators = ActuatorManager()

    while True:
        try:
            # ✅ Read Sensor Data
            temp, hum, moisture, light = sensors.read_sensors()
            actuators.set_display(temp, hum, moisture, light)

            # ✅ Actuator Control Testing
            if moisture < 25:
                actuators.set_watering(True)
            elif moisture > 75:
                actuators.set_watering(False)

            # ✅ LED & Buzzer Alerts
            if moisture < 25:
                actuators.set_led_color("red", brightness=0.9)  # Red LED (Dry)
                actuators.beep(1)
            elif moisture > 50:
                actuators.set_led_color("green", brightness=0.7)  # Green LED (Optimal)
            else:
                actuators.set_led_color("yellow", brightness=0.5)  # Yellow LED (Low moisture)
            time.sleep(5)  # Refresh cycle

        except KeyboardInterrupt:
            print("\n🛑 Test Stopped. Cleaning up...")
            actuators.set_led_color("off")
            actuators.set_watering(False)
            actuators.toggle_relay(False)
            break

# ===========================
# 🏁 SELECT TEST MODE
# ===========================
if __name__ == "__main__":
    print("\n🔍 Choose Test Mode:")
    print("1️⃣ Sensor Test")
    print("2️⃣ Actuator Test")
    print("3️⃣ Full System Test")
    
    choice = input("\nEnter option (1/2/3): ").strip()

    sensors = SensorManager()
    actuators = ActuatorManager()

    if choice == "1":
        run_sensor_test(sensors)
    elif choice == "2":
        run_actuator_test(actuators)
    elif choice == "3":
        run_full_test()
    else:
        print("❌ Invalid choice. Exiting...")
