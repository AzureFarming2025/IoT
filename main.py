# 🚨 MicroPython umqtt.simple + SSL wrap_socket 적용
# ✅ MicroPython 환경 전용 Azure IoT Hub 연결 예제 (ssl.wrap_socket 사용)

import network
import time
import ujson
from umqtt.simple import MQTTClient
import ssl
import socket

WIFI_SSID = "DLive_5F4A"
WIFI_PASSWORD = "62CEED5F49"

# ✅ Azure IoT Hub 설정
IOT_HUB_NAME = "SmartFarm"
IOT_HUB_DEVICE_ID = "test_arduino"
IOT_HUB_SAS_TOKEN = "SharedAccessSignature sr=SmartFarm.azure-devices.net%2Fdevices%2Ftest_arduino&sig=CcUPchgnvxk5Gg%2BlFujn69IDmdjlPDtvk6%2BqHoylf3o%3D&se=1739483764"

# ✅ Wi-Fi 연결
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 15
    while not sta_if.isconnected() and timeout > 0:
        print("⏳ Connecting to Wi-Fi...")
        time.sleep(1)
        timeout -= 1

    if sta_if.isconnected():
        print(f"✅ Wi-Fi connected! IP: {sta_if.ifconfig()[0]}")
        return True
    else:
        print("❌ Wi-Fi connection failed!")
        return False
        
# ✅ MQTT 연결 (ssl.wrap_socket 대체)
def connect_mqtt():
    try:
        sock = socket.socket()
        addr = socket.getaddrinfo(f"{IOT_HUB_NAME}.azure-devices.net", 8883)[0][-1]
        sock.connect(addr)
        ssl_sock = ssl.wrap_socket(sock)

        client = MQTTClient(
            client_id=IOT_HUB_DEVICE_ID,
            server=f"{IOT_HUB_NAME}.azure-devices.net",
            port=8883,
            ssl=False,  # `ssl`은 False로 두고, 아래에 직접 SSL 소켓 연결
            user=f"{IOT_HUB_NAME}.azure-devices.net/{IOT_HUB_DEVICE_ID}/?api-version=2021-04-12",
            password=IOT_HUB_SAS_TOKEN
        )
        # SSL 소켓을 클라이언트에 직접 할당
        client.sock = ssl_sock
        print("✅ Connected to Azure IoT Hub via MQTT with SSL!")
        return client
    except Exception as e:
        print(f"❌ MQTT connection failed: {e}")
        return None

# ✅ 메시지 전송
def send_messages(client):
    messages = ["Accio", "Aguamenti", "Alarte Ascendare", "Expecto Patronum", "Homenum Revelio"]
    for i, msg in enumerate(messages):
        try:
            topic = f"devices/{IOT_HUB_DEVICE_ID}/messages/events/"
            client.publish(topic, msg)
            print(f"📤 Sent message[{i}]: {msg}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to send message[{i}]: {e}")
            break

# 🟢 실행
if connect_wifi():
    mqtt_client = connect_mqtt()
    if mqtt_client:
        send_messages(mqtt_client)
    else:
        print("❌ MQTT connection error.")
else:
    print("❌ Wi-Fi connection error.")
