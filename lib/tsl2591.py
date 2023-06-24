import time
from machine import I2C

INTEGRATIONTIME_100MS = 0x00
INTEGRATIONTIME_200MS = 0x01
INTEGRATIONTIME_300MS = 0x02
INTEGRATIONTIME_400MS = 0x03
INTEGRATIONTIME_500MS = 0x04
INTEGRATIONTIME_600MS = 0x05

TSL2591_ADDR = 0x29
TSL2591_COMMAND_BIT = 0xA0
TSL2591_REGISTER_ENABLE = 0x00
TSL2591_REGISTER_CONTROL = 0x01
TSL2591_REGISTER_CHAN0_LOW = 0x14
TSL2591_REGISTER_CHAN1_LOW = 0x16

TSL2591_INTEGRATIONTIME_100MS = 0x00
GAIN_LOW = 0x00
GAIN_MED = 0x10
GAIN_HIGH = 0x20
GAIN_MAX = 0x30

ADDR = 0x29
READBIT = 0x01
COMMAND_BIT = 0xA0
CLEAR_BIT = 0x40
WORD_BIT = 0x20
BLOCK_BIT = 0x10
ENABLE_POWERON = 0x01
ENABLE_POWEROFF = 0x00
ENABLE_AEN = 0x02
ENABLE_AIEN = 0x10
CONTROL_RESET = 0x80
LUX_DF = 408.0
LUX_COEFB = 1.64
LUX_COEFC = 0.59
LUX_COEFD = 0.86

SENSOR_ADDRESS=0x29

class TSL2591:
    def __init__(self, i2c, addr=TSL2591_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.integration_time = TSL2591_INTEGRATIONTIME_100MS
        self.gain = GAIN_MED
        self.enable()

    def enable(self):
        self.i2c.writeto_mem(self.addr, TSL2591_REGISTER_ENABLE | TSL2591_COMMAND_BIT, bytearray([0x03]))

    def disable(self):
        self.i2c.writeto_mem(self.addr, TSL2591_REGISTER_ENABLE | TSL2591_COMMAND_BIT, bytearray([0x00]))

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time
        self.update_config()

    def set_gain(self, gain):
        self.gain = gain
        self.update_config()

    def update_config(self):
        config = (self.integration_time | self.gain)
        self.i2c.writeto_mem(self.addr, TSL2591_REGISTER_CONTROL | TSL2591_COMMAND_BIT, bytearray([config]))

    def read_word(self, register):
        data = self.i2c.readfrom_mem(self.addr, register | TSL2591_COMMAND_BIT, 2)
        value = data[1] << 8 | data[0]
        return value

    def get_luminosity(self):
        channel0 = self.read_word(TSL2591_REGISTER_CHAN0_LOW)
        channel1 = self.read_word(TSL2591_REGISTER_CHAN1_LOW)
        return channel0, channel1

    def calculate_lux(self, channel0, channel1):
        channel0 = float(channel0)
        channel1 = float(channel1)

        if channel0 == 0:
            return 0

        ratio = channel1 / channel0

        if ratio <= 0.50:
            lux = (0.0304 * channel0) - (0.062 * channel0 * (ratio**1.4))
        elif ratio <= 0.61:
            lux = (0.0224 * channel0) - (0.031 * channel1)
        elif ratio <= 0.80:
            lux = (0.0128 * channel0) - (0.0153 * channel1)
        elif ratio <= 1.30:
            lux = (0.00146 * channel0) - (0.00112 * channel1)
        else:
            lux = 0

        return lux

    def get_lux(self):
        channel0, channel1 = self.get_luminosity()
        lux = self.calculate_lux(channel0, channel1)
        return lux