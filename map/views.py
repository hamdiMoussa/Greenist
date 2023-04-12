import json
from multiprocessing.connection import Client
from statistics import geometric_mean
from unittest import result
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.gis.geos import Polygon
from .models import *
from django.contrib.gis.geos import GEOSGeometry

import pyowm
from .mqtt import start_mqtt_client
from signup.models import client

from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize

from .status import result
from .forms import *

import csv 
from .FWI import *
from datetime import datetime





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











def start_mqtt(request, id):
    # Start the MQTT client
    start_mqtt_client(id)
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    return render(request, 'polygon_detail.html', {})

def polygon_detail(request, iid):
    projects = Project.objects.all()
    my_project = Project.objects.get(idProject=iid) 
    #polygons = [p.Polygon for p in projects if p.Polygon]
    #polygons = myPolygon.objects.all()
    polygon = my_project.Polygon

    nodes = Node.objects.filter(polygon=polygon)

    #node = Node.objects.filter(polygon=polygon).first()
    node0 = nodes[0]
    node1 = nodes[1]
    
    node = nodes[0]
    data = node.Data
    print(node)  
    print(nodes)  




       # get the last Node object and save it to the polygon
    #node = Node.objects.order_by('-Idnode').first()
    #polygon.node = node
    #polygon.save()

    post = Data.objects.order_by('-IdData').first()
    #start_mqtt_client(id)







    
    temperature = data.temperature
    humidity = data.humidity
    wind_speed = data.wind


    with open('testBatch.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.today().strftime('%m/%d/%Y'), temperature, humidity, wind_speed, '0'])


    batchFWI('testBatch.csv')


    with open('testBatch.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        last_row = rows[-1]
        FWI = last_row[-1]
    
    fwi = float(FWI)
    node.FWI=fwi
    node.save()


    
    return render(request, 'polygon_detail.html', {'projects': projects, 'my_project' : my_project, 'polygon': polygon, 'nodes':nodes, 'node':node, 'node0':node0, 'node1':node1, 'parm': data})



def start (request):
    projects = Project.objects.all()
    #polygons = [p.Polygon for p in projects if p.Polygon]
  
    return render(request, 'start.html', {'projects': projects})   



def step_one(request):
    projects = Project.objects.all()
    polygons = [p.Polygon for p in projects if p.Polygon]
    if request.method == 'POST':
        Prject_name = request.POST.get('nom')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(end_date) 

 
        instance = Project( nom=Prject_name, Date_start = start_date, Date_end=end_date )
        
        instance.save()
        


        
       
        return redirect('step_2', id=instance.idProject)
    return render(request, 'step_1.html', {'projects': projects})   

def step_tow(request, id):
    projects = Project.objects.all()
    polygons = [p.Polygon for p in projects if p.Polygon]
    if request.method == 'POST':
        formulaire = Form_client(request.POST)
        if formulaire.is_valid():
            formulaire.enregistrer(id)
            pseudo = formulaire.cleaned_data['pseudo']
            variable = 'client'
            ####### redirect dashboard normally
            #return redirect('map/',variable, pseudo)
            return redirect('stocker_polygone', id=id)
        return render(request, 'step_2.html', {'form': formulaire, 'projects': projects})
        

    return render(request, 'step_2.html', {'form': Form_client(),'projects': projects})   

def stocker_polygone(request, id):
    projects = Project.objects.all()
    polygons = [p.Polygon for p in projects if p.Polygon]
    if request.method == 'POST':
        Prject_name = request.POST.get('nom') 
        Client_name = request.POST.get('client')      
        polygonString = request.POST.get('points')
        print(polygonString)
        polygon = GEOSGeometry(polygonString, srid=4326)
        #myPolygon.nom = request.user
        
        instance = myPolygon(geom=polygon , nom=Prject_name )
        instance.save()

        my_project = Project.objects.get(idProject=id) 
        my_project.Polygon = instance
        my_project.save()


        


        
       
        return redirect('step_4', id=id)
    return render(request, 'map1.html', {'projects': projects})


def step_four(request, id):
    projects = Project.objects.all()
    polygons = [p.Polygon for p in projects if p.Polygon]
    my_project = Project.objects.get(idProject=id)
    poolygon = my_project.Polygon
    nodes = Node.objects.filter(polygon=poolygon)
    
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        ref = request.POST.get('ref')
        Sensors = request.POST.get('Sensors')
        print(lat,lng)
        point = Point(x=float(lng), y=float(lat))
        # node_name = request.POST.get('nom')
        #sensors = request.POST.get('client')
        

        # create a new Data object
        new_data = Data(temperature=0, humidity=0, wind=0)
        new_data.save()
 
        instancee = Node(point=point, ref=ref, Sensors=Sensors, Data=new_data, polygon=poolygon)
        instancee.save()

        
        my_project = Project.objects.get(idProject=id)
        poolygon = my_project.Polygon
        nodes = Node.objects.filter(polygon=poolygon)
       
        


        
        
        return redirect('step_4', id=id)
    
    return render(request, 'step_4.html', {'polygons': polygons, 'projects': projects, 'polygon': poolygon, 'nodes':nodes })















def update_weather(request, id):
    # get updated weather information




    my_project = Project.objects.get(idProject=id) 
    polygon = my_project.Polygon

    status = result(id)
    

    node = Node.objects.filter(polygon=polygon).first()
    node.status = status
    node.save()


    
    
    node = Node.objects.filter(polygon=polygon).first()

    status = node.status
    fwi = node.FWI
    rssi= node.RSSI
    cam=node.camera
    Data = node.Data
    # create a dictionary with the updated information
    data = {
        'temperature': Data.temperature,
        'humidity': Data.humidity,
        'wind': Data.wind,
        'RSSI' : rssi,
        'camera' : cam,
        'fwi' : fwi,
        'status' : status,
        }

    # return a JsonResponse with the updated data
    return JsonResponse(data)



def show(request, seudo):
    my_client = client.objects.get(pseudo=seudo)
    nam = my_client.nom
    print(nam)
    my_project = Project.objects.get(client=my_client)
    polygon = my_project.Polygon
    node = Node.objects.filter(polygon=polygon).first()
    data = node.Data
    return render(request, 'show.html', {'polygon': polygon, 'node':node, 'data':data})
    


def get_polygon(request, polygon_id):
    try:
        polygon = myPolygon.objects.get(idPolygone=polygon_id)
        return JsonResponse({'geom': polygon.geom.geojson})
    except myPolygon.DoesNotExist:
        return JsonResponse({'error': 'Polygon not found'})
    