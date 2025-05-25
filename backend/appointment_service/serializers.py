from rest_framework import serializers

from auth_service.models import User
from .models import Appointment

class AppointmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    datetime = serializers.DateTimeField()
    description = serializers.CharField()
    status = serializers.CharField()
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    def get_doctor(self, obj):
        try:
            user_id = obj.doctor.user  # objectId
            user = User.objects(id=user_id).first()
            if not user:
                return None
            return {
                "id": str(obj.doctor.id),
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        except Exception as e:
            return None

    def get_patient(self, obj):
        try:
            user_id = obj.patient.user  # objectId
            user = User.objects(id=user_id).first()
            if not user:
                return None
            return {
                "id": str(obj.patient.id),
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        except Exception as e:
            return None