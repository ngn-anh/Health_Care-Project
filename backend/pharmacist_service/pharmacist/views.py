# views.py
from datetime import datetime
import json
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pharmacist, Prescription, Medication, Diagnosis  # Thêm Diagnosis
from .serializers import PharmacistSerializer, PrescriptionSerializer, MedicationSerializer
import jwt
from mongoengine import Document, StringField, ListField, DateTimeField
from django.conf import settings
from django.db.models import Sum
from mongoengine.errors import OperationError
from .utils import DISEASE_TO_MEDICATION  # Import ánh xạ bệnh-thuốc

# Mô hình để lưu lịch sử xác minh
class VerificationHistory(Document):
    diagnosis_id = StringField(required=True)
    diagnosis = StringField(required=True)
    dispensed_medications = ListField(StringField())
    pharmacist_id = StringField(required=True)
    verified_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'verification_history'}
# View cho API

class CreatePharmacistView(APIView):
    def post(self, request):
        serializer = PharmacistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Pharmacist created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPrescriptionView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            prescription_id = request.data.get('prescription_id')
            prescription = Prescription.objects.get(id=prescription_id)
            if prescription.status == "pending":
                prescription.status = "verified"
                prescription.pharmacist = Pharmacist.objects.get(user_id=payload['user_id'])
                prescription.save()
                return Response({"message": "Prescription verified"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid prescription"}, status=400)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class DispenseMedicationView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)

            diagnosis_id = request.data.get('diagnosis_id')
            selected_medications = request.data.get('medications', [])  # Danh sách {name, quantity}

            # Lấy chẩn đoán
            diagnosis = Diagnosis.objects.get(id=diagnosis_id)

            # Cập nhật số lượng thuốc trong kho
            dispensed_meds = []
            for med in selected_medications:
                medication = Medication.objects.get(name=med['name'])
                if medication.quantity >= med['quantity']:
                    medication.quantity -= med['quantity']
                    medication.save()
                    dispensed_meds.append(f"{med['name']} (x{med['quantity']})")
                else:
                    return Response({"error": f"Not enough {med['name']} in stock"}, status=400)

            # Lưu lịch sử xác minh
            VerificationHistory(
                diagnosis_id=diagnosis_id,
                diagnosis=diagnosis.diagnosis,
                dispensed_medications=dispensed_meds,
                pharmacist_id=payload['user_id']
            ).save()

            # Xóa chẩn đoán đã xác minh
            diagnosis.delete()

            return Response({"message": "Diagnosis verified and medications dispensed"}, status=status.HTTP_200_OK)
        except Diagnosis.DoesNotExist:
            return Response({"error": "Diagnosis not found"}, status=404)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found"}, status=404)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class ManageInventoryView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(f"GET payload: {payload}")  # Gỡ lỗi
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            medications = Medication.objects.all()
            serializer = MedicationSerializer(medications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(f"POST payload: {payload}")  # Gỡ lỗi
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            serializer = MedicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Medication added"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def put(self, request, id):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(f"PUT payload: {payload}")  # Gỡ lỗi
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            medication = Medication.objects.get(id=id)
            serializer = MedicationSerializer(medication, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Medication updated"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found"}, status=404)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def delete(self, request, id):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        print(f"DELETE request received with token: {token}")  # Gỡ lỗi
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(f"DELETE payload: {payload}")  # Gỡ lỗi
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            medication = Medication.objects.get(id=id)
            print(f"Deleting medication with id: {id}")  # Gỡ lỗi
            medication.delete()
            return Response({"message": "Medication deleted"}, status=status.HTTP_200_OK)
        except Medication.DoesNotExist:
            return Response({"error": f"Medication with id {id} not found"}, status=404)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {str(e)}")  # Gỡ lỗi
            return Response({"error": "Invalid token"}, status=401)
        except Exception as e:
            print(f"Unexpected error in DELETE: {str(e)}")  # Gỡ lỗi
            return Response({"error": str(e)}, status=500)

# View cho giao diện HTML
# views.py
def verify_view(request):
    token = request.GET.get('token')
    if not token:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload['role'] != 'pharmacist':
            return redirect("http://127.0.0.1:7000/api/auth/login_view/")

        # Lấy danh sách chẩn đoán từ MongoDB
        try:
            diagnoses = Diagnosis.objects.all()
            diagnoses = [{'id': str(d.id), 'diagnosis': d.diagnosis.strip()} for d in diagnoses]
        except OperationError:
            diagnoses = []

        # Lấy danh sách thuốc từ kho
        medications = Medication.objects.all()
        medication_list = [{'name': med.name, 'quantity': med.quantity} for med in medications]

        # Gợi ý thuốc dựa trên chẩn đoán
        diagnosis_with_medications = []
        for diag in diagnoses:
            disease = diag['diagnosis'].lower()
            suggested_meds = DISEASE_TO_MEDICATION.get(disease, [])
            formatted_meds = []
            for med_keyword in suggested_meds:
                is_available = False
                for med in medication_list:
                    if med_keyword.lower() in med['name'].lower() and med['quantity'] > 0:
                        is_available = True
                        break
                formatted_name = f"{med_keyword} (A)" if is_available else med_keyword
                formatted_meds.append(formatted_name)

            diagnosis_with_medications.append({
                'id': diag['id'],
                'diagnosis': diag['diagnosis'],
                'suggested_medications': formatted_meds if formatted_meds else ['Không có thuốc gợi ý']
            })

        # Lấy lịch sử xác minh
        history = VerificationHistory.objects.all()
        verification_history = [{
            'diagnosis': h.diagnosis,
            'dispensed_medications': h.dispensed_medications,
            'verified_at': h.verified_at.strftime('%Y-%m-%d %H:%M:%S')
        } for h in history]

        context = {
            'diagnoses': diagnosis_with_medications,
            'token': token,
            'verification_history': verification_history,
            'medication_list': json.dumps(medication_list),  # Chuyển thành JSON
        }
        return render(request, 'pharmacist/verify.html', context)
    except jwt.ExpiredSignatureError:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    except jwt.InvalidTokenError:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    except Exception:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")

def inventory_view(request):
    token = request.GET.get('token')
    if not token:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload['role'] != 'pharmacist':
            return redirect("http://127.0.0.1:7000/api/auth/login_view/")
        return render(request, 'pharmacist/inventory.html')
    except Exception as e:
        print(f"Error decoding token in inventory_view: {e}")
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")

def dashboard_view(request):
    token = request.GET.get('token')
    if not token:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload['role'] != 'pharmacist':
            return redirect("http://127.0.0.1:7000/api/auth/login_view/")

        # Tính tổng số đơn thuốc (bao gồm đã xác minh và đang chờ)
        total_diagnoses = Diagnosis.objects.count()  # Đơn chờ xác minh
        verified_diagnoses = VerificationHistory.objects.count()  # Đơn đã xác minh
        total_prescriptions = total_diagnoses + verified_diagnoses  # Tổng số đơn
        pending_prescriptions = total_diagnoses  # Đơn chờ xác minh
        total_medications = Medication.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        user_info = {"username": payload["username"], "role": payload["role"]}
        context = {
            "user": user_info,
            "total_prescriptions": total_prescriptions,
            "pending_prescriptions": pending_prescriptions,
            "total_medications": total_medications
        }
        return render(request, 'pharmacist/dashboard.html', context)
    except jwt.ExpiredSignatureError:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    except Exception:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")