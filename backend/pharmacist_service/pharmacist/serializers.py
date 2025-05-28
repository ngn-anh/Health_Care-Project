from rest_framework import serializers
from .models import Pharmacist, Medication, Prescription

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['id', 'user_id', 'license_number']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'quantity']

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'patient_id', 'medication', 'quantity_requested', 'status', 'pharmacist']