from django.urls import path
from .views import *
from . import views

urlpatterns = [

    path('', start, name='start'),
    path('show/<str:seudo>/', show, name='show'),
    path('step_3/<int:id>/', stocker_polygone, name='stocker_polygone'),
    path('step_1', step_one, name='step_1'),
    path('step_2/<int:id>/', step_tow, name='step_2'),
    path('step_4/<int:id>/', step_four, name='step_4'),
    
    #path('', index, name='stocker_polygone'),
    #path('stocker_polygone/', stocker_polygone, name='stocker_polygone'),
    #path('', views.stocker_polygone, name='stocker_polygone'),
    path('update/<int:id>/', views.start_mqtt, name='update'),
    #path('update/<int:id>/', views.start_mqtt, name='update'),
    path('polygon_detail/<int:iid>/', views.polygon_detail, name='polygon_detail'),
    #path('get-polygon/<int:polygon_id>/', get_polygon, name='get_polygon'),
    path('update_weather/<int:id>/', views.update_weather, name='update_weather'),
    
]