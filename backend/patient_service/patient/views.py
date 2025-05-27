from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from django.shortcuts import render
import requests

USER_URL = "http://localhost:7000/api/auth/users"

class PatientView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("userId")
            patient = Patient.objects.get(user = user_id)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=200)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientInforView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user")
            res = requests.get(f"{USER_URL}/{user_id}")

            if res.status_code == 200:
                user_data = res.json()
                patient = Patient.objects.get(user=user_id)
                serializer = PatientSerializer(patient)
                patient_data = serializer.data
                patient_data["user"] = user_data  # Gán object user vào trường user trong kết quả trả về
                
                return Response(patient_data, status=200)
            else:
                return Response({"error": "User not found"}, status=404)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientUpdateView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user")
            res = requests.post(
                f"{USER_URL}/update/{user_id}",
                json=request.data
            )
            print("ress: ", res)
            if res.status_code == 200:
                user_data = res.json()
                patient = Patient.objects.get(user=user_id)
                serializer = PatientSerializer(patient)
                patient_data = serializer.data
                patient_data["user"] = user_data  # Gán object user vào trường user trong kết quả trả về
                return Response(patient_data, status=200)
            else:
                return Response({"error": "User not found"}, status=404)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PatientListView(APIView):
    def get(self, request):
        try:
            patients = Patient.objects()
            data = []
            for p in patients:
                user_info = {}
                try:
                    res = requests.get(f"http://localhost:7000/api/auth/users/{p.user}/")
                    if res.status_code == 200:
                        print(res)
                        user_info = res.json()
                        print(user_info)
                except:
                    pass

                data.append({
                    "id": str(p.id),
                    "user_id": p.user,
                    "username": user_info.get("username"),
                    "email": user_info.get("email"),
                    "role": user_info.get("role")
                })

            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class PatientCreateView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)
        Patient(user=user_id).save()
        return Response({"message": "Patient created"}, status=201)
    
class PatientInfoView(APIView):
    def get(self, request, id):
        try:
            patient = Patient.objects(id=ObjectId(id)).first()
            if not patient:
                return Response({"error": "Patient not found"}, status=404)
            return Response({"user_id": patient.user})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class PatientInforByIdView(APIView):
    def get(self, request, id):
        try:
            patient = Patient.objects(_id=ObjectId(id)).first()
            serializer = PatientSerializer(patient)
            patient_data = serializer.data
            user_id = patient_data["user"]
            res = requests.get(f"{USER_URL}/{user_id}")

            if res.status_code == 200:
                user_data = res.json()
                # patient = Patient.objects.get(user=user_id)
                
                patient_data["user"] = user_data  # Gán object user vào trường user trong kết quả trả về
                # print(">>>>data", patient_data)
                return Response(patient_data, status=200)
            else:
                return Response({"error": "User not found"}, status=404)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View render giao diện HTML
def home_view(request):
    return render(request, 'home.html')

def update_view(request):
    return render(request, 'updateInforPatient.html')

def appointment_view(request):
    return render(request, 'patientAppointment.html')