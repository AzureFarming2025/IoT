from machine import Pin, ADC, PWM, I2C
import time
import dht
import ssd1306  # ✅ Updated import
from neopixel import NeoPixel

# PIN DECLARATION
soil_moisture = ADC(Pin(12))
soil_moisture.atten(ADC.ATTN_11DB)
dht_sensor = dht.DHT22(Pin(13))
i2c = I2C(scl=Pin(23), sda=Pin(22))

# ✅ Fixed OLED Initialization
oled = ssd1306.SSD1306_I2C(128, 64, i2c) 

water_servo = PWM(Pin(25), freq=50)
sunscreen_servo = PWM(Pin(32), freq=50)
relay = Pin(2, Pin.OUT)
BUZZER = PWM(Pin(14, Pin.OUT))
button = Pin(33, Pin.IN, Pin.PULL_UP)

# NeoPixel Setup
neo_pixel_pin = Pin(15)
num_pixels = 16  # Adjust based on your NeoPixel meter
np = NeoPixel(neo_pixel_pin, num_pixels)

rainbow = [
    (126, 1, 0), (114, 13, 0), (102, 25, 0), (90, 37, 0),
    (78, 49, 0), (66, 61, 0), (54, 73, 0), (42, 85, 0),
    (30, 97, 0), (18, 109, 0), (6, 121, 0), (0, 122, 5),
    (0, 110, 17), (0, 98, 29), (0, 86, 41), (0, 74, 53)
]

def set_neopixel_color(color):
    for i in range(num_pixels):
        np[i] = color
    np.write()

def rainbow_effect():
    for _ in range(10):
        for i in range(num_pixels):
            np[i] = rainbow[i % len(rainbow)]
        np.write()
        time.sleep(0.1)

def set_water_servo_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    water_servo.duty(duty)

def set_sunscreen_servo_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    sunscreen_servo.duty(duty)

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
    set_neopixel_color((255, 0, 0))  # Red Indicator
    set_water_servo_angle(90)
    relay.on()

def control_sunscreen(temperature):
    if temperature < 35:
        set_sunscreen_servo_angle(0)
    elif temperature < 37:
        set_sunscreen_servo_angle(45)
    else:
        set_sunscreen_servo_angle(90)

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
        if moisture_level > 75:
            set_neopixel_color((0, 0, 255))  # Blue
            set_water_servo_angle(0)
            relay.off()
            oled.text("Soil Too Wet.", 12, 30)
            oled.text("No Watering", 18, 40)
            oled.text("Needed", 35, 50)
        elif moisture_level > 50:
            set_neopixel_color((0, 255, 0))  # Green
            set_water_servo_angle(0)
            relay.off()
            oled.text("Optimal Moisture", 0, 40)
            oled.text("level.", 40, 50)
        elif moisture_level > 25:
            set_neopixel_color((255, 255, 0))  # Yellow
            set_water_servo_angle(45)
            relay.on()
            oled.text("Soil Moisture Low.", 0, 30)
            oled.text("Watering in", 18, 40)
            oled.text("Progress.", 25, 50)
        else:
            rainbow_effect()
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
