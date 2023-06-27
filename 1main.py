import dht
from machine import Pin
import machine
import _thread
from lib.umqttsimple import MQTTClient
from lib.seesaw import Seesaw
from lib.stemma_soil_sensor import StemmaSoilSensor
from lib.tsl2591 import TSL2591
from lib.SendEmail import send_email
from mysecrets import secrets
from lib.pico_i2c_lcd import I2cLcd
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
    user=secrets['mqtt-username'],
    password=secrets['mqtt-password'])

mqtt_client.connect()

# Defining sensors
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

#DHT air temp and moisture 
tempSensor = dht.DHT11(Pin(27))
#Light sensor
lightsensor = TSL2591(i2c)
#Ground Moist sensor
moistsensor = StemmaSoilSensor(i2c)
#LCD screen
lcd = I2cLcd(i2c, 39, 2, 16)

previousDay = ""

# For showing information on LCD screen
def lcd_loop():
    while True:

        lux = lightsensor.get_lux()
        roundedlight = round(lux, 2)
        
        #Get ground moist and temp
        groundmoisture = moistsensor.get_moisture()

        #Get temp and moisture in air
        tempSensor.measure()
        tempValue = tempSensor.temperature()
        humidValue = tempSensor.humidity()

        lcd.hide_cursor()
        lcd.putstr("Fukt jord: {groundmoisture}\n")
        lcd.putstr("Ljusstyrka: {roundedlight}")
        time.sleep(5)
        lcd.clear()
        lcd.putstr("Temperatur: {tempValue}" + chr(223) + "C")
        lcd.putstr("Fuktighet:  {humidValue}%")
        time.sleep(5)
        lcd.clear()

# Start the LCD loop in a separate thread
_thread.start_new_thread(lcd_loop, ())

try:
      while True:
        #Get light value
        lux = lightsensor.get_lux()
        roundedlight = round(lux, 2)
        
        #Get ground moist and temp
        groundmoisture = moistsensor.get_moisture()
        groundtemperature = moistsensor.get_temp()

        #Get temp and moisture in air
        tempSensor.measure()
        tempValue = tempSensor.temperature()
        humidValue = tempSensor.humidity()
        
        #For sending emails
        currentDate = time.localtime()
        print(currentDate)
        hour = currentDate[3] + 2
        day = currentDate[2]
        minute = currentDate[4]
        print('Hour:')
        print(hour)
        nightValues = ""
        dayValues = ""
        eveningValues = ""

        #Saving values for sending later
        if hour == 3 and minute == 0 and day != previousDay:

            nightValues = {
                        "temp": tempValue,
                        "humidity": humidValue,
                        "groundmoist": groundmoisture,
                        "light" : roundedlight
                        }

        if hour == 12 and minute == 0 and day != previousDay:

            dayValues = {
                        "temp": tempValue,
                        "humidity": humidValue,
                        "groundmoist": groundmoisture,
                        "light" : roundedlight
                        }
             
        #Sending email at 18.00
        #The email will consist of temps, humid and light at 03, 08 and 18.
        if hour == 18 and minute == 0 and day != previousDay:
          
            eveningValues = {
                        "temp": tempValue,
                        "humidity": humidValue,
                        "groundmoist": groundmoisture,
                        "light" : roundedlight
                        }
           
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