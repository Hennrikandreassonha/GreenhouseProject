import dht
from machine import Pin
import machine
from lib.umqttsimple import MQTTClient
from lib.seesaw import Seesaw
from lib.stemma_soil_sensor import StemmaSoilSensor
from lib.tsl2591 import TSL2591
from lib.SendEmail import send_email
from secrets import secrets
import json
import time



# For the Mqtt protocol.
mqtt_host = "io.adafruit.com"
mqtt_username = 'Djhonk'
mqtt_password = 'aio_WXdE48OwLFlJ43ptxmLTDcg2spuW'
mqtt_publish_temp = "Djhonk/feeds/Temp"
mqtt_publish_humid = "Djhonk/feeds/Humidity"
mqtt_publish_light = "Djhonk/feeds/Light"
mqtt_publish_groundmoisture = "Djhonk/feeds/Groundmoisture"

mqtt_client_id = "Djhonkensid"

mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host,
    user=mqtt_username,
    password=mqtt_password)

mqtt_client.connect()

# Defining sensors

#DHT air temp and moisture 
tempSensor = dht.DHT11(Pin(27))

i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

#Light sensor
lightsensor = TSL2591(i2c)

#Ground Moist sensor
moistsensor = StemmaSoilSensor(i2c)

previousDay = ""

try:
    while True:
        #Get light value
        lux = lightsensor.get_lux()
        roundedlight = round(lux, 2)
        
        #Get ground moist and temp
        groundmoisture = moistsensor.get_moisture()
        groundtemperature = moistsensor.get_temp()

        #Get temp and moisture in iar
        tempSensor.measure()
        tempValue = tempSensor.temperature()
        humidValue = tempSensor.humidity()
        
        #For sending emails
        currentDate = time.localtime()
        print(currentDate)
        hour = currentDate[3] + 2
        day = currentDate[2]
        print('Hour:')
        print(hour)
        #Sending email at 08.00 and 18.00
        if hour == 18 and day != previousDay:
          send_email("karin.eh@hotmail.se", tempValue, humidValue, groundmoisture, roundedlight)
          previousDay = day
          send_email("andreasson6300@gmail.com", tempValue, humidValue, groundmoisture, roundedlight)
          previousDay = day
          send_email("antonandreasson@outlook.com", tempValue, humidValue, groundmoisture, roundedlight)
          previousDay = day
          send_email("henrik1995a@live.se", tempValue, humidValue, groundmoisture, roundedlight)
          previousDay = day
        
        print(f'Publish light:{roundedlight}')
        print(f'Publish temp:{tempValue}')
        print(f'Publish humid:{humidValue}')
        print(f'Publish ground moist:{groundmoisture}')

        # Create a dictionary to represent the JSON payload
        tempPayload = {
            "temp": tempValue
        }
        humidPayload = {
            "humidity": humidValue
        }
        lightPayload = {
            "light": roundedlight
        }
        groundmoisturePayload = {
            "groundmoisture": groundmoisture
        }

        json_humidPayload = json.dumps(humidPayload)
        json_tempPayload = json.dumps(tempPayload)
        json_lightPayload = json.dumps(lightPayload)
        json_groundmoisture = json.dumps(groundmoisturePayload)

        mqtt_client.publish(mqtt_publish_humid, json_humidPayload)
        mqtt_client.publish(mqtt_publish_temp, json_tempPayload)
        mqtt_client.publish(mqtt_publish_light, json_lightPayload)
        mqtt_client.publish(mqtt_publish_groundmoisture, json_groundmoisture)

        time.sleep(15)

except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()