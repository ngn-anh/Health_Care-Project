from rest_framework import generics, permissions
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.permissions import AllowAny

class ScheduleListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    # permission_classes = [permissions.IsAdminUser]

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    # permission_classes = [permissions.IsAdminUser]

class ScheduleListView(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]  # <-- Cho phép truy cập không cần đăng nhập