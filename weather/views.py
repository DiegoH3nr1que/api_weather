from typing import Any
from bible_verse import main
from datetime import datetime
from random import randrange
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.shortcuts import render, redirect

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializer import WeatherSerializer
from .forms import WeatherForm
from .exception import WeatherException


class WeatherView(View):
    
    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        verse = main.get_bible_verse()
        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getAll())
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                # print('Data: ')
                # print(serializer.data)
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather, "verse":verse}
            else:
                # print('Error: ')
                # print(serializer.errors)
                objectReturn = {"error":serializer.errors, "verse":verse}
        except WeatherException as e:
            objectReturn = {"error":e.message, "verse":verse}

        if not self.authenticate:
            objectReturn["errorAuth"] = "Usuário não autenticado"
        print(objectReturn)

        return render(request, "home.html", objectReturn)

class WeatherGenerate(View):

    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            return redirect('Weather View')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now(),
            city='Sorocaba'
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if (serializer.is_valid()):
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect('Weather View')
    
class WeatherReset(View):

    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            return redirect('Weather View')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request): 
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()

        return redirect('Weather View')
    
class WeatherInsert(View):

    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            return redirect('Weather View')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        weatherForm = WeatherForm()

        return render(request, "form.html", {"form":weatherForm})
    
    def post(self, request):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')
    
class WeatherDelete(View):

    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            return redirect('Weather View')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        # Obter o repositório de clima
        repository = WeatherRepository(collectionName='weathers')
        # Excluir o registro de clima com o ID fornecido
        repository.deleteById(id)
        # Redirecionar de volta para a página principal
        return redirect('Weather View')

class WeatherEdit(View):

    authentication_class = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
            self.authentication = True
        except Exception as e:
            return redirect('Weather View')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        weatherForm = WeatherForm(initial=weather)
        return render(request, "form_edit.html", {"form":weatherForm, "id": id})
    
    def post(self, request, id):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            serializer.id = id
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.update(serializer.data, id)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')
    
class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getByCity(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                # print('Data: ')
                # print(serializer.data)
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                # print('Error: ')
                # print(serializer.errors)
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}
  
        return render(request, "home.html", objectReturn)