from django.contrib import admin
from .models import InsuranceContract, InsuranceClaim

@admin.register(InsuranceContract)
class InsuranceContractAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_name", "insurance_number", "provider", "start_date", "end_date", "is_active", "verified")
    search_fields = ("patient_name", "insurance_number", "provider")
    list_filter = ("provider", "is_active", "verified")

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "contract", "amount", "status", "created_at", "processed_at")
    search_fields = ("contract__patient_name",)
    list_filter = ("status",)
