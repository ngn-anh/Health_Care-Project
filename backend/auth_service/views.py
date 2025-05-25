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