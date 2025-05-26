from rest_framework import serializers
from .models import Appointment
import requests

class AppointmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    datetime = serializers.DateTimeField()
    description = serializers.CharField()
    status = serializers.CharField()
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    def get_user_info(self, user_id):
        try:
            res = requests.get(f"http://localhost:7000/api/auth/users/{user_id}/")
            if res.status_code == 200:
                return res.json()
        except Exception:
            pass
        return None

    def get_doctor(self, obj):
        try:
            doctor_id = obj.doctor
            # Bước 1: Lấy user_id từ doctor_service
            res = requests.get(f"http://localhost:7002/api/doctor/info/{doctor_id}/")
            if res.status_code == 200:
                user_id = res.json().get("user_id")
                return self.get_user_info(user_id)
        except Exception:
            pass
        return None

    def get_patient(self, obj):
        try:
            patient_id = obj.patient
            # Bước 1: Lấy user_id từ patient_service
            res = requests.get(f"http://localhost:7003/api/patients/info/{patient_id}/")
            if res.status_code == 200:
                user_id = res.json().get("user_id")
                return self.get_user_info(user_id)
        except Exception:
            pass
        return None
