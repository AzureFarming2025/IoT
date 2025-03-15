# Execute this command under the path 'wokwi-virtual-test/' where main.py is in.
# python -m mpremote connect port:rfc2217://localhost:4000 run main.py


# soil_sensor = ADC(Pin(34))  # Analog pin for soil moisture sensor
# sensorValue = soil_sensor.read()
    
# STEP 1 : IMPORT MODULES OR LIBRARY
# from machine import Pin, I2C, ADC, PWM
# import ssd1306
# import time

# #STEP 2.2 : DECLARE THE CONNECTION OLED
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# #STEP 3 : THE PROCESS
# while True:
#     # Display the status on the OLED display
#     oled.fill(0)  # Clear the display
#     oled.text("Soil Moisture", 0, 0)
#     oled.text("Percentage: {}%".format(humidityPercent), 0, 20)
#     oled.show()

#     time.sleep(1)  # Delay before next reading cycle

from machine import Pin
from time import sleep
import dht 

print("Hello, ESP32!")

led = Pin(19, Pin.OUT)
sensor = dht.DHT22(Pin(27))

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
