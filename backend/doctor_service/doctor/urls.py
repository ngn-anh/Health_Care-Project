from django.urls import path
from .views import (
    DoctorAppointmentProxyView,
    DoctorAppointmentDetailProxyView,
    DoctorCreateView,
    DoctorInfoView,
    PatientListProxyView,
    appointment_view,
    dashboard_view,
    DoctorInforView,
    DoctorInforByIdView,
    DoctorAllListView,
)
from django.http import JsonResponse

def test_debug_view(request):
    return JsonResponse({"route": "ĐÃ VÀO ROUTE"})

urlpatterns = [
    # path('appointments/', test_debug_view), 
    path('appointments/', DoctorAppointmentProxyView.as_view()),
    path('appointments/<str:id>/', DoctorAppointmentDetailProxyView.as_view()),
    path('patients/', PatientListProxyView.as_view()),
    path('create/', DoctorCreateView.as_view()),
    path("info/<str:id>/", DoctorInfoView.as_view()),
    path("dashboard_view/", dashboard_view, name="dashboard_view"),
    path("appointment_view/", appointment_view, name="appointment_view"),
    path("getAllList/", DoctorAllListView.as_view()),
    path("getInfor/", DoctorInforView.as_view()),
    path("getInforById/<str:id>", DoctorInforByIdView.as_view()),
]
