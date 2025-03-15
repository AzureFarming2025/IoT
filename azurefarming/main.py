print("Hello, ESP32!")

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
