
import json

import paho.mqtt.client as mqtt
from django.conf import settings

from .models import *
import pyowm

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('v3/loraatest02@ttn/devices/eui-70b3d57ed005a5c4/up')
        mqtt_client.subscribe('v3/loraatest02@ttn/devices/eui-2cf7f1c044900011/up')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg, id):
    # Decode the incoming message
    payload_dict =json.loads(msg.payload)
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')


    if msg.topic == 'v3/loraatest02@ttn/devices/eui-2cf7f1c044900011/up':
        print(payload_dict)  # Add this line to check the content of payload_dict
        value = payload_dict['uplink_message']['decoded_payload']['measurement_value']
        valueee = value*10
        print('Measurement valueeeeeeeeeeeee:', valueee)
        my_project = Project.objects.get(idProject=id)
        polygon = my_project.Polygon
        node = polygon.node
        node.camera = valueee
        node.save()

    else:   
         # Get temperature and humidity values from payload
        temperature = payload_dict['uplink_message']['decoded_payload']['temperature']
        humidity = payload_dict['uplink_message']['decoded_payload']['humidity']

        rssi = payload_dict['uplink_message']['rx_metadata'][0]['rssi']
        snr = payload_dict['uplink_message']['rx_metadata'][0]['snr']



        print('temperature :', temperature, 'humidity :', humidity, 'rssi :', rssi, 'snr :', snr, '\n')

   

    
    



        # Replace "YOUR_API_KEY" with your actual API key from OpenWeatherMap
        owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
    
         # Replace "City name" with the name of the city you want weather data for
        location = owm.weather_manager().weather_at_place('Bizerte, TN')
    
        weather = location.weather

        # Get the temperature, humidity, and wind speed
        temperature_owm = weather.temperature('celsius')['temp']
        humidity_owm = weather.humidity
        wind_speed = weather.wind()['speed']




        print('temperature :', temperature, 'humidity :', humidity, 'wind :', wind_speed, '\n')
        # Create a new Post object and save it to the database
    
        my_project = Project.objects.get(idProject=id)
        polygon = my_project.Polygon
        node = polygon.node
        node.RSSI = rssi
        node.save()

        my_project = Project.objects.get(idProject=id)
        polygon = my_project.Polygon
        node = polygon.node
        data = node.Data
        data.temperature = temperature
        data.humidity = humidity
        data.wind = wind_speed
        data.save()


def start_mqtt_client(id):
    # Create a new MQTT client instance
    client = mqtt.Client()

    # Set the client's connection and message handling functions
    client.on_connect = on_connect
    client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, id)

    # Set the client's username and password
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    # Connect to the MQTT broker
    client.connect(
        host=settings.MQTT_SERVER,
        port=settings.MQTT_PORT,
        keepalive=settings.MQTT_KEEPALIVE
    )

    # Start the MQTT loop (this function blocks and waits for incoming messages)
    client.loop_forever()