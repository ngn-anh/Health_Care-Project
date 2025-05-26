from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
from bson import ObjectId

class AppointmentListCreateView(APIView):
    def get(self, request):
        appointments = Appointment.objects()
        data = AppointmentSerializer(appointments, many=True).data
        return Response(data)

    def post(self, request):
        data = request.data.copy()

        # Kiểm tra trường bắt buộc
        if "doctor" not in data or "patient" not in data:
            return Response({"error": "Missing doctor_id or patient_id"}, status=400)

        appointment = Appointment(**data).save()
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

        # Kiểm tra nếu update doctor_id hoặc patient_id
        if "doctor_id" in data and not data["doctor_id"]:
            return Response({"error": "doctor_id cannot be empty"}, status=400)

        if "patient_id" in data and not data["patient_id"]:
            return Response({"error": "patient_id cannot be empty"}, status=400)

        appointment.update(**data)
        appointment.reload()
        return Response(AppointmentSerializer(appointment).data)

    def delete(self, request, id):
        appointment = Appointment.objects(id=ObjectId(id)).first()
        if not appointment:
            return Response({"error": "Not found"}, status=404)
        appointment.delete()
        return Response(status=204)
