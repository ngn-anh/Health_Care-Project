from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
import requests

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'email',
            'phone_number', 'address', 'role', 'is_active'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Mật khẩu phải có ít nhất 6 ký tự.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Mật khẩu xác nhận không khớp."})
        if data['role'] == 'admin':
            raise serializers.ValidationError({"role": "Không thể tự đăng ký tài khoản quản trị viên."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        try:
            user = User.objects.create(
                username=validated_data['username'],
                full_name=validated_data['full_name'],
                email=validated_data['email'],
                password=make_password(validated_data['password']),
                role=validated_data['role'],
                date_of_birth=validated_data.get('date_of_birth', None),
                phone_number=validated_data.get('phone_number', ''),
                address=validated_data.get('address', ''),
                gender=validated_data.get('gender', ''),
                insurance_number=validated_data.get('insurance_number', ''),
            )
            # Tự động tạo profile cho mọi user
            try:
                if user.role == 'patient':
                    requests.post("http://localhost:8002/api/patient/create-profile/", json={
                        "user_id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "address": user.address,
                        "date_of_birth": str(user.date_of_birth) if user.date_of_birth else None,
                        "gender": user.gender,
                        "insurance_number": user.insurance_number,
                    })
                elif user.role == 'doctor':
                    requests.post("http://localhost:8003/api/doctor/create-profile/", json={"user_id": user.id})
                # Thêm các role khác nếu có service riêng
            except Exception as e:
                print("Không thể tạo profile:", e)

            return user
        except IntegrityError as e:
            if 'username' in str(e):
                raise serializers.ValidationError({"username": "Tên người dùng đã tồn tại."})
            if 'email' in str(e):
                raise serializers.ValidationError({"email": "Email đã tồn tại."})
            raise serializers.ValidationError("Đăng ký thất bại.")
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username hoặc mật khẩu không đúng.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Username hoặc mật khẩu không đúng.")

        if not user.is_active:
            raise serializers.ValidationError("Tài khoản đã bị khóa.")

        data['user'] = user
        return data
