from django.urls import path
from .views import PatientCreateView, PatientInfoView, PatientListView

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('create/', PatientCreateView.as_view()),
    path("info/<str:id>/", PatientInfoView.as_view()),
]
