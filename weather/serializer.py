#serializers.py
from dataclasses import dataclass
from datetime import datetime
from rest_framework import serializers
from .models import WeatherEntity

class WeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    date = serializers.DateTimeField() 
    city = serializers.CharField(max_length=255, allow_blank=True) 
    atmosphericPressure = serializers.FloatField(required=True) 
    humidity = serializers.FloatField(required=True)
    weather = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        return WeatherEntity(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)