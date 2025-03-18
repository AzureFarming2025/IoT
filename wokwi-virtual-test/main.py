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

from machine import Pin, ADC, PWM, I2C
import time 
import dht
from neopixel import NeoPixel
import ssd1306

# **🔹 Pin Definitions**
PIN_DHT = 27           # DHT22 (Temperature & Humidity Sensor)
PIN_SOIL = 26         # Soil Moisture Sensor (Analog)
PIN_LDR = 25          # Light Sensor (Analog)
PIN_SERVO_LOCKER = 13 # Servo Motor for Locker
PIN_SERVO_PUMP = 12   # Servo Motor for Water Pump
PIN_NEOPIXEL = 18     # NeoPixel LED Ring

# **🔹 Initialize Sensors**
dht_sensor = dht.DHT22(Pin(PIN_DHT))  
soil_sensor = ADC(Pin(PIN_SOIL))     
soil_sensor.atten(ADC.ATTN_11DB)     
ldr_sensor = ADC(Pin(PIN_LDR))       
ldr_sensor.atten(ADC.ATTN_11DB)      

# **🔹 Initialize Actuators**
servo_locker = PWM(Pin(PIN_SERVO_LOCKER), freq=50)  
servo_pump = PWM(Pin(PIN_SERVO_PUMP), freq=50)      
neo_ring = NeoPixel(Pin(PIN_NEOPIXEL), 16)  
      

# **🔹 OLED Display Setup**
i2c = I2C(0, scl=Pin(15), sda=Pin(2)) 
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  

# **🔹 Set Servo Angle**
def set_servo_angle(servo, angle):
    duty = int((angle / 180) * 65535 / 10) + 1638  
    servo.duty_u16(duty)

# **🔹 Read Sensor Data**
def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        soil_moisture = soil_sensor.read()
        light_level = ldr_sensor.read()
        return temp, hum, soil_moisture, light_level
    except Exception as e:
        print("Sensor Error:", e)
        return None, None, None, None

# **🔹 Update OLED Display**
def update_oled(temp, hum, soil, light):
    oled.fill(0)
    oled.text(f"T:{temp}C", 0, 0)
    oled.text(f"H:{hum}%", 0, 10)
    oled.text(f"S:{soil}", 0, 20)
    oled.text(f"L:{light}", 0, 30)
    oled.show()

# **🔹 Control NeoPixels Based on Light Intensity**
def control_neopixels(state):
    color = (0, 255, 0) if state else (255, 0, 0)  
    for i in range(16):  
        neo_ring[i] = (color[0], color[1], color[2])  
    neo_ring.write()

# **🔹 Control Water Pump Based on Soil Moisture**
def control_pump(soil):
    if soil < 2000:
        set_servo_angle(servo_pump, 90)
        print("Water Pump: ON")
    else:
        set_servo_angle(servo_pump, 0)
        print("Water Pump: OFF")

# **🔹 Process Serial Commands for Manual Control**
def process_command(command):
    global servo_locker
    command = command.strip().lower()

    if command == "pump on":
        set_servo_angle(servo_pump, 90)
        print("Water Pump: ON")
    elif command == "pump off":
        set_servo_angle(servo_pump, 0)
        print("Water Pump: OFF")
    elif command.startswith("locker "):
        try:
            angle = int(command.split()[1])
            if 0 <= angle <= 180:
                set_servo_angle(servo_locker, angle)
                print(f"Locker Set to: {angle}°")
            else:
                print("Error: Angle must be 0-180")
        except ValueError:
            print("Error: Invalid angle format")
    else:
        print("Unknown command. Available commands: pump on, pump off, locker <angle>")

# **🔹 Main Execution Loop**
def main():
    while True:
        temp, hum, soil, light = read_sensors()

        if temp is not None:
            update_oled(temp, hum, soil, light)

        # Automatic Control Logic
        control_pump(soil)  
        control_neopixels(light < 1000)  

        # Read Serial Input for Manual Control
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip()
            process_command(user_input)

        time.sleep(2)

# **🔹 Run the Program**
main()
