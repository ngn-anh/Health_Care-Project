import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import jwt
from django.conf import settings
from bson import ObjectId
from doctor.serializers import DiagnosisSerializer
from doctor.models import Diagnosis, Doctor
from rest_framework import status
from .ml_model import diagnose_with_ai



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
        

class DoctorPatientListView(APIView):
    def get(self, request):
        try:
            # Xác thực token
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return Response({"error": "Missing or invalid token"}, status=401)

            token = auth.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get("user_id")

            # Tìm bác sĩ theo user_id
            doctor = Doctor.objects(user=user_id).first()
            if not doctor:
                return Response({"error": "Doctor not found"}, status=404)

            doctor_id = str(doctor.id)

            # Gọi sang appointment_service để lấy các lịch hẹn của bác sĩ này
            res = requests.get("http://localhost:7001/api/appointments/", params={"doctor": doctor_id})
            if res.status_code != 200:
                return Response({"error": "Failed to fetch appointments", "detail": res.text}, status=res.status_code)

            appointments = res.json()

            # Lấy danh sách patient_id duy nhất
            patient_ids = set()
            for appt in appointments:
                if "patient" in appt:
                    patient = appt["patient"]
                    if isinstance(patient, dict):
                        patient_id = patient.get("id")
                    else:
                        patient_id = patient
                    if patient_id:
                        patient_ids.add(patient_id)

            # Lấy thông tin từng bệnh nhân
            patients_data = []
            for patient_id in patient_ids:
                try:
                    info_res = requests.get(f"http://localhost:7003/api/patients/info/{patient_id}/")
                    if info_res.status_code != 200:
                        continue
                    user_id = info_res.json().get("user_id")

                    user_res = requests.get(f"http://localhost:7000/api/auth/users/{user_id}/")
                    if user_res.status_code != 200:
                        continue
                    user_info = user_res.json()
                    user_info["id"] = patient_id
                    patients_data.append(user_info)
                except Exception:
                    continue

            return Response(patients_data, status=200)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        
class DiagnosisCreateView(APIView):
    def post(self, request):
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            diag = Diagnosis(**data)
            diag.save()
            return Response(DiagnosisSerializer(diag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiagnosisHistoryView(APIView):
    def get(self, request, patient_id):
        diagnoses = Diagnosis.objects(patient_id=patient_id)
        data = [DiagnosisSerializer(d).data for d in diagnoses]
        return Response(data)
    

        
class AIDiagnosisInternalView(APIView):
    def post(self, request):
        try:
            symptoms = request.data.get("symptoms", [])
            doctor_id = request.data.get("doctor_id", "longDoctor")
            patient_id = request.data.get("patient_id", "anonymous")

            if not isinstance(symptoms, list):
                return Response({"error": "Triệu chứng phải là danh sách."}, status=400)

            result = diagnose_with_ai(symptoms)

            # ✅ Nếu finished → lưu vào MongoDB
            if result.get("finished"):
                # Tách ra prediction và advice từ message
                match_diagnosis = re.search(r"Diagnosis: ([\w\- ]+)", result["message"])
                match_advice = re.search(r"Advice: (.+)", result["message"])
                prediction = match_diagnosis.group(1) if match_diagnosis else "unknown"
                advice = match_advice.group(1) if match_advice else "N/A"

                Diagnosis.objects.create(
                    doctor_id=doctor_id,
                    patient_id=patient_id,
                    symptoms=", ".join(symptoms),
                    diagnosis=prediction,
                    prescription=advice
                )

            return Response(result)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
# View render giao diện HTML
def dashboard_view(request):
    return render(request, 'doctor_dashboard.html')

def appointment_view(request):
    return render(request, 'doctor_appointment_page.html')

def list_patient_view(request):
    return render(request, 'doctor_list_patient.html')

def diagonsis_view(request):
    return render(request, 'doctor_diagnosis.html')