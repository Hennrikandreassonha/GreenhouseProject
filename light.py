from lib.tsl2591 import TSL2591
import machine
i2clight = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)

tsl = TSL2591(i2clight)  # initialize
lux = tsl.get_lux()

print(lux)