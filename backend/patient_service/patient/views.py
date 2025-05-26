from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Patient
import requests
from bson import ObjectId

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