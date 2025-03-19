from machine import Pin
from time import sleep
import dht 

led = Pin(19, Pin.OUT)
sensor = dht.DHT22(Pin(32))

while True:
   
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        if temp > 25.0:
            led.value(1)
        else:
            led.value(0)
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        print('Failed to read sensor.')