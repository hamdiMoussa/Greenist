from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/map/polygon_detail/(?P<polygon_id>\d+)/$', consumers.PolygonConsumer.as_asgi()),
]