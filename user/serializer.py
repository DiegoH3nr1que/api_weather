#serializers.py
from rest_framework import serializers
from .models import UserEntity

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField(allow_blank=True, required=True)
    email = serializers.EmailField(allow_blank=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return UserEntity(**validated_data)
