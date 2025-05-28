from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.data.get('role') == 'admin':
            return Response({'error': 'Không được đăng ký tài khoản quản trị viên.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'message': 'Đăng nhập thành công',
                'user': {
                    'id': str(user.id),
                    'full_name': user.full_name,
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

#Quản lý người dùng chỉ dành cho quản trị viên
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User in permission:", request.user)
        user = request.user
        return hasattr(user, 'role') and user.role == 'admin'
    
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        data = request.data
        # Không cho phép tạo tài khoản admin qua API này
        if data.get('role') == 'admin':
            return Response({'error': 'Không được tạo tài khoản quản trị viên.'}, status=status.HTTP_403_FORBIDDEN)
        password = data.get('password', '123456')
        from django.contrib.auth.hashers import make_password
        user = User(
            username=data['username'],
            full_name=data['full_name'],
            email=data['email'],
            password=make_password(password),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', ''),
            role=data['role'],
            is_active=data.get('is_active', True)
        )
        try:
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        # Cập nhật các trường
        user.full_name = data.get('full_name', user.full_name)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
