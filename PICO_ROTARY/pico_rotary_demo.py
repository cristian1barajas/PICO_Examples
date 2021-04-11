#=================================================================
# Project : Rotary demo
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

from machine import Pin,I2C, Timer, ADC
from i2c_lcd import I2cLcd
import time
import utime

# The PCF8574= 0x27, PCF8574A = 0x3f  
DEFAULT_I2C_ADDR = 0x3f

# define rotary module pin
sw = Pin(20, Pin.IN, Pin.PULL_UP)
b = Pin(19, Pin.IN)
a = Pin(18, Pin.IN)
 
    
MAX_MENU_ITEM = 3
MODE_MAIN_MENU  = 0
MODE_BRIGHTNESS = 1
MODE_CONTRAST   = 2
MODE_FREQUENCY  = 3
    
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) #100kHz
lcd = I2cLcd(i2c ,DEFAULT_I2C_ADDR,2, 16)
lcd.move_to(0,0)
lcd.putstr("Rotary demo")
utime.sleep_ms(2000)

prevState = a.value()
curState = a.value()
bUp = True
menuIdx = 0  
selIdx = 0 
mode = 0 
brightness = 8 
contrast   = 8 
freq    = 880 


#====================================================
def show_menu():    
    lcd.clear()
    
    if (mode == MODE_MAIN_MENU):
        if (selIdx==0):
            lcd.move_to(0,0)
            lcd.putstr("   Brightness")
            lcd.move_to(0,1)
            lcd.putstr("   Contrast")
        elif (selIdx==1):
            lcd.move_to(0,0)
            lcd.putstr("   Contrast")
            lcd.move_to(0,1)
            lcd.putstr("   Frequency")
        elif (selIdx==2):
            lcd.move_to(0,0)
            lcd.putstr("   Frequency")
            lcd.move_to(0,1)
            lcd.putstr("                ")
    
        lcd.move_to(0,0)
        lcd.putstr("->")
    
    elif (mode==MODE_BRIGHTNESS):
        lcd.move_to(0,0)
        lcd.putstr("   Brightness")
        lcd.move_to(7,1)
        lcd.putstr("{0:d}".format(brightness))

    elif (mode==MODE_CONTRAST):
        lcd.move_to(0,0)
        lcd.putstr("   Contrast")
        lcd.move_to(7,1)
        lcd.putstr("{0:d}".format(contrast))

    elif (mode==MODE_FREQUENCY):
        lcd.move_to(0,0)
        lcd.putstr("   Frequency")
        lcd.move_to(3,1)
        lcd.putstr("{0:.1f} MHz".format(freq/10))
 
#=========================================================== 
def Button_Handler():
    global mode
    
    if (mode == MODE_MAIN_MENU):
        if (selIdx==0):
            mode = MODE_BRIGHTNESS 
        elif (selIdx==1):
            mode = MODE_CONTRAST  
        else:  
            mode = MODE_FREQUENCY           
    
    else: # return to main menu
         mode = MODE_MAIN_MENU 
    show_menu()



#====================================================
def ChangeValue():
    global selIdx
    global brightness, contrast, freq

    if (mode == MODE_MAIN_MENU):
        if (bUp):
            if (selIdx != MAX_MENU_ITEM-1):
                selIdx = selIdx + 1
             
        else:
            if (selIdx !=0):
                selIdx = selIdx - 1
            
                 
    elif (mode == MODE_BRIGHTNESS):
        if (bUp):
            if (brightness != 15):
                brightness = brightness + 1
             
        else: 
            if (brightness !=0):
                brightness= brightness - 1
            
    
    elif  (mode == MODE_CONTRAST):
        if (bUp):
            if (contrast != 15):
                contrast= contrast + 1
            
        else: 
            if (contrast !=0):
                contrast= contrast - 1
           

    elif (mode == MODE_FREQUENCY):
        if (bUp):
            freq += 1
            if (freq == 1080) :
                freq = 880
           
        else:
            freq -= 1;
            if (freq == 879):
                freq = 1079
    show_menu()


#============================================================== 
show_menu() 
while (True):
    curState =  a.value() 

    if (prevState != curState and curState==0):
        if ( b.value() != curState):      
            bUp = True
        else:        
            bUp  = False
       
        if (bUp):
            print("Up")
        else :
            print("Down")
        ChangeValue()
        
    prevState = curState 
        
    if (sw.value() == 0): # pressed
        utime.sleep_ms(30)
        while (True):
            if (sw.value() == 1):
                break;
        utime.sleep_ms(30)   
        print("button pressed")
        Button_Handler()
 


