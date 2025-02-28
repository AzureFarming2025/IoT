from machine import Pin
import dht
import time

DHT_PIN = 32
dht_sensor = dht.DHT11(Pin(DHT_PIN))

def read_dht():
    """Reads temperature and humidity from DHT11 sensor."""
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print(f"🌡 Temp: {temp}°C, 💧 Humidity: {hum}%")
        return temp, hum
    except Exception as e:
        print("❌ DHT Read Error:", e)
        return None, None
