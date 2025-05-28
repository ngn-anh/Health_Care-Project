from django.urls import path
from .views import (
    AIDiagnosisInternalView,
    DiagnosisCreateView,
    DiagnosisHistoryView,
    DoctorAppointmentProxyView,
    DoctorAppointmentDetailProxyView,
    DoctorCreateView,
    DoctorInfoView,
    DoctorPatientListView,
    PatientListProxyView,
    appointment_view,
    dashboard_view,
    diagonsis_view,
    list_patient_view,
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
    path("my-patients/", DoctorPatientListView.as_view(), name="my_patients"),
    path("diagnosis/create/", DiagnosisCreateView.as_view(), name="create_diagnosis"),
    path("diagnosis/history/<str:patient_id>/", DiagnosisHistoryView.as_view(), name="history_diagnosis"),
    path("diagnosis/ai/", AIDiagnosisInternalView.as_view(), name="internal_ai_diagnosis"),

    path("dashboard_view/", dashboard_view, name="dashboard_view"),
    path("appointment_view/", appointment_view, name="appointment_view"),
    path("list_patient_view/", list_patient_view, name="list_patient_view"),
    path("diagonsis_view/", diagonsis_view, name="diagonsis_view"),
    

]
