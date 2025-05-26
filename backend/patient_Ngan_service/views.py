from rest_framework.views import APIView
from rest_framework.response import Response
from auth_service.models import Patient, User

class PatientListView(APIView):
    def get(self, request):
        try:
            patients = Patient.objects()
            data = []
            for p in patients:
                user = User.objects(id=p.user).first()
                if user:
                    data.append({
                        "id": str(p.id),
                        "user_id": str(user.id),
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    })
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
