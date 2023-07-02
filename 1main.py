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
import network

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

# DHT air temp and moisture
tempSensor = dht.DHT11(Pin(27))
# Light sensor
lightsensor = TSL2591(i2c)
# Ground Moist sensor
moistsensor = StemmaSoilSensor(i2c)
# LCD screen
lcd = I2cLcd(i2c, 39, 2, 16)

previousDay = ""
lcddisplay1 = True

lux = lightsensor.get_lux() * 100
roundedlight = round(lux, 0)

groundmoisture = moistsensor.get_moisture()

tempSensor.measure()
tempValue = tempSensor.temperature()
humidValue = tempSensor.humidity()

# Initiating values, avoiding error later.
values = {}
values["temp"] = int(tempValue)
values["humidity"] = int(humidValue)
values["groundmoist"] = int(groundmoisture)
values["light"] = int(roundedlight)

nightValues = values.copy()
dayValues = values.copy()

while True:
    try:
        while True:
            # Get light value
            lux = lightsensor.get_lux() * 100
            roundedlight = round(lux, 0)

            # Get ground moist and temp
            groundmoisture = moistsensor.get_moisture()

            # Get temp and moisture in air
            tempSensor.measure()
            tempValue = tempSensor.temperature()
            humidValue = tempSensor.humidity()

            # For sending emails
            currentDate = time.localtime()
            hour = currentDate[3] + 2
            day = currentDate[2]

            # Create an empty dictionary

            # Convert the values to integers
            values["temp"] = int(tempValue)
            values["humidity"] = int(humidValue)
            values["groundmoist"] = int(groundmoisture)
            values["light"] = int(roundedlight)

            # Saving values for sending later
            if hour == 3 and day != previousDay:
                nightValues = values.copy()

            if hour == 12 and day != previousDay:
                dayValues = values.copy()

            # Sending email at 18.00
            # The email will consist of temps, humid and light at 03, 08 and 18.
            if hour == 18 and day != previousDay:

                eveningValues = values.copy()

                try:

                    send_email("henrik1995a@live.se", dayValues, nightValues, eveningValues)
                    send_email("karin.eh@hotmail.se", dayValues, nightValues, eveningValues)
                    send_email("Richard.jurmo.berg@gmail.com", dayValues, nightValues, eveningValues)
                    send_email("henrik1995a@live.se", dayValues, nightValues, eveningValues)
                    send_email("andreasson6300@gmail.com", tempValue, humidValue, groundmoisture, roundedlight)
                    previousDay = day
                    send_email("antonandreasson@outlook.com", tempValue, humidValue, groundmoisture, roundedlight)
                    previousDay = day
                    
                    print("Success! Mail has been sent")

                    previousDay = day
                    #Email has been sent.
                    
                except Exception as e:
                    
                    print(f'Failed to send email: {e}')

            print(f'Publish light:{roundedlight}')
            print(f'Publish temp:{tempValue}')
            print(f'Publish humid:{humidValue}')
            print(f'Publish ground moist:{groundmoisture}')

            # send_email("henrik1995a@live.se", dayValues, nightValues, eveningValues)
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

            #If the hour is past 9 backlight will be off.

            from Utilities.Functions import Functions

            print(f'Hour: {hour}')

            if not Functions.HourIsPastNine(hour):
                lcd.backlight_off()

            else: 
                lcd.backlight_on()

            # For displaying data in LCD
            # Writing out the values.
            lcd.clear()

            if lcddisplay1:
                
                lcd.move_to(0, 0)
                lcd.putstr("Fukt jord: {}\n".format(groundmoisture))
                lcd.move_to(0, 1)
                lcd.putstr("Ljusstyrka: {}".format(roundedlight))
                lcddisplay1 = False

            else:

                lcd.move_to(0, 0)
                lcd.putstr("Temperatur: {}{}C".format(tempValue, chr(223)))
                lcd.move_to(0, 1)
                lcd.putstr("Fuktighet:  {}%".format(humidValue))
                lcddisplay1 = True

            print("")
            time.sleep(15)

    except Exception as e:
        
        print(f'Error in main loop: {e}')

        # If error occours, pico will reset. Making it upload data again.
        wlan = network.WLAN(network.STA_IF)      
        wlan.disconnect()
        time.sleep(1)
        machine.reset()