
import time

from periphery import I2C

# Open i2c-0 controller
i2c = I2C("/dev/i2c-1")
# Read byte at address 0x100 of EEPROM at 0x50

try:
    while True:
        msgs = [I2C.Message([0x00, 0x00], read=True)]
        i2c.transfer(0x4d, msgs)
        data = msgs[0].data
        number = (data[0] << 6) | (data[1] >> 2)
        print("Result: %i/1024" % number)
        time.sleep(0.25)
finally:
    i2c.close()
