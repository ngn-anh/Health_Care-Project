from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
from bson import ObjectId
import requests
from mongoengine.errors import DoesNotExist
import datetime
import pytz

DOCTOR_URL = "http://localhost:7002/api/doctor"
PATIENT_URL = "http://localhost:7003/api/patients"

class AppointmentListCreateView(APIView):
    def get(self, request):
        doctor_id = request.GET.get("doctor")
        if doctor_id:
            appointments = Appointment.objects(doctor=doctor_id)
        else:
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

class AppointmentListView(APIView):
    def get(self, request):
        patient_id = request.query_params.get('patient')
        if not patient_id:
            return Response({"error": "patientId is required"}, status=400)

        try:
            # 1. Lấy danh sách appointment thô
            appointments = Appointment.objects(patient=patient_id)

            # 2. Chuẩn bị list kết quả
            result = []
            for appt in appointments:
                # 2.1 chuyển mỗi appt sang dict và convert ObjectId sang string
                appt_dict = appt.to_mongo().to_dict()
                appt_dict["_id"] = str(appt_dict["_id"])
                # giữ lại doctor/patient id trước khi overwrite
                doctor_id = str(appt_dict.get("doctor"))
                # patient_id = str(appt_dict.get("patient"))
                # print(" doctor_id", doctor_id)
                # print ("api: ", f"{DOCTOR_URL}/getInforById/{doctor_id}")
                # 2.2 gọi API lấy chi tiết doctor
                try:
                    dr_res = requests.get(f"{DOCTOR_URL}/getInforById/{doctor_id}")

                    if dr_res.status_code == 200:
                        appt_dict["doctor"] = dr_res.json()
                    else:
                        appt_dict["doctor"] = {"error": "Doctor not found"}
                except Exception:
                    appt_dict["doctor"] = {"error": "Cannot fetch doctor info"}

                # # 2.3 gọi API lấy chi tiết patient
                # try:
                #     pt_res = requests.get(f"{PATIENT_URL}/getInforById/{patient_id}")
                #     if pt_res.status_code == 200:
                #         appt_dict["patient"] = pt_res.json()
                #     else:
                #         appt_dict["patient"] = {"error": "Patient not found"}
                # except Exception:
                #     appt_dict["patient"] = {"error": "Cannot fetch patient info"}

                result.append(appt_dict)

            return Response(result, status=200)

        except DoesNotExist:
            return Response({"error": "Không tìm thấy lịch hẹn"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AppointmentUpdateView(APIView):
    def post(self, request, id):
        try:
            appointment = Appointment.objects(id=ObjectId(id)).first()
            new_status = request.data.get('status')
            
            if new_status is None:
                return Response({'error': 'Thiếu trường status'}, status=400)

            # Cập nhật và lưu
            appointment.status = new_status
            appointment.save()
            appointment.reload() 

            # Serialize và trả về dữ liệu sau cập nhật
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=200)
        except DoesNotExist:
            return Response({"error": "Không tìm thấy"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AppointmentCreateView(APIView):
    def post(self, request):
        try:
            data = request.data
            patient = data.get("patient")
            doctor = data.get("doctor")
            description = data.get("description")
            datetime_str = data.get("datetime")
            status = data.get("status")

            # Kiểm tra dữ liệu đầu vào
            if not all([patient, doctor, description, datetime_str, status]):
                return Response({"error": "Thiếu thông tin"}, status=400)

            # Chuyển đổi datetime string sang đối tượng datetime
            try:
                dt = datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
                
            except Exception:
                return Response({"error": "Datetime không hợp lệ"}, status=400)

            # Tạo và lưu appointment bằng mongoengine
            appointment = Appointment(
                patient=patient,
                doctor=doctor,
                description=description,
                datetime=dt,
                status=status
            )
            appointment.save()

            return Response({
                "message": "Đặt lịch thành công",
                "appointment_id": str(appointment.id)
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

