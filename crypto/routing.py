from django.urls import path
from .consumers import CoinsConsumers


ws_urlpatterns = [
    path('ws/coins/', CoinsConsumers.as_asgi())
]