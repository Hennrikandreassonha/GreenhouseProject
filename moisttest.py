import machine
from lib.stemma_soil_sensor import StemmaSoilSensor
import time
SDA_PIN = 0 # update this
SCL_PIN = 1 # update this

i2c = machine.I2C(0, sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000)
print(i2c.scan())
seesaw = StemmaSoilSensor(i2c)

# get moisture
moisture = seesaw.get_moisture()

# get temperature
temperature = seesaw.get_temp()

#SCL ÄR GRÖN
#SDA ÄR VIT

while True:
    print (seesaw.get_moisture())
    print (seesaw.get_temp())
    time.sleep(1)