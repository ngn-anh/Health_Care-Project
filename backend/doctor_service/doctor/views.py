from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import jwt
from django.conf import settings
from bson import ObjectId
from doctor.models import Doctor

from mongoengine.errors import DoesNotExist
from .serializers import DoctorSerializer


APPOINTMENT_BASE = "http://localhost:7001/api/appointments/"
PATIENT_SERVICE_URL = "http://localhost:7003/api/patients/"

class DoctorAppointmentProxyView(APIView):
    def get(self, request):
        try:
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return Response({"error": "Missing or invalid token"}, status=401)

            token = auth.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get("user_id")

            doctor = Doctor.objects(user=(user_id)).first()
            if not doctor:
                print(user_id)
                return Response({"error": "Doctor not found"}, status=404)

            doctor_id = str(doctor.id)
            res = requests.get(APPOINTMENT_BASE, params={"doctor": doctor_id})

            if res.status_code == 200:
                try:
                    data = res.json()
                except ValueError:
                    return Response({"error": "Invalid JSON from appointment service", "raw": res.text}, status=500)
                return Response(data, status=200)
            elif res.status_code == 404:
                # Nếu không có lịch hẹn => trả mảng rỗng thay vì lỗi
                return Response([], status=200)
            else:
                return Response({
                    "error": f"Unexpected status from appointment service: {res.status_code}",
                    "raw": res.text
                }, status=res.status_code)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        try:
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return Response({"error": "Missing or invalid token"}, status=401)

            token = auth.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get("user_id")

            # Lúc này bạn tìm doctor_id theo user_id
            doctor = Doctor.objects(user=(user_id)).first()
            if not doctor:
                return Response({"error": "Doctor not found"}, status=404)

            doctor_id = str(doctor.id)
            if not doctor_id:
                return Response({"error": "Token has no user_id"}, status=401)

            data = request.data.copy()
            data["doctor"] = doctor_id
            print(doctor_id)
            res = requests.post(APPOINTMENT_BASE, json=data)

            try:
                data = res.json()
            except ValueError:
                return Response({"error": "Invalid response from appointment service", "raw": res.text}, status=500)

            return Response(data, status=res.status_code)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DoctorAppointmentDetailProxyView(APIView):
    def get(self, request, id):
        try:
            res = requests.get(f"{APPOINTMENT_BASE}{id}/")
            try:
                data = res.json()
            except ValueError:
                return Response({"error": "Invalid response from appointment service", "raw": res.text}, status=500)

            return Response(data, status=res.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def put(self, request, id):
        try:
            res = requests.put(f"{APPOINTMENT_BASE}{id}/", json=request.data)
            try:
                data = res.json()
            except ValueError:
                return Response({"error": "Invalid response from appointment service", "raw": res.text}, status=500)

            return Response(data, status=res.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def delete(self, request, id):
        try:
            res = requests.delete(f"{APPOINTMENT_BASE}{id}/")
            return Response(status=res.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class PatientListProxyView(APIView):
    def get(self, request):
        try:
            res = requests.get(PATIENT_SERVICE_URL)
            return Response(res.json(), status=res.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DoctorCreateView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)
        doctor = Doctor(user=user_id)
        doctor.save()
        return Response({"message": "Doctor created"}, status=201)
    
class DoctorInfoView(APIView):
    def get(self, request, id):
        try:
            doctor = Doctor.objects(id=ObjectId(id)).first()
            if not doctor:
                return Response({"error": "Doctor not found"}, status=404)
            return Response({"user_id": doctor.user})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    
# View render giao diện HTML
def dashboard_view(request):
    return render(request, 'doctor_dashboard.html')

def appointment_view(request):
    return render(request, 'doctor_appointment_page.html')

USER_URL = "http://localhost:7000/api/auth/users"

class DoctorAllListView(APIView):
    def get(self, request):
        try:
            doctors = Doctor.objects()  # Lấy tất cả bác sĩ
            result = []

            for doc in doctors:
                # Chuyển Doctor Document → dict
                doc_dict = doc.to_mongo().to_dict()
                # Convert các ObjectId sang string
                doc_dict["_id"] = str(doc_dict["_id"])
                if isinstance(doc_dict.get("user"), ObjectId):
                    user_id = str(doc_dict["user"])
                else:
                    user_id = doc_dict.get("user")

                # Gọi API lấy chi tiết user
                try:
                    user_res = requests.get(f"{USER_URL}/{user_id}")
                    if user_res.status_code == 200:
                        user_data = user_res.json()
                    else:
                        user_data = {"error": "User not found"}
                except Exception:
                    user_data = {"error": "Cannot fetch user"}

                # Ghi đè trường user
                doc_dict["user"] = user_data
                result.append(doc_dict)

            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DoctorInforView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get("user")
            res = requests.get(f"{USER_URL}/{user_id}")

            if res.status_code == 200:
                user_data = res.json()
                doctor = Doctor.objects.get(user=user_id)
                doctor_dict = doctor.to_mongo().to_dict()
                doctor_dict["_id"] = str(doctor_dict["_id"])  # Convert ObjectId to string
                serializer = DoctorSerializer(doctor_dict)
                doctor_data = serializer.data
                doctor_data["user"] = user_data  # Gán object user vào trường user trong kết quả trả về

                return Response(doctor_data, status=200)
            else:
                return Response({"error": "User not found"}, status=404)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bác sĩ"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DoctorInforByIdView(APIView):
    def get(self, request, id):
        try:
            doctor = Doctor.objects(id=ObjectId(id)).first()
            serializer = DoctorSerializer(doctor)
            doctor_data = serializer.data
            user_id = doctor_data["user"]
            res = requests.get(f"{USER_URL}/{user_id}")

            if res.status_code == 200:
                user_data = res.json()
                
                doctor_data["user"] = user_data  # Gán object user vào trường user trong kết quả trả về

                return Response(doctor_data, status=200)
            else:
                return Response({"error": "User not found"}, status=404)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy bác sĩ"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)