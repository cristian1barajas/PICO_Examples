#=================================================================
# Project : BMP180 pressure sensor
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

from machine import Pin,I2C
from i2c_lcd import I2cLcd
import time
import utime
from bmp180_lib import BMP180

# The PCF8574= 0x27, PCF8574A = 0x3f  
DEFAULT_I2C_ADDR = 0x3f

#=================================================================

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) #100kHz
lcd = I2cLcd(i2c ,DEFAULT_I2C_ADDR,2,16)
lcd.move_to(0,0)
lcd.putstr("BMP180 demo")
utime.sleep_ms(3000)

BMP180_I2C_ADR = 0x77
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000) #100kHz
bmp180 = BMP180(i2c1, BMP180_I2C_ADR)
                   
while (True):
    temp = bmp180.read_Temperature()
    p = bmp180.readPressure()
    print("Temp = {0:.1f}C".format( temp))
    print("Pressure = {0:.1f} Pa".format( p))

    lcd.move_to(0,0)
    lcd.putstr("T : {0:.2f} C".format(temp))
    lcd.move_to(0,1)
    lcd.putstr("P : {0:d} Pa".format(p))
    
    utime.sleep_ms(500)



