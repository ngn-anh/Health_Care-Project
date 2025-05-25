from django.urls import path
from .views import (
    DoctorAppointmentProxyView,
    DoctorAppointmentDetailProxyView,
    PatientListProxyView,
)
from django.http import JsonResponse

def test_debug_view(request):
    return JsonResponse({"route": "ĐÃ VÀO ROUTE"})

urlpatterns = [
    # path('appointments/', test_debug_view), 
    path('appointments/', DoctorAppointmentProxyView.as_view()),
    path('appointments/<str:id>/', DoctorAppointmentDetailProxyView.as_view()),
    path('patients/', PatientListProxyView.as_view()),
]
