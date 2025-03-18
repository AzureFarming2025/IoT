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

#from machine import Pin, ADC, PWM, I2C
#import time 
#mport dht
#from neopixel import NeoPixel
#import ssd1306 

# **🔹 Pin Definitions**
""" PIN_DHT = 27           # DHT22 (Temperature & Humidity Sensor)
PIN_SOIL = 26         # Soil Moisture Sensor (Analog)
PIN_LDR = 25          # Light Sensor (Analog)
PIN_SERVO_LOCKER = 13 # Servo Motor for Locker
PIN_SERVO_PUMP = 12   # Servo Motor for Water Pump
PIN_NEOPIXEL = 18     # NeoPixel LED Ring

# **🔹 Initialize Sensors**
#dht_sensor = dht.DHT22(Pin(PIN_DHT))  
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
main()"""
print("=====================\n")
print("Program: Automatic Water Flow for Home Gardeners Controlled by Irrigation System  ")
print("Date: ../11/24")
print("Created by: Khairul Iman Bin Zakaria")
print("\n=====================\n")

# IMPORT LIBRARY/MODULE
from machine import Pin, ADC, PWM, I2C
import time
import dht
import OLED_LIB


# PIN DECLARATION
soil_moisture = ADC(Pin(12))
soil_moisture.atten(ADC.ATTN_11DB)
dht_sensor = dht.DHT22(Pin(13))
i2c = I2C(scl=Pin(23), sda=Pin(22))
oled = OLED_LIB.SSD1306_I2C(128, 64, i2c)
water_servo = PWM(Pin(25), freq=50)
sunscreen_servo = PWM(Pin(32), freq=50)
relay = Pin(2, Pin.OUT)
leds = {
    "blue": Pin(19, Pin.OUT),
    "green": Pin(27, Pin.OUT),
    "yellow": Pin(26, Pin.OUT),
    "red": Pin(4, Pin.OUT)
}
BUZZER = PWM(Pin(14, Pin.OUT))
button = Pin(33, Pin.IN, Pin.PULL_UP)


# FOR SERVO (Water Flow)
def set_water_servo_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    water_servo.duty(duty)


# FOR SERVO (Sunscreen)
def set_sunscreen_servo_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    sunscreen_servo.duty(duty)


# FOR INDICATORS LED
def turn_off_leds():
    for led in leds.values():
        led.off()


# FOR BYPASS BUTTON
def button_behavior():
    oled.fill_rect(0, 30, 128, 34, 0)
    oled.text("Watering in", 18, 40)
    oled.text("progress.", 25, 50)
    oled.show()
    for i in range(3):
        BUZZER.freq(700)
        BUZZER.duty(70)
        time.sleep(0.5)
        BUZZER.duty(0)
        time.sleep(0.5)
    for _ in range(3):
        leds["red"].on()
        time.sleep(0.5)
        leds["red"].off()
        time.sleep(0.5)
    leds["red"].on()
    set_water_servo_angle(90)
    relay.on()


# PROGRAM FOR SUNSCREEN SHADE NET
def control_sunscreen(temperature):
    if temperature <35 :  
        set_sunscreen_servo_angle(0)  
    elif temperature <37:  
        set_sunscreen_servo_angle(45)  
    else:  
        set_sunscreen_servo_angle(90)  


# MAIN PROGRAM
while True:
    moisture_level = soil_moisture.read() / 4095 * 100
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    

    oled.fill(0)
    oled.text("Moisture: {:.1f}%".format(moisture_level), 0, 0)
    oled.text("Temp: {:.1f}C".format(temperature), 0, 10)
    

    
    control_sunscreen(temperature)

    if button.value() == 0:
        button_behavior()
    else:
        oled.fill_rect(0, 30, 128, 34, 0)
        turn_off_leds()
        if moisture_level > 75:
            leds["blue"].on()
            set_water_servo_angle(0)
            relay.off()
            oled.text("Soil Too Wet.", 12, 30)
            oled.text("No Watering", 18, 40)
            oled.text("Needed", 35, 50)
        elif moisture_level >50:
            leds["green"].on()
            set_water_servo_angle(0)
            relay.off()
            oled.text("Optimal Moisture", 0, 40)
            oled.text("level.", 40, 50)
        elif moisture_level >25:
            leds["yellow"].on()
            set_water_servo_angle(45)
            relay.on()
            oled.text("Soil Moisture Low.", 0, 30)
            oled.text("Watering in", 18, 40)
            oled.text("Progress.", 25, 50)
        else:
            leds["red"].on()
            for i in range(3):
                BUZZER.freq(700)
                BUZZER.duty(70)
                time.sleep(0.5)
                BUZZER.duty(0)
                time.sleep(0.5)

            
            set_water_servo_angle(90)
            relay.on()
            oled.text("Soil too dry.", 13, 30)
            oled.text("Watering in", 18, 40)
            oled.text("progress.", 25, 50)

    oled.show()
    time.sleep(1)









