from django.urls import path
from .views import ScheduleListCreateView, ScheduleDetailView

urlpatterns = [
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
]