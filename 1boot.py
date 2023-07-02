import network
from mysecrets import secrets
import time
import ntptime
import machine

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets['wifi-ssid'], secrets['wifi-password'])
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

try:
    ntptime.settime()

except Exception as e:
    print(f'Failed to set time: {e}')
    machine.reset()
    time.sleep(1)

print(time.localtime())