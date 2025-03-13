# Virtualization & Simulation Plan  

https://wokwi.com/projects/425327218373883905

We initially used **Proteus 8** to validate circuit connections and power but didn’t test the code there.  
To better match our **breadboard setup** and validate the code, we’ll now use **Wokwi**, leveraging custom chips to replicate actual device behavior.  

#### **Next Steps**  
- **Leander** will handle the **device connections**.  
- **SAN** will integrate them with the **Azure-connected handler**.  

#### **Notes**  
- Previously, **Wokwi’s limited device support** was a blocker.  
- We found a way to **add custom chips**, ensuring correct pin configuration and behavior.  
- This will bring the simulation **closer to real hardware operation**.


# 🚀 ESP32 MicroPython & Azure IoT Setup Guide

This guide provides step-by-step instructions to set up MicroPython on an ESP32 board and connect it to Azure IoT. It covers macOS and Windows environments, including using the Pymakr plugin and Azure IoT Explorer.

---

## 📌 1. Prerequisites
- **Python 3.x** installed ([python.org](https://www.python.org/downloads/))
- **VSCode** with **Pymakr plugin** installed
- **ESP32 DOIT DevKit v1**
- **Azure IoT Hub** set up with a registered device

---

## 💻 2. Install MicroPython on ESP32 (macOS/Windows)

### 2.1 Install `esptool.py`
```bash
pip install esptool
```

### 2.2 Erase Flash Memory
```bash
esptool.py --port COM3 erase_flash  # Use '/dev/tty.usbserial-0001' for macOS
```

### 2.3 Flash MicroPython Firmware
Download from [MicroPython](https://micropython.org/download/esp32/).
```bash
esptool.py --port COM3 --baud 115200 write_flash -z 0x1000 firmware/ESP32_GENERIC-20241129-v1.24.1.bin
```

---

## 🧩 3. Set Up Pymakr Plugin (VSCode)
### 3.1 Install Pymakr Plugin
- Open **VSCode** > Extensions > Search `Pymakr` > Install
- **Copy plugin settings** from the repository.

### 3.2 Create `pymakr.conf`

🚨 I already setted up pymakr configuration file.

```json
{
  "address": "COM3",
  "auto_connect": true,
  "sync_folder": "src"
}
```

### 3.3 Test Connection with ESP32
```bash
mpremote connect COM3
>>> print("Hello, MicroPython!")
```

---

## ☁️ 4. Connect to Azure IoT Hub (Windows)
### 4.1 Install Azure IoT Explorer
- Download from [Azure IoT Explorer](https://github.com/Azure/azure-iot-explorer/releases).

### 4.2 Get Device Connection String (SAS Token)
- Log in to **Azure Portal** > IoT Hub > Devices > Select Device > **Generate SAS Token**
- Copy the connection string.

### 4.3 Send Telemetry from ESP32
```python
import urequests
url = "https://<your-iot-hub>.azure-devices.net/devices/<device-id>/messages/events?api-version=2020-09-30"
headers = {
    "Authorization": "SharedAccessSignature sr=<sas-uri>&sig=<signature>&se=<expiry>&skn=<policy>"
}
response = urequests.post(url, json={"temperature": 23.5}, headers=headers)
print(response.status_code)
```

---

## 📝 Notes
- Confirm `COM` port on Windows using `Device Manager`.
- For macOS, replace `COM3` with `/dev/tty.usbserial-0001`.
- Share this repository with your friend for the exact environment setup.

🚀 Happy Coding!