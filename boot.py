import network
from mysecrets import secrets
import time
import ntptime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets['wifi-ssid'], secrets['wifi-password'])
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

ntptime.settime()
print(time.localtime())
