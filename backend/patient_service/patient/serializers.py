from rest_framework import serializers

class PatientSerializer(serializers.Serializer):
    _id = serializers.CharField()
    user = serializers.CharField()
    medical_record_id = serializers.CharField(allow_blank=True, required=False)
