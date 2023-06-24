import network
from secrets import secrets
import time
import ntptime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Lennart', 'bastu2022')
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

ntptime.settime()