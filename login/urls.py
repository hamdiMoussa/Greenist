from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.connect,name='connect') ,
    path('loginsv',views.connect_supervisor,name='login_supervisor')

]