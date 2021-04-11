#=================================================================
# Project : DHT11 Temperature & humidity sensor
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

from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time
import utime
from dht22 import  DHT22

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

#=================================================================

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000) #100kHz
lcd = I2cLcd(i2c ,DEFAULT_I2C_ADDR, 2, 16)
lcd.putstr("DHT22 Demo")

dht_data = Pin(28,Pin.IN,Pin.PULL_UP)
dht11 = DHT22(dht_data,None,dht11=False)

while True:
    t,h = dht11.read()
    if t is None:
        print(" sensor error")
    else:
        print("{:3.1f}'C  {:3.1f}%".format(t,h))
            
    lcd.move_to(0,1)
    s = "{0:.1f}C  {1:.1f}%".format(t,h)
    lcd.putstr(s)
    lcd.putstr(' ' * (16-len(s)) )
            
    #DHT22 not responsive if delay to short
    utime.sleep_ms(500)



