import sys
sys.path.append("/remote")
sys.path.append("/remote/lib")
sys.path.append("/remote/devices")
sys.path.append("/remote/control")
sys.path.append("/remote/iot")

import time
from iot.iot_behavior import IoTBehavior

def main():
    iot = IoTBehavior()
    iot.set_mode("automate")  # automate
    
    print("🌐 Waiting for MQTT cloud messages... (manual mode)")

    while True:
        iot.update_system()
        time.sleep(1)

if __name__ == "__main__":
    main()
