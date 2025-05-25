from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from auth_service.models import Doctor, Patient

class AppointmentListCreateView(APIView):
    def get(self, request):
        appointments = Appointment.objects()
        data = AppointmentSerializer(appointments, many=True).data
        return Response(data)

    def post(self, request):
        appointment = Appointment(**request.data).save()
        return Response(AppointmentSerializer(appointment).data, status=201)

class AppointmentDetailView(APIView):
    def get(self, request, id):
        appointment = Appointment.objects(id=ObjectId(id)).first()
        if not appointment:
            return Response({"error": "Not found"}, status=404)
        return Response(AppointmentSerializer(appointment).data)

    def put(self, request, id):
        appointment = Appointment.objects(id=ObjectId(id)).first()
        if not appointment:
            return Response({"error": "Not found"}, status=404)

        data = request.data.copy()

        # Xử lý doctor
        if "doctor" in data:
            try:
                data["doctor"] = Doctor.objects.get(id=ObjectId(data["doctor"]))
            except DoesNotExist:
                return Response({"error": "Invalid doctor ID"}, status=400)

        # Xử lý patient
        if "patient" in data:
            try:
                data["patient"] = Patient.objects.get(id=ObjectId(data["patient"]))
            except DoesNotExist:
                return Response({"error": "Invalid patient ID"}, status=400)

        # Cập nhật và reload
        appointment.update(**data)
        appointment.reload()
        return Response(AppointmentSerializer(appointment).data)

    def delete(self, request, id):
        appointment = Appointment.objects(id=ObjectId(id)).first()
        if not appointment:
            return Response({"error": "Not found"}, status=404)
        appointment.delete()
        return Response(status=204)