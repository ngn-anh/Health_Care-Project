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
            print("api1: ", f"http://localhost:7000/api/auth/users/{user_id}/")
            res = requests.get(f"http://localhost:7000/api/auth/users/{user_id}/")
            if res.status_code == 200:
                return res.json()
        except Exception:
            pass
        return None

    def get_doctor(self, obj):
        try:
            doctor_id = obj.doctor
            print("api2: ", f"http://localhost:7002/api/doctor/info/{doctor_id}/")
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
            print("api3: ", f"http://localhost:7003/api/patients/info/{patient_id}/")
            res = requests.get(f"http://localhost:7003/api/patients/info/{patient_id}/")
            if res.status_code == 200:
                user_data = res.json()
                user_id = user_data.get("user_id")
                user_info = self.get_user_info(user_id) or {}
                user_info["id"] = patient_id  # Thêm ID bệnh nhân vào kết quả
                return user_info
        except Exception:
            pass
        return None
