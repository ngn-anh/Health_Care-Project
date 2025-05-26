import requests
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    phone = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    fullname = serializers.CharField(allow_blank=True, required=False)
    gender = serializers.CharField(allow_blank=True, required=False)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    fullname = serializers.CharField(allow_blank=True, required=False)
    gender = serializers.CharField(allow_blank=True, required=False)


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data).save()

        try:
            if validated_data['role'] == 'doctor':
                # Gọi sang doctor_service
                requests.post("http://localhost:7002/api/doctor/create/", json={"user_id": str(user.id)})
            elif validated_data['role'] == 'patient':
                # Gọi sang patient_service
                requests.post("http://localhost:7003/api/patients/create/", json={"user_id": str(user.id)})
        except Exception as e:
            print("❌ Failed to notify related service:", e)

        return user
