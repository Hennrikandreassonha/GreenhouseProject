from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

lcd = I2cLcd(i2c, 39, 2, 16)
print(i2c.scan())
weather = '%s%sC' % (str(11), chr(223))
lcd.backlight_on()
print("hi")
while True:
    lcd.putstr("Fukt jord:  1000\n")
    lcd.putstr("Ljusstyrka: 1000")

    sleep(5)
    lcd.clear()

    lcd.putstr("Temperatur: 33" + chr(223) + "C")
    lcd.putstr("Fuktighet:  55%")
    sleep(5)
    lcd.clear()