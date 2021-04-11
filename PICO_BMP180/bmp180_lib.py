# bmp180_lib.py

from machine import Pin, I2C
import time
import utime



class BMP180:
   
       
    BMP085_ULTRALOWPOWER    =  0
    BMP085_STANDARD         =  1
    BMP085_HIGHRES          =  2
    BMP085_ULTRAHIGHRES     =  3
                            
    BMP085_CAL_AC1          =  0xAA  # Calibration data (16 bits)
    BMP085_CAL_AC2          =  0xAC  # Calibration data (16 bits)
    BMP085_CAL_AC3          =  0xAE  # Calibration data (16 bits)    
    BMP085_CAL_AC4          =  0xB0  # Calibration data (16 bits)
    BMP085_CAL_AC5          =  0xB2  # Calibration data (16 bits)
    BMP085_CAL_AC6          =  0xB4  # Calibration data (16 bits)
    BMP085_CAL_B1           =  0xB6  # Calibration data (16 bits)
    BMP085_CAL_B2           =  0xB8  # Calibration data (16 bits)
    BMP085_CAL_MB           =  0xBA  # Calibration data (16 bits)
    BMP085_CAL_MC           =  0xBC  # Calibration data (16 bits)
    BMP085_CAL_MD           =  0xBE  # Calibration data (16 bits)
                            
    BMP085_CONTROL          =  0xF4 
    BMP085_TEMPDATA         =  0xF6
    BMP085_PRESSUREDATA     =  0xF6
    BMP085_READTEMPCMD      =  0x2E
    BMP085_READPRESSURECMD  =  0x34

    oversampling = BMP085_ULTRAHIGHRES
    
    DEBUG          = 0
    USE_DS_PARA    = 0
   
    # i2c_adr = 0x77
    #----------------------------------------------------------
    def __init__(self, i2c, i2c_adr):
        
        self.i2c = i2c;
        self.i2c_adr = i2c_adr;
        self.read_calibration()
         

    #----------------------------------------------------------
    def write_reg(self, reg, value):  
        self.i2c.writeto_mem(self.i2c_adr, reg, bytes([value]) )  
 
    
    #----------------------------------------------------------
    def read_signed16(self, mem_loc):  
        v = self.i2c.readfrom_mem(self.i2c_adr, mem_loc,2)
        value  = v[0] << 8  | v[1]
       
        # convert to negative
        if (value >= 0x8000):
            value =  value - 65536
    
        return value
    
    #----------------------------------------------------------
    def read_unsigned8(self, mem_loc):  
        v = self.i2c.readfrom_mem(self.i2c_adr, mem_loc,1)
        return v[0]

    #----------------------------------------------------------
    def read_unsigned16(self, mem_loc):  
        v = self.i2c.readfrom_mem(self.i2c_adr, mem_loc,2)
        value  = v[0] << 8  | v[1]
        return value
    
    #----------------------------------------------------------
    def read_calibration(self):  
        self.ac1 = self.read_signed16(self.BMP085_CAL_AC1)
        self.ac2 = self.read_signed16(self.BMP085_CAL_AC2)
        self.ac3 = self.read_signed16(self.BMP085_CAL_AC3)
        self.ac4 = self.read_unsigned16(self.BMP085_CAL_AC4)
        self.ac5 = self.read_unsigned16(self.BMP085_CAL_AC5)
        self.ac6 = self.read_unsigned16(self.BMP085_CAL_AC6)
        self.b1  = self.read_signed16(self.BMP085_CAL_B1);
        self.b2  = self.read_signed16(self.BMP085_CAL_B2);
        self.mb  = self.read_signed16(self.BMP085_CAL_MB);
        self.mc  = self.read_signed16(self.BMP085_CAL_MC);
        self.md  = self.read_signed16(self.BMP085_CAL_MD);
  
        if (self.DEBUG==1):
            print("AC1 = {0:d}".format(self.ac1))
            print("AC2 = {0:d}".format(self.ac2))
            print("AC3 = {0:d}".format(self.ac3))
            print("AC4 = {0:d}".format(self.ac4))
            print("AC5 = {0:d}".format(self.ac5))
            print("AC6 = {0:d}".format(self.ac6))
            print("b1 = {0:d}".format(self.b1))
            print("b2 = {0:d}".format(self.b2))
            print("mb = {0:d}".format(self.mb))
            print("mc = {0:d}".format(self.mc))
            print("md = {0:d}".format(self.md))
            
    # return uint16_t        
    #----------------------------------------------------------
    def readRawTemperature(self): 
        self.write_reg(self.BMP085_CONTROL, self.BMP085_READTEMPCMD)
        utime.sleep_ms(5)
          
        rawtemp =   self.read_unsigned16(self.BMP085_TEMPDATA)
        if (self.DEBUG == 1):
            print("Raw temp : {0:d}".format(rawtemp))
            
        return rawtemp
   
    #----------------------------------------------------------
    def read_Temperature(self):
        UT = self.readRawTemperature();

       
        # use datasheet numbers!
        if (self.USE_DS_PARA==1):
            self.UT = 27898
            self.ac6 = 23153
            self.ac5 = 32757
            self.mc = -8711
            self.md = 2868
        
        self.B5 = self.computeB5(UT)
        temp = (self.B5+8) >> 4
        temp /= 10;
        return temp;

    #----------------------------------------------------------
    def computeB5(self, UT):
        X1 = (UT -  self.ac6) * ( self.ac5) >> 15
        X2 = ( self.mc << 11) / (X1+ self.md)
        b5 = int(X1 + X2)
        
        if (self.DEBUG==1):
            print("X1 = {0:d}".format(X1))
            print("X2 = {0:d}".format(int(X2)))
            print("b5 = {0:d}".format(b5))
       
        return b5
    
    #----------------------------------------------------------
    def readRawPressure(self):
        self.write_reg(self.BMP085_CONTROL, self.BMP085_READPRESSURECMD + (self.oversampling << 6))

        if (self.oversampling == self.BMP085_ULTRALOWPOWER): 
            utime.sleep_ms(5)
        elif  (self.oversampling == self.BMP085_STANDARD): 
            utime.sleep_ms(8)
        elif (self.oversampling == self.BMP085_HIGHRES) :
            utime.sleep_ms(14)
        else :
            utime.sleep_ms(26)

        raw = self.read_unsigned16(self.BMP085_PRESSUREDATA)
        raw <<= 8
        raw |= self.read_unsigned8(self.BMP085_PRESSUREDATA+2)
        raw >>= (8 - self.oversampling)
        
        if (self.DEBUG == 1):
            print("Raw pressure : {0:d}".format(raw))
        return raw
        

    #----------------------------------------------------------
    def readPressure(self):
        UT = self.readRawTemperature()
        UP = self.readRawPressure()
        
        # use datasheet numbers!
        if (self.USE_DS_PARA==1):
            UT = 27898
            UP = 23843
            self.ac6 = 23153
            self.ac5 = 32757
            self.mc = -8711
            self.md = 2868
            self.b1 = 6190
            self.b2 = 4
            self.ac3 = -14383
            self.ac2 = -72
            self.ac1 = 408
            self.ac4 = 32741
            self.oversampling = 0
 
        B5 = self.computeB5(UT);

        # do pressure calcs
        B6 = B5 - 4000
        X1 = ( self.b2 * ( (B6 * B6)>>12 )) >> 11
        X2 = ( self.ac2 * B6) >> 11
        X3 = int(X1 + X2)
        B3 = int(((( self.ac1 * 4 + X3) << self.oversampling) + 2) / 4)

        if (self.DEBUG==1):
            print("b5 = {0:d}".format(B5))
            print("b6 = {0:d}".format(B6))
            print("x1 = {0:d}".format(X1))
            print("x2 = {0:d}".format(X2))
            print("x3 = {0:d}".format(X3))
            print("b3 = {0:d}".format(int(B3)))
          
        X1 = ( self.ac3 * B6) >> 13;
        X2 = ( self.b1 * ((B6 * B6) >> 12)) >> 16;
        X3 = ((X1 + X2) + 2) >> 2;
        B4 = ( self.ac4 * (X3 + 32768)) >> 15;
        B7 = ( UP - B3) * ( 50000  >> self.oversampling );

        if (B7 < 0x80000000) :
            p = (B7 * 2) / B4;
        else: 
            p = (B7 / B4) * 2
  
        if (self.DEBUG==1):
            print("X1 = {0:d}".format(X1))
            print("X2 = {0:d}".format(X2))
            print("X3 = {0:d}".format(X3))
            print("B4 = {0:d}".format(B4))
            print("B7 = {0:d}".format(int(B7)))
        
        X1 = (int(p) >> 8) * ( int(p) >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * int(p)) >> 16

        if (self.DEBUG==1):
            print("p = {0:d}".format(int(p) ))
            print("X1 = {0:d}".format(X1))
            print("X2 = {0:d}".format(X2))


        p = p + ((X1 + X2 + 3791)>>4)
        
        if (self.DEBUG==1):
            print("p = {0:d}".format(int(p)))
 
        return int(p);


if __name__ == "__main__":
    i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000) #100kHz
    print(i2c.scan())
    BMP180_I2C_ADR = 0x77
    bmp180 = BMP180(i2c, BMP180_I2C_ADR)
    temp = bmp180.read_Temperature()
    print("Temp = {0:.1f}C".format( temp))
    p = bmp180.readPressure()
    print("Pressure = {0:.1f} Pa".format( p))
     

    
    








