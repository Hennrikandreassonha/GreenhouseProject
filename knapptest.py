from machine import Pin
import time

button_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)
lamp = Pin(15, mode=Pin.OUT)

toggle = False
lastValue = 0

def change_screen_RGB(pin):
    global lastValue, toggle
    if button_pin.value() != 0 and not lastValue == 1:
        print("Toggled")
        toggle = True
        lastValue = button_pin.value()

    
    # Perform the desired action when the button is pushed

button_pin.irq(trigger=Pin.IRQ_RISING, handler=change_screen_RGB)

while True:
    # Your existing code here...

    if toggle:
        print("inne i toggle")
        print (lamp.value())

        if(lamp.value() == 1):
            lamp.off()
        else:
            lamp.on()

        toggle = False
        lastValue = 0

    # Continue executing other tasks in the main loop
    print("looping")
    time.sleep(5)
