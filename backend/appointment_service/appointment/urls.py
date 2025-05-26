from django.urls import path
from .views import AppointmentListCreateView, AppointmentDetailView

urlpatterns = [
    path('', AppointmentListCreateView.as_view()),
    path('<str:id>/', AppointmentDetailView.as_view()),
]
