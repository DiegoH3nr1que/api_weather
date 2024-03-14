from django.urls import path
from weather.views import WeatherView
from weather.views import WeatherGenerate
urlpatterns = [
    path('', WeatherView.as_view(), name='Weather View'),
    path('generate',WeatherGenerate.as_view(), name='Weather Generate')
]
