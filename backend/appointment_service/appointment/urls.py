from django.urls import path
from .views import ( AppointmentListCreateView, AppointmentDetailView, 
                    AppointmentListView, AppointmentUpdateView, AppointmentCreateView )

urlpatterns = [
    path('', AppointmentListCreateView.as_view()),
    path('<str:id>/', AppointmentDetailView.as_view()),
    path('getAllList', AppointmentListView.as_view()),
    path('updateStatus/<str:id>', AppointmentUpdateView.as_view()),
    path('create', AppointmentCreateView.as_view()),
]
