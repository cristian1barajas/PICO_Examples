#=================================================================
# Project : MPU6050 sensor
#		 : 
# Date	: 2021-02-01
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
from mpu6050_lib import mpu6050

# The PCF8574= 0x27, PCF8574A = 0x3f  
DEFAULT_I2C_ADDR = 0x27

#=================================================================

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) #100kHz
lcd = I2cLcd(i2c ,DEFAULT_I2C_ADDR,4, 20)
lcd.move_to(0,0)
lcd.putstr("MPU6050 demo")
utime.sleep_ms(3000)

MPU6050_I2C_ADR = 0x68
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000) #100kHz
mpu6050_sensor = mpu6050(i2c1, MPU6050_I2C_ADR)
lcd.clear()
lcd.move_to(4,0)
lcd.putstr("Accel")
lcd.move_to(13,0)
lcd.putstr("Gyro")
blankstr = "                    "

while (True):
    dict_accel = mpu6050_sensor.read_AccelRegisters()
    dict_gyro  = mpu6050_sensor.read_GyroRegisters()

    lcd.move_to(0,1)
    lcd.putstr(blankstr)
    lcd.move_to(0,1)
    lcd.putstr("X : {0:.2f}".format(dict_accel['ax']))
    lcd.move_to(13,1)
    lcd.putstr("{0:.2f}".format(dict_gyro['gx']))
    lcd.move_to(0,2)
    lcd.putstr(blankstr)
    lcd.move_to(0,2)
    lcd.putstr("Y : {0:.2f}".format(dict_accel['ay']))
    lcd.move_to(13,2)
    lcd.putstr("{0:.2f}".format(dict_gyro['gy']))
    lcd.move_to(0,3)
    lcd.putstr(blankstr)
    lcd.move_to(0,3)
    lcd.putstr("Z : {0:.2f}".format(dict_accel['az']))
    lcd.move_to(13,3)
    lcd.putstr("{0:.2f}".format(dict_gyro['gz']))

    utime.sleep_ms(250)


