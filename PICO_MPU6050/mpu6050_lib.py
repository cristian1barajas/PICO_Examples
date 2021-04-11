# mpu6050

from machine import Pin, I2C
import time
import utime



class mpu6050:
   
   
    # MPU6050 registers

    SMPLRT_DIV     = 0x19     
    CONFIG         = 0x1A     
    GYRO_CONFIG    = 0x1B      
    ACCEL_CONFIG   = 0x1C       
    ACCEL_XOUT_H   = 0x3B
    ACCEL_XOUT_L   = 0x3C
    ACCEL_YOUT_H   = 0x3D
    ACCEL_YOUT_L   = 0x3E
    ACCEL_ZOUT_H   = 0x3F
    ACCEL_ZOUT_L   = 0x40
    TEMP_OUT_H     = 0x41
    TEMP_OUT_L     = 0x42
    GYRO_XOUT_H    = 0x43
    GYRO_XOUT_L    = 0x44    
    GYRO_YOUT_H    = 0x45
    GYRO_YOUT_L    = 0x46
    GYRO_ZOUT_H    = 0x47
    GYRO_ZOUT_L    = 0x48
    PWR_MGMT_1     = 0x6B  
   
    # i2c_adr = 0x68
    #----------------------------------------------------------
    def __init__(self, i2c, i2c_adr):
        
        self.i2c = i2c;
        self.i2c_adr = i2c_adr;
        self.write_reg(self.PWR_MGMT_1, 0x00)
        utime.sleep_ms(1)
        self.write_reg(self.GYRO_CONFIG, 0x00)  # Setting the gyro to full scale +/- 250deg./s 
        self.write_reg(self.ACCEL_CONFIG, 0x00) # Setting the accel to +/- 2g

    #----------------------------------------------------------
    def write_reg(self, reg, value):  
        self.i2c.writeto_mem(self.i2c_adr, reg, bytes([value]) )  
 
    # Request Accel Registers (3B - 40)
    #----------------------------------------------------------
    def read_AccelRegisters(self):  
        v = self.i2c.readfrom_mem(self.i2c_adr, self.ACCEL_XOUT_H, 6)
        valueX = v[0] << 8  | v[1]
        valueY = v[2] << 8  | v[3]
        valueZ = v[4] << 8  | v[5]
        
        #debug
        #print("AccelRegisters")
        #for i in range(6):
        #    print("V[ ] = {0:02X}".format(v[i]))
        
        # convert to negative
        if (valueX > 0x8000):
            valueX =  valueX - 65536
        if (valueY > 0x8000):
            valueY =  valueY - 65536
        if (valueZ > 0x8000):
            valueZ =  valueZ - 65536
  
        # for +/- 2g
        d = dict()
        d['ax'] = valueX / 16384.0; # LSB Sensitivity
        d['ay'] = valueY / 16384.0; # LSB Sensitivity
        d['az'] = valueZ / 16384.0; # LSB Sensitivity 
        return d

    # Request Accel Registers (0x43 - 0x48)
    #----------------------------------------------------------
    def read_GyroRegisters(self):      
        v = self.i2c.readfrom_mem(self.i2c_adr, self.GYRO_XOUT_H, 6)
        valueX = v[0] << 8  | v[1]
        valueY = v[2] << 8  | v[3]
        valueZ = v[4] << 8  | v[5]
        
        #debug
        #print("GyroRegisters")
        #for i in range(6):
        #    print("V[ ] = {0:02X}".format(v[i]))
        
        # convert to negative
        if (valueX > 0x8000):
            valueX =  valueX - 65536
        if (valueY > 0x8000):
            valueY =  valueY - 65536
        if (valueZ > 0x8000):
            valueZ =  valueZ - 65536
   
        # for +/- 250 deg/s
        d = dict()
        d['gx'] = valueX / 131.0; # LSB Sensitivity
        d['gy'] = valueY / 131.0; # LSB Sensitivity
        d['gz'] = valueZ / 131.0; # LSB Sensitivity 
        return d
  
if __name__ == "__main__":
    i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000) #100kHz
    print(i2c.scan())
    MPU6050_I2C_ADR = 0x68
    mpu_sensor = mpu6050(i2c, MPU6050_I2C_ADR)
    dict_accel = mpu_sensor.read_AccelRegisters()
    dict_gyro  = mpu_sensor.read_GyroRegisters()
    print("Accl : x={0:.2f}, y={1:.2f}, z={2:.2f}".format(dict_accel['ax'], dict_accel['ay'],dict_accel['az']))
    print("Gyro : x={0:.2f}, y={1:.2f}, z={2:.2f}".format(dict_gyro['gx'], dict_gyro['gy'],dict_gyro['gz']))

    
    







