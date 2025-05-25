from rest_framework import serializers
from .models import Doctor, Patient, User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    phone = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data).save()
        if validated_data['role'] == 'doctor':
            Doctor(user=str(user.id)).save()
        elif validated_data['role'] == 'patient':
            Patient(user=str(user.id)).save()
        return user