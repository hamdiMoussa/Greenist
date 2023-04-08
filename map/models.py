# from django.contrib.gis.db import models

# # Create your models here.
# class myPolygon(models.Model):
   
#     geom = models.PolygonField()


from ast import NodeTransformer
from django.conf import settings
from django.db import models
from django.utils import timezone

############polyg##########
from django.contrib.gis.db import models
from signup.models import *
from signup.models import supervisor



# class test(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     published_date = models.DateTimeField(blank=True, null=True)

#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()

#     def __str__(self):
#         return self.title
    

class Data(models.Model):
    IdData = models.AutoField(primary_key=True)
    temperature = models.BigIntegerField()
    humidity = models.BigIntegerField()
    wind = models.BigIntegerField(default= 0)
    
    
    
    def __str__(self):
        return f' Temperature: {self.temperature}, Humidity: {self.humidity}, wind: {self.wind}'






class Node(models.Model):
    Idnode = models.AutoField(primary_key=True) 
    ref =  models.CharField(max_length=50, null=True)
    Sensors = models.CharField(max_length=50, null=True)
    RSSI = models.BigIntegerField(null=True)
    Battery_value = models.BigIntegerField(null=True)
    point = models.PointField(null=True)

    Data = models.ForeignKey(Data, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')

   



class myPolygon(models.Model):
    idPolygone = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, null=True)
    geom = models.PolygonField()
    status = models.CharField(max_length=50, null=True)
    WFI=models.BigIntegerField(null=True)

    node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True,)
    #client = models.CharField(max_length=50, null=True)
    #node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True,)
    #client = models.ForeignKey(client, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    #supervisor = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    






class Project(models.Model):
    idProject = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, null=True)
    Date_start = models.DateField(null=True)
    Date_end = models.DateField(null=True)
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    Polygon = models.ForeignKey(myPolygon, on_delete=models.CASCADE, null=True,)
    
    

    
   
  

  


    #node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True,)
    #client = models.ForeignKey(client, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    #supervisor = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')















   