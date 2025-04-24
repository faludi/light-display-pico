from wifi_network import WiFi
from thingspeak import ThingSpeakApi
from time import sleep
from machine import Pin, PWM

field_num = 1
max_light = 3000 # ceiling for lux value
fade_iterations = 100 # steps to fade light over 5 seconds
sample_rate = 5 # sample rate in seconds

led_pwm = PWM(Pin(2), freq=300, duty_u16=0)
status_led = Pin("LED", Pin.OUT)

#ThingSpeak Initialization
thingspeak = ThingSpeakApi()

#Network Initialization
network = WiFi()
ip = network.connect()

#Main Program
last_light = light_output = 0
while True:
    res = thingspeak.read_single_field(field_num)
    status_led.on()
    sleep(0.1)
    status_led.off()
    light = float(res.json()[f'field{field_num}'])
    print("light:", light, "Lux")
    light_level = light/max_light * 65535
#     print("light out:", light_level)
    difference = light_level - last_light
    for iteration in range (fade_iterations):
        light_output += difference/fade_iterations
        sleep(5/fade_iterations)
        led_pwm.duty_u16(int(light_output))
    last_light = light_level
