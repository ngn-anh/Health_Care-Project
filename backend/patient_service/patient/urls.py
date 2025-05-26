from django.urls import path
from .views import PatientView, update_patient_template_view

urlpatterns = [
    path("getInfor/<str:id>", PatientView.as_view()),
    path("update/", update_patient_template_view, name="update_patient"),
]
