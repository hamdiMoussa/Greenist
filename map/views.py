import json
from statistics import geometric_mean
from unittest import result
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.gis.geos import Polygon
from .models import *
from django.contrib.gis.geos import GEOSGeometry

import pyowm
from .mqtt import start_mqtt_client


from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize



def weather(request):
    # Replace "YOUR_API_KEY" with your actual API key from OpenWeatherMap
    owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
    
    # Replace "City name" with the name of the city you want weather data for
    location = owm.weather_manager().weather_at_place('Bizerte, TN')
    
    weather = location.weather

    # Get the temperature, humidity, and wind speed
    temperature = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    wind_speed = weather.wind()['speed']
    
    # Create a dictionary of the weather data to pass to the template
    weather_data = {'temperature': temperature, 'humidity': humidity, 'wind_speed': wind_speed}
    
    return render(request, 'weather.html', {'temp': temperature, 'hum': humidity, 'wind': wind_speed} )





def result():
    post = Node.objects.order_by('-IdNode').first()
    tempp = post.temperature
    humm = post.humidity
    windd = post.wind

    if tempp > 30 and humm < 30 and windd > 30:
     #if tempp > 20 and humm < 80 and windd > 4:
        status = 'Risk'
    else:
        status = 'SAFE'
    return status





def start_mqtt(request):
    # Start the MQTT client
    start_mqtt_client()
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    return render(request, 'polygon_detail.html', {})

def polygon_detail(request, id):
    polygons = myPolygon.objects.all()
    polygon = myPolygon.objects.get(idPolygone=id)
    

    status = result()
    polygon.status = status
    polygon.save()
   # get the last Node object and save it to the polygon
    #node = Node.objects.order_by('-id').first()
    #polygon.node = node
    #polygon.save()

    
    post = Node.objects.order_by('-IdNode').first()

    
    return render(request, 'polygon_detail.html', {'polygons': polygons, 'polygon': polygon, 'parm': post})

   

def stocker_polygone(request):
    polygons = myPolygon.objects.all()
    if request.method == 'POST':
        Prject_name = request.POST.get('nom') 
        Client_name = request.POST.get('client')      
        polygonString = request.POST.get('points')
        print(polygonString)
        polygon = GEOSGeometry(polygonString, srid=4326)
        #myPolygon.nom = request.user
        instance = myPolygon(geom=polygon , nom=Prject_name , client=Client_name)
        
        instance.save()
        


        
       
        return redirect('stocker_polygone')
    return render(request, 'map1.html', {'polygons': polygons})



def update_weather(request):
    # get updated weather information
    post = Node.objects.order_by('-IdNode').first()

    # create a dictionary with the updated information
    data = {
        'temperature': post.temperature,
        'humidity': post.humidity,
        'wind': post.wind,
    }

    # return a JsonResponse with the updated data
    return JsonResponse(data)





def get_polygon(request, polygon_id):
    try:
        polygon = myPolygon.objects.get(idPolygone=polygon_id)
        return JsonResponse({'geom': polygon.geom.geojson})
    except myPolygon.DoesNotExist:
        return JsonResponse({'error': 'Polygon not found'})
    