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

try:
    while True:
        
        tempSensor.measure()
        tempValue = tempSensor.temperatue()
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
        
        print(f'Publish light:{tempValue}')
        print(f'Publish temp:{humidValue}')
        print(f'Publish humid:{lightValue}')

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