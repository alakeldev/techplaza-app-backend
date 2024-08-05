from django.urls import path
from .views import GetWeatherView

urlpatterns = [
    path('weather/', GetWeatherView.as_view(), name='get_weather'),
]