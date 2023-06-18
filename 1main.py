import dht
from machine import Pin
import machine
from lib.umqttsimple import MQTTClient
from SendEmail import send_email
from secrets import secrets
import json
import time
import urequests

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
emailSent = False

try:
    while True:

        currentDate = time.localtime()
        day = currentDate[2]
        hour = currentDate[3]

        if hour == 18 and not emailSent:
            send_email("henrik1995a@live.se", "123","123","123","123")
            emailSent = True

        if button.value() == 1:
            print("Button was pushed!")
        
        tempSensor.measure()
        print(f'Publish light:{photoResistor.read_u16():.2f}')
        print(f'Publish temp:{tempSensor.temperature():.2f}')
        print(f'Publish humid:{tempSensor.humidity():.2f}')

        # Create a dictionary to represent the JSON payload
        humidPayload = {
            "humidity": tempSensor.humidity()
        }
        tempPayload = {
            "temp": tempSensor.temperature()
        }
        lightPayload = {
            "light": photoResistor.read_u16()
        }

        # Convert the payload dictionary to a JSON string
        json_humidPayload = json.dumps(humidPayload)
        json_tempPayload = json.dumps(tempPayload)
        json_lightPayload = json.dumps(lightPayload)

        # Publish the JSON payload
        mqtt_client.publish(mqtt_publish_humid, json_humidPayload)
        mqtt_client.publish(mqtt_publish_temp, json_tempPayload)
        mqtt_client.publish(mqtt_publish_light, json_lightPayload)

        time.sleep(15)

except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()