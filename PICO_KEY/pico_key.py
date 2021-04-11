#=================================================================
# Project : Key input
#         : 
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
from machine import Pin
from time import sleep

# define LED : GP16
builtin_led = Pin(25, Pin.OUT)
led = Pin(16, Pin.OUT)
key = Pin(17, Pin.IN, Pin.PULL_UP)
builtin_led.high()
led.high()

while (True):
    if (key.value()==0):
        sleep(0.05) # 50ms
        led.toggle()
        while(True):
            if (key.value()==1):
                break
        sleep(0.05)
        

 

