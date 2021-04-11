#=================================================================
# Project : blinking led
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
led = Pin(16, Pin.OUT)

while (True):
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
