from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import jwt
from django.conf import settings
from auth_service.models import Doctor  
from bson import ObjectId



APPOINTMENT_BASE = "http://localhost:8000/api/appointments/"
PATIENT_SERVICE_URL = "http://localhost:8000/api/patients/"

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