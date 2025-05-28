from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pharmacist, Prescription, Medication
from .serializers import PharmacistSerializer, PrescriptionSerializer, MedicationSerializer
import jwt
from django.conf import settings
from django.db.models import Sum

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

class ManageInventoryView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
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
        if not token:
            return Response({"error": "Token required"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload['role'] != 'pharmacist':
                return Response({"error": "Unauthorized"}, status=403)
            medication = Medication.objects.get(id=id)
            medication.delete()
            return Response({"message": "Medication deleted"}, status=status.HTTP_200_OK)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found"}, status=404)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# View cho giao diện HTML
def verify_view(request):
    token = request.GET.get('token')
    if not token:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload['role'] != 'pharmacist':
            return redirect("http://127.0.0.1:7000/api/auth/login_view/")
        return render(request, 'pharmacist/verify.html')
    except Exception as e:
        print(f"Error decoding token in verify_view: {e}")  # Gỡ lỗi
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
        print(f"Error decoding token in inventory_view: {e}")  # Gỡ lỗi
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")

def dashboard_view(request):
    token = request.GET.get('token')
    if not token:
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload['role'] != 'pharmacist':
            return redirect("http://127.0.0.1:7000/api/auth/login_view/")
        total_prescriptions = Prescription.objects.count()
        pending_prescriptions = Prescription.objects.filter(status="pending").count()
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
        print("Token expired in dashboard_view")  # Gỡ lỗi
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
    except Exception as e:
        print(f"Error decoding token in dashboard_view: {e}")  # Gỡ lỗi
        return redirect("http://127.0.0.1:7000/api/auth/login_view/")
