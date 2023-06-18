import dht
from machine import Pin
import machine
from lib.umqttsimple import MQTTClient
from SendEmail import send_email
from secrets import secrets
import json
import time

# import schedule

# For the Mqtt protocol.
mqtt_host = "io.adafruit.com"
mqtt_username = secrets['mqtt-username']
mqtt_password = secrets['mqtt-password']
mqtt_publish_temp = "Djhonk/feeds/Temp"
mqtt_publish_humid = "Djhonk/feeds/Humidity"
mqtt_publish_light = "Djhonk/feeds/Light"

mqtt_client_id = "Djhonkensid"

mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host,
    user=mqtt_username,
    password=mqtt_password)

mqtt_client.connect()

# Defining sensors
tempSensor = dht.DHT11(Pin(27))
photoResistor = machine.ADC(0)

button = machine.Pin(1)
previousDay = ""

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

button_pin.irq(trigger=Pin.IRQ_RISING, handler=change_screen_RGB)

try:
    while True:
        
        #Toggla RGB skärmen med en loop av något slag.
        if toggle:

            if(lamp.value() == 1):
                lamp.off()
            else:
                lamp.on()

        toggle = False
        lastValue = 0

        tempSensor.measure()
        tempValue = tempSensor.temperature()
        humidValue = tempSensor.humidity()
        lightValue = photoResistor.read_u16()

        currentDate = time.localtime()
        print(currentDate)
        hour = currentDate[3] + 2
        day = currentDate[2]

        if hour == 11 and day != previousDay:
          send_email("henrik1995a@live.se", tempValue, humidValue, 123, lightValue)
          previousDay = day

        if button.value() == 1:
            print("Button was pushed!")
        
        print(f'Publish light:{lightValue}')
        print(f'Publish temp:{tempValue}')
        print(f'Publish humid:{humidValue}')

        # Create a dictionary to represent the JSON payload
        tempPayload = {
            "temp": tempValue
        }
        humidPayload = {
            "humidity": humidValue
        }
        lightPayload = {
            "light": lightValue
        }

        json_humidPayload = json.dumps(humidPayload)
        json_tempPayload = json.dumps(tempPayload)
        json_lightPayload = json.dumps(lightPayload)

        mqtt_client.publish(mqtt_publish_humid, json_humidPayload)
        mqtt_client.publish(mqtt_publish_temp, json_tempPayload)
        mqtt_client.publish(mqtt_publish_light, json_lightPayload)

        time.sleep(15)

except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()