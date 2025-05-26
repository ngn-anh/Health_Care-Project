from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from django.shortcuts import render


class PatientView(APIView):
    def get(self, request, id):
        try:
            patient = Patient.objects.get(_id=ObjectId(id))
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=200)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View render giao diện HTML
def update_patient_template_view(request):
    return render(request, 'updateInforPatient.html')