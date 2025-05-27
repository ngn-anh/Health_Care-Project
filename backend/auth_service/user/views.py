from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.hashers import check_password
import jwt, datetime
from django.conf import settings
from mongoengine.errors import NotUniqueError
from bson import ObjectId

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
            except NotUniqueError:
                return Response({"error": "Username hoặc Email đã tồn tại!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects(username=username).first()

        if user and check_password(password, user.password):
            payload = {
                "user_id": str(user.id),  # ✅ Đây là thứ SimpleJWT cần!
                "username": user.username,
                "role": user.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            return Response({
                "access": token,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            })

        return Response({"error": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserDetailView(APIView):
    def get(self, request, id):
        user = User.objects(id=ObjectId(id)).first()
        serializer = UserSerializer(user)

        if not user:
            return Response({"error": "User not found"}, status=404)
        return Response(serializer.data, status=200)

class UserUpdateView(APIView):
    def post(self, request, id):
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        new_email = data.get("email")
        if new_email and new_email != user.email:
            if User.objects(email=new_email).first():
                return Response(
                    {"error": "Email already in use by another user."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        update_fields = {
            "set__fullname": data.get("fullname", user.fullname),
            "set__email": new_email or user.email,
            "set__phone": data.get("phone", user.phone),
            "set__gender": data.get("gender", user.gender),
            "set__address": data.get("address", user.address)
        }

        # Gọi update
        User.objects(id=ObjectId(id)).update(**update_fields)

        # Lấy lại user đã cập nhật để serialize
        updated_user = User.objects(id=ObjectId(id)).first()
        serializer = UserSerializer(updated_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
# View render giao diện HTML
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')