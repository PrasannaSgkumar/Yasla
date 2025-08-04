# appointments/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/stylist/(?P<stylist_id>\d+)/$', consumers.AppointmentConsumer.as_asgi()),
    re_path(r'ws/salon/(?P<salon_id>\d+)/$', consumers.AppointmentConsumer.as_asgi()),
]
