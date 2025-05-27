from django.urls import path
from .views import AppointmentListCreateView, AppointmentDetailView, AppointmentListView

urlpatterns = [
    path('', AppointmentListCreateView.as_view()),
    path('<str:id>/', AppointmentDetailView.as_view()),
    path('getAllList', AppointmentListView.as_view()),
]
