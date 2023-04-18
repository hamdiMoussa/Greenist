# import paho.mqtt.client as mqtt
# from django.conf import settings


# def on_connect(mqtt_client, userdata, flags, rc):
#     if rc == 0:
#         print('Connected successfullyyyyyyyyyyy')
#         mqtt_client.subscribe('django/mqtt')
#     else:
#         print('Bad connection. Code:', rc)


# def on_message(mqtt_client, userdata, msg):
#     print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')



from map.mqtt import *
from map.models import *
import json

from django.apps import AppConfig
import paho.mqtt.client as mqtt
from django.conf import settings


import pyowm



# topics = ['v3/loraatest02@ttn/devices/eui-70b3d57ed005a5c4/up', 'v3/loraatest02@ttn/devices/eui-70b3d57ed005c92e/up', 'v3/loraatest02@ttn/devices/eui-2cf7f1c044900011/up']

# def on_connect(mqtt_client, userdata, flags, rc):

#     if rc == 0:
#         print('Connected successfully')
        
#         #hamdi card
#         mqtt_client.subscribe(topics[0])

#         #yassmin card
#         mqtt_client.subscribe(topics[1])

#         #camera 
#         mqtt_client.subscribe(topics[2])
#     else:
#         print('Bad connection. Code:', rc)

# def on_message(mqtt_client, userdata, msg):
   
#     # Decode the incoming message
#     payload_dict =json.loads(msg.payload)
#     print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

#     if msg.topic == topics[2]:
#         print(payload_dict)  # Add this line to check the content of payload_dict
#         value = payload_dict['uplink_message']['decoded_payload']['measurement_value']
#         valueee = value*10
#         print('Measurement valueeeeeeeeeeeee:', valueee)
#         # my_project = Project.objects.get(idProject=id)
#         # polygon = my_project.Polygon
#         # nodes = Node.objects.filter(polygon=polygon)

#         nodes = Node.objects.all()
#         node = nodes[0]
#         node.camera = valueee
#         node.save()
#     else:
#         for topic in topics:
#             if msg.topic == topic :
#                 # my_project = Project.objects.get(idProject=id)
#                 # polygon = my_project.Polygon
#                 # nodes = Node.objects.filter(polygon=polygon)
#                 nodes = Node.objects.all()
#                 for node in nodes:
#                   if msg.topic == f'v3/loraatest02@ttn/devices/{node.ref}/up':  
#                     temperature = payload_dict['uplink_message']['decoded_payload']['temperature']
#                     humidity = payload_dict['uplink_message']['decoded_payload']['humidity']

#                     rssi = payload_dict['uplink_message']['rx_metadata'][0]['rssi']
#                     snr = payload_dict['uplink_message']['rx_metadata'][0]['snr']

#                     print('temperature :', temperature, 'humidity :', humidity, 'rssi :', rssi, 'snr :', snr, '\n')
#                     # Replace "YOUR_API_KEY" with your actual API key from OpenWeatherMap
#                     owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
    
#                     # Replace "City name" with the name of the city you want weather data for
#                     location = owm.weather_manager().weather_at_place('Bizerte, TN')
    
#                     weather = location.weather

#                     # Get the temperature, humidity, and wind speed
#                     temperature_owm = weather.temperature('celsius')['temp']
#                     humidity_owm = weather.humidity
#                     wind_speed = weather.wind()['speed']

#                     print('temperature :', temperature, 'humidity :', humidity, 'wind :', wind_speed, '\n')
#                     # Create a new Post object and save it to the database

#                     node.RSSI = rssi
#                     node.save()
#                     new_data = Data.objects.create(temperature=temperature, humidity=humidity, wind=wind_speed, node=node)
#                     #datas.append(new_data)
#                     new_data.save()









# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
# client.connect(
#     host=settings.MQTT_SERVER,
#     port=settings.MQTT_PORT,
#     keepalive=settings.MQTT_KEEPALIVE
# )

# client.loop_forever()



# Create a new MQTT client instance
client = mqtt.Client()

# Set the client's connection and message handling functions
client.on_connect = on_connect
client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)

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

