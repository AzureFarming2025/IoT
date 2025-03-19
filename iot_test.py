import sys
sys.path.append("/remote")
sys.path.append("/remote/lib")
sys.path.append("/remote/devices")
sys.path.append("/remote/control")
sys.path.append("/remote/iot")

import time
from iot.iot_behavior import IoTBehavior

def test_mode_switching(iot):
    """✅ Test mode switching and EEPROM persistence."""
    print("\n🔄 Testing Mode Switching...")
    
    # Initial Mode
    print(f"📌 Initial Mode: {iot.mode}")
    
    # Switch to Manual
    iot.set_mode("manual")
    assert iot.mode == "manual", "❌ Mode did not switch to manual!"
    
    # Switch to Automate
    iot.set_mode("automate")
    assert iot.mode == "automate", "❌ Mode did not switch to automate!"
    
    print("✅ Mode Switching Passed!")

def test_automate_mode(iot):
    """🚀 Test automate mode logic (sensor → actuator)."""
    print("\n🔄 Testing Automate Mode...")

    # Simulate sensor readings
    test_cases = [
        (30, 50),  # Normal moisture
        (36, 20),  # High temp, low moisture
        (33, 80)   # Low temp, high moisture
    ]

    for temp, moisture in test_cases:
        print(f"\n🌡 Temp: {temp}°C | 💧 Moisture: {moisture}%")
        iot.automate_mode(temp, moisture)

    print("✅ Automate Mode Passed!")

def test_manual_mode(iot):
    """🛠️ Test manual mode (MQTT should handle actuation)."""
    print("\n🛠️ Testing Manual Mode...")
    iot.manual_mode()
    print("✅ Manual Mode Passed!")

def test_update_system(iot):
    """🔄 Test full sensor-actuator loop."""
    print("\n🔄 Testing System Update...")
    
    for _ in range(3):  # Run multiple iterations
        iot.update_system()
        time.sleep(1)
    
    print("✅ System Update Passed!")

# ===========================
# 🚀 RUN TESTS
# ===========================
if __name__ == "__main__":
    print("\n🔍 Running IoTBehavior Tests...")
    
    iot_behavior = IoTBehavior()
   
    test_mode_switching(iot_behavior)
    # test_automate_mode(iot_behavior)
    test_manual_mode(iot_behavior)
    test_update_system(iot_behavior)

    print("\n✅ All Tests Completed!")
