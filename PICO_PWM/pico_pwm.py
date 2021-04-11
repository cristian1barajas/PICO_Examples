#=================================================================
# Project : PWM
#         : Read a value from the ADC0 and output PWM to drive a LED
# Date    : 2021-02-01
# Version : 1.0
#
# Note:
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY : without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
#
# Board : Raspberry Pi Pico
#
#=================================================================
from machine import Pin, PWM, ADC
from time import sleep

pwm_led = PWM(Pin(15))
pwm_led.freq(1000)
adc0 = ADC(Pin(26))

while True:
    value = adc0.read_u16()
    pwm_led.duty_u16(value)
    print(value)    
    sleep(0.1)
        

 

