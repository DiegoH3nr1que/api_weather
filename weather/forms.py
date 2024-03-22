from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import WeatherEntity

class WeatherForm(forms.Form):
    temperature = forms.FloatField()
    date = forms.DateTimeField() 
    city = forms.CharField(max_length=255, required=True) 
    atmosphericPressure = forms.FloatField() 
    humidity = forms.FloatField(required=True)
    weather = forms.CharField(max_length=255)


    # def __init__(self, *args, **kwargs):
    #     self.fields['temperature'].label = 'temperatura'