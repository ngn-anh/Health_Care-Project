# doctor_service/serializers.py

from rest_framework import serializers

class DiagnosisSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    doctor_id = serializers.CharField()
    patient_id = serializers.CharField()
    symptoms = serializers.CharField()
    diagnosis = serializers.CharField()
    prescription = serializers.CharField()
    note = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
