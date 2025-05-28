from django.urls import path
from .views import CreatePharmacistView, VerifyPrescriptionView, ManageInventoryView, verify_view, inventory_view, dashboard_view

urlpatterns = [
    path('create/', CreatePharmacistView.as_view()),
    path('verify/', VerifyPrescriptionView.as_view()),
    path('inventory/', ManageInventoryView.as_view()),
    path('verify_view/', verify_view, name='verify_view'),
    path('inventory_view/', inventory_view, name='inventory_view'),
    path('dashboard/', dashboard_view, name='dashboard_view'),
]