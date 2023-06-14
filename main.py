import dht
from machine import Pin
import machine
from math import sin
from lib.umqttsimple import MQTTClient
import json
import time
import smtplib
from email.message import EmailMessage
import schedule

#For the Mqtt protocol.
mqtt_host = "io.adafruit.com"
mqtt_username = "Djhonk"
mqtt_password = "aio_WXdE48OwLFlJ43ptxmLTDcg2spuW"
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

tempSensor = dht.DHT11(Pin(27))
photoResistor = machine.ADC(0)

def send_email(temp, humid, light):
    msg = EmailMessage()
    msg.set_content(f'Temp is: {temp}°\nHumidity is: {humid}\nLight level is: {light}')

    msg['Subject'] = 'Greenhouse update'
    msg['From'] = ['sender-email']
    msg['To'] = ['reciever-email']

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(['sender-email'], ['sendEmail-password'])
    server.send_message(msg)
    server.quit()


try:
    while True:

        tempSensor.measure()
        print(f'Publish light:{photoResistor.read_u16():.2f}')
        print(f'Publish temp:{tempSensor.temperature():.2f}')
        print(f'Publish humid:{tempSensor.humidity():.2f}')

        schedule.every().day.at('18:00').do(lambda: send_email(tempSensor.temperature(), tempSensor.humidity(), photoResistor.read_u16()))

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

        schedule.run_pending()

        time.sleep(15)

except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()