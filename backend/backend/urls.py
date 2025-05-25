from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_service.urls')),
    path('api/doctor/', include('doctor_service.urls')),
    path('api/appointments/', include('appointment_service.urls')),
    path('api/patients/', include('patient_service.urls')),
    # path('api/records/', include('medical_record_service.urls')),
    # path('api/pharmacy/', include('pharmacy_service.urls')),
    # path('api/insurance/', include('insurance_service.urls')),
    # path('api/labs/', include('lab_service.urls')),
]
