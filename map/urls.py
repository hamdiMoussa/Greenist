from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', stocker_polygone, name='stocker_polygone'),
    #path('', index, name='stocker_polygone'),
   # path('stocker_polygone/', stocker_polygone, name='stocker_polygone'),
    #path('', views.stocker_polygone, name='stocker_polygone'),
    path('UPdate', views.start_mqtt, name='update'),
    path('polygon_detail/<int:id>/', views.polygon_detail, name='polygon_detail'),
   # path('get-polygon/<int:polygon_id>/', get_polygon, name='get_polygon'),
     path('update_weather/', views.update_weather, name='update_weather'),
    
]