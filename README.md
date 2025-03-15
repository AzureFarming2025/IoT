
# 🚀 ESP32 MicroPython & Azure IoT Quick Setup  

This guide covers **MicroPython setup on ESP32**, **Wokwi simulation**, and **Azure IoT connection**.

## ⚡ Wokwi + ESP32 Simulation  

**1️⃣ Install `mpremote`**  
```bash
pip install mpremote
```

**2️⃣ Run the Simulation**

This should be **done** **before** connecting the source code.

1. Open `diagram.json` in Wokwi
2. Click **"Simulate"**

**3️⃣ Connect Source code to Wokwi**

```bash
python -m mpremote connect port:rfc2217://localhost:4000 run wokwi-virtual-test/main.py

```
This enables real-time testing in Wokwi.


---
## 🚀 Virtualization & Simulation Plan  

🔗 [**Wokwi Simulation Project (Initial Setup)**](https://wokwi.com/projects/425327218373883905)

→ Clone this as the **initial setup** to work locally on `Wokwi for vscode`. (Check the `wokwi-virtual-test` directory in this repo for updates.)

We initially used **Proteus 8** for circuit validation but didn’t test the code there.  
Now, to better match our **breadboard setup**, we’ll use **Wokwi** for **circuit simulation and code validation** before moving to hardware. 

### 🔹 Using Custom Chips in Wokwi  

Wokwi supports many **common components**, but if a needed chip **isn’t available**, we can create a **custom chip** to mimic its behavior.  

Ideally, create **separate Wokwi projects** for each custom chip on website and **compile them individually**.  

- Define **pin mappings & specs** based on [Wokwi docs](https://docs.wokwi.com/chips-api/chip-json).  
- Generate **JSON config** and **c** file using GPT based on datasheets.  

- For vscode(local) testings, the chip should be compiled: [Custom chip compiler](https://github.com/wokwi/wokwi-chip-clang-action)

- Simulate **sensor values & interactions** for testing.  

Custom chips **aren’t the main focus**, but they help **fill hardware gaps** in the virtual environment.


---

## 📌 ESP32 MicroPython Setup

**1️⃣ Prerequisites**

- **Python 3.x** → [Download](https://www.python.org/downloads/)
- **VSCode** with **Pymakr plugin**
- **ESP32 DOIT DevKit v1**
- **Azure IoT Hub** with a registered device


**2️⃣ Flash MicroPython Firmware**

```bash
pip install esptool
esptool --port COM3 erase_flash  # Use 'esptool.py' and '/dev/tty.usbserial-0001' for macOS  
esptool --port COM4 --baud 115200 write_flash -z 0x1000 firmware/ESP32_GENERIC-20241129-v1.24.1.bin
```

**3️⃣ Set Up Pymakr in VSCode**

- Install **Pymakr Plugin** → **Extensions > Search "Pymakr" > Install**
- Create `pymakr.conf` *(already in repo)*:

  ```bash
  {
    "address": "COM3",
    "auto_connect": true,
    "sync_folder": "src"
  }
  ```
---

## ☁️ Connect to Azure IoT Hub

**1️⃣ Install Azure IoT Explorer**

🔗 [Download](https://github.com/Azure/azure-iot-explorer/releases)

**2️⃣ Get Device Connection String (SAS Token)**

- **Easiest:** Use **Azure IoT Hub** VSCode extension to copy/generate it.
- **Alternative:**
    - **Azure Portal** → IoT Hub → Devices → Select Device → **Generate SAS Token**
    - Copy the connection string.

**3️⃣ Send Telemetry from ESP32**

```python
import urequests

url = "https://<your-iot-hub>.azure-devices.net/devices/<device-id>/messages/events?api-version=2020-09-30"
headers = {
    "Authorization": "SharedAccessSignature sr=<sas-uri>&sig=<signature>&se=<expiry>&skn=<policy>"
}
response = urequests.post(url, json={"temperature": 23.5}, headers=headers)
print(response.status_code)

```