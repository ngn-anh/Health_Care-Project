from django.urls import path
from .views import (
    PatientView, home_view, PatientInforView, update_view, 
    PatientUpdateView, PatientCreateView, PatientInfoView, 
    PatientListView, PatientInforByIdView, appointment_view,
)

urlpatterns = [
    path("home", PatientView.as_view()),
    path("getInfor", PatientInforView.as_view()),
    path("getInforById/<str:id>", PatientInforByIdView.as_view()),
    path("updateInfor", PatientUpdateView.as_view()),
    path('', PatientListView.as_view(), name='patient-list'),
    path('create/', PatientCreateView.as_view()),
    path("info/<str:id>/", PatientInfoView.as_view()),

    path("home_view/", home_view, name="home_view"),
    path("update_view/", update_view, name="update_view"),
    path("appointment_view/", appointment_view, name="appointment_view"),

]
