#views.py
from datetime import datetime
from random import randrange
from django.views import View
from django.shortcuts import render, redirect
from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializer import WeatherSerializer

class WeatherView(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weathers = WeatherSerializer(repository.getAll(), many=True)
        return render(request, "home.html", {"weathers":weathers})
    

class WeatherGenerate(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now()
        )
        serializer = WeatherSerializer(data= weather)
        repository.insert(serializer.data)

        return redirect('Weather View')
        
class WeatherReset(View):

    def get(self, request):
		    pass